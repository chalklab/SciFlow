""" django view file """
from django.shortcuts import render
from crosswalks.cw_functions import *

# TODO: add functions for each dataset type


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
