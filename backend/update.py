#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from pywiki_light import *
import re

verbose = False

categories = [
    ('01', "Catégorie:Commune de l'Ain"),
    ('02', "Catégorie:Commune de l'Aisne"),
    ('03', "Catégorie:Commune de l'Allier"),
    ('04', "Catégorie:Commune des Alpes-de-Haute-Provence"),
    ('05', "Catégorie:Commune des Hautes-Alpes"),
    ('06', "Catégorie:Commune des Alpes-Maritimes"),
    ('07', "Catégorie:Commune de l'Ardèche"),
    ('08', "Catégorie:Commune des Ardennes"),
    ('09', "Catégorie:Commune de l'Ariège"),
    ('10', "Catégorie:Commune de l'Aube"),
    ('11', "Catégorie:Commune de l'Aude"),
    ('12', "Catégorie:Commune de l'Aveyron"),
    ('13', "Catégorie:Commune des Bouches-du-Rhône"),
    ('14', "Catégorie:Commune du Calvados"),
    ('15', "Catégorie:Commune du Cantal"),
    ('16', "Catégorie:Commune de la Charente"),
    ('17', "Catégorie:Commune de la Charente-Maritime"),
    ('18', "Catégorie:Commune du Cher"),
    ('19', "Catégorie:Commune de la Corrèze"),
    ('2A', "Catégorie:Commune de la Corse-du-Sud"),
    ('2B', "Catégorie:Commune de la Haute-Corse"),
    ('21', "Catégorie:Commune de la Côte-d'Or"),
    ('22', "Catégorie:Commune des Côtes-d'Armor"),
    ('23', "Catégorie:Commune de la Creuse"),
    ('24', "Catégorie:Commune de la Dordogne"),
    ('25', "Catégorie:Commune du Doubs"),
    ('26', "Catégorie:Commune de la Drôme"),
    ('27', "Catégorie:Commune de l'Eure"),
    ('28', "Catégorie:Commune d'Eure-et-Loir"),
    ('29', "Catégorie:Commune du Finistère"),
    ('30', "Catégorie:Commune du Gard"),
    ('31', "Catégorie:Commune de la Haute-Garonne"),
    ('32', "Catégorie:Commune du Gers"),
    ('33', "Catégorie:Commune de la Gironde"),
    ('34', "Catégorie:Commune de l'Hérault"),
    ('35', "Catégorie:Commune d'Ille-et-Vilaine"),
    ('36', "Catégorie:Commune de l'Indre"),
    ('37', "Catégorie:Commune d'Indre-et-Loire"),
    ('38', "Catégorie:Commune de l'Isère"),
    ('39', "Catégorie:Commune du département du Jura"),
    ('40', "Catégorie:Commune des Landes"),
    ('41', "Catégorie:Commune de Loir-et-Cher"),
    ('42', "Catégorie:Commune de la Loire"),
    ('43', "Catégorie:Commune de la Haute-Loire"),
    ('44', "Catégorie:Commune de la Loire-Atlantique"),
    ('45', "Catégorie:Commune du Loiret"),
    ('46', "Catégorie:Commune du Lot"),
    ('47', "Catégorie:Commune de Lot-et-Garonne"),
    ('48', "Catégorie:Commune de la Lozère"),
    ('49', "Catégorie:Commune de Maine-et-Loire"),
    ('50', "Catégorie:Commune de la Manche"),
    ('51', "Catégorie:Commune de la Marne"),
    ('52', "Catégorie:Commune de la Haute-Marne"),
    ('53', "Catégorie:Commune de la Mayenne"),
    ('54', "Catégorie:Commune de Meurthe-et-Moselle"),
    ('55', "Catégorie:Commune de la Meuse"),
    ('56', "Catégorie:Commune du Morbihan"),
    ('57', "Catégorie:Commune de la Moselle"),
    ('58', "Catégorie:Commune de la Nièvre"),
    ('59', "Catégorie:Commune du Nord"),
    ('60', "Catégorie:Commune de l'Oise"),
    ('61', "Catégorie:Commune de l'Orne"),
    ('62', "Catégorie:Commune du Pas-de-Calais"),
    ('63', "Catégorie:Commune du Puy-de-Dôme"),
    ('64', "Catégorie:Commune des Pyrénées-Atlantiques"),
    ('65', "Catégorie:Commune des Hautes-Pyrénées"),
    ('66', "Catégorie:Commune des Pyrénées-Orientales"),
    ('67', "Catégorie:Commune du Bas-Rhin"),
    ('68', "Catégorie:Commune du Haut-Rhin"),
    ('69', "Catégorie:Commune du Rhône"),
    ('70', "Catégorie:Commune de la Haute-Saône"),
    ('71', "Catégorie:Commune de Saône-et-Loire"),
    ('72', "Catégorie:Commune de la Sarthe"),
    ('73', "Catégorie:Commune de la Savoie"),
    ('74', "Catégorie:Commune de la Haute-Savoie"),
    # Paris n'ayant qu'une communne, le 75 n'est pas listé ici
    ('76', "Catégorie:Commune de la Seine-Maritime"),
    ('77', "Catégorie:Commune de Seine-et-Marne"),
    ('78', "Catégorie:Commune des Yvelines"),
    ('79', "Catégorie:Commune des Deux-Sèvres"),
    ('80', "Catégorie:Commune de la Somme"),
    ('81', "Catégorie:Commune du Tarn"),
    ('82', "Catégorie:Commune de Tarn-et-Garonne"),
    ('83', "Catégorie:Commune du Var"),
    ('84', "Catégorie:Commune de Vaucluse"),
    ('85', "Catégorie:Commune de la Vendée"),
    ('86', "Catégorie:Commune de la Vienne"),
    ('87', "Catégorie:Commune de la Haute-Vienne"),
    ('88', "Catégorie:Commune du département des Vosges"),
    ('89', "Catégorie:Commune de l'Yonne"),
    ('90', "Catégorie:Commune du Territoire de Belfort"),
    ('91', "Catégorie:Commune de l'Essonne"),
    ('92', "Catégorie:Commune des Hauts-de-Seine"),
    ('93', "Catégorie:Commune de la Seine-Saint-Denis"),
    ('94', "Catégorie:Commune du Val-de-Marne"),
    ('95', "Catégorie:Commune du Val-d'Oise"),
    ('971', "Catégorie:Commune de la Guadeloupe‎"),
    ('972', "Catégorie:Commune de la Martinique‎"),
    ('973', "Catégorie:Commune de la Guyane‎"),
    ('974', "Catégorie:Commune de La Réunion‎"),
    ('976', "Catégorie:Commune de Mayotte")
]

