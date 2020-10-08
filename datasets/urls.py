""" django urls file for the dataset app """
from django.urls import path
from datasets import views


urlpatterns = [
    path('', views.home, name='home'),
    path('jsonlds/', views.jsonlds, name='jsonlds'),
    path("jsonlds/view/<jsonldid>", views.jsonldview, name='jsonldview'),

]
