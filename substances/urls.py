from django.urls import path
from . import views


urlpatterns = [
    path("substances/", views.home),
    path("substances/chunk/", views.chunk)
]