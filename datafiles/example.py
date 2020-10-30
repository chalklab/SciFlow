""" example code for the datafiles app"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sciflow.settings")
django.setup()

from datafiles.df_functions import *
from django.conf import settings

baserdir = settings.BASE_DIR
path = baserdir+'/datafiles/test.jsonld'
f = open(path)
file = f.read()

added = adddatafile(file, 1)
