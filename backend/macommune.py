#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup, NavigableString
import datetime
import json
import configparser
import os               # Files and folder manipulations
import re               # Regular expressions
import csv              # CSV file manipulations
import sys
import mysql.connector
from collections import Counter
from termcolor import colored
import pymysql


# Constants
VERBOSE = 1
LANGUAGE = 'fr'
WD_BASE_URL = 'https://www.wikidata.org/wiki/'
WP_BASE_URL = 'https://{}.wikipedia.org/'.format(LANGUAGE)
WP_PARSOID_URL = WP_BASE_URL + 'api/rest_v1/page/html/'
WP_API_BASE = WP_BASE_URL + "w/api.php"
WP_DB = LANGUAGE + 'wiki'

errors = []

# DB connection

config = configparser.ConfigParser()
config.read(os.path.expanduser('~/.my.cnf'))

db_user = config['client']['user']
db_password = config['client']['password']
db_host = 'localhost'
db_name = 'ma_commune'


conn = pymysql.connect(host=db_host,
                       port=3306,
                       user=db_user,
                       passwd=db_password,
                       db=db_name)

cur = conn.cursor()


"""
Données à récupérer d'un article
- Titre
- id Wikidata
- Présence d'un fichier de prononciation
- Remplissage du plan
- Taille de chaque section (en octet)
- présence d'un article détaillé pour la section
- évaluation (depuis la PDD)
- images
"""


class Article(object):
    def __init__(self, qid):
        self.qid = qid
        # The label in Wikidata for the selected LANGUAGE
        self.wd_label = ''
        # The description in Wikidata for the selected LANGUAGE
        self.wd_description = ''
        # The aliases in Wikidata for the selected LANGUAGE
        self.wd_aliases = []
        self.wp_url = ''                # The full URL to the Wikipedia article
        self.wp_title = ''
        self.wp_badges = []
        self.claims = {}
        self.commonscat = []
        self.population = []
        self.wd_images = []

        # Get item content
        wd_url = "{}Special:EntityData/{}.json".format(WD_BASE_URL, self.qid)
        print("Fetching: {}".format(wd_url))
        response = requests.get(wd_url)
        wd_content = json.loads(response.text)
        self.item_content = wd_content['entities'][self.qid]

    def getLabel(self):
        global errors
        if LANGUAGE in self.item_content['labels'].keys():
            self.wd_label = self.item_content['labels'][LANGUAGE]['value']
        else:
            errors.append('No {} label for item {}'.format(LANGUAGE, self.qid))

    def getDescription(self):
        global errors
        descriptions = self.item_content['descriptions']
        if LANGUAGE in descriptions.keys():
            self.wd_label = descriptions[LANGUAGE]['value']
        else:
            errors.append('No {} description for item {}'.format(
                LANGUAGE, self.qid))

    def getAliases(self):
        global errors
        if self.item_content['aliases']:
            if LANGUAGE in self.item_content['aliases']:
                aliases = self.item_content['aliases'][LANGUAGE]
                for alias in aliases:
                    self.wd_aliases.append(alias['value'])

    def getSitelink(self):
        sitelinks = self.item_content['sitelinks']
        if WP_DB in sitelinks.keys():
            self.wp_url = sitelinks[WP_DB]['url']
            self.wp_title = sitelinks[WP_DB]['title']
            self.wp_badges = sitelinks[WP_DB]['badges']
        else:
            errors.append('No {} sitelink for item {}'.format(
                LANGUAGE, self.qid))

    def getWikidataContent(self):
        """
        Retrieves some data about the city from the Wikidata item

        Données à récupérer depuis Wikidata :
        - P373  Catégorie Commons
        - P1082 Population
        - P18   présence ou non d'une image enregistrée
        - P17   Pays (pour extension éventuelle du projet à d'autre pays)
        - P281  Code postal
        - P374  code commune INSEE
        - P625  coordonnées géographiques

        """
        global errors

        self.getLabel()
        self.getDescription()
        self.getAliases()
        self.getSitelink()

        # Claims
        self.claims = self.item_content['claims']

        self.commonscat = self.getClaimContent('P373')  # Catégorie Commons
        if len(self.commonscat) > 1:
            errors.append('More than one commonscat for {}'.format(self.qid))

        self.population = self.getClaimContent('P1082')  # Population
        if len(self.population) > 1:
            errors.append('More than one population value for {}'.format(
                self.qid))

        self.wd_images = self.getClaimContent('P18')  # Image

        self.wd_country = self.getClaimContent('P17')  # Pays
        if len(self.wd_country) > 1:
            errors.append('More than one country value for {}'.format(
                self.qid))

        self.wd_postal_code = self.getClaimContent('P281')  # Code postal
        if len(self.wd_postal_code):
            for code in self.wd_postal_code:
                if len(code) != 5:
                    errors.append('Wrong postal code for {}: {}'.format(
                        self.qid, code))
        else:
            errors.append("Missing postal code for {}".format(self.qid))

        self.wd_insee_code = self.getClaimContent('P374')  # Code Insee
        if len(self.wd_insee_code):
            for code in self.wd_insee_code:
                if len(code) != 5:
                    errors.append('Wrong insee code for {}: {}'.format(
                        self.qid, code))
        else:
            errors.append("Missing insee code for {}".format(self.qid))

        self.wd_coords = self.getClaimContent('P625')  # Code coords

        print(self.qid, self.wd_label, self.wd_description, self.wd_aliases,
              self.wp_url, self.wp_title, self.wp_badges,)

    def getClaimContent(self, prop):
        """
        returns a list of the preferred values for the claim.
        If claims with a "preffered" rank are present, they are returned,
        else those with a "normal" rank are.

        Claims with an "obsolete" rank, or with an ending date qualifier
        are ignored.

        If there are no claims with that property, an empty list is returned.
        """

        preffered_values = []
        normal_values = []
        result = []

        if prop in self.claims.keys():
            claims = self.claims[prop]

            for c in claims:
                get_value = True
                if 'qualifiers' in c.keys():
                    qualifiers = c['qualifiers']
                    if 'P582' in qualifiers.keys():
                        get_value = False
                if get_value and c['rank'] == 'normal':
                    normal_values.append(getClaimValue(c['mainsnak']))
                elif get_value and c['rank'] == 'preffered':
                    preffered_values.append(getClaimValue(c['mainsnak']))

            if preffered_values:
                result = preffered_values
            elif normal_values:
                result = normal_values

        if VERBOSE:
            print("{}: {}".format(prop, result))
        return result

    def getWikipediaSections(self):
        print('Retrieving sections for {}'.format(self.wp_title))
        response = requests.get(WP_PARSOID_URL + self.wp_title)
        soup = BeautifulSoup(response.text)
        headers = {}
        soup_headers = soup.find_all('h2')
        for first, second in zip(soup_headers, soup_headers[1:]):
            section_length = len(' '.join(text for text in between(
                soup.find('h2', text=first.text),
                soup.find('h2', text=second.text))))

            section_title = first.text.strip()
            headers[section_title] = {"length": section_length}

        # Looking for detailed articles
        soup_detailed = soup.find_all('div', 'loupe')
        for s in soup_detailed:
            section_title = s.find_previous("h2").text.strip()
            if section_title in headers:
                headers[section_title]['detailed'] = True

        print(headers)


