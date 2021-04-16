""" example code for the datafiles app"""
import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sciflow.settings")
django.setup()


from datasets.serializer import *
from datasets.views import *
import views

f1 = False
if f1:
    dset = DatasetSerializer(Datasets.objects.get(id=5))
    print(json.dumps(dset.data, indent=2))

f2 = False
if f2:
    file = JsonFileSerializer(JsonFiles.objects.get(id=2))
    print(json.dumps(file.data, indent=2))

f3 = False
if f3:
    views.home(False)

f4 = False
if f4:
    test = {"top": "this is the top level", "middle": {},
            "bottom": "this is the bottom level"}
    mid = test['middle']
    mid.update({"update": "this is the updated middle"})
    print(test)

f5 = False
if f5:
    updatestats()

f6 = True
if f6:
    viewdataset(None, 3)
