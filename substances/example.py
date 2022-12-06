"""example functions for development"""
import os
import django
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sciflow.settings")
django.setup()
from datafiles.df_functions import *
from substances.sub_functions import *
from substances.external import *
from scyjava import config, jimport
from workflow.gdb_functions import *
from django.core.exceptions import ObjectDoesNotExist
from rdkit import Chem
from rdkit.Chem import AllChem
from substances.views import *


# get latest substance facet_lookup file
runfl = False
if runfl:
    subview(None, 7860)


# check casrns in substances using inchikeys
runkey = False
if runkey:
    meta, ids, srcs = {}, {}, {}
    nocas = Substances.objects.filter(casrn__isnull=True).values_list('inchikey', flat=True).order_by('id')
    for key in nocas:
        comchem(key, meta, ids, srcs)
        if meta:
            print(meta)
            exit()

# add rdkit molfiles for substances
runmol = False
if runmol:
    done = Structures.objects.all().values_list('substance_id', flat=True)
    subs = Identifiers.objects.all().filter(type='csmiles').\
        exclude(substance_id__in=done).values_list('substance_id', flat=True)
    for sub in subs:
        if sub not in done:
            smiles = Identifiers.objects.all().filter(type='csmiles', substance_id=sub)
            for smile in smiles:
                print("Processing structure " + smile.value)
                mo = Chem.MolFromSmiles(smile.value)
                mh = Chem.AddHs(mo)
                AllChem.EmbedMolecule(mh, randomSeed=0xf00d)
                mf = Chem.MolToMolBlock(mh)
                struc = Structures(substance_id=sub, molfile=mf)
                struc.save()
                print("Saved structure " + smile.value)

# update pubchem csmiles where not available
runpcs = False
if runpcs:
    subids = Identifiers.objects.all().filter(type='inchikey', source='pubchem').values_list('substance_id', flat=True)
    for subid in subids:
        ids = Identifiers.objects.all().filter(substance_id=subid).values_list('type', flat=True)
        if 'csmiles' not in ids:
            key = Identifiers.objects.get(substance_id=subid, type='inchikey', source='pubchem')
            apipath = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/"
            respnse = requests.get(apipath + 'inchikey/' + key.value + '/json').json()
            props = respnse["PC_Compounds"][0]["props"]
            for prop in props:
                if prop["urn"]["label"] == "SMILES" and prop["urn"]["name"] == "Canonical":
                    smiles = prop["value"]["sval"]
                    idid = Identifiers(substance_id=subid, type='csmiles', value=smiles, source='pubchem')
                    idid.save()
                    print(idid)
                    break
        if 'ismiles' not in ids:
            key = Identifiers.objects.get(substance_id=subid, type='inchikey', source='pubchem')
            apipath = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/"
            respnse = requests.get(apipath + 'inchikey/' + key.value + '/json').json()
            props = respnse["PC_Compounds"][0]["props"]
            for prop in props:
                if prop["urn"]["label"] == "SMILES" and prop["urn"]["name"] == "Isomeric":
                    smiles = prop["value"]["sval"]
                    idid = Identifiers(substance_id=subid, type='ismiles', value=smiles, source='pubchem')
                    idid.save()
                    print(idid)
                    break
        else:
            print(subid)

# update pubchem ids where not available
runpci = False
if runpci:
    subids = Identifiers.objects.all().filter(type='inchikey', source='pubchem').values_list('substance_id', flat=True)
    for subid in subids:
        ids = Identifiers.objects.all().filter(substance_id=subid).values_list('type', flat=True)
        if 'pubchem' not in ids:
            key = Identifiers.objects.get(substance_id=subid, type='inchikey', source='pubchem')
            apipath = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/"
            respnse = requests.get(apipath + 'inchikey/' + key.value + '/json').json()
            cid = respnse["PC_Compounds"][0]["id"]["id"]["cid"]
            idid = Identifiers(substance_id=subid, type='pubchem', value=cid, source='pubchem')
            idid.save()
            print(idid)
        else:
            print(subid)

