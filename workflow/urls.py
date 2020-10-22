""" urls for the workflow app """
from django.urls import path
from workflow import views


urlpatterns = [
    path('errors/', views.errors, name='errors'),
]
