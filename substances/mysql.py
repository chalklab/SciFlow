""" mysql functions for substances (including the identifiers and descriptors tables) """
from .models import *
from django.db.models import Q


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


def subsearch(query):
    """ searches based on the value field in the identifiers table and returns all substances pertaining to it"""
    if query is not None:
        lookups = Q(value__icontains=query)
        j = Identifiers.objects.filter(lookups).distinct()
        results = []
        for i in j:
            subid = i.substance_id
            sub = Substances.objects.get(id=subid)
            if sub not in results:
                results.append(sub)
        context = {'results': results, "query": query}
        return context
