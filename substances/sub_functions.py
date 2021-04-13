""" functions for use with the substances and related tables..."""
from django.db.models import Q
from substances.external import *
from substances.models import *
from crosswalks.models import *
from datetime import datetime
from workflow.log_functions import *
import json
import os
import random
import string


def addsubstance(identifier, output='meta'):
    """
    add new substance to the database and populate identifiers and descriptors
    The identifier string can be any chemical metadata.  If it is not the
    inchikey for the compound then the identifier is used to find the inchikey
    The code checks for the existance of the substance in the substances
    table before adding
    :param identifier
    :param output determines how much data is returned from the function
    """

    # check for substance in the database
    found = Identifiers.objects.values().filter(value=identifier).\
        values_list('value', 'substance_id')
    found = dict(found)
    if found:
        meta = Substances.objects.get(id=found[identifier])
        ids = Identifiers.objects.values().\
            filter(substance_id=found[identifier])
        descs = Descriptors.objects.values().\
            filter(substance_id=found[identifier])
        srcs = Sources.objects.values().filter(substance_id=found[identifier])
        if output == 'all':
            return meta, ids, descs, srcs
        else:
            return meta

    # check if the identifier is a inchikey and if not find one from pubchem
    idtype = getidtype(identifier)
    if idtype != "inchikey":
        # Modified to call this definition directly. Deleted pubchemkey
        key = pubchemsyns(identifier)
    else:
        key = identifier

    # get substance data from sources
    meta, ids, descs, srcs = getsubdata(key)

    # save metadata to the substances table
    fm = 'unknown'
    nm = 'unknown'
    mw = 0
    mm = 0
    casrn = None
    if "pubchem" in ids:
        if "iupacname" in ids['pubchem']:
            nm = ids['pubchem']['iupacname']
    elif "chembl" in meta:
        if meta['chembl']['prefname'] is not None:
            nm = meta['chembl']['prefname']
    if "pubchem" in meta:
        if "formula" in meta['pubchem']:
            fm = meta['pubchem']['formula']
        if "mw" in meta['pubchem']:
            mw = meta['pubchem']['mw']
        if "mim" in meta['pubchem']:
            mm = meta['pubchem']['mim']
    elif "chembl" in meta:
        if "full_molformula" in meta['chembl']:
            fm = meta['chembl']['full_molformula']
        if "full_mwt" in meta['chembl']:
            mw = meta['chembl']['full_mwt']
        if "mw_monoisotopic" in meta['chembl']:
            mm = meta['chembl']['mw_monoisotopic']
    if "wikidata" in ids:
        if "casrn" in ids['wikidata']:
            casrn = ids['wikidata']['casrn']
    sub = Substances(name=nm, formula=fm, molweight=mw,
                     monomass=mm, casrn=casrn)
    sub.save()
    subid = sub.id

    # save ids to the identifiers table
    saveids(subid, ids)

    # save descs to the descriptors table
    savedescs(subid, descs)

    # savesrcs to sources table
    savesrcs(subid, srcs)

    if output == 'all':
        return meta, ids, descs, srcs
    elif output == 'sub':
        return sub
    else:
        return meta


def updatesubstance(subid, field, value):
    """update a field in the entr in the substances table"""
    sub = Substances.objects.get(id=subid)
    setattr(sub, field, value)
    sub.save()


def getidtype(identifier):
    """ try and determine the type of identifier given """

    # is the string an inchikey?
    m = re.search('^[A-Z]{14}-[A-Z]{10}-[A-Z]$', identifier)
    if m:
        return "inchikey"

    # is the string an inchi?
    n = re.search('^InChI=1S?/', identifier)
    if n:
        return "inchi"

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
    """searches for cmpd in DB and gets data or adds new cmpd with data"""
    meta, ids, descs, srcs = {}, {}, {}, {}
    try:
        pubchem(identifier, meta, ids, descs, srcs)
    except Exception as exception:
        srcs.update({"pubchem": {"result": 0, "notes": exception}})
    try:
        classyfire(identifier, descs, srcs)
    except Exception as exception:
        srcs.update({"classyfire": {"result": 0, "notes": exception}})
    try:
        wikidata(identifier, ids, srcs)
    except Exception as exception:
        srcs.update({"wikidata": {"result": 0, "notes": exception}})
    try:
        chembl(identifier, meta, ids, descs, srcs)
    except Exception as exception:
        srcs.update({"chembl": {"result": 0, "notes": exception}})
    try:
        comchem(identifier, meta, ids, srcs)
    except Exception as exception:
        srcs.update({"comchem": {"result": 0, "notes": exception}})

    return meta, ids, descs, srcs


