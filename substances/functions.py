""" functions for use with the substances and related tables..."""
from .sources import *
from .mysql import *
from sciflow.settings_local import gdrive
from crosswalks.models import *
from datetime import datetime
import json
import os


def addsubstance(identifier):
    """ add a new substance to the database and populate identifiers and descriptors """
    idtype = getidtype(identifier)
    key = identifier
    if idtype != "inchikey":
        # check pubchem for this string
        key = pubchemkey(identifier)

    meta, ids, descs, srcs = getsubdata(key)
    # save metadata to the substances table
    nm = ids['pubchem']['iupacname']
    fm = meta['pubchem']['formula']
    mw = meta['pubchem']['mw']
    mm = meta['pubchem']['mim']
    try:
        cn = ids['wikidata']['casrn']
    except:
        cn = None
    sub = Substances(name=nm, formula=fm, molweight=mw, monomass=mm, casrn=cn)
    sub.save()
    subid = sub.id

    # save ids to the identifiers table
    saveids(subid, ids)

    # save descs to the descriptors table
    savedescs(subid, descs)

    #savesrcs to sources table
    savesrcs(subid, srcs)


    return meta, ids, descs, srcs


def getidtype(identifier):
    """ try and determine the type of identifier given """

    # is the string an inchikey?
    m = re.search('^[A-Z]{14}-[A-Z]{10}-[A-Z]$', identifier)
    if m:
        return "inchikey"

    # is the string an inchi?
    n = re.search('^InChI=1S?/', identifier)
    if n:
        return "inch"

    # is the string a CASRN?
    o = re.search('^[0-9]{2,7}-[0-9]{2}-[0-9]$', identifier)
    if o:
        return "casrn"

    # is the string a ChEMBL ID?
    p = re.search('^CHEMBL[0-9]+$', identifier)
    if p:
        return "chemblid"

    # is the string a DSSTOX ID?
    q = re.search('^DTXSID[0-9]+$', identifier)
    if q:
        return "dsstox"

    return "other"


def getsubdata(identifier):
    """ searches for compound in database and gets its data or adds new compound with data """
    meta, ids, descs, srcs = {}, {}, {}, {}
    try:
        pubchem(identifier, meta, ids, descs, srcs)
        #update sources table with 'success'
    except Exception as exception:
        #update sources table with exception
        meta["pubchem"] = {"error: "+str(exception)}
        srcs["pubchem"] = 0
    try:
        classyfire(identifier, meta, ids, descs, srcs)
    except Exception as exception:
        meta["classyfire"] = {"error: "+str(exception)}
        srcs["classyfire"] = 0
    try:
        wikidata(identifier, meta, ids, descs, srcs)
    except Exception as exception:
        meta["wikidata"] = {"error: "+str(exception)}
        srcs["wikidata"] = 0
    try:
        chembl(identifier, meta, ids, descs, srcs)
    except Exception as exception:
        meta["chembl"] = {"error: "+str(exception)}
        srcs["chembl"] = 0
    return meta, ids, descs, srcs


def pubchemkey(identifier):
    """ searches PubChem for compound inchikey """
    inchikey = pubchemsyns(identifier)
    return inchikey


def createsubjld(identifier):
    """ create a SciData JSON-LD file for a compound, ingest in the graph and update DB with graph location """

    # get the substance template file from the database
    tmpl = Templates.objects.get(type="compound")
    sd = json.loads(tmpl.json)
    cmpd = sd['@graph']['scidata']['system']['facets'][0]

    # get the metadata fields from the database that needs to be included in the file
    fields = Metadata.objects.filter(sdsubsection="compound")

    # get the substance info (metadata, identifiers, descriptors)
    subid = getsubid(identifier)
    substance = Substances.objects.get(id=subid)
    ids = dict(substance.identifiers_set.all().values_list('type', 'value'))
    descs = substance.descriptors_set.all().values_list('type', 'value')

    # add general metadata
    sd['@graph']['title'] = "Substance SciData JSON-LD file for " + substance.name
    sd['@graph']['starttime'] = str(datetime.now())

    # add general compound metadata
    cmpd['name'] = substance.name
    cmpd['formula'] = substance.formula
    cmpd['molweight'] = substance.molweight
    cmpd['monoisotopicmass'] = substance.monomass

    # loop through fields to add them to the appropriate sections
    for field in fields:
        label = field.label
        section = field.sdsubsubsection
        value = []
        if section == 'identifiers':
            # if identifier is inchikey then populate other locations in json file
            value = get_item(ids, label)
            if label == 'inchikey':
                base = sd['@context'][3]['@base'].replace('<inchikey>', value)
                sd['@context'][3]['@base'] = base
                sd['@id'] = base
                sd['@graph']['permalink'] = base
                uid = sd['@graph']['uid'].replace('<inchikey>', value)
                sd['@graph']['uid'] = uid
        elif section == 'descriptors':
            if field.group is None:
                # expecting only one value in list
                vlst = get_items(descs, label)
                if len(vlst) == 1:
                    value = vlst[0]
                else:
                    value = vlst
            else:
                gflds = field.group.split(',')
                for gfld in gflds:
                    vlst = get_items(descs, gfld)
                    if vlst is not None:
                        for val in vlst:
                            if field.datatype == "xsd:string":
                                value.append(val)
                            elif field.datatype == "xsd:integer" or field.datatype == "xsd:nonNegativeInteger":
                                value.append(int(val))

        # add field to cmpd
        if field.output == "datum":
            cmpd[section].update({label: value})
        elif field.output == "array":
            cmpd[section][label] = value

    # TODO add molecular graph

    # add compound data into sd file
    sd['@graph']['scidata']['system']['facets'][0] = cmpd

    # save file
    filename = identifier + '.jsonld'
    filepath = os.path.join(gdrive, 'tmp', filename)
    with open(filepath, 'w') as outfile:
        json.dump(sd, outfile)
        outfile.close()
        os.chmod(filepath, 0o777)
    try:
        f = open(filepath)
        f.close()
        # TODO add logging here
    except FileNotFoundError as fnf_error:
        print(fnf_error)  # TODO add logging here
        return False
    return filename


def get_item(d, key):
    """ extracts the value of dictionary using the key variable for the field name """
    return d.get(key)


def get_items(tpls, key):
    """ extracts values from tuples where the first value is equal to the key """
    lst = []
    for tpl in tpls:
        if tpl[0] == key:
            lst.append(tpl[1])
    return lst


def saveids(subid, ids):
    """ save identifier metadata """
    for source, e in ids.items():
        for k, v in e.items():
            # check if value is list or string
            if isinstance(v, list):
                for x in v:
                    ident = Identifiers(substance_id=subid, type=k, value=x, source=source)
                    ident.save()
            else:
                ident = Identifiers(substance_id=subid, type=k, value=v, source=source)
                ident.save()


def savedescs(subid, descs):
    """ save descriptor metadata """
    for source, e in descs.items():
        for k, v in e.items():
            # check if value is list or string
            if isinstance(v, list):
                for x in v:
                    desc = Descriptors(substance_id=subid, type=k, value=x, source=source)
                    desc.save()
            else:
                desc = Descriptors(substance_id=subid, type=k, value=v, source=source)
                desc.save()


def savesrcs(subid, srcs):
    """ save sources data """
    src = Sources(substance_id=subid, chembl=srcs["chembl"], classyfire=srcs["classyfire"],
                  pubchem=srcs["pubchem"], wikidata=srcs["wikidata"])
    src.save()