sections_lookup_table = {
    u"geography": [u"Géographie", u"Lieux et monuments", u"Monuments", u"Jumelages", u"Environnement", u"Édifice religieux", u"Communes limitrophes", u"Édifices religieux", u"Lieux-dits et écarts", u"Climat", u"Vignoble", u"Lieux, monuments et pôles d'intérêt", u"Sites et monuments", u"Patrimoine naturel", u"Monuments et sites", u"Monuments et lieux touristiques", u"Géologie", u"Hydrographie", u"Lieux-dits"],
    u"history": [u"Histoire", u"Héraldique", u"Blasonnement", u"Emblèmes", u"Armoiries", u"Archives", u"Blason", u"Historique"],
    u"economy": [u"Économie", u"Tourisme", u"Économie et tourisme", u"Activités économiques", u"Activité économique"],
    u"demographics": [u"Population et société", u"Personnalités liées à la commune", u"Démographie", u"Enseignement", u"Personnalités liées", u"Personnalités", u"Personnalité liée à la commune", u"Cultes", u"Culte", u"Éducation"],
    u"etymology": [u"Toponymie", u"Toponyme", u"Toponymie et héraldique", u"Dénomination", u"Étymologie", u"Nom des habitants"],
    u"governance": [u"Politique et administration", u"Administration", u"Santé", u"Jumelage", u"Intercommunalité"],
    u"culture": [u"Culture locale et patrimoine", u"Culture et patrimoine", u"Activité et manifestations", u"Vie locale", u"Sports", u"Équipements", u"Équipements, services et vie locale", u"Culture", u"Événements", u"Patrimoine", u"Vie pratique", u"Équipements et services", u"Langue bretonne", u"Patrimoine religieux", u"Associations", u"Manifestations", u"Équipements ou services", u"Activités festives", u"Activité culturelle et manifestations", u"Loisirs", u"Activité, label et manifestations", u"Vie associative", u"Cadre de vie", u"Cinéma", u"Activités", u"Activités et manifestations", u"Gastronomie", u"Manifestations culturelles et festivités", u"Festivités", u"Sport", u"Patrimoine civil", u"Distinctions culturelles", u"Animations", u"Infrastructures", u"Fêtes et loisirs", u"Société", u"Vie culturelle", u"Littérature", u"Activités associatives, culturelles, festives et sportives"],
    u"infrastructure": [u"Urbanisme", u"Transports", u"Transport", u"Voies de communication et transports", u"Transports et voies de communications", u"Urbanisme et habitat", u"Transports en commun", u"Urbanisation", u"Industrie"],
}

