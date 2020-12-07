"""example functions for development"""
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sciflow.settings")
django.setup()

from substances.sub_functions import *
from datafiles.df_functions import *
from substances.external import *

# add a new substance to the database
add = None
if add:
    key = "AOAOXSUNFXXSGI-UHFFFAOYSA-N"
    added = addsubstance(key)
    if not added:
        print("Substance not added")
        exit()

    # generate the JSON-LD file for the substance
    jsonld = createsubjld(key)

    # store the JSON-LD in the facet_lookups/facet_files tables
    facetid = addfacetfile(jsonld)

    # update facet file with the facet_id
    jsonld['@id'] = jsonld['@id'].replace('<facetid>', str(facetid))

    # save the facet file to the facet_file table
    saved = updatefacetfile(jsonld)
    if saved:
        print("Facet JSON-LD saved to the DB!")
    else:
        print("Error: something happened on the way to the DB!")

# check output of pubchem request
runpc = True
if runpc:
    key = 'VWNMWKSURFWKAL-HXOBKFHXSA-N'
    meta, ids, descs, srcs = {}, {}, {}, {}
    pubchem(key, meta, ids, descs, srcs)
    print(meta, ids, descs)
    print(json.dumps(srcs, indent=4))

# check output of chembl request
runcb = None
if runcb:
    key = 'VWNMWKSURFWKAL-HXOBKFHXSA-N'
    meta, ids, descs, srcs = {}, {}, {}, {}
    chembl(key, meta, ids, descs, srcs)
    print(meta, ids, descs)
    print(json.dumps(srcs, indent=4))

# check output of classyfire request
runcf = None
if runcf:
    key = 'VWNMWKSURFWKAL-HXOBKFZXSA-N'  # (bad inchikey)
    meta, ids, descs, srcs = {}, {}, {}, {}
    classyfire(key, meta, ids, descs, srcs)
    print(meta, ids, descs)
    print(json.dumps(srcs, indent=4))

# check output of wikidata request
runwd = None
if runwd:
    key = 'BSYNRYMUTXBXSQ-CHALKCHALK-N'  # (bad inchikey for aspirin)
    meta, ids, descs, srcs = {}, {}, {}, {}
    wikidata(key, meta, ids, descs, srcs)
    print(meta, ids, descs)
    print(json.dumps(srcs, indent=4))
