from django.urls import path
from substances import views


urlpatterns = [
    path("", views.home, name='home'),
    path("view/<subid>", views.view, name='view'),
]
