"""imports"""
from django.shortcuts import render
from django.utils import timezone
from .models import Substances
from .models import Identifiers
from .models import Systems
from .functions import *


def home(request):
    """view to generare list of substances on homepage"""
    substances = Substances.objects.all().filter(name__contains='benzene').order_by('name')
    return render(request, "substances/home.html", {'substances': substances})


def index(request):
    """present an overview page about the substance in sciflow"""
    subcount = Substances.objects.count()
    idcount = Identifiers.objects.count()
    syscount = Systems.objects.count()

    return render(request, "substances/index.html", {'subcount': subcount, 'idcount': idcount, 'syscount': syscount})


def view(request, subid):
    """present an overview page about the substance in sciflow"""
    substance = Substances.objects.get(id=subid)
    ids = substance.identifiers_set.all()
    # ids = Identifiers.objects.all().filter(substance_id=subid)
    return render(request, "substances/view.html", {'substance': substance, "ids": ids})


def add(request, identifier):
    """ check the identifier to see if compound alredy in system and if not add """

    # id the compound in the database?
    hits = Substances.objects.all().filter(identifiers__value__exact=identifier).count()
    idtype = getidtype(identifier)
    meta, ids, descs = {}, {}, {}
    if hits == 0:
        if idtype == "other" or idtype == "casrn" or idtype == "smiles":
            # check pubchem for this string
            key = pubchemkey(identifier)

        meta, ids, descs = getsubdata(key)
        # save metadata to the substances table
        nm = ids['pubchem']['iupacname']
        fm = meta['pubchem']['formula']
        mw = meta['pubchem']['mw']
        mm = meta['pubchem']['mim']
        cn = ids['wikidata']['casrn']
        sub = Substances(name=nm, formula=fm, molweight=mw, monomass=mm, casrn=cn)
        sub.save()
        subid = sub.id
        # save ids to the identifiers table
        for k, v in ids['pubchem'].items():
            ident = Identifiers(substance_id=subid, type=key, value=v, source='pubchem')
            ident.save()

        # save descs

    else:
        alldata = {}

    return render(request, "substances/add.html",
                  {"hits": hits, "idtype": idtype, "meta": meta, "ids": ids, "descs": descs})
