""" import from django"""
from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Substances)
admin.site.register(SubstancesSystems)
admin.site.register(Identifiers)
admin.site.register(Systems)
admin.site.register(Descriptors)
admin.site.register(Sources)
admin.site.register(Templates)
