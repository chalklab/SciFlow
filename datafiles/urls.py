""" django urls file for the dataset app """
from django.urls import path
from datafiles import views


urlpatterns = [
    path("files/view/<fileid>", views.view, name='view'),
]
