""" django admin config """
from django.contrib import admin
from .models import *


admin.site.register(Nspaces)
admin.site.register(Ontterms)
admin.site.register(Metadata)
