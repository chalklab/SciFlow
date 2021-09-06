""" django view file """
import json

from django.shortcuts import render, redirect
from datasets.ds_functions import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from contexts.ctx_functions import *


def ctxlist(request):
    ctxs = getctxs()
    return render(request, "contexts/list.html", {'contexts': ctxs})


def ctxview(request, ctxid):
    ctx = getctx(ctxid)
    ds = getset(ctx.dataset_id)
    cws = ctx.crosswalks_set.all().order_by('table', 'field')
    onts = list[cws.values('ontterm_id', 'ontterm__url')]
    return render(request, "contexts/view.html",
                  {'context': ctx, 'dataset': ds, 'crosswalks': cws, 'onts': onts})


def cwklist(request):
    """view to generate list of namespaces"""
    crosswalks = getcwks()
    return render(request, "crosswalks/list.html", {'crosswalks': crosswalks})


def cwkview(request, cwkid):
    """view to show all data about a namespace"""
    crosswalk = getcwk(cwkid)
    return render(request, "crosswalks/view.html", {'crosswalk': crosswalk})


def nsplist(request):
    """view to generate list of namespaces"""
    spaces = getnsps()
    return render(request, "nspaces/list.html", {'spaces': spaces})


def nspview(request, nspid):
    """view to show all data about a namespace"""
    space = getnsp(nspid)
    terms = onttermsbyns(nspid)
    return render(request, "nspaces/view.html", {'space': space, 'terms': terms})


def nspadd(request):
    """view to show all data about a namespace"""
    if request.method == "POST":
        # save new namespace
        data = request.POST
        nspace = Nspaces()
        nspace.name = data['name']
        nspace.ns = data['alias']
        nspace.path = data['path']
        nspace.homepage = data['homepage']
        nspace.save()
        return redirect('/nspaces/')

    aliases = nsaliases()
    oonts = olsonts()  # list of tuples (four values)
    oonts.sort(key=lambda tup: tup[1])
    return render(request, "nspaces/add.html", {'aliases': aliases, 'onts': oonts})


def ontlist(request):
    """view to generate list of namespaces"""
    terms = getonts()
    return render(request, "ontterms/list.html", {'ontterms': terms})


def ontview(request, ontid):
    """view to show all data about an ont term"""
    term = getont(ontid)
    space = getnsp(term.nspace_id)
    uri = term.url.replace(space.ns + ':', space.path)
    return render(request, "ontterms/view.html", {'term': term, 'uri': uri})


def ontadd(request):
    """view to show all data about a ontterms"""
    if request.method == "POST":
        # save new namespace
        data = request.POST
        ontterm = Ontterms()
        ontterm.title = data['title']
        ontterm.definition = data['alias']
        ontterm.code = data['code']
        ontterm.nspace_id = data['nspace_id']
        ontterm.sdsection = data['sdsubsection']
        ontterm.sdsubsection = data['sdsubsection']
        ontterm.save()
        return redirect('/ontterms/')

    sdsects = [('methodology', 'Methodology (the "how" section)'), ('system', 'System (the "what" section)'), ('dataset', 'Dataset (the "data" section)')]
    subsects = [('procedure', 'methodology', 'Procedure'), ('chemical', 'system', 'Chemical'),
                ('exptdata', 'dataset', 'Experimental data')]

    nss = Nspaces.objects.all().values_list('ns', 'name').order_by('name')
    aliases = nsaliases()
    onts = olsonts()  # list of tuples (four elements)
    kept = []
    onts.sort(key=lambda tup: tup[0])
    # remove entries that are not in the namespace list
    for i, ont in enumerate(onts):
        if ont[0] in aliases:
            kept.append(ont)
    return render(request, "ontterms/add.html",
                  {'nss': nss, 'sdsects': sdsects, 'subsects': subsects, 'onts': kept, 'aliases': aliases})


# ajax functions (wrappers)
@csrf_exempt
def ontterms(request, ontid):
    oterms = olsont(ontid)
    return JsonResponse({"ontterms": oterms}, status=200)
