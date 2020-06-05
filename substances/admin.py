""" import from django"""
from django.contrib import admin

# Register your models here.

from .models import Substances
from .models import Identifiers

admin.site.register(Substances)
admin.site.register(Identifiers)
