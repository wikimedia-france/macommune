#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pywiki_light import *
import MySQLdb
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


sections_lookup_table = {
    "section_geography":
        ["Géographie",
         "Lieux et monuments",
         "Monuments",
         "Jumelages",
         "Environnement",
         "Édifice religieux",
         "Communes limitrophes",
         "Édifices religieux",
         "Lieux-dits et écarts",
         "Climat",
         "Vignoble",
         "Lieux, monuments et pôles d'intérêt",
         "Sites et monuments",
         "Patrimoine naturel",
         "Monuments et sites",
         "Monuments et lieux touristiques",
         "Géologie",
         "Hydrographie",
         "Lieux-dits"],
    "section_history":
        ["Histoire",
         "Héraldique",
         "Blasonnement",
         "Emblèmes",
         "Armoiries",
         "Archives",
         "Blason",
         "Historique"],
    "section_economy":
        ["Économie",
         "Tourisme",
         "Économie et tourisme",
         "Activités économiques",
         "Activité économique"],
    "section_demographics":
        ["Population et société",
         "Personnalités liées à la commune",
         "Démographie",
         "Enseignement",
         "Personnalités liées",
         "Personnalités",
         "Personnalité liée à la commune",
         "Cultes",
         "Culte",
         "Éducation"],
    "section_etymology":
        ["Toponymie",
         "Toponyme",
         "Toponymie et héraldique",
         "Dénomination",
         "Étymologie",
         "Nom des habitants"],
    "section_governance":
        ["Politique et administration",
         "Administration",
         "Santé",
         "Jumelage",
         "Intercommunalité"],
    "section_culture":
        ["Culture locale et patrimoine",
         "Culture et patrimoine",
         "Activité et manifestations",
         "Vie locale",
         "Sports",
         "Équipements",
         "Équipements, services et vie locale",
         "Culture",
         "Événements",
         "Patrimoine",
         "Vie pratique",
         "Équipements et services",
         "Langue bretonne",
         "Patrimoine religieux",
         "Associations",
         "Manifestations",
         "Équipements ou services",
         "Activités festives",
         "Activité culturelle et manifestations",
         "Loisirs",
         "Activité, label et manifestations",
         "Vie associative",
         "Cadre de vie",
         "Cinéma",
         "Activités",
         "Activités et manifestations",
         "Gastronomie",
         "Manifestations culturelles et festivités",
         "Festivités",
         "Sport",
         "Patrimoine civil",
         "Distinctions culturelles",
         "Animations",
         "Infrastructures",
         "Fêtes et loisirs",
         "Société",
         "Vie culturelle",
         "Littérature",
         "Activités associatives, culturelles, festives et sportives"],
    "section_infrastructure":
        ["Urbanisme",
         "Transports",
         "Transport",
         "Voies de communication et transports",
         "Transports et voies de communications",
         "Urbanisme et habitat",
         "Transports en commun",
         "Urbanisation",
         "Industrie"],
}

communes = {}
error_report = []


def get_all_items(query):
    try:
        r = requests.post('https://query.wikidata.org/sparql',
                          data={'format': 'json', 'query': query})
        raw_items = json.loads(r.text)['results']['bindings']
    except (requests.exceptions.ConnectionError, ZeroReturnError, ValueError):
        print("Request to https://query.wikidata.org/sparql failed")
        time.sleep(5)
        return get_all_items(query)
        
    qids = []
    for item in raw_items:
        qids += [item['item']['value'].split('/')[-1]]
    return qids


def initialise_structure(qids):
    for qid in qids:
        communes[qid] = {
            "qid": qid,
            "title": "",
            "wp_title": "",
            "wv_title": "",
            "commons_category": "",
            "suggest_str": "",
            "image_url": "",
            "population": 0,
            "insee": 0,
            "badge": "",
            "latitude": 0,
            "longitude": 0,
            "geoshape": '{"type":"MultiPolygon","coordinates":[]}',
            "progress": "",
            "importance": "",
            "section_geography": 0,
            "section_history": 0,
            "section_economy": 0,
            "section_demographics": 0,
            "section_etymology": 0,
            "section_governance": 0,
            "section_culture": 0,
            "section_infrastructure": 0,
        }


