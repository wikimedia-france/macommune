#!/usr/bin/python3
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from mc_frontend.models import Communes, Geoloc, get_sections_length
from pywiki_light import *
import re
import time
import datetime
import configparser
import os
import requests
import json
from json import encoder
from unidecode import unidecode
encoder.FLOAT_REPR = lambda o: format(o, '.6f')

config = configparser.ConfigParser()
config.read(os.path.dirname(__file__) + 'config.ini')



class Command(BaseCommand):
    help = 'Fetch datas from Wikidata, Wikipedia and Wikimedia\'s map service to populate the database.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--partial',
            action='store_true',
            dest='partial',
            help='Don\'t fetch datas that are relatively stable.',
        )

    def handle(self, *args, **options):
        self.stdout.write("Update started at {}".format(datetime.datetime.now()))
        
        self.articles = {}
        self.geolocs = {}
        self.error_report = []
        
        self.frwiki = Pywiki("frwiki")
        self.frwiki.login()
        self.wdwiki = Pywiki("wikidatawiki")
        self.wdwiki.login()

        qids = self.get_all_items("""
            SELECT DISTINCT ?item
            WHERE { ?item wdt:P31/wdt:P279* wd:Q484170 . }""")
        self.initialise_structure(qids)

        count = 0
        while len(qids) > 0:
            wp_titles = self.get_wikidata_datas(qids[:50])
            self.get_article_datas(wp_titles)
            self.get_pdd_datas(wp_titles, qids[:50])
            self.get_geoshape_datas(qids[:50])
            count += len(qids[:50])
            self.stdout.write(str(count))
            del qids[:50]

        self.update_DB()
        self.save_error_report()

        self.stdout.write("Update finished at {}".format(datetime.datetime.now()))


    def get_all_items(self, query):
        try:
            r = requests.post('https://query.wikidata.org/sparql',
                              data={'format': 'json', 'query': query})
            raw_items = json.loads(r.text)['results']['bindings']
        except (requests.exceptions.ConnectionError, ZeroReturnError, ValueError):
            self.stdout.write("Request to https://query.wikidata.org/sparql failed")
            time.sleep(5)
            return self.get_all_items(query)
            
        qids = []
        for item in raw_items:
            qids += [item['item']['value'].split('/')[-1]]
        return qids


    def initialise_structure(self, qids):
        for qid in qids:
            self.articles[qid] = {
                "qid": qid,
                "section_geography": 0,
                "section_history": 0,
                "section_economy": 0,
                "section_demographics": 0,
                "section_etymology": 0,
                "section_governance": 0,
                "section_culture": 0,
                "section_infrastructure": 0,
            }
            self.geolocs[qid] = {
                "qid": qid
            }


    def get_geoshape_datas(self, qids):
        payload = {
            'getgeojson': 1,
            'ids': ','.join(qids)
        }
        try:
            r = requests.get('https://maps.wikimedia.org/geoshape', params=payload)
            features = json.loads(r.text)['features']
        except (requests.exceptions.ConnectionError,
                SSL.Error,
                SSL.ZeroReturnError,
                ValueError):
            self.stdout.write("Request to https://maps.wikimedia.org/geoshape failed")
            time.sleep(5)
            return self.get_geoshape_datas(qids)
        for feature in features:
            qid = feature['id']
            self.geolocs[qid]['geoshape'] = json.dumps(feature['geometry'],
                                                   separators=(',', ':'))


    def get_wikidata_datas(self, qids):
        """
        limit: 50 (500)
        """
        # Request 100 pages out of the given category
        # with their qid, first image, and last revision
        responses = self.wdwiki.request({
            "action": "wbgetentities",
            "format": "json",
            "ids": "|".join(qids),
            "props": "sitelinks|aliases|labels|claims",
            "languages": "fr|en"
        })

        wp_titles = []
        if "entities" in responses:
            for qid in responses["entities"]:
                response = responses["entities"][qid]
                try:
                    title = response["sitelinks"]["frwiki"]["title"]
                    self.articles[qid]['wp_title'] = title
                except (TypeError, KeyError):
                    self.error_report += [{"qid": qid,
                                      "message": "{{P|31}} '{{Q|Q484170}}' \
                                      without an article on frwiki."}]
                    continue
                self.articles[qid]['title'] = response["labels"]["fr"]["value"]
                self.articles[qid]['badge'] = response["sitelinks"]["frwiki"]["badges"]
                frlabel = response["labels"]["fr"]["value"]
                self.articles[qid]['suggest_str'] = unidecode(frlabel).lower()
                suggest = self.articles[qid]['suggest_str']
                self.articles[qid]['suggest_str'] = re.sub('\W+', ' ', suggest).strip()
                wp_titles += [response["sitelinks"]["frwiki"]["title"]]
                if self.articles[qid]['badge']:
                    self.articles[qid]['badge'] = self.articles[qid]['badge'][0]
                else:
                    self.articles[qid]['badge'] = ""
                try:
                    frwvtitle = response["sitelinks"]["frwikivoyage"]["title"]
                    self.articles[qid]['wv_title'] = frwvtitle
                except (TypeError, KeyError):
                    pass
                try:
                    p1082 = response["claims"]["P1082"][0]["mainsnak"]["datavalue"]
                    self.articles[qid]['population'] = p1082["value"]["amount"]
                except (TypeError, KeyError):
                    pass
                try:
                    p374 = response["claims"]["P374"][0]["mainsnak"]
                    self.articles[qid]['insee'] = p374["datavalue"]["value"]
                except (TypeError, KeyError):
                    pass
                try:
                    p373 = response["claims"]["P373"][0]["mainsnak"]
                    self.articles[qid]['commons_category'] = p373["datavalue"]["value"]
                except (TypeError, KeyError):
                    pass
                try:
                    p625 = response["claims"]["P625"][0]["mainsnak"]
                    coordinates = p625["datavalue"]["value"]
                    self.geolocs[qid]['latitude'] = coordinates["latitude"]
                    self.geolocs[qid]['longitude'] = coordinates["longitude"]
                except (TypeError, KeyError):
                    self.error_report += [{"qid": qid,
                                      "message": "{{P|31}} '{{Q|Q484170}}' \
                                       without {{P|625}}."}]
                    pass
        return wp_titles


    def get_article_datas(self, titles):
        """
        limit: 50 (500)
        """

        responses = self.frwiki.request({
            "format": "json",
            "action": "query",
            "prop": "pageprops|pageimages|revisions",
            "ppprop": "wikibase_item",
            "piprop": "original",
            "pilimit": 50,
            "rvprop": "ids|timestamp|content",
            "titles": "|".join(titles),
        })

        # Analyse each returned pages one by one
        titles = []
        if "query" in responses:
            for i in responses["query"]["pages"]:
                response = responses["query"]["pages"][i]
                try:
                    qid = response["pageprops"]["wikibase_item"]

                    #if 'original' in response:
                    #    communes[qid]["image_url"] = response["original"]["source"]

                    text = response["revisions"][0]["*"]
                    sections_length = get_sections_length(text)
                    # Split the revision's content into section titles and content
                    for section, value in sections_length.items():
                        self.articles[qid][section] = value

                except Exception:
                    self.stdout.write("--> Error with the article '{}'".format(
                        responses["query"]["pages"][i]["title"]))


    def get_pdd_datas(self, titles, qids):
        """
        limit: 50 (500)
        """
        responses = self.frwiki.request({
            "format": "json",
            "action": "query",
            "prop": "revisions",
            "rvprop": "ids|timestamp|content",
            "titles": "Discussion:" + "|Discussion:".join(titles),
        })

        if "query" in responses:
            for i in responses["query"]["pages"]:
                response = responses["query"]["pages"][i]

                title = response["title"][11:]
                try:
                    content = response["revisions"][0]["*"]
                    try:
                        regex = r"{{Wikiprojet.*Avancement *= *(\?|ébauche|BD|B|A)"
                        progress = re.findall(
                            regex,
                            content,
                            re.DOTALL | re.UNICODE | re.IGNORECASE)[0]
                        self.articles[qids[titles.index(title)]]['progress'] = progress
                    except IndexError:
                        self.articles[qids[titles.index(title)]]['progress'] = "?"
                    try:
                        regex = r"{{Wikiprojet.*Communes de France *\| *(\?|faible|moyenne|élevée|maximum)"
                        reg = re.findall(
                            regex,
                            content,
                            re.DOTALL | re.UNICODE | re.IGNORECASE)[0]
                        self.articles[qids[titles.index(title)]]['importance'] = reg
                    except IndexError:
                        self.articles[qids[titles.index(title)]]['importance'] = "?"
                except KeyError:
                    self.articles[qids[titles.index(title)]]['progress'] = "?"
                    self.articles[qids[titles.index(title)]]['importance'] = "?"


    def update_DB(self):
        for qid in self.articles:
            self.stdout.write(qid)
            commune, created = Communes.objects.get_or_create(qid=qid)
            Communes.objects.filter(qid=qid).update(**self.articles[qid])

    def save_error_report(self):
        content = "Bot-generated report, don't edit this page manually."
        if len(self.error_report) > 0:
            for error in self.error_report:
                content += "* {{Q|" + error['qid'] + "}}: " + error['message'] + "\n"
            self.wdwiki.replace("Wikidata:WikiProject France/Communes/Rapport",
                           content,
                           "update report",
                           nocreate=True)



