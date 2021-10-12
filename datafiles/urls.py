""" django urls file for the dataset app """
from django.urls import path
from datafiles import views


urlpatterns = [
    path("files/ingest/", views.ingestion, name='ingest'),
    path("files/view/<fileid>", views.viewfile, name='view'),
    path("files/clean/<fileid>", views.clean, name='clean'),
    path("files/jsonld/<fileid>", views.jsonld, name='jsonld'),
    path('references/index', views.getrefs, name='index'),
    path('references/view/<refid>', views.viewref, name='index'),
    path('references/search/<query>', views.search, name='index')
]