def getmeta(subid):
    """get the basic metadata for a substance"""
    meta = Substances.objects.values().get(id=subid)
    return meta


def createsubjld(subid):
    """
    create SciData JSON-LD file for cmpd,
    ingest in graph and update DB with graphname
    """

    # get the substance template file from the database
    tmpl = Templates.objects.get(type="compound")
    sd = json.loads(tmpl.json)
    cmpd = sd['@graph']['scidata']['system']['facets'][0]

    # get the metadata fields from the DB that need to be included in the file
    fields = Metadata.objects.filter(sdsubsection="compound")

    # get the substance info (metadata, identifiers, descriptors)
    substance = Substances.objects.get(id=subid)
    ids = dict(substance.identifiers_set.all().values_list('type', 'value'))
    descs = substance.descriptors_set.all().values_list('type', 'value')

    # add general metadata
    sd['generatedAt'] = str(datetime.now())
    title = "Chemical Substance SciData JSON-LD file for " + substance.name
    sd['@graph']['title'] = title

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
            # if identifier=inchikey then populate other locations in json file
            val = get_item(ids, label)
            if label == 'inchikey':
                last = len(sd['@context']) - 1
                base = sd['@context'][last]['@base'].replace("<inchikey>", val)
                sd['@context'][last]['@base'] = base
                sd['@graph']['@id'] = base
                sd['@graph']['permalink'] = base
                uid = sd['@graph']['uid'].replace("<inchikey>", val)
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
                            elif field.datatype == "xsd:integer" or \
                                    field.datatype == "xsd:nonNegativeInteger":
                                value.append(int(val))
        # add field to cmpd
        if field.output == "datum":
            cmpd[section].update({label: value})
        elif field.output == "array":
            cmpd[section][label] = value

    # add molecular graph
    # get molfile from pubchem (if available)
    if "pubchem" in ids.keys():
        pcid = ids["pubchem"]
        mol = pubchemmol(pcid)
        atoms = mol['atoms']
        bonds = mol['bonds']
        chrgs = mol['chrgs']

        # get list of elements in the compound
        elements = []
        for atom in atoms:
            if atom[3] not in elements:
                elements.append(atom[3])

        # create element section for file
        els = []
        ids = list(sd['@graph']['ids'])
        for i, symbol in enumerate(elements):
            idx = str(i + 1)
            name = elementdata(symbol, 'Symbol', 'Name')
            chebi = elementdata(symbol, 'Symbol', 'ChEBI')
            ids.append(chebi)
            el = {}
            el.update({"@id": "element/" + idx + "/"})
            el.update({"@type": "obo:NCIT_C1940"})
            el.update({"name": name})
            el.update({"element": chebi})
            els.append(el)
        sd['@graph']['ids'] = ids

        # add elements to the cmpd
        cmpd['molgraph']['elements'] = els

        # create stats on bonds - # of each bond order per atom (number)
        bstats = {}
        for idx, bond in enumerate(bonds):
            if bond[0] not in bstats:
                bstats.update({str(bond[0]): {}})
            if bond[1] not in bstats:
                bstats.update({str(bond[1]): {}})
            if bond[2] not in bstats[bond[0]]:
                bstats[bond[0]].update({str(bond[2]): 0})
            if bond[2] not in bstats[bond[1]]:
                bstats[bond[1]].update({str(bond[2]): 0})
            bstats[bond[0]][bond[2]] += 1
            bstats[bond[1]][bond[2]] += 1

        # create atom section for file
        atms = []
        for i, atom in enumerate(atoms):
            idx = str(i + 1)
            atm = {}
            atm.update({"@id": "atom/" + idx + "/"})
            atm.update({"@type": "obo:CHEBI_33250"})
            eidx = None
            for key, value in enumerate(elements):
                if value == atom[3]:
                    eidx = str(key + 1)
                    break
            atm.update({"element": "element/" + eidx + "/"})
            atm.update({"xcoord": atom[0]})
            atm.update({"ycoord": atom[1]})
            atm.update({"zcoord": atom[2]})
            if idx in bstats.keys():
                if '1' in bstats[idx].keys():
                    atm.update({"singlebonds": bstats[idx]['1']})
                if '2' in bstats[idx].keys():
                    atm.update({"doublebonds": bstats[idx]['2']})
                if '3' in bstats[idx].keys():
                    atm.update({"triplebonds": bstats[idx]['3']})
            for chrg in chrgs:
                if chrg[0] == idx:
                    atm.update({"charge": chrg[1]})
            atms.append(atm)

        # add atoms to the cmpd
        cmpd['molgraph']['atoms'] = atms

        # create bond seection for file
        bnds = []
        for i, bond in enumerate(bonds):
            idx = str(i + 1)
            bnd = {}
            bnd.update({"@id": "bond/" + idx + "/"})
            bnd.update({"@type": "ss:SIO_011118"})
            bnd.update({"order": bond[2]})
            atms = ["atom/" + str(bond[0]) + "/", "atom/" + str(bond[1]) + "/"]
            bnd.update({"atoms": atms})
            bnds.append(bnd)

        # add bonds to the cmpd
        cmpd['molgraph']['bonds'] = bnds

    # add compound data into sd template file
    sd['@graph']['scidata']['system']['facets'][0] = cmpd

    return sd


