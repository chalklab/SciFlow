""" views for substances """
from django.shortcuts import render
from django.shortcuts import redirect
from .models import *
from .mysql import *
from .functions import *
from sciflow.settings import BASE_DIR



def list(request):
    """view to generare list of substances on homepage"""
    if request.method == "POST":
        query = request.POST.get('q')
        return redirect('search/'+str(query))


    substances = Substances.objects.all().order_by('name')
    return render(request, "substances/list.html", {'substances': substances})


def home(request):
    """present an overview page about the substance in sciflow"""
    subcount = Substances.objects.count()
    idcount = Identifiers.objects.count()
    descount = Descriptors.objects.count()

    return render(request, "substances/home.html", {'subcount': subcount, 'idcount': idcount, 'descount': descount})


def subview(request, subid):
    """present an overview page about the substance in sciflow"""
    substance = Substances.objects.get(id=subid)
    ids = substance.identifiers_set.all()
    descs = substance.descriptors_set.all()
    srcs = substance.sources_set.all()
    if not descs:
        key = ""
        for i in ids:
            if i.type == 'inchikey':
                key = i.value
                break
        m, i, descs = getsubdata(key)
        savedescs(subid, descs)
    return render(request, "substances/subview.html", {'substance': substance, "ids": ids, "descs": descs, "srcs": srcs})

def subids(request, subid):
    """present an overview page about the substance in sciflow"""
    substance = Substances.objects.get(id=subid)
    ids = substance.identifiers_set.all()
    return render(request, "substances/subids.html", {'substance': substance, "ids": ids})

def subdescs(request, subid):
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
    return render(request, "substances/subdescs.html", {'substance': substance, "descs": descs})


def add(request, identifier):
    """ check the identifier to see if compound already in system and if not add """
    # id the compound in the database?
    hits = Substances.objects.all().filter(identifiers__value__exact=identifier).count()
    if hits == 0:
        meta, ids, descs, srcs = addsubstance(identifier)
    else:
        subid = getsubid(identifier)
        return redirect("/substances/view/" + str(subid))

    return render(request, "substances/add.html", {"hits": hits, "meta": meta, "ids": ids, "descs": descs})

def ingest(request):

    if request.method == "POST":
        inchikey = request.POST.get('ingest')
        return redirect("/substances/add/" + str(inchikey))



    return render(request, "substances/ingest.html",)

def ingestlist(request):
    """ add many compounds from a text file list of identifiers """
    path = BASE_DIR + "/json/herg_chemblids.txt"
    file = open(path)
    lines = file.readlines()
    # get a list of all chemblids currently in the DB
    qset = Identifiers.objects.all().filter(type__exact='chembl').values_list('value', flat=True)
    chemblids = list(qset)
    count = 0
    names = []
    for identifier in lines:
        identifier = identifier.rstrip("\n")
        if identifier not in chemblids:
            meta, ids, descs = addsubstance(identifier)
            names.append(ids['pubchem']['iupacname'])
        count += 1
        if count == 1:
            break
    return names


def normalize(request, identifier):
    """ create a SciData JSON-LD file for a compound, ingest in the graph and update data file with graph location """
    success = createsubjld(identifier)
    return render(request, "substances/normalize.html", {"success": success})


def search(request, query):
    """ search for a substance """
    context = subsearch(query)

    if request.method == "POST":
        query = request.POST.get('q')
        return redirect('/substances/search/'+str(query))

    return render(request, "substances/search.html", context)
