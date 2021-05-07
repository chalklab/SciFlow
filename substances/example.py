"""example functions for development"""
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sciflow.settings")
django.setup()

from substances.sub_functions import *
from substances.views import *
from datafiles.df_functions import *
from substances.external import *
from scyjava import config, jimport

# add a new substance to the database
add = None
if add:
    key = "AOAOXSUNFXXSGI-UHFFFAOYSA-N"
    added = addsubstance(key)
    if not added:
        print("Substance not added")
        exit()

    # generate the JSON-LD file for the substance
    subid = added.id
    jsonld = createsubjld(subid)

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
runpc = None
if runpc:
    key = 'VWNMWKSURFWKAL-HXOBKFHXSA-N'
    meta, ids, descs, srcs = {}, {}, {}, {}
    pubchem(key, meta, ids, descs, srcs)
    print(meta, ids, descs)
    print(json.dumps(srcs, indent=4))

# check output of chembl request
runcb = None
if runcb:
    key = 'REEUVFCVXKWOFE-UHFFFAOYSA-K'
    # key = 'aspirin'
    meta, ids, descs, srcs = {}, {}, {}, {}
    chembl(key, meta, ids, descs, srcs)
    print(meta, ids, descs)
    print(json.dumps(srcs, indent=4))

# check output of classyfire request
runcf = None
if runcf:
    key = 'VWNMWKSURFWKAL-HXOBKFZXSA-N'  # (bad inchikey)
    descs, srcs = {}, {}
    classyfire(key, descs, srcs)
    print(descs)
    print(json.dumps(srcs, indent=4))

# check output of wikidata request
runwd = None
if runwd:
    key = 'BSYNRYMUTXBXSQ-CHALKCHALK-N'  # (bad inchikey for aspirin)
    ids, srcs = {}, {}
    wikidata(key, ids, srcs)
    print(ids)
    print(json.dumps(srcs, indent=4))

# Get data from commonchemistry using CASRNs
runcc1 = None
if runcc1:
    subs = Substances.objects.all().values_list(
        'id', 'casrn').filter(
        casrn__isnull=False)  # produces tuples
    for sub in subs:
        found = Sources.objects.filter(
            substance_id__exact=sub[0],
            source__exact='comchem')
        if not found:
            meta, ids, srcs = {}, {}, {}
            comchem(sub[1], meta, ids, srcs)
            saveids(sub[0], ids)
            savesrcs(sub[0], srcs)
            print(sub)
            print(json.dumps(srcs, indent=4))

runcc2 = None
if runcc2:
    # process compounds with no casrn in substances table
    subs = Substances.objects.all().values_list(
        'id', flat=True).filter(
        casrn__isnull=True)
    for sub in subs:
        found = Sources.objects.filter(
            substance_id__exact=sub,
            source__exact='comchem')
        if not found:
            key = getinchikey(sub)
            if key:
                meta, ids, srcs = {}, {}, {}
                if comchem(key, meta, ids, srcs):
                    saveids(sub, ids)
                    # update casrn field in substances
                    updatesubstance(sub, 'casrn', ids['comchem']['casrn'])
                    print('CASRN updated')
                savesrcs(sub, srcs)
                print(sub)
                print(json.dumps(srcs, indent=4))
            else:
                print(sub)

runlm = None
if runlm:
    apipath = "https://commonchemistry.cas.org/api/detail?cas_rn="
    f = open("reach_ids.txt", "r")
    for line in f:
        parts = line.replace('\n', '').split(':')
        print(parts)
        res = requests.get(apipath + parts[1])
        if res.status_code == 200:
            with open(parts[0] + '.json', 'w') as outfile:
                json.dump(res.json(), outfile)
                print('Found')
        else:
            print('Not found')

# check output of getinchikey function
rungi = None
if rungi:
    subid = 1
    out = getinchikey(subid)
    print(out)

# test scyjava
runsj = None
if runsj:
    config.add_endpoints('io.github.egonw.bacting:managers-cdk:0.0.16')
    workspaceRoot = "."
    cdkClass = jimport("net.bioclipse.managers.CDKManager")
    cdk = cdkClass(workspaceRoot)

    print(cdk.fromSMILES("CCC"))

runls = True
if runls:
    subview(None, 5044)
