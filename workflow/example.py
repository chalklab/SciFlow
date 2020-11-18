"""example functionality for testing"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sciflow.settings")
django.setup()

from datafiles.df_functions import *
from django.conf import settings
from substances.sub_functions import *
# from datafiles.models import *
# from workflow.gdb_functions import *

basedir = settings.BASE_DIR
fpath = basedir + '/static/files/240_72215_2324256.jsonld'
with open(fpath) as f:
    json = json.load(f)
test = jsonld.to_rdf(json, {"processingMode": "json-ld-1.0"})
print(test)