communes = {}


"""
Get a set of comunes in the given category and analyse it's data
"""
def get_communes_in_cat(self, category, gcm_continue=""):
    # Request 100 pages out of the given category with their qid, first image, and last revision
    responses = self.request({
        "format":       "json",
        "action":       "query",
	    "prop":         "pageprops|pageimages|revisions",
	    "ppprop":       "wikibase_item",
	    "piprop":       "original",
	    "pilimit":      50,
	    "rvprop":       "ids|timestamp|content",
        "generator":    "categorymembers",
        "gcmtitle":     category,
        "gcmtype":      "page",
        "gcmnamespace": NS_MAIN,
        "gcmlimit":     50,
        "gcmcontinue":  gcm_continue,
    })
    
    # Check if there are some pages left in the category
    gcm_continue = None
    if "continue" in responses:
        if "gcmcontinue" in responses["continue"]:
            gcm_continue = responses["continue"]["gcmcontinue"]
    
    # Analyse each returned pages one by one
    titles = []
    qids = []
    if "query" in responses:
        for i in responses["query"]["pages"]:
            try:
                response = responses["query"]["pages"][i]
                
                # Collect all the interesting datas from the response for the current town
                title = response["title"]
                qid = response["pageprops"]["wikibase_item"]
                timestamp = response["revisions"][0]["timestamp"]
                image = None
                if response.has_key("original"):
                    image = response["original"]["source"]

                sections_weight = weigh_sections(response["revisions"][0]["*"], title)

                # Store all thoose fetched datas
                titles += [title]
                qids += [qid]
                communes[qid] = {
                    "qid": qid,
                    "name":"",
                    "wp_title": "fr:"+title,
                    "image_url": image,
                    "population":0,
                    "insee":0,
                    "commons_cat":"",
                    "badge":"",
                    "latitude":0,
                    "longitude":0,
                    "progress":"",
                    "importance":"",
                    "sections": sections_weight,
                    "timestamp": timestamp,
                }
            except:
                print "--> Error with the article '"+responses["query"]["pages"][i]["title"]+"'"
    
    return (titles, qids, gcm_continue)
Pywiki.get_communes_in_cat = get_communes_in_cat


def weigh_sections(content, title):
    # Initialise the weight structure
    sections_weight = {
        u"geography": 0,
        u"history": 0,
        u"economy": 0,
        u"demographics": 0,
        u"etymology": 0,
        u"governance": 0,
        u"culture": 0,
        u"infrastructure": 0,
    }
    
    # Split the revision's content into section titles and content
    splited_content = re.split("\n==([^=]+)==", content)
    
    # Search and regroup sections into the choosen one according to a lookup table and sum their weight
    for j in range(1, len(splited_content), 2):
        for section in sections_weight:
            if splited_content[j].strip() in sections_lookup_table[section]:
                sections_weight[section] += len(splited_content[j+1])
                break
    
    return sections_weight