def get_item(d, key):
    """extracts value of dictionary using the key variable as field name"""
    return d.get(key)


def get_items(tpls, key):
    """extracts values from tuples where the first value is equals the key"""
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
                    ident = Identifiers(substance_id=subid, type=k, value=x,
                                        source=source)
                    ident.save()
            else:
                # add random str in iso field to make csmiles pseudo 'unique'
                if k == 'csmiles':
                    chars = string.ascii_uppercase + string.digits
                    rstr = ''.join(random.choice(chars) for _ in range(5))
                    ident = Identifiers(substance_id=subid, type=k, value=v,
                                        iso=rstr, source=source)
                else:
                    ident = Identifiers(substance_id=subid, type=k, value=v,
                                        source=source)
                ident.save()


def getsubids(identifier):
    """get all the entries in the identifiers table for a substance"""

    # check if identifier is numeric (substance_id) or not
    if type(identifier) is int:
        subid = identifier
    else:
        # get substance table id
        subid = getsubid(identifier)
    # get all entries in the identifiers table for this substance_id
    ids = Identifiers.objects.values().\
        filter(substance_id__exact=subid).values_list('type', 'value')
    return dict(ids)


def getsubdescs(identifier):
    """get all the entries in the descriptors table for a substance"""

    # check if identifier is numeric (substance_id) or not
    if type(identifier) is int:
        subid = identifier
    else:
        # get substance table id
        subid = getsubid(identifier)
    # get all entries in the identifiers table for this substance_id
    ids = Descriptors.objects.values().\
        filter(substance_id__exact=subid).values_list('type', 'value')
    return dict(ids)


def getsubsrcs(identifier):
    """get all the entries in the sources table for a substance"""

    # check if identifier is numeric (substance_id) or not
    if type(identifier) is int:
        subid = identifier
    else:
        # get substance table id
        subid = getsubid(identifier)
    # get all entries in the identifiers table for this substance_id
    ids = Sources.objects.values().\
        filter(substance_id__exact=subid).values_list('type', 'value')
    return dict(ids)


