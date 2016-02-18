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

verbose = 1

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

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

Données à récupérer depuis Wikidata :
- Catégorie Commons
- Population
- présence ou non d'une image enregistrée
- Pays (pour extension éventuelle du projet à d'autre pays)
- Code postal
- Code Insee
- Département
"""


class Article(object):
    def __init__(self):
        self.label = ''
        self.title = ''
        self.qid = ''

    def getWikidataContent(self):
        wd_url = "https://www.wikidata.org/wiki/Special:EntityData/{}.json".format(self.qid)
        print("Fetching: {}".format(wd_url))
        response = requests.get(wd_url)
        wd_content = json.loads(response.text)
        print(wd_content['sitelinks'])

######
commune = Article()

commune.qid = "Q214396"
# "Q214396" = Broons

commune.getWikidataContent()


