#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
# from bs4 import BeautifulSoup
import json

verbose = False


def query_category(category, gcmcontinue=''):
    api_base = "https://fr.wikipedia.org/w/api.php"

    params = [('format', 'json'),
              ('action', 'query'),
              ('prop', 'info|pageprops'),
              ('generator', 'categorymembers'),
              ('inprop', 'url'),
              ('ppprop', 'wikibase_item'),
              ('gcmlimit', 500),
              ('gcmnamespace', 0),
              ('gcmtitle', category)]

    if gcmcontinue:
        params.append(('gcmcontinue', gcmcontinue))

    try:
        response = requests.get(api_base, params=params)
        return json.loads(response.text)
    except 'ConnectionError':
        print('Server unreachable')


def extract_communes_data(pages, dep_number):
    results = []
    for key, page in pages.items():
        if 'pageprops' in page:
            qid = page['pageprops']['wikibase_item']
        else:
            qid = ''
        results.append((page['title'],
                        dep_number,
                        page['canonicalurl'],
                        qid))
    return results


def writecsv(text, file):
    if len(text):
        with open(file, "w") as f:
            f.write(text)
            f.close()

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
              ('976', "Catégorie:Commune de Mayotte")]

communes = [('Paris', '75', 'https://fr.wikipedia.org/wiki/Paris', 'Q90')]
for c in categories:
    communes_data = query_category(c[1])
    if 'query' in communes_data:
        if 'pages' in communes_data['query']:
            new_communes = extract_communes_data(
                communes_data['query']['pages'],
                c[0])
            if verbose:
                print(new_communes)
            communes += new_communes

    while 'continue' in communes_data:
        gcmcontinue = communes_data['continue']['gcmcontinue']
        communes_data = query_category(c[1], gcmcontinue)
        if 'query' in communes_data:
            if 'pages' in communes_data['query']:
                new_communes = extract_communes_data(
                    communes_data['query']['pages'],
                    c[0])
                if verbose:
                    print(new_communes)
                communes += new_communes

        print('continue for {}'.format(c[0]))
    else:
        print('OK for {}'.format(c[0]))

communes = sorted(communes)

output = ""
counters = {}
for c in communes:
    title, dep_number, url, qid = c
    output += '"{}" ; "{}" ; "{}" ; "{}"\n'.format(title, dep_number, url, qid)
    if dep_number not in counters:
        counters[dep_number] = 1
    else:
        counters[dep_number] += 1

    if not qid:
        print("Missing Qid for {} ({}, {})".format(title, dep_number, url))

for k in sorted(counters.keys()):
    print(k, counters[k])

writecsv(output, 'resources/extract-wikipedia-categories.csv')
