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


def addsubgraphname(subid, graphname):
    """ add the graph name to graphdb in the substances table """
    sub = Substances.objects.get(id=subid)
    sub.graphdb = graphname
    sub.save()


def updatesubstancefield(inchikey, field, content):
    """ For a given InChIKey, it will change the provided field with the content given """
    subid = Identifiers.objects.get(value=inchikey).substance_id
    substance = Substances.objects.filter(id=subid)
    substance.update(**{field: content})


def clearsubstancefield(inchikey, field):
    """ For a given InChIKey, it will change the provided field to NULL """
    subid = Identifiers.objects.get(value=inchikey).substance_id
    substance = Substances.objects.filter(id=subid)
    substance.update(**{field: None})


def addidentifier(inchikey, idtype, value, source):
    """ For a given InChIKey, add identifier (type & value) to that substance. Source may be set to None """
    subid = Identifiers.objects.get(value=inchikey).substance_id
    Identifiers.objects.create(substance_id=subid, type=idtype, value=value, source=source)


def createsubstance(inchikey, name, formula):
    """ add substance table using the provided information """
    Substances.objects.create(name=name, formula=formula)
    subid = Substances.objects.get(name=name, formula=formula).id
    Identifiers.objects.create(substance_id=subid, type="inchikey", value=inchikey)

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
