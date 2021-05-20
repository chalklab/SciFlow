""" urls for the substances app """
from django.urls import path
from crosswalks import views


urlpatterns = [
    path("nslist", views.nslist, name='nslist'),
    path("nsview/<nsid>", views.nsview, name='nsview'),
    path("ontterm/<tid>", views.ontterm, name='ontterm'),
]
