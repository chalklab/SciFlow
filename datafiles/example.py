""" example code for the datafiles app"""
import os
import django
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sciflow.settings")
django.setup()

from django.conf import settings
from datafiles.views import *
from pyld import jsonld

f1 = False
if f1:
    baserdir = settings.BASE_DIR
    directory = baserdir + '/static/trcquads/'
    setobjs = requests.get('https://sds.coas.unf.edu/trc/datasets/sddslist')
    setlist = setobjs.json()
    for fname, url in setlist.items():
        print(fname)
        opts = {'algorithm': 'URDNA2015', 'format': 'application/n-quads',
                "processingMode": "json-ld-1.0"}
        normalized = jsonld.normalize(url, opts)
        f = open(directory + "/" + fname + ".txt", "w")
        f.write(normalized)
        f.close()

f2 = True
if f2:
    fid = 8095
    viewfile(None, fid)
