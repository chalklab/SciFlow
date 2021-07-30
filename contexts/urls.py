""" urls for the substances app """
from django.urls import path
from contexts import views


urlpatterns = [
    path("contexts/", views.ctxlist, name='ctxlist'),
    path("contexts/view/<ctxid>", views.ctxview, name='ctxview'),
    path("xwalks/", views.cwklist, name='cwklist'),
    path("xwalks/view/<cwkid>", views.cwkview, name='cwkview'),
    path("nspaces/", views.nsplist, name='nsplist'),
    path("nspaces/view/<nspid>", views.nspview, name='nspview'),
    path("ontterms/", views.ontlist, name='ontlist'),
    path("ontterms/view/<ontid>", views.ontview, name='ontview'),
]
