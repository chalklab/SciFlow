""" urls for the substances app """
from django.urls import path
from contexts import views


urlpatterns = [
    path("", views.index, name='ctxlist'),
    path("view/<ctxid>", views.view, name='ctxview'),

    path("nslist", views.nslist, name='nslist'),
    path("nsview/<nsid>", views.nsview, name='nsview'),
    path("ontterm/<tid>", views.ontterm, name='ontterm'),
]
