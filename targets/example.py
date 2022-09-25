import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sciflow.settings")
django.setup()


""" functions for use with the targets and related tables..."""
from targets.target_functions import *


identifier = 'CHEMBL240'
meta, ids, descs, srcs = gettargdata(identifier)

# add meta
try:
    indb = Targets.objects.get(chembl_id=identifier)
except Targets.DoesNotExist:
    indb = None
if not indb:
    nm, ttype, taxid, chemblid, organism = "", "", "", "", ""
    if "chembl" in meta:
        if meta['chembl']['prefname']:
            nm = meta['chembl']['prefname']
        if meta['chembl']['targettype']:
            ttype = meta['chembl']['targettype']
        if meta['chembl']['taxid']:
            taxid = meta['chembl']['taxid']
        if meta['chembl']['chemblid']:
            chemblid = meta['chembl']['chemblid']
        if meta['chembl']['organism']:
            organism = meta['chembl']['organism']
    target = Targets(name=nm, type=ttype, tax_id=taxid, chembl_id=chemblid, organism=organism)
    target.save()
    targid = target.id
    print('Added metadata')
else:
    print('Metadata already ingested')
    targid = indb.id

# add ids if not present
for src, entries in ids.items():
    found = Targids.objects.filter(source=src, target_id=targid)
    if not found:
        for itype, vals in entries.items():
            try:
                indb = Targids.objects.get(target_id=targid, type=itype)
            except Targids.DoesNotExist:
                indb = None
            if not indb:
                if isinstance(vals, (str, int)):
                    tid = Targids(target_id=targid, type=itype, value=vals, source=src)
                    tid.save()
                else:
                    for val in vals:
                        tid = Targids(target_id=targid, type=itype, value=val, source=src)
                        tid.save()
        print('Added identifiers')
    else:
        print('IDs already ingested')

# add descs if not present
for src, entries in descs.items():
    found = Targdescs.objects.filter(source=src, target_id=targid)
    if not found:
        for itype, vals in entries.items():
            try:
                indb = Targdescs.objects.get(target_id=targid, type=itype)
            except Targdescs.DoesNotExist:
                indb = None
            if not indb:
                if isinstance(vals, (str, int)):
                    tid = Targdescs(target_id=targid, type=itype, value=vals, source=src)
                    tid.save()
                else:
                    for val in vals:
                        tid = Targdescs(target_id=targid, type=itype, value=val, source=src)
                        tid.save()
        print('Added descriptors')
    else:
        print('Descriptors already ingested')

print(targid)
