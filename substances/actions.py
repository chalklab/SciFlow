""" functions related to actions needed by view functions"""
from .functions import *
from .models import Substances
from .models import Identifiers
from .models import Descriptors


def addsubstance(identifier):
    """ add a new substance to the database and populate identifiers and descriptors """
    idtype = getidtype(identifier)
    key = ""
    if idtype != "inchikey":
        # check pubchem for this string
        key = pubchemkey(identifier)

    meta, ids, descs = getsubdata(key)
    # save metadata to the substances table
    nm = ids['pubchem']['iupacname']
    fm = meta['pubchem']['formula']
    mw = meta['pubchem']['mw']
    mm = meta['pubchem']['mim']
    try:
        cn = ids['wikidata']['casrn']
    except Exception as ex:
        cn = None
    sub = Substances(name=nm, formula=fm, molweight=mw, monomass=mm, casrn=cn)
    sub.save()
    subid = sub.id

    # save ids to the identifiers table
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

    # save descs
    savedescs(subid, descs)

    # TODO how to insert ignore?
    return meta, ids, descs


def getsubid(identifier):
    """ get all the data about a substance """
    sub = Substances.objects.all().filter(identifiers__value__exact=identifier)
    return sub[0].id


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
