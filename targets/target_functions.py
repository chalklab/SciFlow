import re
from django.core.exceptions import ObjectDoesNotExist
from targets.external import *
from datetime import datetime
from targets.models import *
from substances.models import *


def getgenedata(identifier):

    """search chembl API for gene data"""
    meta, ids, descs, srcs = {}, {}, {}, {}
    try:
        search_chembl(identifier, meta, ids, descs, srcs)
    except Exception as exception:
        srcs.update({"chembl": {"result": 0, "notes": exception}})
    return meta, ids, descs, srcs


def addgene(identifier, output='meta'):

    """
    add new gene to the database
    :param identifier
    :param output determines how much data is returned from the function
    """

    # assign chemblid to key
    key = identifier

    # get gene data from sources
    meta, ids, descs, srcs = getgenedata(key)
    if output == "all":
        return [meta, ids, descs, srcs]
    else:
        return meta


def createtargjld(addedtarg):
    """
    create SciData JSON-LD file for a target
    """

    # get the substance template file from the database
    tmpl = Templates.objects.get(type="target")
    meta = addedtarg[0]['chembl']
    ids = addedtarg[1]['chembl']
    descs = addedtarg[2]['chembl']
    srcs = addedtarg[3]['chembl']
    sd = json.loads(json.dumps(tmpl))
    # print(sd)

    gene = sd['@graph']['scidata']['system']['facets'][0]
    gene_chembl_id = ids.get('chembl_id').replace('CHEMBL', '')
    # get the metadata fields from the DB that need to be included in the file
    # fields = Metadata.objects.filter(sdsubsection="compound")

    # add general metadata
    sd['generatedAt'] = str(datetime.now())
    title = "Gene SciData JSON-LD for " + ids.get('pref_name')
    sd['@graph']['title'] = title
    uid = sd['@graph']['uid'].replace("<chemblid>", gene_chembl_id)
    sd['@graph']['uid'] = uid
    pl = sd['@graph']['permalink'].replace("<chemblid>", gene_chembl_id)
    sd['@graph']['permalink'] = pl
    last = len(sd['@context']) - 1
    base = sd['@context'][last]['@base'].replace("<chemblid>", gene_chembl_id)
    sd['@context'][last]['@base'] = base
    gid = sd['@graph']['@id'].replace("<chemblid>", gene_chembl_id)
    sd['@graph']['@id'] = gid

    # add general gene metadata
    if ids.get('pref_name'):
        sd['@graph']['scidata']['system']['facets'][0]['name'] = ids.get('pref_name')
    if ids.get('organism'):
        sd['@graph']['scidata']['system']['facets'][0]['organism'] = ids.get('organism')
    if ids.get('tax_id'):
        sd['@graph']['scidata']['system']['facets'][0]['organism#'] = "NCBI:txid" + str(ids.get('tax_id'))
    if ids.get('target_type'):
        sd['@graph']['scidata']['system']['facets'][0]['target_type'] = ids.get('target_type')
    sd['@graph']['scidata']['system']['facets'][0]['accession_id'] = ids.get('accession_id')

    # add compound data into sd template file
    sd['@graph']['scidata']['system']['facets'][0] = gene
    # sd = json.dumps(sd)
    return sd

# creategenejld(addgene("CHEMBL240"))


# tid = "CHEMBL240"
# with open("scidata_gene_"+tid + '.jsonld', 'w') as f:
#     final_output = json.dump(creategenejld(addgene(tid)), f)

# might not be needed because no targ_id in identifier section
def gettargid(identifier):
    target = Targets.objects.all().filter(identifiers_values_exact=identifier)
    if target:
        return target[0].id
    else:
        return False


def getidtype(identifier):
    p = re.search('^CHEMBL[0-9]+$', identifier)
    if p:
        return "chemblid"
    return "other"


def gettargdata(identifier):
    """ from ChEMBL, UniProt, and Wikidata """
    # ChEMBL
    meta, ids, descs, srcs, = {}, {}, {}, {}
    try:
        search_chembl(identifier, meta, ids, descs, srcs)
    except Exception as exception:
        srcs.update({"chembl": {"result": 0, "notes": exception}})
    # UniProt TODO

    # Wikidata TODO

    return meta, ids, descs, srcs


def updatetarget(targid, field, value):
    target = Targets.objects.get(id=targid)
    setattr(target, field, value)
    target.save()


def saveids(targid, ids):
    for source, e in ids.items():
        for k, v in e.items():
            if isinstance(v, list):
                for x in v:
                    ident = Identifiers(target_id=targid, type=k, value=x, source=source)
                    ident.save()
            else:
                print("not saved")


def savedescs(targid, descs):
    for source, e in descs.items():
        for k, v in e.items():

            if isinstance(v, list):
                for x in v:
                    desc = Descriptors(target_id=targid, type=k, value=x, source=source)
                    desc.save()
            else:
                desc = Descriptors(target_id=targid, type=k, value=v, source=source)
                desc.save()


def savesrcs(targid, srcs):
    for x, y in srcs.items():
        src = Sources(target_id=targid, source=x, result=y["result"], notes=y.get("notes", "Null"))
        src.save()


def addtarget(identifier, output='meta'):
    found = dict(Identifiers.objects.values().filter(value=identifier).values_list('value', 'id'))
    if found:
        meta = Targets.objects.get(id=found[identifier])
        ids = Targids.objects.values().filter(target_id=found[identifier])
        descs = Targdescs.objects.values().filter(target_id=found[identifier])
        srcs = Targsrcs.objects.values().filter(target_id=found[identifier])
        if output == 'all':
            return meta, ids, descs, srcs
        else:
            return meta
    idtype = getidtype(identifier)
    if idtype != "chemblid":
        print('Not a ChEMBL ID!')
        exit()

    # no existing data for this target so find and add it
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
    else:
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

    if output == 'all':
        return meta, ids, descs, srcs
    elif output == 'meta':
        return meta
    else:
        return meta


def tempcreatetargjld():
    with open('/Users/n01387071/Downloads/chembl_target_2085.jsonld', 'r') as chembl2085:
        # function is specific to computer, insert where chembl_target_2085.jsonld is located
        chembl2085 = chembl2085.read()
        return chembl2085


def getaddtarg(section, meta):
    targid = False
    for key, value in meta[section].items():
        if targid:
            break
        else:
            if key[0] == '@':  # ignore jsonld special names
                continue
            if isinstance(value, dict):
                for k, v in value.items():
                    if targid:
                        break
                    else:
                        if k[0] == '@':  # ignore jsonld special names
                            continue
                        else:
                            if v.startswith('CHEMBL'):
                                targid = Targets.objects.values('id').get(chembl_id=v)['id']
                                break
            else:
                # cast all values to str (avoids error)
                if str(value).startswith('CHEMBL'):
                    try:
                        targid = Targets.objects.values('id').get(chembl_id=value)['id']
                    except ObjectDoesNotExist:
                        targid = False
                    break

    if not targid:
        target = addtarget("CHEMBL2085", 'target')  # temporary identifier = "CHEMBL2085"
        targid = target.id
        # TODO addtarget
        # sub = addsubstance(identifier, 'sub')
        # subid = sub.id
        # print('target not found')

    return targid


def targingraph(targid):
    """ whatever is in the graphdb field for a substance"""
    found = Targets.objects.all().values_list('graphdb', flat=True).get(id=targid)
    if found:
        return found
    return False


def targinfiles(targid):
    """ whatever is in the graphdb field for a substance"""
    found = Targets.objects.all().values_list('facet_lookup_id', flat=True).get(id=targid)
    if found:
        return found
    return False
