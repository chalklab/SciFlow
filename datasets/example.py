""" example code for the datafiles app"""
import datetime
import os
import django
import time
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sciflow.settings")
django.setup()

from datasets.serializer import *
from datasets.views import *
from datetime import datetime
from workflow.gdb_functions import *
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

f6 = False
if f6:
    viewdataset(None, 3)

f7 = True
if f7:
    fids = JsonFiles.objects.filter(type='normalized', version=4,
                                    file__contains='herg').order_by('json_lookup_id').values_list('json_lookup_id', flat=True)
    for fid in fids:
        file = JsonFiles.objects.filter(json_lookup_id=fid).order_by('-version')[0]
        if file.comments == 'done':
            print('Done file ' + str(fid))
            continue
        temp1 = file.file.replace('chalklab:substance:', 'chemtwin_')
        temp2 = temp1.replace('"version":"2","@graph"', '"version":"3","@graph"')
        temp3 = re.sub(r'"generatedAt":".+?"', '"generatedAt":"' + datetime.now().isoformat() + '"', temp2)
        new = JsonFiles()
        new.version = file.version + 1
        new.json_lookup_id = file.json_lookup_id
        new.type = file.type
        new.file = temp3
        new.comments = 'done'
        new.save()
        print(new.id)
        outcome = addgraph('data', file.json_lookup_id, 'remote',
                           'https://scidata.unf.edu/data/' + str(file.json_lookup_id).zfill(8))
        time.sleep(4)