def savedescs(subid, descs):
    """ save descriptor metadata """
    for source, e in descs.items():
        for k, v in e.items():
            # check if value is list or string
            if isinstance(v, list):
                for x in v:
                    desc = Descriptors(substance_id=subid, type=k, value=x,
                                       source=source)
                    desc.save()
            else:
                desc = Descriptors(substance_id=subid, type=k, value=v,
                                   source=source)
                desc.save()


def savesrcs(subid, srcs):
    """ save sources data """
    # srcs = {"pubchem": {"result":1, "notes":None}
    for x, y in srcs.items():
        src = Sources(substance_id=subid, source=x, result=y["result"],
                      notes=y.get("notes", "Null"))
        src.save()


def getsubid(identifier):
    """get substance id for substance identifier - return false if not found"""
    sub = Substances.objects.all().filter(identifiers__value__exact=identifier)
    if sub:
        return sub[0].id
    else:
        return False


def subingraph(subid):
    """ whatever is in the graphdb field for a substance"""
    found = Substances.objects.all().\
        values_list('graphdb', flat=True).get(id=subid)
    if found:
        return found
    return False


def subinfiles(subid):
    """ whatever is in the graphdb field for a substance"""
    found = Substances.objects.all().\
        values_list('facet_lookup_id', flat=True).get(id=subid)
    if found:
        return found
    return False


def getinchikey(subid):
    """ get the InChIKey of compound from its substance_id """
    # try pubchem
    found = Identifiers.objects.all().values_list('value', flat=True).\
        filter(substance_id=subid, type='inchikey')
    keys = list(set(found))
    if len(keys) == 0:
        errorlog("SUB_E01: Couldn't find inchikey for substance " + str(subid))
    elif len(keys) == 1:
        actlog(
            "SUB_A01: Got inchikey '" + str(keys) + "' for sub " + str(subid))
        return keys[0]
    elif len(keys) > 1:
        errorlog(
            "SUB_E02: Many inchikeys (" + str(keys) + ") 4 sub " + str(subid))
    return False


def subsearch(query):
    """search based on value field in identifiers and returns all substances"""
    if query is not None:
        lookups = Q(value__icontains=query)
        j = Identifiers.objects.filter(lookups).distinct()
        results = []
        for i in j:
            subid = i.substance_id
            sub = Substances.objects.get(id=subid)
            if sub not in results:
                results.append(sub)
        context = {'results': results, "query": query}
        return context


def elementdata(strng, field1, field2):
    """generate elements dictionary"""
    basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = basedir + '/static/files/elements.json'
    f = open(path)
    j = json.loads(f.read())
    rows = j['Table']['Row']
    fields = j['Table']['Columns']['Column']
    sidx = fields.index(field1)
    didx = fields.index(field2)
    answer = False
    for row in rows:
        if row['Cell'][sidx] == strng:
            answer = row['Cell'][didx]
            break
    return answer


searchterms = {'compound': ['^[A-Z]{14}-[A-Z]{10}-[A-Z]$',
                            '^InChI=',
                            '^[0-9]{2,7}-[0-9]{2}-[0-9]$']}


def getaddsub(section, meta):
    """ take array of metadata from a cmpds section and find in DB """
    regexs = searchterms[section]
    subid = False
    identifier = False
    for key, value in meta[section].items():
        if subid:
            break
        else:
            if key[0] == '@':  # ignore jsonld special names
                continue
            if isinstance(value, dict):
                for k, v in value.items():
                    if subid:
                        break
                    else:
                        if k[0] == '@':  # ignore jsonld special names
                            continue
                        else:
                            for regex in regexs:
                                if re.search(regex, v):
                                    identifier = v
                                    subid = getsubid(v)
                                    break
            else:
                for regex in regexs:
                    # cast all values to str (avoids error)
                    if re.search(regex, str(value)):
                        identifier = value
                        subid = getsubid(value)
                        break

    if not subid:
        sub = addsubstance(identifier, 'sub')
        subid = sub.id

    return subid
