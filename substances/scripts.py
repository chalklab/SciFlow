""" example code for the cifs app"""
import os
from itertools import islice

import django
import pymysql
pymysql.install_as_MySQLdb()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sciflow.settings")
django.setup()

from substances.models import *
from substances.sub_functions import *
from datafiles.df_functions import *


def addsub(key):
    sub = addsubstance(key, 'meta')
    f = open(key + '.jsonld', 'w')
    if not sub.graphdb:
        jld = createsubjld(sub.id)
        print(jld)
        f.write(str(jld).replace("'",'"'))
    else:
        fid = sub.graphdb.replace('https://scidata.unf.edu/facet/','')
        facet = FacetFiles.objects.filter(facet_lookup_id=fid).order_by('-version')[0]
        f.write(facet.file)
    f.close()
    print(sub.graphdb)


addsub('UHOVQNZJYSORNB-UHFFFAOYSA-N')