from django.urls import path
from . import views


urlpatterns = [
    path("substances/", views.home, name='home'),
    #path("substances/chunk/", views.chunk),
]
