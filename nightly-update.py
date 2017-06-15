#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from pywiki_light import *
import pymysql
import re
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
    u"section_geography": [u"Géographie", u"Lieux et monuments", u"Monuments", u"Jumelages", u"Environnement", u"Édifice religieux", u"Communes limitrophes", u"Édifices religieux", u"Lieux-dits et écarts", u"Climat", u"Vignoble", u"Lieux, monuments et pôles d'intérêt", u"Sites et monuments", u"Patrimoine naturel", u"Monuments et sites", u"Monuments et lieux touristiques", u"Géologie", u"Hydrographie", u"Lieux-dits"],
    u"section_history": [u"Histoire", u"Héraldique", u"Blasonnement", u"Emblèmes", u"Armoiries", u"Archives", u"Blason", u"Historique"],
    u"section_economy": [u"Économie", u"Tourisme", u"Économie et tourisme", u"Activités économiques", u"Activité économique"],
    u"section_demographics": [u"Population et société", u"Personnalités liées à la commune", u"Démographie", u"Enseignement", u"Personnalités liées", u"Personnalités", u"Personnalité liée à la commune", u"Cultes", u"Culte", u"Éducation"],
    u"section_etymology": [u"Toponymie", u"Toponyme", u"Toponymie et héraldique", u"Dénomination", u"Étymologie", u"Nom des habitants"],
    u"section_governance": [u"Politique et administration", u"Administration", u"Santé", u"Jumelage", u"Intercommunalité"],
    u"section_culture": [u"Culture locale et patrimoine", u"Culture et patrimoine", u"Activité et manifestations", u"Vie locale", u"Sports", u"Équipements", u"Équipements, services et vie locale", u"Culture", u"Événements", u"Patrimoine", u"Vie pratique", u"Équipements et services", u"Langue bretonne", u"Patrimoine religieux", u"Associations", u"Manifestations", u"Équipements ou services", u"Activités festives", u"Activité culturelle et manifestations", u"Loisirs", u"Activité, label et manifestations", u"Vie associative", u"Cadre de vie", u"Cinéma", u"Activités", u"Activités et manifestations", u"Gastronomie", u"Manifestations culturelles et festivités", u"Festivités", u"Sport", u"Patrimoine civil", u"Distinctions culturelles", u"Animations", u"Infrastructures", u"Fêtes et loisirs", u"Société", u"Vie culturelle", u"Littérature", u"Activités associatives, culturelles, festives et sportives"],
    u"section_infrastructure": [u"Urbanisme", u"Transports", u"Transport", u"Voies de communication et transports", u"Transports et voies de communications", u"Urbanisme et habitat", u"Transports en commun", u"Urbanisation", u"Industrie"],
}
communes = {}
error_report = []


def get_all_items(query):
    r = requests.post('https://query.wikidata.org/sparql', data = {'format': 'json', 'query': query})
    raw_items = json.loads(r.text)['results']['bindings']
    qids = []
    for item in raw_items:
        qids += [item['item']['value'].split('/')[-1]]
    return qids




def initialise_structure(qids):
    for qid in qids:
        communes[qid] = {
            "qid": qid,
            "title":"",#
            "wp_title": "",#
            "wv_title": "",#
            "commons_category":"",#
            "suggest_str":"",#
            "image_url": "",#
            "population":0,#
            "insee":0,#
            "badge":"",#
            "latitude":0,#
            "longitude":0,#
            "geoshape": '{"type":"MultiPolygon","coordinates":[]}',#
            "progress":"",#
            "importance":"",#
            "section_geography": 0,#
            "section_history": 0,#
            "section_economy": 0,#
            "section_demographics": 0,#
            "section_etymology": 0,#
            "section_governance": 0,#
            "section_culture": 0,#
            "section_infrastructure": 0,#
        }



def get_geoshape_datas(qids):
    r = requests.get('https://maps.wikimedia.org/geoshape?getgeojson=1&ids=' + ','.join(qids))
    features = json.loads(r.text)['features']
    for feature in features:
        qid = feature['id']
        communes[qid]['geoshape'] = json.dumps(feature['geometry'], separators=(',', ':'))


