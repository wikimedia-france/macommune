#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup, NavigableString
import datetime
import json
import os               # Files and folder manipulations
import re               # Regular expressions
import csv              # CSV file manipulations
import sys
from collections import Counter
from termcolor import colored

# Constants
VERBOSE = 1
LANGUAGE = 'fr'
WD_BASE_URL = 'https://www.wikidata.org/wiki/'
WP_BASE_URL = 'https://{}.wikipedia.org/wiki/'.format(LANGUAGE)

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

        self.country = ""

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
        - Département ???

        """
        wd_url = "{}Special:EntityData/{}.json".format(WD_BASE_URL, self.qid)
        print("Fetching: {}".format(wd_url))
        response = requests.get(wd_url)
        wd_content = json.loads(response.text)
        item_content = wd_content['entities'][self.qid]

        # Label, description, aliases
        self.wd_label = item_content['labels'][LANGUAGE]['value']
        self.wd_description = item_content['descriptions'][LANGUAGE]['value']

        if item_content['aliases']:
            aliases = item_content['aliases'][LANGUAGE]
            for alias in aliases:
                self.wd_aliases.append(alias['value'])

        # Link to Wikipedia
        self.wp_url = item_content['sitelinks'][LANGUAGE + 'wiki']['url']
        self.wp_title = item_content['sitelinks'][LANGUAGE + 'wiki']['title']
        self.wp_badges = item_content['sitelinks'][
            LANGUAGE + 'wiki']['badges']  # list

        # Claims
        self.claims = item_content['claims']
        print(self.getClaimContent('P131'))

        print(self.qid, self.wd_label, self.wd_description, self.wd_aliases,
              self.wp_url, self.wp_title, self.wp_badges)

    def getClaimContent(self, property):
        """
        returns an array of the preferred values for the claim.
        If claims with a "preffered" rank are present, they are returned,
        else those with a "normal" rank are.

        Claims with an "obsolete" rank, or with an ending date qualifier
        are ignored.
        """

        preffered_values = []
        normal_values = []

        claims = self.claims[property]

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
            return preffered_values
        else:
            return normal_values


def getClaimValue(mainsnak):
    if mainsnak['datatype'] == 'wikibase-item':
        return mainsnak['datavalue']['value']['numeric-id']
    else:
        return "unknown datatype: {}".format(mainsnak['datatype'])

######

communes = ['Q90',  # Paris
            'Q214396',  # Broons
            'Q895168' # Bouquenom (ancienne commune)
            ]
commune = Article('Q214396')
# "Q214396" = Broons
commune.getWikidataContent()

commune = Article('Q895168')
commune.getWikidataContent()