"""user app url paths file"""
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', include('social_django.urls')),
    path('', views.index),
    #  TODO missing login.html template?
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'), name='login'),
    path('requests/', views.requests, name='requests'),
    path('dashboard/', views.dashboard),
    path('logout/', views.logout),
    path('error/', views.error),
]
