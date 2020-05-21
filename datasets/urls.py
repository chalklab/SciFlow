from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name='home'),
    path('ingestion', views.ingestion, name='ingestion'),
    path('ingestion/results', views.ingestionresults, name='ingestionresults'),
]
