from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from pywiki_light import *
from nightly_update import get_sections_length
import hashlib
import re


class Aliases(models.Model):
    alias = models.CharField(max_length=64)
    qid = models.CharField(max_length=16)

    class Meta:
        db_table = 'aliases'


class Communes(models.Model):
    qid = models.CharField(primary_key=True, max_length=16)
    title = models.CharField(max_length=255)
    wp_title = models.CharField(max_length=255)
    wv_title = models.CharField(max_length=255)
    commons_category = models.CharField(max_length=255)
    suggest_str = models.CharField(max_length=255)
    insee = models.CharField(max_length=16)
    population = models.IntegerField(blank=True, null=True)
    badge = models.CharField(max_length=20, blank=True, null=True)
    progress = models.CharField(max_length=20, blank=True, null=True)
    importance = models.CharField(max_length=20, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    geoshape = models.TextField()
    section_geography = models.IntegerField()
    section_history = models.IntegerField()
    section_economy = models.IntegerField()
    section_demographics = models.IntegerField()
    section_etymology = models.IntegerField()
    section_governance = models.IntegerField()
    section_culture = models.IntegerField()
    section_infrastructure = models.IntegerField()
    updated = models.DateTimeField()

    class Meta:
        db_table = 'communes'
        indexes = [
            models.Index(fields=['qid']),
            models.Index(fields=['suggest_str']),
        ]


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        db_table = 'django_migrations'


class SectionStats(models.Model):
    section_title = models.CharField(max_length=64)
    mean_size = models.IntegerField()
    importance = models.CharField(max_length=20, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'section_stats'


class Sections(models.Model):
    qid = models.ForeignKey(Communes,
                            models.DO_NOTHING,
                            db_column='qid',
                            blank=True,
                            null=True)
    title = models.CharField(max_length=64)
    size = models.IntegerField()
    has_sub_article = models.IntegerField()

    class Meta:
        db_table = 'sections'


class Article:
    def __init__(self, qid):
        self.qid = qid

        self.anoncontributors = -1
        self.averages = {}
        self.coordinates = []
        self.extract = ""
        self.fr_wp_limits = []
        self.images = []
        self.length = -1
        self.links = -1
        self.linkshere = -1
        self.pageimage = []
        self.pageviews = []
        self.percentages = {}
        self.sections_live = {}
        self.registeredcontributors = -1
        self.todo_list = ""
        self.wd_claims = {}
        self.wd_description = ""
        self.wd_label = ""
        self.wd_sitelinks_number = -1
        self.wp_article = []
        self.wp_title = ""
        self.wv_article = []

        self.sections = [
            'section_geography',
            'section_history',
            'section_economy',
            'section_demographics',
            'section_etymology',
            'section_governance',
            'section_culture',
            'section_infrastructure']

        fields = self.sections + [
            'qid',
            'title',
            'insee',
            'suggest_str',
            'badge',
            'importance',
            'progress',
            'population',
            'commons_category',
            'wp_title',
            'wv_title',
            'updated'
        ]

        values = Communes.objects.filter(qid=qid).values(*fields)
        if len(values):
            self.data = values[0]
            self.data['local_db'] = True
            self.data['updated'] = datetime.timestamp(self.data['updated'])

            self.wp_title = self.data['wp_title']

            # In case the population data is missing:
            if self.data['population']:
                self.population = self.data['population']
            else:
                self.population = 0
        else:
            self.data = {}
            self.data['local_db'] = False

        if 'importance' in self.data:
            self.importance = self.data['importance']
            self.sections_stats('importance')

    def sections_stats(self, criterion):
        if criterion == 'population':
            pop_range_min = 10**(len(str(self.population)) - 1)
            if pop_range_min < 10:
                pop_range_min = 0
            pop_range_max = 10**(len(str(self.population)) + 1)
            data = Communes.objects.filter(
                population__range=(pop_range_min, pop_range_max))
        elif criterion == 'importance':
            data = Communes.objects.filter(
                importance=self.importance)

        stats = data.values(*self.sections)
        stats = list(stats)

        for i in self.sections:
            self.averages[i] = avg(stats, i)
            self.percentages[i] = int(self.data[i] / self.averages[i] * 100)

    def get_data(self):
        return {'qid': self.qid,
                'local_db': self.data,
                'anoncontributors': self.anoncontributors,
                'averages': self.averages,
                'coordinates': self.coordinates,
                'extract': self.extract,
                'fr_wp_limits': self.fr_wp_limits,
                'images': self.images,
                'images_number': len(self.images),
                'links': self.links,
                'linkshere': self.linkshere,
                'live_wd_data': self.live_wd_data,
                'pageviews': self.pageviews,
                'registeredcontributors': self.registeredcontributors,
                'pageimage': self.pageimage,
                'percentages': self.percentages,
                'sections_live': self.sections_live,
                'todo_list': self.todo_list,
                'wd_claims': self.wd_claims,
                'wd_description': self.wd_description,
                'wd_label': self.wd_label,
                'wd_sitelinks_number': self.wd_sitelinks_number,
                'wp_article': self.wp_article,
                'wp_title': self.wp_title,
                'wv_article': self.wv_article}

    def get_live_wd_data(self):
        try:
            wdwiki = Pywiki("wikidatawiki")
            wdwiki.login()

            props = [
                "info",
                "aliases",
                "labels",
                "descriptions",
                "claims",
                "datatype",
                "sitelinks/urls"
            ]

            payload = {
                "action": "wbgetentities",
                "format": "json",
                "ids": self.qid,
                "props": "|".join(props),
                "languages": "fr",
                "languagefallback": 1,
                "formatversion": "2"
            }

            results = wdwiki.request(payload)
            entity = results['entities'][self.qid]

            # TODO remove this inclusion
            self.live_wd_data = entity

            # claims
            if len(entity['claims']):
                self.wd_claims = entity['claims']
                # TODO manage specific properties.

            # descriptions
            if 'fr' in entity['descriptions']:
                self.wd_description = entity['descriptions']['fr']['value']

            # labels
            if 'fr' in entity['labels']:
                self.wd_label = entity['labels']['fr']['value']

            # sitelinks
            self.wd_sitelinks_number = len(entity['sitelinks'])

            if self.wd_sitelinks_number:
                if 'frwiki' in entity['sitelinks']:
                    self.wp_article = entity['sitelinks']['frwiki']
                    if self.wp_title == "":
                        self.wp_title = self.wp_article['title']

                if 'frwikivoyage' in entity['sitelinks']:
                    self.wv_article = entity['sitelinks']['frwikivoyage']

        except Exception as e:
            print("Can't retrieve live WD data for {}: {}".format(self.qid, e))

    def get_live_wp_data(self):
        try:
            frwiki = Pywiki("frwiki")
            frwiki.login()

            props = ['contributors',
                     'revisions',
                     'images',
                     'extracts',
                     'info',
                     'links',
                     'linkshere',
                     'pageimages',
                     'pageviews',
                     'coordinates']
            payload = {
                "action": "query",
                "format": "json",
                "prop": "|".join(props),
                "titles": "{0}|Discussion:{0}/À faire".format(self.wp_title),
                "formatversion": "2",
                "pclimit": "max",
                "rvprop": "ids|timestamp|flags|comment|user|content",
                "imlimit": "max",
                "exsentences": "2",
                "exintro": 1,
                "explaintext": 1,
                "plnamespace": "0",
                "pllimit": "max",
                "lhlimit": "max",
                "colimit": "max",
                "coprop": "type|name|dim|country|region",
                "coprimary": "all",
                "codistancefrompage": "Paris"
            }
            results = frwiki.request(payload)

            self.limits = results['limits']
            pages = results['query']['pages']

            # Looking for the todo page first, then the main article

            for page in pages:
                if 'À faire' in page['title']:
                    if 'missing' not in page:
                        self.todo_list = page['revisions'][0]['content']
                else:
                    # Main article
                    if 'anoncontributors' in page:
                        self.anoncontributors = page['anoncontributors']

                    if 'contributors' in page:
                        self.registeredcontributors = len(page['contributors'])

                    if 'coordinates' in page:
                        self.coordinates = page['coordinates']

                    if 'extract' in page:
                        self.extract = page['extract']

                    if 'images' in page:
                        for i in page['images']:
                            if i['title'][-4:].lower() != '.svg':
                                self.images.append([
                                    i['title'],
                                    commons_file_url(i['title'], 120)])

                    if 'links' in page:
                        self.links = len(page['links'])

                    if 'linkshere' in page:
                        self.linkshere = len(page['linkshere'])

                    if 'pageimage' in page:
                        self.pageimage = [
                            page['pageimage'],
                            commons_file_url(page['pageimage'], 200)]

                    if 'pageviews' in page:
                        self.pageviews = page['pageviews']

                    if 'revisions' in page:
                        self.sections_live = get_sections_length(
                            page['revisions'][0]['content'])

        except Exception as e:
            print("Can't retrieve live WP data for {}: {}".format(self.qid, e))


def avg(source_list, key):
    # Returns the average number of bytes in a section for a list of articles
    return int(float(sum(d[key] for d in source_list)) / len(source_list))


def commons_file_url(filename, width=0):
    # Returns the direct URL of a file on Wikimedia Commons.
    # Per https://commons.wikimedia.org/wiki/Commons:FAQ#What_are_the_strangely_named_components_in_file_paths.3F
    if filename[:8] == 'Fichier:':
        filename = filename[8:]
    elif filename[:5] == 'File':
        filename = filename[5:]

    filename = re.sub(' ', '_', filename)

    hashed_filename = hashlib.md5(filename.encode('utf-8')).hexdigest()

    base_url = "https://upload.wikimedia.org/wikipedia/commons"

    if not width:
        url = "{}/{}/{}/{}".format(
            base_url,
            hashed_filename[:1],
            hashed_filename[:2],
            filename)

    else:
        url = "{}/thumb/{}/{}/{}/{}px-{}".format(
            base_url,
            hashed_filename[:1],
            hashed_filename[:2],
            filename,
            width,
            filename)
        if filename[-4:].lower() == '.svg':
            url += ".png"

    return url
