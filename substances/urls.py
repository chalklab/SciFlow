""" urls for the substances app """
from django.urls import path, re_path
from substances import views


urlpatterns = [
    path("", views.home, name='home'),
    path("list/", views.list, name='list'),
    re_path(r'^search/(?:(?P<query>.+)/)?$', views.search, name='search'),
    path("molfile/<subid>", views.molfile, name='molfile'),
    path("check/<action>", views.subcheck, name='subcheck'),
    path("view/<subid>", views.subview, name='subview'),
    path("view/<subid>/subids", views.subids, name='subids'),
    path("view/<subid>/subdescs", views.subdescs, name='subdescs'),
    path("add/<identifier>/<mode>", views.add, name='add'),
    path("newjld/<subid>", views.newjld, name='newjld'),
    path("showfacet/<facetid>", views.showfacet, name='showfacet'),
    path("showdata/<dataid>", views.showdata, name='showdata'),
    path("ingest/<identifier>", views.add, name='add'),
    path("ingest/", views.ingest, name='ingest'),
    path("sublist/", views.sublist, name='sublist'),
    path("ingestlist/", views.ingestlist, name='ingestlist'),
    path("normalize/<identifier>", views.normalize, name='normalize'),
]
