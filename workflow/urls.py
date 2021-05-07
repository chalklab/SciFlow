""" urls for the workflow app """
from django.urls import path
from workflow import views


urlpatterns = [
    path('logs', views.logs, name='logs'),
    path('logs/<lid>', views.viewlog, name='viewlog'),
]
