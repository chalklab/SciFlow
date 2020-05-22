from django.urls import path
from substances import views


urlpatterns = [
    path("", views.home, name='home'),
    path("chunk/", views.view, name='view'),
]
