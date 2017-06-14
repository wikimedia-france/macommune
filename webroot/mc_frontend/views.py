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
