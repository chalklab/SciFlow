""" urls for the substances app """
from django.urls import path, re_path
from substances import views


urlpatterns = [
    path("", views.home, name='home'),
    re_path(r'^search/(?:(?P<query>.+)/)?$', views.search, name='search'),
    path("view/<subid>", views.view, name='view'),
    path("add/<identifier>", views.add, name='add'),
    path("ingestlist/", views.ingestlist, name='ingestlist'),
    path("normalize/<identifier>", views.normalize, name='normalize'),
]
