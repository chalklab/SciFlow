""" functions for use with the substances and related tables..."""
import re
from .sources import *


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
        return "chembid"

    # is the string a DSSTOX ID?
    q = re.search('^DTXSID[0-9]+$', identifier)
    if q:
        return "dsstox"

    return "other"


def getsubdata(identifier):
    """ searches for compound in database and gets its data or adds new compound with data """
    meta, ids, descs = {}, {}, {}
    pubchem(identifier, meta, ids, descs)
    classyfire(identifier, meta, ids, descs)
    wikidata(identifier, meta, ids, descs)
    return meta, ids, descs


def pubchemkey(identifier):
    """ searches PubChem for compound inchikey """
    inchikey = pubchemsyns(identifier)
    return inchikey
