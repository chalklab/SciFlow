""" functions to interact with MySQL """
from .models import *


# used in datasets/mysql.py:getcodenames
def getdatasetnames():
    """ retrieve the shortnames of all the datasets """
    qset = Datasets.objects.all().values_list('datasetname', flat=True).order_by('id')
    lst = list(qset)
    return lst


# used in datasets/mysql.py:getcodenames
def getsourcecodes():
    """ retrieve the shortnames of all the datasets """
    qset = Datasets.objects.all().values_list('sourcecode', flat=True).order_by('id')
    lst = list(qset)
    return lst


# used in validation.py:validate
def getcodesnames():
    """ create unique string to match a file to a dataset """
    codes = getsourcecodes()
    names = getdatasetnames()
    output = {}
    for i in range(len(codes)):
        output.update({names[i]: codes[i] + ":" + names[i]})
    return output
