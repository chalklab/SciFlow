""" example code for the datafiles app"""
import os
import django
import requests
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sciflow.settings")
django.setup()

from django.conf import settings
from datafiles.views import *
from pyld import jsonld
from quads.qd_functions import add


# function to grab datafiles from the sciflow database (using the PHP sciflow interface) and save in quads table
# dlist 1 (herg), 3 (trc)
f1 = True
if f1:
    fobjs = requests.get('https://sds.coas.unf.edu/sciflow/files/dlist/3/23265')
    flist = fobjs.json()
    for url in flist:
        opts = {'algorithm': 'URDNA2015', 'format': 'application/n-quads', 'processingMode': 'json-ld-1.1'}
        normalized = jsonld.normalize(url, opts)
        quads = normalized.split('\n')
        for quad in quads:
            add(quad)
        print('Processed ' + url)
    exit()
