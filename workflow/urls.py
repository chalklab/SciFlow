""" urls for the workflow app """
from django.urls import path
from workflow import views


urlpatterns = [
    path('actlog/<fid>', views.actlog, name='actlog'),
]
