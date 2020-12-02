""" urls for the workflow app """
from django.urls import path
from workflow import views


urlpatterns = [
    path('logs', views.logs, name='logs'),
    path('actlog/<lid>', views.actlog, name='actlog'),
]
