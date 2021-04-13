""" example code for the datafiles app"""
import os
import django
import json


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sciflow.settings")
django.setup()


from datasets.serializer import *
import views

f1 = False
if f1:
    dset = DatasetSerializer(Datasets.objects.get(id=5))
    print(json.dumps(dset.data, indent=2))

f2 = False
if f2:
    file = JsonFileSerializer(JsonFiles.objects.get(id=2))
    print(json.dumps(file.data, indent=2))

f3 = True
if f3:
    views.home(False)
