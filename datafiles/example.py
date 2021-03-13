""" example code for the datafiles app"""
import os
import django
import requests
import json
from pyld import jsonld

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sciflow.settings")
django.setup()

from datafiles.df_functions import *
from django.conf import settings

baserdir = settings.BASE_DIR
directory = baserdir+'/static/trcquads/'
setlist = requests.get('https://sds.coas.unf.edu/trc/datasets/sddslist').json()
# print(setlist[0:9])
# exit()
for fname, url in setlist.items():
    print(fname)
    normalized = jsonld.normalize(url, {'algorithm': 'URDNA2015', 'format': 'application/n-quads', "processingMode": "json-ld-1.0"})
    f = open(directory+"/"+fname+".txt", "w")
    f.write(normalized)
    f.close()
