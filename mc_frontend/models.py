from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from pywiki_light import *


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
        self.averages = {}
        self.percentages = {}

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
                'article': self.data,
                'averages': self.averages,
                'percentages': self.percentages,
                'live_wp_data': self.live_wp_data}

    def get_live_wp_data(self):
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
            "coprop": "globe|type|name|dim|country|region",
            "coprimary": "all",
            "codistancefrompage": "Paris"
        }
        self.live_wp_data = frwiki.request(payload)


def avg(source_list, key):
    # Returns the average number of bytes in a section for a list of articles
    return int(float(sum(d[key] for d in source_list)) / len(source_list))
