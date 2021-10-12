""" django admin config """
from django.contrib import admin
from datafiles.models import Datasets


admin.site.register(Datasets)
