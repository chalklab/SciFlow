""" example code for the datafiles app"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sciflow.settings")
django.setup()

from datafiles.functions import *


addfile()
