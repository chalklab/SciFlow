"""example functions for development"""
import json
import os
import django
import time
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sciflow.settings")
django.setup()
from datafiles.df_functions import *
from substances.sub_functions import *
from substances.external import *
from scyjava import config, jimport
from workflow.gdb_functions import *
from workflow.admin_functions import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from rdkit import Chem
from rdkit.Chem import AllChem
from substances.views import *
from external import wikidata
from django.test import RequestFactory
from django.db.models import Q

if True:
    subs = Substances.objects.values_list('id', 'inchikey', 'name').all().order_by('inchikey')
    for sub in subs:
        # check inchikey
        found = Identifiers.objects.filter(substance__id=sub[0], value=sub[1])
        if not found:
            addkey = Identifiers(substance_id=sub[0], type='inchikey', value=sub[1], source='trc')
            addkey.save()
            print(sub[1] + " added")

            # check name
            found = Identifiers.objects.filter(substance__id=sub[0], value=sub[2])
            if not found:
                addname = Identifiers(substance_id=sub[0], type='iupacname', value=sub[2], source='trc')
                addname.save()
                print(sub[2] + " added")
            else:
                print(sub[2] + " already present")
        else:
            print(sub[1])

# clean duplicate chemtwins from Jena
if False:
    qry = """
    JSON { "graph" : ?g, "key" : ?obj } WHERE {
        GRAPH ?g {
            ?sub wdt:P235 ?obj .
            {
                SELECT ?obj WHERE {
                    GRAPH ?g {
                        ?sub wdt:P235 ?obj .
                    }
                }
                group by ?obj
                having (count(?obj) > 1)
            }
        }
    }
    """
    out = query(qry, 'chemtwin')
    if out.status_code == 200:
        jsn = out.content.decode('utf-8')
        hits = json.loads(jsn)
        for hit in hits:
            facid = int(hit['g'].replace('https://scidata.unf.edu/facet/', ''))
            sub = Substances.objects.filter(facet_lookup_id=facid)
            if sub:
                print("found: " + sub[0].inchikey)
            else:
                print("not found: " + str(facid))
                resp = delgraph(hit['g'], 'chemtwin')
                print(resp)
    else:
        print(out.content)


# add missing facet_lookp entries (and files)
if False:
    facetids = FacetLookup.objects.all().values_list('id', flat=True)
    subids = Substances.objects.exclude(facet_lookup_id__in=facetids).values_list('id', flat=True)
    for subid in subids:
        sub = Substances.objects.get(id=subid)
        newjld(RequestFactory().request(), sub.id, sub.facet_lookup_id)
        print("Saved chemtwin of " + sub.inchikey)
        rpath = 'https://sds.coas.unf.edu/sciflow/files/facet/'
        lpath = 'uploads/tranche/chalklab/chemtwin/' + sub.inchikey + '.jsonld'
        uploaded = uploadfile(rpath, lpath, sub.id)
        if uploaded:
            print("ChemTwin uploaded to scidata")
        exit()

# add data from 671 substances that are not available anywhere else...
if False:
    tmps = Substances.objects.values_list('inchikey', flat=True).filter(available='no').order_by('inchikey')
    nakeys = []
    for tmp in tmps:
        nakeys.append(tmp)
    subs = TRCSubstances.objects.using('trc').filter(inchikey__in=nakeys)
    for sub in subs:
        # find sub in sciflow
        sfsub = Substances.objects.get(inchikey=sub.inchikey)
        # update sub
        sfsub.name = sub.name
        sfsub.formula = sub.formula
        sfsub.molweight = sub.mw
        if sfsub.comments is None:
            sfsub.comments = 'trc data only'
        else:
            sfsub.comments = sfsub.comments + '; trc data added'
        sfsub.available = 'yes'
        sfsub.save()
        print("updated " + str(sfsub.id))
        trcids = sub.trcidentifiers_set.all()
        # add identifiers
        for trcid in trcids:
            ident = Identifiers(substance_id=sfsub.id, type=trcid.type, value=trcid.value, source=trcid.source)
            ident.save()
            print("added " + trcid.value)
        # add chemtwin
        saved = newjld(RequestFactory().request(), sfsub.id)
        print("saved chemtwin of " + sfsub.inchikey)
        rpath = 'https://sds.coas.unf.edu/sciflow/files/facet/'
        lpath = 'uploads/tranche/chalklab/chemtwin/' + sfsub.inchikey + '.jsonld'
        uploaded = uploadfile(rpath, lpath, sfsub.id)
        if uploaded:
            print("chemtwin uploaded to scidata")

# remove incorrect inchikeys (most generic) from identifiers
if False:
    subs = Substances.objects.values('id', 'inchikey').all().order_by('id')
    total = 0
    for sub in subs:
        keys = Identifiers.objects.filter(substance_id=sub['id'], type='inchikey').values('id', 'value')
        cleaned = 0
        for key in keys:
            if key['value'] != sub['inchikey']:
                Identifiers.objects.filter(id=key['id']).delete()
                cleaned += 1
        total += cleaned
        print(str(sub['id']) + ": " + str(cleaned) + " cleaned")
    print(str(total) + " cleaned")

# check classyfire code
if False:
    key = 'ZMRUPTIKESYGQW-UHFFFAOYSA-N'
    classyfire(key, {}, {}, {})

# check wikidata code
if False:
    key = 'UHOVQNZJYSORNB-UHFFFAOYSA-N'
    ids, srcs = {}, {}
    wikidata(key, ids, srcs)
    print(srcs)