"""
limit: 50 (500)
"""
def get_wikidata_datas(self, qids):
    global error_report
    # Request 100 pages out of the given category with their qid, first image, and last revision
    responses = self.request({
        "action":    "wbgetentities",
        "format":    "json",
        "ids":       "|".join(qids),
        "props":     "sitelinks|aliases|labels|claims",
        "languages": "fr|en"
    })
    
    wp_titles = []
    if "entities" in responses:
        for qid in responses["entities"]:
            response = responses["entities"][qid]
            try:
                communes[qid]['wp_title'] = response["sitelinks"]["frwiki"]["title"]
            except (TypeError, KeyError):
                error_report += [{"qid": qid, "message": "{{P|31}} '{{Q|Q484170}}' without an article on frwiki."}]
                continue
            communes[qid]['title'] = response["labels"]["fr"]["value"]
            communes[qid]['badge'] = response["sitelinks"]["frwiki"]["badges"]
            communes[qid]['suggest_str'] = unidecode(response["labels"]["fr"]["value"]).lower().replace('-', ' ')
            communes[qid]['suggest_str'] = re.sub('\W+', ' ', communes[qid]['suggest_str']).strip()
            wp_titles += [response["sitelinks"]["frwiki"]["title"]]
            if communes[qid]['badge']:
                communes[qid]['badge'] = communes[qid]['badge'][0]
            else:
                communes[qid]['badge'] = ""
            try:
                communes[qid]['wv_title'] = response["sitelinks"]["frwikivoyage"]["title"]
            except (TypeError, KeyError):
                pass
            try:
                communes[qid]['population'] = response["claims"]["P1082"][0]["mainsnak"]["datavalue"]["value"]["amount"]
            except (TypeError, KeyError):
                pass
            try:
                communes[qid]['insee'] = response["claims"]["P374"][0]["mainsnak"]["datavalue"]["value"]
            except (TypeError, KeyError):
                pass
            try:
                communes[qid]['commons_category'] = response["claims"]["P373"][0]["mainsnak"]["datavalue"]["value"]
            except (TypeError, KeyError):
                pass
            try:
                coordinates = response["claims"]["P625"][0]["mainsnak"]["datavalue"]["value"]
                communes[qid]['latitude'] = coordinates["latitude"]
                communes[qid]['longitude'] = coordinates["longitude"]
            except (TypeError, KeyError):
                error_report += [{"qid": qid, "message": "{{P|31}} '{{Q|Q484170}}' without {{P|625}}."}]
                pass
    return wp_titles
Pywiki.get_wikidata_datas = get_wikidata_datas

"""
limit: 50 (500)
"""
def get_article_datas(self, titles):
    responses = self.request({
        "format":       "json",
        "action":       "query",
	    "prop":         "pageprops|pageimages|revisions",
	    "ppprop":       "wikibase_item",
	    "piprop":       "original",
	    "pilimit":      50,
	    "rvprop":       "ids|timestamp|content",
	    "titles":       u"|".join(titles),
    })
    
    # Analyse each returned pages one by one
    titles = []
    qids = []
    if "query" in responses:
        for i in responses["query"]["pages"]:
            try:
                response = responses["query"]["pages"][i]
                
                qid = response["pageprops"]["wikibase_item"]
                
                if response.has_key("original"):
                    communes[qid]["image_url"] = response["original"]["source"]
                # Split the revision's content into section titles and content
                splited_content = re.split("\n==([^=]+)==", response["revisions"][0]["*"])
                
                # Search and regroup sections into the choosen one according to a lookup table and sum their weight
                for j in range(1, len(splited_content), 2):
                    for section in ["section_geography", "section_history", "section_economy", "section_demographics", "section_etymology", "section_governance", "section_culture", "section_infrastructure"]:
                        if splited_content[j].strip() in sections_lookup_table[section]:
                            communes[qid][section] += len(splited_content[j+1])
                            break
            
            except:
                print "--> Error with the article '"+responses["query"]["pages"][i]["title"]+"'"
Pywiki.get_article_datas = get_article_datas


