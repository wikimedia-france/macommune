from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/item/(?P<qid>Q[1-9][0-9]*)$', views.item_api, name='item_api'),
    url(r'^api/complete/(?P<snak>.*)$', views.autocomplete, name='complete'),
    url(r'^api/geoshape/(?P<min_lat>[0-9.-]+)/(?P<max_lat>[0-9.-]+)/(?P<min_lng>[0-9.-]+)/(?P<max_lng>[0-9.-]+)$', views.geo_api, name='geo_api'),
    url(r'^api/files/(?P<category>.*)$', views.files, name='files_api'),
    url(r'^(?P<qid>Q[1-9][0-9]*)\/*(?P<title>.*)$',
        views.entity, name='entity_details'),
    url(r'', views.index, name='homepage')
]
