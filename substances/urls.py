from django.urls import path
from . import views


urlpatterns = [
    path("substances/", views.index),
    path("substances/view/<subid>", views.view),
]