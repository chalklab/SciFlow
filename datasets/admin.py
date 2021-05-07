""" django admin config """
from django.contrib import admin
from .models import Datasets


admin.site.register(Datasets)
