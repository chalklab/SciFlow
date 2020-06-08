"""imports"""
from django.shortcuts import render
from django.shortcuts import redirect
from .models import *
from .actions import *
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
    descs = substance.descriptors_set.all()
    if not descs:
        key = ""
        for i in ids:
            if i.type == 'inchikey':
                key = i.value
                break
        m, i, descs = getsubdata(key)
        savedescs(subid, descs)
    return render(request, "substances/view.html", {'substance': substance, "ids": ids, "descs": descs})


def add(request, identifier):
    """ check the identifier to see if compound alredy in system and if not add """
    # id the compound in the database?
    hits = Substances.objects.all().filter(identifiers__value__exact=identifier).count()
    if hits == 0:
        meta, ids, descs = addsubstance(identifier)
    else:
        subid = getsubid(identifier)
        return redirect("/substances/view/" + str(subid))

    return render(request, "substances/add.html",
                  {"hits": hits, "meta": meta, "ids": ids, "descs": descs})
