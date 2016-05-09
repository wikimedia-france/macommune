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

# Constants
VERBOSE = 0
LANGUAGE = 'fr'
WD_BASE_URL = 'https://www.wikidata.org/wiki/'
WP_BASE_URL = 'https://{}.wikipedia.org/'.format(LANGUAGE)
WP_PARSOID_URL = WP_BASE_URL + 'api/rest_v1/page/html/'
WP_API_BASE = WP_BASE_URL + "w/api.php"
WP_DB = LANGUAGE + 'wiki'

errors = []


class Article(object):
    def __init__(self, initial_data):
        if VERBOSE:
            print("Create new article with data:")
            print(initial_data)
        self.qid = initial_data['qid']
        self.title = initial_data['title']
        self.wp_title = initial_data['wp_title']
        self.insee = initial_data['insee']
        self.progress = initial_data['progress']
        self.importance = initial_data['importance']

        split_title= self.wp_title.split(':')
        if len(split_title) == 2:
            self.wp_title_no_prefix = split_title[1]
        else:
            self.wp_title_no_prefix = ''
            errors.append('Wrong title for item {}'.format(self.qid))
        # The label in Wikidata for the selected LANGUAGE
        self.wd_label = ''
        # The description in Wikidata for the selected LANGUAGE
        self.wd_description = ''
        # The aliases in Wikidata for the selected LANGUAGE
        self.wd_aliases = []
        self.wp_url = ''                # The full URL to the Wikipedia article
        self.wp_badges = []
        self.claims = {}
        self.commonscat = []
        self.population = []
        self.wd_images = []
        self.donotupdate = False

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

        # Get item content
        try:
            wd_url = "{}Special:EntityData/{}.json".format(WD_BASE_URL,
                                                           self.qid)
            if VERBOSE:
                print("Fetching: {}".format(wd_url))
            response = requests.get(wd_url)
            wd_content = json.loads(response.text)
            self.item_content = wd_content['entities'][self.qid]
        except requests.exceptions.RequestException as e:
            errors.append('Error when retrieving data for {}: {}'.format(
                self.qid, e))
            self.donotupdate = True

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
        url = WP_PARSOID_URL + self.wp_title_no_prefix
        print('Retrieving sections for {}'.format(url))

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text)
            headers = {}
            soup_headers = soup.find_all('h2')
            for first, second in zip(soup_headers, soup_headers[1:]):
                section_size = len(' '.join(text for text in between(
                    soup.find('h2', text=first.text),
                    soup.find('h2', text=second.text))))

                section_title = first.text.strip()
                headers[section_title] = {"size": section_size,
                                          "has_sub_article": False}

            # Looking for detailed articles
            soup_detailed = soup.find_all('div', 'loupe')
            for s in soup_detailed:
                if s.find_previous("h2") is not None:
                    section_title = s.find_previous("h2").text.strip()
                else:
                    errors.append('Sub article error for {}'.format(
                        self.qid))
                # last section is not in headers but we don't need it
                if section_title in headers:
                    headers[section_title]['has_sub_article'] = True

            self.sections= headers
            print(headers)

        except requests.exceptions.RequestException as e:
            errors.append('Error when retrieving sections for {}: {}'.format(
                self.qid, e))
            self.donotupdate = True

    def updateEval(self, cnx, evaluation):
         cnx.autocommit(False)
         cursor = cnx.cursor()

         try:
            updates = []
            if 'importance' in evaluation:
                importance = evaluation['importance']
                updates.append("importance='{}'".format(importance))
            if 'progress' in evaluation:
                progress = evaluation['progress']
                updates.append("progress='{}'".format(progress))

            if len(updates):
                query = "UPDATE communes SET {} WHERE qid='{}';".format(
                    ', '.join(updates), self.qid)

                print(query)
                cursor.execute(query)

            cnx.commit()


         except Exception as e:
            errors.append('Could not update data for {}: {} // {}'.format(
            self.qid, e, query))
            cnx.rollback()

         cursor.close()

    def updateDB(self, cnx):
        if VERBOSE:
            print("Updating DB for {}".format(self.qid))
        cnx.autocommit(False)
        if self.donotupdate == False:
            cursor = cnx.cursor()

            try:
                # update the main table
                # for now we only add badges and importance
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
                    query = "UPDATE communes set updated=now() WHERE qid='{}'".format(
                            self.qid)
                cursor.execute(query)

                # delete rows relative to the commune in sections
                query = "DELETE FROM sections WHERE qid='{}';".format(self.qid)
                cursor.execute(query)

                # insert the new sections
                for section_title, v in self.sections.items():
                    if v['has_sub_article'] == True:
                        has_sub_article = "TRUE"
                    else:
                        has_sub_article = "FALSE"
                    
                    cursor.execute("INSERT INTO sections (qid, title, size, has_sub_article) VALUES(%(qid)s, %(section_title)s, %(size)s, %(has_sub_article)r);",
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

            # select title, COUNT(qid) AS number, AVG(size) AS mean_size FROM sections GROUP BY title ORDER BY number DESC;

def get_communes(cnx, insee=''):
    fields = ['qid', 'title', 'wp_title', 'insee', 'progress', 'importance']

    cursor = cnx.cursor()
    query = "SELECT {} FROM communes".format(', '.join(fields))
    if insee:
        query += " WHERE insee LIKE '{}%' ORDER BY insee;".format(insee)
    else:
        query += " ORDER BY updated;"
    cursor.execute(query)

    communes = [dict(zip(fields, c)) for c in cursor]

    cursor.close()
    return communes


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


def extract_communes_data(pages, category):
    results = []
    for page in pages:
        title = page['title'].split(':')[1]
        results.append((title,
                        category))
    return results


# DB connection
def db_connect():
    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~/.my.cnf'))

    db_user = config['client']['user']
    db_password = config['client']['password']
    db_host = 'localhost'
    db_name = 'ma_commune'

    cnx = pymysql.connect(host=db_host,
                       port=3306,
                       user=db_user,
                       passwd=db_password,
                       db=db_name,
                       charset="utf8",
                       use_unicode=True)

    return cnx
