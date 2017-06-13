from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/(?P<qid>Q[1-9][0-9]*)$', views.api, name='api'),
    url(r'^(?P<qid>Q[1-9][0-9]*)\/*(?P<title>.*)$',
        views.entity, name='entity_details'),
    url(r'', views.index, name='homepage')
]