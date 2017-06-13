import json
from django.http import HttpResponse
from django.shortcuts import render
from .models import Article


# Create your views here.
def index(request):
    return render(request, 'mc_frontend/homepage.html', {})


def entity(request, qid, title):
    return render(request, 'mc_frontend/homepage.html', {})


def api(request, qid):
    commune = Article(qid)
    data = commune.get_data()
    return HttpResponse(json.dumps(data), content_type='application/json')
