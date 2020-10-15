""" django urls file for the dataset app """
from django.urls import path
from datasets import views


urlpatterns = [
    path('', views.home, name='home'),
    path('datasets/index/', views.index, name='index'),
    path("datasets/view/<setid>", views.view, name='view'),
    # path('jsonlds/upload', views.model_form_upload, name='model_form_upload'),
    path('jsonlds/upload', views.upload_file, name='model_form_upload'),
    path('jsonlds/', views.jsonlds, name='jsonlds'),
    path("jsonlds/view/<jsonldid>", views.jsonldview, name='jsonldview'),

]

