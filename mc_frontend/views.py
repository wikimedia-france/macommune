import json
from django.http import HttpResponse
from django.shortcuts import render
from .models import Article, Communes
from unidecode import unidecode
import re


# Create your views here.
def index(request):
    return render(request, 'mc_frontend/homepage.html', {})


def entity(request, qid, title):
    return render(request, 'mc_frontend/homepage.html', {})


def item_api(request, qid):
    commune = Article(qid)
    data = commune.get_data()
    return HttpResponse(json.dumps(data), content_type='application/json')


def autocomplete(request, snak):
    snak = unidecode(snak).lower().replace('-', ' ')
    snak = re.sub('\W+', ' ', snak).strip()

    data = Communes.objects.filter(suggest_str__istartswith=snak)
    values = {'snak': snak,
              'values': list(data.values('wp_title', 'qid'))}
    return HttpResponse(json.dumps(values), content_type='application/json')


def geo_api(request, min_lat, max_lat, min_lng, max_lng):
    min_lat = float(min_lat)
    max_lat = float(max_lat)
    min_lng = float(min_lng)
    max_lng = float(max_lng)
    
    #Check if the area is not to big
    if (max_lat - min_lat) * (max_lng - min_lng) > 1:
        values = {
            'type': 'FeatureCollection',
            'features': [],
        }
        return HttpResponse(json.dumps(values), content_type='application/json')
    
    #Fetch the geoshape of all cities in the given area
    data = Communes.objects.filter(latitude__range=[min_lat, max_lat], longitude__range=[min_lng, max_lng])
    dataset = data.values('wp_title', 'qid', 'geoshape')
    
    #Build the geoJSON response
    features = []
    for commune in dataset:
        features += [{
            "type": "Feature",
            "properties": {
                "title": commune['wp_title'],
                "qid": commune['qid']
            },
            "geometry": json.loads(commune['geoshape']),
        }]
    
    values = {
        'type': 'FeatureCollection',
        'features': features,
    }
    
    return HttpResponse(json.dumps(values), content_type='application/json')
