""" urls for the substances app """
from django.urls import path
from substances import views


urlpatterns = [
    path("", views.home, name='home'),
    path("view/<subid>", views.view, name='view'),
    path("add/<identifier>", views.add, name='add'),
    path("ingestlist/", views.ingestlist, name='ingestlist'),
    path("normalize/<identifier>", views.normalize, name='normalize'),
]
