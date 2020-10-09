""" urls for the workflow app """
from django.urls import path
from workflow import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('ingestion/', views.ingestion, name='ingestion'),
    path('results/', views.ingestionresults, name='ingestionresults'),
    path('test/', views.test, name='test'),
    path('errors/', views.errors, name='errors'),
]