def get_communes(cnx, insee=''):
    cur = cnx.cursor()
    query = "SELECT qid FROM communes"
    if insee:
        query += " WHERE insee LIKE '{}%'".format(insee)
    query += " ORDER BY insee;"
    cur.execute(query)

    qids = []
    for row in cur:
        qids.append(row[0])

    cur.close()
    return qids


def between(current, end):
        while current and current != end:
            if isinstance(current, NavigableString):
                text = current
                if len(text):
                    yield text
            current = current.next_element


def getClaimValue(mainsnak):
    if mainsnak['datatype'] == 'wikibase-item':
        return mainsnak['datavalue']['value']['numeric-id']
    elif mainsnak['datatype'] == 'string':
        return mainsnak['datavalue']['value']
    elif mainsnak['datatype'] == 'quantity':
        return int(mainsnak['datavalue']['value']['amount'])
    elif mainsnak['datatype'] == 'commonsMedia':
        return mainsnak['datavalue']['value']
    elif mainsnak['datatype'] == 'external-id':
        return mainsnak['datavalue']['value']
    elif mainsnak['datatype'] == 'globe-coordinate':
        coords = mainsnak['datavalue']['value']
        return (coords['latitude'], coords['longitude'])
    else:
        if VERBOSE:
            print(mainsnak)
        return "unknown datatype: {}".format(mainsnak['datatype'])


def query_category(category, cmcontinue=''):
    params = [('format', 'json'),
              ('action', 'query'),
              ('list', 'categorymembers'),
              ('cmlimit', 500),
              ('cmnamespace', 1),
              ('cmtitle', category)]

    if cmcontinue:
        params.append(('cmcontinue', cmcontinue))

    try:
        response = requests.get(WP_API_BASE, params=params)
        return json.loads(response.text)
    except 'ConnectionError':
        print('Server unreachable')


def extract_communes_data(pages, category):
    results = []
    for page in pages:
        title = page['title'].split(':')[1]
        results.append((title,
                        category))
    return results


def getEvaluations():
    imp_base = "Category:Article sur les communes de France d'importance "
    imp_cats = ["maximum",
                "élevée",
                "moyenne",
                "faible",
                "inconnue"]

    communes_eval = []
    for c in imp_cats:
        communes_data = query_category(imp_base + c)
        if 'query' in communes_data:
            if 'categorymembers' in communes_data['query']:
                new_communes = extract_communes_data(
                    communes_data['query']['categorymembers'],
                    c)
                communes_eval += new_communes

        while 'continue' in communes_data:
            cmcontinue = communes_data['continue']['cmcontinue']
            communes_data = query_category(imp_base + c, cmcontinue)
            if 'query' in communes_data:
                if 'categorymembers' in communes_data['query']:
                    new_communes = extract_communes_data(
                        communes_data['query']['categorymembers'],
                        c)
                    communes_eval += new_communes

            print('continue for {}'.format(c))
        else:
            print('OK for {}'.format(c))

    return communes_eval


######

communes = get_communes(conn, '93')

#communes_eval = dict(getEvaluations())


for c in communes:
    commune = Article(c)
    commune.getWikidataContent()
    commune.getWikipediaSections()
    # commune.importance = communes_eval[commune.wp_title]
    #print(commune.importance)

print(errors)

conn.close()
