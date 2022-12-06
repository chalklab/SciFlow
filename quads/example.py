""" example code for the datafiles app"""
import os
import django
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sciflow.settings")
django.setup()

from pyld import jsonld
from quads.qd_functions import *


# function to grab datafiles from the sciflow database (using the PHP sciflow interface) and save in quads table
# dlist 1 (herg), 3 (trc)
f1 = True
if f1:
    setobjs = requests.get('https://sds.coas.unf.edu/trc/datasets/sddslist/1')
    # setobjs = requests.get('https://sds.coas.unf.edu/sciflow/files/twinlist')
    setlist = setobjs.json()
    done = Quads.objects.order_by('obj').values_list('obj', flat=True).distinct()
    cnt = 1
    offset = 0
    for fname, url in setlist.items():
        if cnt > offset:
            opts = {'algorithm': 'URDNA2015', 'format': 'application/n-quads', 'processingMode': 'json-ld-1.1'}
            normalized = jsonld.normalize(url, opts)
            quads = normalized.split('\n')
            for qidx, quad in enumerate(quads):
                if quad == '':
                    quads.pop(qidx)
                    continue
                q = quad.replace(' .', '').replace('> ', '>@@@').replace('" <', '"@@@<').split('@@@')
                if len(q) == 3:
                    q.append(None)
                elif len(q) > 4:
                    print(q)
                    exit()
                quads[qidx] = q
            addbulk(quads)
            print(str(cnt).zfill(5) + ' processed ' + fname + ':' + url)
        else:
            print(str(cnt).zfill(5) + ' already processed ' + fname)
        cnt += 1