def get_wikidata_datas(self, qids):
    # Request 100 pages out of the given category with their qid, first image, and last revision
    responses = self.request({
        "action":    "wbgetentities",
        "format":    "json",
        "ids":       "|".join(qids),
        "props":     "sitelinks|aliases|labels|claims",
        "languages": "fr|en"
    })
    
    if "entities" in responses:
        for qid in responses["entities"]:
            response = responses["entities"][qid]
            communes[qid]['name'] = response["labels"]["fr"]["value"]
            communes[qid]['badge'] = response["sitelinks"]["frwiki"]["badges"]
            try:
                communes[qid]['population'] = response["claims"]["P1082"][0]["mainsnak"]["datavalue"]["value"]["amount"]
            except (TypeError, KeyError):
                pass
            try:
                communes[qid]['insee'] = response["claims"]["P374"][0]["mainsnak"]["datavalue"]["value"]
            except (TypeError, KeyError):
                pass
            try:
                communes[qid]['commons_cat'] = response["claims"]["P373"][0]["mainsnak"]["datavalue"]["value"]
            except (TypeError, KeyError):
                pass
            try:
                coordinates = response["claims"]["P625"][0]["mainsnak"]["datavalue"]["value"]
                communes[qid]['latitude'] = coordinates["latitude"]
                communes[qid]['longitude'] = coordinates["longitude"]
            except (TypeError, KeyError):
                pass
Pywiki.get_wikidata_datas = get_wikidata_datas


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


# DB connection
"""
def db_connect():
    try:
        

    except pymysql.err.OperationalError : 
        sys.exit("Invalid Input: Wrong username/database or password found, please try again")

    return cnx


def updateDB(self, cnx):
    self.conn = pymysql.connect(read_default_file="~/my.cnf")
    self.curr = self.conn.cursor()
    try:
        # update the main table
        # for now we only add badges
        updates = []
        if len(self.wp_badges):
            badges = '|'.join(self.wp_badges)
            updates.append("badge ='{}'".format(badges))

        if len(updates):
            query = "UPDATE communes SET {} WHERE qid='{}'".format(
                ', '.join(updates), self.qid)
        else:
            # If no other update to table communes is performed,
            # update the timestamp manually
            query = "UPDATE communes \
            set updated=now() WHERE qid='{}'".format(
                    self.qid)
        cursor.execute(query)

        # delete rows relative to the commune in sections
        query = "DELETE FROM sections WHERE qid='{}';".format(self.qid)
        cursor.execute(query)

        # insert the new sections
        for section_title, v in self.sections.items():
            cursor.execute("INSERT INTO sections \
                (qid, title, size, has_sub_article) \
                 VALUES(%(qid)s, %(section_title)s, \
                  %(size)s, %(has_sub_article)r);",
                           {'qid': self.qid,
                            'section_title': section_title,
                            'size': v['size'],
                            'has_sub_article': False})

        cnx.commit()
    except Exception as e:
        errors.append('Could not update data for {}: {} // {}'.format(
                      self.qid, e, pymysql.paramstyle))
        cnx.rollback()

    cursor.close()
"""

frwiki = Pywiki("frwiki-NeoBot")
frwiki.login()
wdwiki = Pywiki("wikidatawiki-NeoBot")
wdwiki.login()

for category in categories:
    gcm_continue = ""
    print category[0] + ". " + category[1]
    while gcm_continue != None:
        (titles, qids, gcm_continue) = frwiki.get_communes_in_cat(category[1], gcm_continue)
        wdwiki.get_wikidata_datas(qids)
        frwiki.get_pdd_datas(titles, qids)
        print len(communes)
    save_in_db()
    
print communes['Q147987']
print communes['Q130994']
