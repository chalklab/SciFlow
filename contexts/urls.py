""" urls for the substances app """
from django.urls import path
from contexts import views


urlpatterns = [
    path("contexts/", views.ctxlist, name='ctxlist'),
    path("contexts/add/", views.ctxadd, name='ctxadd'),
    path("contexts/view/<ctxid>", views.ctxview, name='ctxview'),
    path("contexts/write/<ctxid>", views.jswrtctx, name='ctxwrite'),
    path("xwalks/", views.cwklist, name='cwklist'),
    path("xwalks/add/", views.jscwkadd, name='cwkadd'),
    path("xwalks/view/<cwkid>", views.cwkview, name='cwkview'),
    path("xwalks/read/<cwkid>", views.jscwkread, name='cwkread'),
    path("xwalks/delete/", views.jsdelcwk, name='cwkdelete'),
    path("nspaces/", views.nsplist, name='nsplist'),
    path("nspaces/add/", views.nspadd, name='nspadd'),
    path("nspaces/view/<nspid>", views.nspview, name='nspview'),
    path("ontterms/", views.ontlist, name='ontlist'),
    path("ontterms/view/<ontid>", views.ontview, name='ontview'),
    path("ontterms/add/", views.ontadd, name='ontadd'),
    path("ontterms/js/<ontid>", views.ontterms, name='ontterms'),

]