# remove duplicate substances by inchikey
if False:
    keys = Substances.objects.distinct().values_list('inchikey', flat=True). \
        annotate(keycnt=Count('inchikey')).filter(keycnt__gt=1)
    for key in keys:
        print(key)
        dupes = Substances.objects.filter(inchikey=key).values_list('id', flat=True)
        delid = max(dupes)
        facid = Substances.objects.values_list('facet_lookup_id', flat=True).get(id=delid)
        # delete entries in identifiers
        delcnt = Identifiers.objects.filter(substance_id=delid).delete()
        print("deleted " + str(delcnt) + " in identifiers")
        # delete entries in descriptors
        delcnt = Descriptors.objects.filter(substance_id=delid).delete()
        print("deleted " + str(delcnt) + " in descriptors")
        # delete entries in sources
        delcnt = Sources.objects.filter(substance_id=delid).delete()
        print("deleted " + str(delcnt) + " in sources")
        # delete entries in structures
        delcnt = Structures.objects.filter(substance_id=delid).delete()
        print("deleted " + str(delcnt) + " in structures")
        # delete entries in facet_files
        delcnt = FacetFiles.objects.filter(facet_lookup_id=facid).delete()
        print("deleted " + str(delcnt) + " in facet files")
        # delete entries in json_facets
        delcnt = JsonFacets.objects.filter(facet_lookup_id=facid).delete()
        print("deleted " + str(delcnt) + " in json facets")
        # delete substance entry
        delcnt = Substances.objects.get(id=delid).delete()
        print("deleted " + str(delcnt) + " in substances")
        # delete entry in facet_lookup
        delcnt = FacetLookup.objects.get(id=facid).delete()
        print("deleted " + str(delcnt) + " in facet lookup")

# add trc substances to sciflow
if False:
    tmp = requests.get('https://sds.coas.unf.edu/trc/admin/keylist')
    keys = json.loads(tmp.content)
    ctkeys = Identifiers.objects.values_list('value', flat=True).filter(type='inchikey',
                                                                        lastcheck__isnull=False).distinct()
    # add compounds not found in substances
    nfsubs = Substances.objects.filter(available='no').values_list('inchikey', flat=True)
    count = 0
    for key in keys:
        count += 1
        if key in ctkeys or key in nfsubs or key:
            print(str(count) + ": found " + key)
            continue
        print(key)
        exit()
        subid = add(RequestFactory().request(), key, 'addoffline')
        if subid:
            saved = newjld(RequestFactory().request(), subid)
            rpath = 'https://sds.coas.unf.edu/sciflow/files/facet/'
            lpath = 'uploads/tranche/chalklab/chemtwin/' + key + '.jsonld'
            uploadfile(rpath, lpath, subid)
        else:
            print('InChIKey ' + key + ' not found anywhere')
        # exit()

# check casrns in substances using inchikeys
if False:
    meta, ids, srcs = {}, {}, {}
    nocas = Substances.objects.filter(casrn__isnull=True).values_list('inchikey', flat=True).order_by('id')
    for key in nocas:
        comchem(key, meta, ids, srcs)
        if meta:
            print(meta)
            exit()

# add rdkit molfiles for substances
if False:
    done = Structures.objects.all().values_list('substance_id', flat=True)
    subs = Identifiers.objects.all().filter(type='csmiles'). \
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
if False:
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
if False:
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
if False:
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
if False:
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
if False:
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
if False:
    key = 'VWNMWKSURFWKAL-HXOBKFHXSA-N'
    meta, ids, descs, srcs = {}, {}, {}, {}
    pubchem(key, meta, ids, descs, srcs)
    print(meta, ids, descs)
    print(json.dumps(srcs, indent=4))

# check output of chembl request
if False:
    key = 'SBPBAQFWLVIOKP-UHFFFAOYSA-N'
    meta, ids, descs, srcs = {}, {}, {}, {}
    chembl(key, meta, ids, descs, srcs)
    print(meta, ids, descs)
    print(json.dumps(srcs, indent=4))

# check output of classyfire request
if False:
    # key = 'VWNMWKSURFWKAL-HXOBKFZXSA-N'  # (bad inchikey)
    key = 'SIEHZFPZQUNSAS-UHFFFAOYSA-N'
    ids, descs, srcs = {}, {}, {}
    classyfire(key, ids, descs, srcs)
    print(descs)
    print(json.dumps(srcs, indent=4))

# check output of wikidata request
if False:
    # key = 'BSYNRYMUTXBXSQ-CHALKCHALK-N'  # (bad inchikey for aspirin)
    key = 'SBPBAQFWLVIOKP-UHFFFAOYSA-N'
    ids, srcs = {}, {}
    wikidata(key, ids, srcs)
    print(ids)
    print(json.dumps(srcs, indent=4))

# Get data from commonchemistry using CASRNs
if False:
    key = 'BSYNRYMUTXBXSQ-UHFFFAOYSA-N'
    meta, ids, srcs = {}, {}, {}
    comchem(key, meta, ids, srcs)
    print(ids)
    print(json.dumps(srcs, indent=4))

# process compounds with no casrn in substances table
if False:
    subs = Substances.objects.all().values_list('id', flat=True).filter(casrn__isnull=True)
    for sub in subs:
        found = Sources.objects.filter(substance_id__exact=sub, source__exact='comchem')
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

# cjeck reach ids for casrn
if False:
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
if False:
    subid = 1
    out = getinchikey(subid)
    print(out)

# test scyjava
if False:
    config.add_endpoints('io.github.egonw.bacting:managers-cdk:0.0.16')
    workspaceRoot = "."
    cdkClass = jimport("net.bioclipse.managers.CDKManager")
    cdk = cdkClass(workspaceRoot)

    print(cdk.fromSMILES("CCC"))
