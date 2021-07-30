""" functions file for the datafiles app"""
from contexts.models import *


def getctxs():
    """get a list of contexts"""
    ctxs = Contexts.objects.all()
    return ctxs


def getctx(ctxid):
    """get a list of contexts"""
    ctx = Contexts.objects.get(id=ctxid)
    return ctx


def getcwks():
    """get a list of contexts"""
    cwks = Crosswalks.objects.all().order_by('field')
    return cwks


def getcwk(ctxid):
    """get a list of contexts"""
    cwk = Crosswalks.objects.get(id=ctxid)
    return cwk


def getnsps():
    """get a list of namespaces"""
    spaces = Nspaces.objects.all()
    return spaces


def getnsp(nsid):
    """get the data about a namespace"""
    space = Nspaces.objects.get(id=nsid)
    return space


def getonts():
    """get the data for an ont term"""
    terms = Ontterms.objects.all().filter(to_remove__isnull=True).order_by('title')
    return terms


def getont(otid):
    """get the data for an ont term"""
    term = Ontterms.objects.get(id=otid)
    return term


def onttermsbyns(nsid):
    """get the ont terms using a namespace"""
    terms = Ontterms.objects.all().filter(nspace_id=nsid)
    return terms