# fix empty molgraphs in json-ld files
runfix = False
if runfix:
    fixes = FacetFiles.objects.all().filter(file__contains='"atoms":[]').filter(file__contains='chemtwin')
    for fix in fixes:
        # just replace the file don't create a new version in facet_files
        sub = Substances.objects.get(facet_lookup_id=fix.facet_lookup_id)
        try:
            pcid = Identifiers.objects.get(substance_id=sub.id, type='pubchem', source='pubchem')
            jld = createsubjld(sub.id)
            jld["@id"] = sub.graphdb
            fix.file = json.dumps(jld, separators=(',', ':'))
            fix.save()
            print('Fixed facet_lookup ' + str(fix.facet_lookup_id))
        except ObjectDoesNotExist:
            print('Facet_lookup ' + str(fix.facet_lookup_id) + ' not fixed (no PubChem id)')

# add a new substance jld to the database
runjld = False
if runjld:
    subs = Substances.objects.all().order_by('id')
    for sub in subs:
        if sub.graphdb is None:
            continue
        facet = FacetLookup.objects.get(id=sub.facet_lookup_id)
        if facet.currentversion == 1:
            subid = sub.id
            # generate new json-ld file (as python dictionary)
            jld = createsubjld(subid)
            jld["@id"] = sub.graphdb  # updating the graphname from the initial ingest
            # get the latest version of this file from facet_files
            lastver = FacetFiles.objects.filter(facet_lookup_id=sub.facet_lookup_id).order_by('-version')[0]
            newver = lastver.version + 1
            # load into facet_files
            file = FacetFiles(facet_lookup_id=sub.facet_lookup_id,
                              file=json.dumps(jld, separators=(',', ':')), type='raw', version=newver)
            file.save()
            # add json-ld to the graph replacing the old version
            addgraph('facet', sub.facet_lookup_id, 'remote', sub.graphdb)
            # update facet_lookup
            lookup = FacetLookup.objects.get(id=sub.facet_lookup_id)
            lookup.currentversion = newver
            lookup.save()
            print("Updated '" + sub.graphdb + "'")
            time.sleep(3)
        else:
            print("Already updated '" + sub.graphdb + "'")

# add a new substance to the database
add = False
if add:
    # example substance that is not found online...
    meta = {
        "name": "sodium gadolinium titanate",
        "formula": "GdNaO4Ti",
        "molweight": 292.104,
        "iupacname": "Gadolinium sodium titanium oxide",
        "inchi": "InChI=1S/Gd.Na.4O.Ti/q+3;+1;4*-2;+4",
        "inchikey": "HZKODDDQUJIOQB-UHFFFAOYSA-N"
    }
    key = "HZKODDDQUJIOQB-UHFFFAOYSA-N"
    added = addsubstance(key)

    if not added:
        print("Substance not added")
        print(added)
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
runpc = False
if runpc:
    key = 'VWNMWKSURFWKAL-HXOBKFHXSA-N'
    meta, ids, descs, srcs = {}, {}, {}, {}
    pubchem(key, meta, ids, descs, srcs)
    print(meta, ids, descs)
    print(json.dumps(srcs, indent=4))

# check output of chembl request
runcb = False
if runcb:
    key = 'DXDHALJBYXNDKW-UHFFFAOYSA-N'
    # key = 'aspirin'
    meta, ids, descs, srcs = {}, {}, {}, {}
    chembl(key, meta, ids, descs, srcs)
    print(meta, ids, descs)
    print(json.dumps(srcs, indent=4))

# check output of classyfire request
runcf = False
if runcf:
    # key = 'VWNMWKSURFWKAL-HXOBKFZXSA-N'  # (bad inchikey)
    key = 'SIEHZFPZQUNSAS-UHFFFAOYSA-N'
    descs, srcs = {}, {}
    classyfire(key, descs, srcs)
    print(descs)
    print(json.dumps(srcs, indent=4))

# check output of wikidata request
runwd = False
if runwd:
    # key = 'BSYNRYMUTXBXSQ-CHALKCHALK-N'  # (bad inchikey for aspirin)
    key = 'SBPBAQFWLVIOKP-UHFFFAOYSA-N'
    ids, srcs = {}, {}
    wikidata(key, ids, srcs)
    print(ids)
    print(json.dumps(srcs, indent=4))

# Get data from commonchemistry using CASRNs
runcc1 = True
if runcc1:
    key = 'BSYNRYMUTXBXSQ-UHFFFAOYSA-N'
    meta, ids, srcs = {}, {}, {}
    comchem(key, meta, ids, srcs)
    print(ids)
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
