from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from pywiki_light import *
from .constants import SECTIONS_LOOKUP_TABLE
import hashlib
import re
from urllib.parse import quote


class Communes(models.Model):
    qid = models.CharField(primary_key=True, max_length=16)
    title = models.CharField(max_length=255, default='')
    wp_title = models.CharField(max_length=255, null=True, default=None)
    wv_title = models.CharField(max_length=255, null=True, default=None)
    commons_category = models.CharField(max_length=255, null=True, default=None)
    suggest_str = models.CharField(max_length=255, default='')
    insee = models.CharField(max_length=16, null=True, default=None)
    population = models.IntegerField(default=0)
    badge = models.CharField(max_length=20, blank=True, default='')
    progress = models.CharField(max_length=20, blank=True, default='?')
    importance = models.CharField(max_length=20, blank=True, default='?')
    section_geography = models.IntegerField(default=0)
    section_history = models.IntegerField(default=0)
    section_economy = models.IntegerField(default=0)
    section_demographics = models.IntegerField(default=0)
    section_etymology = models.IntegerField(default=0)
    section_governance = models.IntegerField(default=0)
    section_culture = models.IntegerField(default=0)
    section_infrastructure = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['qid']),
            models.Index(fields=['suggest_str']),
        ]


class Geoloc(models.Model):
    qid = models.OneToOneField(Communes, primary_key=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, default=None)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, default=None)
    geoshape = models.TextField(null=True, default=None)

    class Meta:
        indexes = [
            models.Index(fields=['latitude', 'longitude']),
        ]


class Sections(models.Model):
    qid = models.ForeignKey(Communes,
                            models.DO_NOTHING,
                            db_column='qid',
                            blank=True,
                            null=True)
    title = models.CharField(max_length=64)
    size = models.IntegerField()
    has_sub_article = models.IntegerField()


class Article:
    def __init__(self, qid):
        self.qid = qid

        self.anoncontributors = -1
        self.area = -1
        self.averages = {}
        self.commons_category = ""
        self.coordinates = []
        self.extract = ""
        self.fr_wp_limits = []
        self.images = []
        self.length = -1
        self.links = -1
        self.linkshere = -1
        self.mayor = ""
        self.nearby = {}
        self.pageimage = []
        self.pageviews = []
        self.percentages = {}
        self.population = -1
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
                'area': self.area,
                'anoncontributors': self.anoncontributors,
                'averages': self.averages,
                'commons_category': self.commons_category,
                'coordinates': self.coordinates,
                'extract': self.extract,
                'fr_wp_limits': self.fr_wp_limits,
                'images': self.images[:25],
                'images_number': len(self.images),
                'mayor': self.mayor,
                'nearby': self.nearby,
                'length': self.length,
                'links': self.links,
                'linkshere': self.linkshere,
                'pageviews': self.pageviews,
                'registeredcontributors': self.registeredcontributors,
                'pageimage': self.pageimage,
                'percentages': self.percentages,
                'sections_live': self.sections_live,
                'todo_list': self.todo_list,
                # 'wd_claims': self.wd_claims,
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

            # claims
            if len(entity['claims']):
                self.wd_claims = entity['claims']
                # P6: Mayor
                if 'P6' in self.wd_claims:
                    self.mayor = get_value_from_statements(
                        self.wd_claims['P6'], 'newest')

                # P373: Commons category
                if 'P373' in self.wd_claims:
                    self.commons_category = get_value_from_statements(
                        self.wd_claims['P373'], 'first')

                # P1082: Population
                if 'P1082' in self.wd_claims:
                    self.population = int(get_value_from_statements(
                        self.wd_claims['P1082'], 'newest')['amount'])

                # P2046: Area
                if 'P2046' in self.wd_claims:
                    self.area = float(get_value_from_statements(
                        self.wd_claims['P2046'], 'newest')['amount'])

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
            # First request
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
                                filename = sanitize_file_name(i['title'])
                                if filename not in file_blacklist:
                                    self.images.append([
                                        'https://commons.wikimedia.org/wiki/File:{}'.format(quote(filename)),
                                        commons_file_url(filename, 400)])

                    if 'links' in page:
                        self.links = len(page['links'])

                    if 'linkshere' in page:
                        self.linkshere = len(page['linkshere'])

                    if 'pageimage' in page:
                        self.pageimage = [
                            page['pageimage'],
                            commons_file_url(
                                sanitize_file_name(page['pageimage']),
                                200)]

                    if 'pageviews' in page:
                        self.pageviews = page['pageviews']

                    if 'revisions' in page:
                        self.length = len(page['revisions'][0]['content'])
                        self.sections_live = get_sections_length(
                            page['revisions'][0]['content'])

            # 2nd request
            coordinates = "{}|{}".format(
                self.coordinates[0]['lat'],
                self.coordinates[0]['lon'])
            payload = {
                "action": "query",
                "format": "json",
                "prop": "coordinates|pageimages|pageterms",
                "generator": "geosearch",
                "formatversion": "2",
                "colimit": "50",
                "piprop": "thumbnail",
                "pithumbsize": "144",
                "pilimit": "50",
                "wbptterms": "description",
                "ggscoord": coordinates,
                "ggsradius": "10000",
                "ggslimit": "50",
                "ggsprop": "type|name|dim|country|region"
            }

            results = frwiki.request(payload)

        except Exception as e:
            print("Can't retrieve live WP data for {}: {}".format(self.qid, e))

        try:
            if 'pages' in results['query']:
                self.nearby = results['query']['pages']
        except Exception as e:
            print("Can't retrieve nearby data for {}: {}".format(self.qid, e))


