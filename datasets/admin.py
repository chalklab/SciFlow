""" import from django"""
from django.contrib import admin

# Register your models here.

from .models import Datasets

admin.site.register(Datasets)
