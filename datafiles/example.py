""" example code for the datafiles app"""
import time
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sciflow.settings")
django.setup()

from datafiles.views import *
from workflow.gdb_functions import *


f1 = False
if f1:
    fid = 8095
    viewfile(None, fid)


f2 = True
if f2:
    """
    goes though data files in a dataset looking for 
    duplicates in json_lookup and attemtps to clean them up
    currently missing code for any entries in the json_errors table
    """
    uids = list(JsonLookup.objects.filter(dataset_id=1).values_list('uniqueid', flat=True).distinct())
    count = 0
    for uid in uids:
        # get list of unique uniqueids
        hits = list(JsonLookup.objects.filter(uniqueid=uid).values_list('id', flat=True))
        if len(hits) == 2:
            remvid = max(hits)  # get the highest id the one to update/remove
            keepid = min(hits)  # get the highest id the one to keep
            remvidstr = str(remvid).zfill(8)
            keepidstr = str(keepid).zfill(8)

            # get the entries in the json_files table
            files = JsonFiles.objects.filter(json_lookup_id__in=hits)
            fcount = len(files)
            for file in files:
                if file.json_lookup_id == remvid:
                    # update the json_lookup_id
                    file.json_lookup_id = keepid
                    # update the version
                    if file.type == 'raw':
                        file.version = fcount - 1
                    if file.type == 'normalized':
                        file.version = fcount
                # update file for uid format
                temp = file.file.replace('chembl:herg:', 'chembl_herg_')
                # update DB id in graphname
                temp2 = temp.replace('/' + remvidstr + '"', '/' + keepidstr + '"')
                print(temp2)
                file.file = temp2
                file.save()

            # replace both versions in the graph with the new, latest one
            path = 'https://scidata.unf.edu/data/'
            gnames = path + keepidstr + '","' + path + remvidstr
            outcome = addgraph('data', keepid, 'remote', gnames)
            print(outcome)
            # update entries in the json_actlogs table
            acts = JsonActlog.objects.filter(json_lookup_id=remvid)
            acts.update(json_lookup_id=keepid)
            # update entries in the json_facets table
            facs = JsonFacets.objects.filter(json_lookup_id=remvid)
            facs.update(json_lookup_id=keepid)
            # remove duplicate entry in json_lookup
            JsonLookup.objects.filter(id=remvid).delete()
            # update the currentversion of the entry that remains
            keep = JsonLookup.objects.get(id=keepid)
            keep.currentversion = fcount
            keep.save()
            time.sleep(5)
            print(keepidstr)
