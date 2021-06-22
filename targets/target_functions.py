import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sciflow.settings")
django.setup()


""" functions for use with the targets and related tables..."""

from targets.external import *
from datetime import datetime
import json
from targets.template_target import tmpl
from targets.models import *

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
    key=identifier

    # get gene data from sources
    meta, ids, descs, srcs = getgenedata(key)
    return [meta, ids, descs, srcs]



def creategenejld(addedgene):
    """
    create SciData JSON-LD file for cmpd,
    ingest in graph and update DB with graphname
    """

    # get the substance template file from the database
    # tmpl = Templates.objects.get(type="compound")
    meta, ids, descs, srcs = addedgene[0]['chembl'], addedgene[1]['chembl'], addedgene[2]['chembl'], addedgene[3]['chembl']
    sd = json.loads(json.dumps(tmpl))
    # print(sd)
    gene = sd['@graph']['scidata']['system']['facets'][0]
    gene_chembl_id = ids.get('chembl_id').replace('CHEMBL','')
    # get the metadata fields from the DB that need to be included in the file
    # fields = Metadata.objects.filter(sdsubsection="compound")

    # get the substance info (metadata, identifiers, descriptors)
    # substance = Substances.objects.get(id=subid)
    # ids = dict(substance.identifiers_set.all().values_list('type', 'value'))
    # descs = substance.descriptors_set.all().values_list('type', 'value')

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
        sd['@graph']['scidata']['system']['facets'][0]['organism#'] = "NCBI:txid"+str(ids.get('tax_id'))
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
                    if value.startswith('CHEMBL'):
                        targid = Targets.objects.values('id').get(chembl_id=value)['id']
                        break

    if not targid:
        #TODO addtarget
        # sub = addsubstance(identifier, 'sub')
        # subid = sub.id
        print('target not found')

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