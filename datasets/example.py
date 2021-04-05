""" example code for the datafiles app"""
import os
import django
import json
from datasets.serializer import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sciflow.settings")
django.setup()





set = DatasetSerializer(Datasets.objects.get(id=5))
print(json.dumps(set.data, indent=2))

file = JsonFileSerializer(JsonFiles.objects.get(id=2))
print(json.dumps(file.data, indent=2))
