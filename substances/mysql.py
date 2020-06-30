""" mysql functions for substances (including the identifiers and descriptors tables) """
from .models import *


def getsubid(identifier):
    """ get all the data about a substance """
    sub = Substances.objects.all().filter(identifiers__value__exact=identifier)
    if sub:
        return sub[0].id
    else:
        return False


def ingraph(subid):
    """ whatever is in the grapdb field for a substance"""
    temp = Substances.objects.all().values_list('graphdb', flat=True).get(id=subid)
    print(temp)
    return temp


def getinchikey(subid):
    """ get the InChIKey of compound from its table id """
    temp = Identifiers.objects.all().values_list('value', flat=True).get(substance_id=subid, type='inchikey')
    print(temp)
    return temp


def addsubgraphname(subid, graphname):
    """ add the graph name to graphdb in the substances table """
    sub = Substances.objects.get(id=subid)
    sub.graphdb = graphname
    sub.save()
