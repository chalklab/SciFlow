""" functions file for the contexts app"""
from contexts.models import *
from contexts.ols_functions import *


def getctxs():
    """get a list of contexts"""
    ctxs = Contexts.objects.all()
    return ctxs


def lstctxs(idlist=[]):
    """get a list of contexts"""
    if idlist:
        clist = Contexts.objects.filter(id__in=idlist).values_list('id', 'name').order_by('name')
    else:
        clist = Contexts.objects.values_list('id', 'name').order_by('name')
    return clist


def getctx(ctxid):
    """get a context"""
    ctx = Contexts.objects.get(id=ctxid)
    return ctx


def getcwks(setid):
    """get a list of crosswalks for a dataset"""
    if setid == '':
        cwks = Crosswalks.objects.all().values_list('id', 'table', 'field', 'ontterm__title').order_by('field')
    else:
        cwks = Crosswalks.objects.all().filter(dataset_id=setid).\
            values_list('id', 'table', 'field', 'ontterm__title').order_by('field')
    return cwks


def getcwk(ctxid):
    """get a a crosswalk"""
    cwk = Crosswalks.objects.get(id=ctxid)
    return cwk


def getnsps():
    """get a list of namespaces"""
    spaces = Nspaces.objects.all().order_by('name')
    return spaces


def getnsp(nsid):
    """get the data about a namespace"""
    space = Nspaces.objects.get(id=nsid)
    return space


def nsaliases():
    aliases = Nspaces.objects.all().values_list('ns', flat=True).order_by('ns')
    return aliases


def getonts():
    """get the list of ont terms"""
    return Ontterms.objects.all().filter(to_remove__isnull=True).order_by('title')


def getont(otid):
    """get the data for an ont term"""
    term = Ontterms.objects.get(id=otid)
    return term


def onttermsbyns(nsid):
    """get the ont terms using a namespace"""
    terms = Ontterms.objects.all().filter(nspace_id=nsid)
    return terms


def ctxonts():
    """
    gets the ontologies in ols and then filters for only those already in sciflow
    namespaces are already aligned otherwise this will not work
    """
    kept = []
    aliases = list(nsaliases())
    print(aliases)
    allonts = olsonts()
    allonts.sort(key=lambda tup: tup[0])
    for i, ont in enumerate(allonts):
        if ont[0] in aliases:
            kept.append(ont)
    print(kept)
    exit()

    return allonts