def get_geoshape_datas(qids):
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
        print("Request to https://maps.wikimedia.org/geoshape failed")
        time.sleep(5)
        return get_geoshape_datas(qids)
    for feature in features:
        qid = feature['id']
        communes[qid]['geoshape'] = json.dumps(feature['geometry'],
                                               separators=(',', ':'))


def get_wikidata_datas(self, qids):
    """
    limit: 50 (500)
    """
    global error_report
    # Request 100 pages out of the given category
    # with their qid, first image, and last revision
    responses = self.request({
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
                communes[qid]['wp_title'] = title
            except (TypeError, KeyError):
                error_report += [{"qid": qid,
                                  "message": "{{P|31}} '{{Q|Q484170}}' \
                                  without an article on frwiki."}]
                continue
            communes[qid]['title'] = response["labels"]["fr"]["value"]
            communes[qid]['badge'] = response["sitelinks"]["frwiki"]["badges"]
            frlabel = response["labels"]["fr"]["value"]
            communes[qid]['suggest_str'] = unidecode(frlabel).lower()
            suggest = communes[qid]['suggest_str']
            communes[qid]['suggest_str'] = re.sub('\W+', ' ', suggest).strip()
            wp_titles += [response["sitelinks"]["frwiki"]["title"]]
            if communes[qid]['badge']:
                communes[qid]['badge'] = communes[qid]['badge'][0]
            else:
                communes[qid]['badge'] = ""
            try:
                frwvtitle = response["sitelinks"]["frwikivoyage"]["title"]
                communes[qid]['wv_title'] = frwvtitle
            except (TypeError, KeyError):
                pass
            try:
                p1082 = response["claims"]["P1082"][0]["mainsnak"]["datavalue"]
                communes[qid]['population'] = p1082["value"]["amount"]
            except (TypeError, KeyError):
                pass
            try:
                p374 = response["claims"]["P374"][0]["mainsnak"]
                communes[qid]['insee'] = p374["datavalue"]["value"]
            except (TypeError, KeyError):
                pass
            try:
                p373 = response["claims"]["P373"][0]["mainsnak"]
                communes[qid]['commons_category'] = p373["datavalue"]["value"]
            except (TypeError, KeyError):
                pass
            try:
                p625 = response["claims"]["P625"][0]["mainsnak"]
                coordinates = p625["datavalue"]["value"]
                communes[qid]['latitude'] = coordinates["latitude"]
                communes[qid]['longitude'] = coordinates["longitude"]
            except (TypeError, KeyError):
                error_report += [{"qid": qid,
                                  "message": "{{P|31}} '{{Q|Q484170}}' \
                                   without {{P|625}}."}]
                pass
    return wp_titles


Pywiki.get_wikidata_datas = get_wikidata_datas


def get_article_datas(self, titles):
    """
    limit: 50 (500)
    """

    responses = self.request({
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

                if 'original' in response:
                    communes[qid]["image_url"] = response["original"]["source"]

                text = response["revisions"][0]["*"]
                sections_length = get_sections_length(text)
                # Split the revision's content into section titles and content
                for section, value in sections_length.items():
                    communes[qid][section] = value

            except Exception:
                print("--> Error with the article '{}'".format(
                    responses["query"]["pages"][i]["title"]))


Pywiki.get_article_datas = get_article_datas


def get_sections_length(text):
    sections = ["section_geography",
                "section_history",
                "section_economy",
                "section_demographics",
                "section_etymology",
                "section_governance",
                "section_culture",
                "section_infrastructure"]

    result = {}
    for section in sections:
        result[section] = 0

    splcont = re.split("\n==([^=]+)==", text)
    # Search and regroup sections into the choosen one
    # according to a lookup table and sum their weight
    for j in range(1, len(splcont), 2):
        for section in sections:
            s = splcont[j].strip()
            if s in sections_lookup_table[section]:
                result[section] += len(splcont[j + 1])
                break

    return result


def get_pdd_datas(self, titles, qids):
    """
    limit: 50 (500)
    """
    responses = self.request({
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
                    communes[qids[titles.index(title)]]['progress'] = progress
                except IndexError:
                    communes[qids[titles.index(title)]]['progress'] = "?"
                try:
                    regex = r"{{Wikiprojet.*Communes de France *\| *(\?|faible|moyenne|élevée|maximum)"
                    reg = re.findall(
                        regex,
                        content,
                        re.DOTALL | re.UNICODE | re.IGNORECASE)[0]
                    communes[qids[titles.index(title)]]['importance'] = reg
                except IndexError:
                    communes[qids[titles.index(title)]]['importance'] = "?"
            except KeyError:
                communes[qids[titles.index(title)]]['progress'] = "?"
                communes[qids[titles.index(title)]]['importance'] = "?"


Pywiki.get_pdd_datas = get_pdd_datas


def update_DB():
    conn = MySQLdb.connect(host=config.get('mysql', 'host'),
                           port=int(config.get('mysql', 'port')),
                           user=config.get('mysql', 'user'),
                           passwd=config.get('mysql', 'password'),
                           db=config.get('mysql', 'database'),
                           charset='utf8'
                           )
    with conn.cursor() as curr:
        for qid in communes:
            curr.execute("""
                INSERT INTO communes (`qid`, `title`, `wp_title`, `wv_title`,
                `commons_category`, `suggest_str`, `insee`, `population`,
                `badge`, `progress`, `importance`, `latitude`, `longitude`,
                `geoshape`, `section_geography`, `section_history`,
                `section_economy`, `section_demographics`, `section_etymology`,
                `section_governance`,`section_culture`,
                `section_infrastructure`, `updated`)
                VALUES(%(qid)s, %(title)s, %(wp_title)s, %(wv_title)s,
                %(commons_category)s, %(suggest_str)s, %(insee)s,
                %(population)s, %(badge)s, %(progress)s, %(importance)s,
                %(latitude)s, %(longitude)s, %(geoshape)s,
                %(section_geography)s, %(section_history)s,
                %(section_economy)s, %(section_demographics)s,
                %(section_etymology)s, %(section_governance)s,
                %(section_culture)s, %(section_infrastructure)s,
                NOW()) ON DUPLICATE KEY UPDATE `qid`=VALUES(`qid`),
                `title`=VALUES(`title`), `wp_title`=VALUES(`wp_title`),
                `wv_title`=VALUES(`wv_title`),
                `commons_category`=VALUES(`commons_category`),
                `suggest_str`=VALUES(`suggest_str`),
                `insee`=VALUES(`insee`), `population`=VALUES(`population`),
                `badge`=VALUES(`badge`), `progress`=VALUES(`progress`),
                `importance`=VALUES(`importance`),
                `latitude`=VALUES(`latitude`), `longitude`=VALUES(`longitude`),
                `geoshape`=VALUES(`geoshape`),
                `section_geography`=VALUES(`section_geography`),
                `section_history`=VALUES(`section_history`),
                `section_economy`=VALUES(`section_economy`),
                `section_demographics`=VALUES(`section_demographics`),
                `section_etymology`=VALUES(`section_etymology`),
                `section_governance`=VALUES(`section_governance`),
                `section_culture`=VALUES(`section_culture`),
                `section_infrastructure`=VALUES(`section_infrastructure`),
                `updated`=NOW()
                """, communes[qid])
        conn.commit()


print("Update started at {}".format(datetime.datetime.now()))
frwiki = Pywiki("frwiki")
frwiki.login()
wdwiki = Pywiki("wikidatawiki")
wdwiki.login()


qids = get_all_items("""
    SELECT DISTINCT ?item
    WHERE { ?item wdt:P31/wdt:P279* wd:Q484170 . }""")
initialise_structure(qids)

count = 0
while len(qids) > 0:
    wp_titles = wdwiki.get_wikidata_datas(qids[:50])
    frwiki.get_article_datas(wp_titles)
    frwiki.get_pdd_datas(wp_titles, qids[:50])
    get_geoshape_datas(qids[:50])
    count += len(qids[:50])
    print(count)
    del qids[:50]

update_DB()

content = "Bot-generated report, don't edit this page manually."
if len(error_report) > 0:
    for error in error_report:
        content += "* {{Q|" + error['qid'] + "}}: " + error['message'] + "\n"
    wdwiki.replace("Wikidata:WikiProject France/Communes/Rapport",
                   content,
                   "update report",
                   nocreate=True)

print("Update finished at {}".format(datetime.datetime.now()))
