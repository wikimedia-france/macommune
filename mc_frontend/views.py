import json
from django.http import HttpResponse
from django.shortcuts import render
from .models import Article, Communes, Geoloc, get_commons_files, sections_stats
from .constants import IMPORTANCES, SECTIONS_NAMES
from unidecode import unidecode
import random
import re


# Create your views here.
def index(request):
    communes = Communes.objects.filter().values('qid', 'title', 'wp_title')
    examples = []
    count = 0
    while count < 5:
        examples.append(random.choice(communes))
        count = count + 1
    return render(request, 'mc_frontend/homepage.html', {'examples': examples})


def entity(request, qid, title):
    return render(request, 'mc_frontend/homepage.html', {})


def item_api(request, qid):
    commune = Article(qid)
    commune.get_local_data()
    commune.get_live_wd_data()
    commune.get_live_todo()
    commune.get_live_wp_data()
    data = commune.get_data()
    return HttpResponse(json.dumps(data), content_type='application/json')


def file_api(request, category):
    values = get_commons_files(category)
    return HttpResponse(json.dumps(values), content_type='application/json')


def autocomplete(request, snak):
    snak = unidecode(snak).lower().replace('-', ' ')
    snak = re.sub('\W+', ' ', snak).strip()

    data = Communes.objects.filter(
        suggest_str__istartswith=snak).extra(
        select={'value': 'wp_title', 'qid': 'qid'})[:8]
    values = {'snak': snak,
              'values': list(data.values('value', 'qid'))}
    return HttpResponse(json.dumps(values), content_type='application/json')


def geo_api(request, min_lat, max_lat, min_lng, max_lng):
    GEO_SEARCH_MARGIN = 0.1
    GEO_MAX_POLYGONS = 600

    min_lat = float(min_lat) - GEO_SEARCH_MARGIN
    max_lat = float(max_lat) + GEO_SEARCH_MARGIN
    min_lng = float(min_lng) - GEO_SEARCH_MARGIN
    max_lng = float(max_lng) + GEO_SEARCH_MARGIN

    # Fetch the geoshape of all cities in the given area
    data = Geoloc.objects.filter(
        latitude__range=[min_lat, max_lat],
        longitude__range=[min_lng, max_lng])[:GEO_MAX_POLYGONS+1]
    if len(data) > GEO_MAX_POLYGONS:
        values = {
            'type': 'FeatureCollection',
            'features': [],
        }
        return HttpResponse(json.dumps(values),
                            content_type='application/json')
    
    formated_sections_name = ['qid__'+section_name for section_name in SECTIONS_NAMES]
    dataset = data.values('qid__title', 'qid', 'geoshape', 'qid__importance', *formated_sections_name)

    # Compute the average percentage sections 
    stats = {}
    for importance in IMPORTANCES:
        (stats[importance], _) = sections_stats(importance)

    # Build the geoJSON response
    features = []
    for commune in dataset:
        if commune['geoshape'] is not None:
            global_average = 0
            commune['qid__importance'] = commune['qid__importance'].lower()
            for section in stats[commune['qid__importance']]:
                global_average += commune['qid__'+section] / stats[commune['qid__importance']][section]
            features += [{
                "type": "Feature",
                "properties": {
                    "title": commune['qid__title'],
                    "qid": commune['qid'],
                    "avg": (global_average*100)/len(stats[commune['qid__importance']]),
                },
                "geometry": json.loads(commune['geoshape']),
            }]

    values = {
        'type': 'FeatureCollection',
        'features': features,
    }

    return HttpResponse(json.dumps(values), content_type='application/json')
