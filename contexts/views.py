""" django view file """
from django.shortcuts import render
from contexts.ctx_functions import *
from datasets.ds_functions import *


def index(request):
    ctxs = getctxs()
    return render(request, "contexts/list.html", {'contexts': ctxs})


def view(request, ctxid):
    ctx = getctx(ctxid)
    ds = getset(ctx.dataset_id)
    cws = ctx.crosswalks_set.all()
    onts = list[cws.values('ontterm_id', 'ontterm__url')]
    return render(request, "contexts/view.html",
                  {'context': ctx, 'dataset': ds, 'crosswalks': cws, 'onts': onts})


def nslist(request):
    """view to generate list of namespaces"""
    spaces = getnspaces()
    return render(request, "nspaces/list.html", {'spaces': spaces})


def nsview(request, nsid):
    """view to show all data about a namespace"""
    space = getnspace(nsid)
    terms = onttermsbyns(nsid)
    return render(request, "nspaces/view.html", {'space': space, 'terms': terms})


def ontterm(request, tid):
    """view to show all data about an ont term"""
    term = getterm(tid)
    space = getnspace(term.nspace_id)
    url = term.url.replace(space.ns + ':', space.path)
    return render(request, "terms/view.html", {'term': term, 'url': url})
