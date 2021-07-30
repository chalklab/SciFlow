""" sciflow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import logout as auth_logout


def logout(request):
    """logout function"""
    auth_logout(request)
    return redirect('/')


urlpatterns = [
    path('', include('datasets.urls')),
    path('', include('datafiles.urls')),
    path('', include('contexts.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('logout/', logout, name='logout'),
    path('files/', include('datafiles.urls')),
    path('substances/', include('substances.urls')),
    path('workflow/', include('workflow.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
