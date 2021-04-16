""" django urls file for the dataset app """
from django.urls import path
from datasets import views


urlpatterns = [
    path('', views.home, name='home'),
    path('datasets/index/', views.index, name='index'),
    path("datasets/view/<setid>", views.viewdataset, name='view'),
]