"""
limit: 50 (500)
"""
def get_pdd_datas(self, titles, qids):
    responses = self.request({
        "format":       "json",
        "action":       "query",
	    "prop":         "revisions",
	    "rvprop":       "ids|timestamp|content",
	    "titles":       u"Discussion:"+u"|Discussion:".join(titles),
    })
    
    if "query" in responses:
        for i in responses["query"]["pages"]:
            response = responses["query"]["pages"][i]
            
            title = response["title"][11:]
            try:
                content = response["revisions"][0]["*"]
                try:
                    communes[qids[titles.index(title)]]['progress'] = re.findall(ur"{{Wikiprojet.*Avancement *= *(\?|ébauche|BD|B|A)", content, re.DOTALL | re.UNICODE | re.IGNORECASE)[0]
                except IndexError:
                    communes[qids[titles.index(title)]]['progress'] = "?"
                try:
                    communes[qids[titles.index(title)]]['importance'] = re.findall(ur"{{Wikiprojet.*Communes de France *\| *(\?|faible|moyenne|élevée|maximum)", content, re.DOTALL | re.UNICODE | re.IGNORECASE)[0]
                except IndexError:
                    communes[qids[titles.index(title)]]['importance'] = "?"
            except KeyError:
                communes[qids[titles.index(title)]]['progress'] = "?"
                communes[qids[titles.index(title)]]['importance'] = "?"
Pywiki.get_pdd_datas = get_pdd_datas  


def update_DB():
    conn = pymysql.connect(user=config.get('mysql', 'user'), password=config.get('mysql', 'password'), charset='utf8')
    with conn.cursor() as curr:
        curr.execute('USE ma_commune');
        for qid in communes:
            curr.execute(u"INSERT INTO communes (`qid`, `title`, `wp_title`, `wv_title`, `commons_category`, `suggest_str`, `insee`, `population`, `badge`, `progress`, `importance`, `latitude`, `longitude`, `geoshape`, `section_geography`, `section_history`, `section_economy`, `section_demographics`, `section_etymology`, `section_governance`, `section_culture`, `section_infrastructure`, `updated`) VALUES(%(qid)s, %(title)s, %(wp_title)s, %(wv_title)s, %(commons_category)s, %(suggest_str)s, %(insee)s, %(population)s, %(badge)s, %(progress)s, %(importance)s, %(latitude)s, %(longitude)s, %(geoshape)s, %(section_geography)s, %(section_history)s, %(section_economy)s, %(section_demographics)s, %(section_etymology)s, %(section_governance)s, %(section_culture)s, %(section_infrastructure)s, NOW()) ON DUPLICATE KEY UPDATE `qid`=VALUES(`qid`), `title`=VALUES(`title`), `wp_title`=VALUES(`wp_title`), `wv_title`=VALUES(`wv_title`), `commons_category`=VALUES(`commons_category`), `suggest_str`=VALUES(`suggest_str`), `insee`=VALUES(`insee`), `population`=VALUES(`population`), `badge`=VALUES(`badge`), `progress`=VALUES(`progress`), `importance`=VALUES(`importance`), `latitude`=VALUES(`latitude`), `longitude`=VALUES(`longitude`), `geoshape`=VALUES(`geoshape`), `section_geography`=VALUES(`section_geography`), `section_history`=VALUES(`section_history`), `section_economy`=VALUES(`section_economy`), `section_demographics`=VALUES(`section_demographics`), `section_etymology`=VALUES(`section_etymology`), `section_governance`=VALUES(`section_governance`), `section_culture`=VALUES(`section_culture`), `section_infrastructure`=VALUES(`section_infrastructure`), `updated`=NOW()", communes[qid])
        conn.commit()
        

print ("Update started at {}".format(datetime.datetime.now()))
frwiki = Pywiki("frwiki")
frwiki.login()
wdwiki = Pywiki("wikidatawiki")
wdwiki.login()I don't, sorry, beyond Julien and Max.


qids = get_all_items('SELECT DISTINCT ?item WHERE { ?item wdt:P31/wdt:P279* wd:Q484170 . }')
initialise_structure(qids)

count = 0
while len(qids) > 0:
    wp_titles = wdwiki.get_wikidata_datas(qids[:50])
    frwiki.get_article_datas(wp_titles)
    frwiki.get_pdd_datas(wp_titles, qids[:50])
    get_geoshape_datas(qids[:50])
    count += len(qids[:50])
    print count
    del qids[:50]
    
update_DB()

content = "Bot-generated report, don't edit this page manually."
if len(error_report) > 0:
    for error in error_report:
        content += "* {{Q|" + error['qid'] + "}}: " + error['message'] + "\n"
    wdwiki.replace("Wikidata:WikiProject France/Communes/Rapport", content, "update report", nocreate=True)

print ("Update finished at {}".format(datetime.datetime.now()))

