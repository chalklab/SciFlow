""" django view file """
import json

from django.shortcuts import render, redirect
from contexts.ctx_functions import *
from contexts.models import *
from datasets.ds_functions import *


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

    nss = Nspaces.objects.all().values_list('ns', flat=True)
    return render(request, "nspaces/add.html", {'aliases': nss})


def ontlist(request):
    """view to generate list of namespaces"""
    ontterms = getonts()
    return render(request, "ontterms/list.html", {'ontterms': ontterms})


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
        nspace = Ontterms()
        nspace.name = data['name']
        nspace.ns = data['alias']
        nspace.path = data['path']
        nspace.homepage = data['homepage']
        nspace.save()
        return redirect('/nspaces/')

    nss = Nspaces.objects.all().values_list('ns','name')
    return render(request, "ontterms/add.html", {'aliases': nss})
