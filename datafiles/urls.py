""" django urls file for the dataset app """
from django.urls import path
from datafiles import views


urlpatterns = [
    path("ingest/", views.ingestion, name='view'),
    path("view/<fileid>", views.viewfile, name='view'),
    path("clean/<fileid>", views.clean, name='clean'),
    path("jsonld/<fileid>", views.jsonld, name='jsonld'),
]