def avg(source_list, key):
    # Returns the average number of bytes in a section for a list of articles
    return int(float(sum(d[key] for d in source_list)) / len(source_list))


def sanitize_file_name(filename):
    if filename[:8] == 'Fichier:':
        filename = filename[8:]
    elif filename[:5] == 'File':
        filename = filename[5:]

    filename = re.sub(' ', '_', filename)

    return filename


def commons_file_url(filename, width=0):
    # Returns the direct URL of a file on Wikimedia Commons.
    # Per https://frama.link/commons_path

    hashed_filename = hashlib.md5(filename.encode('utf-8')).hexdigest()

    base_url = "https://upload.wikimedia.org/wikipedia/commons"

    if not width:
        path = "{}/{}/{}".format(
            hashed_filename[:1],
            hashed_filename[:2],
            filename)

    else:
        path = "thumb/{}/{}/{}/{}px-{}".format(
            hashed_filename[:1],
            hashed_filename[:2],
            filename,
            width,
            filename)
        if filename[-4:].lower() == '.svg':
            url += ".png"

    return "{}/{}".format(base_url, quote(path))


def get_value_from_statements(statements, sorting='all'):
    # Given a list of WD statements, get one value
    # or a list of values
    if sorting == 'all':
        values = []
        for s in statements:
            values.append[get_value_from_statement(s)]
        return values
    elif sorting == 'first':
        value = get_value_from_statement(statements[0])
        return value
    elif sorting == 'newest':
        date_props = ['P580', 'P585']
        most_recent_val = 0
        most_recent_year = 0
        for s in statements:
            for prop in date_props:
                if 'qualifiers' in s and prop in s['qualifiers']:
                    year = int(extract_year(
                        s['qualifiers'][prop][0]['datavalue']['value']))
                    if year > most_recent_year:
                        most_recent_year = year
                        most_recent_val = get_value_from_statement(s)

        if most_recent_year == 0:
            # If no date qualifier found, use the first available
            most_recent_val = get_value_from_statements(
                statements, 'first')
        return most_recent_val


def get_value_from_statement(statement):
    base_value = statement['mainsnak']['datavalue']['value']
    if statement['mainsnak']['datatype'] == "wikibase-item":
        value = base_value['id']
    else:
        value = base_value

    return value


def extract_year(value):
    # Returns the date from a WD date value
    year_regex = "^(?P<year>[+-]*\d+)-"
    return re.match(year_regex, value['time']).group('year')


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
            if s in SECTIONS_LOOKUP_TABLE[section]:
                result[section] += len(splcont[j + 1])
                break

    return result
