"""example functions for development"""
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sciflow.settings")
django.setup()


from contexts.ctx_functions import *

# add a new substance to the database
nslist = None
if nslist:
    nslist = getnsps()
    print(nslist)
    exit()

term = True
if term:
    data = getont(13)
    print(data.sdsection)
    exit()
