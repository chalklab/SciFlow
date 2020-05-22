from django.urls import path
from datasets import views


urlpatterns = [
    path('', views.ingestion, name='ingestion'),
    path('results/', views.ingestionresults, name='ingestionresults'),
]
