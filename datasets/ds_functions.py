"""functions to support dataset view functions"""
from datafiles.df_functions import *
from pathlib import Path
from sciflow.settings import *


def testimport():
    """ import test data from static/files in the DB"""
    folder = Path(BASE_DIR + "/static/files/")
    for file in folder.iterdir():
        if str(file).endswith('.jsonld'):
            filename = str(file).split("\\")[-1]
            filetype = None
            with open(filename, "r") as f:
                data = json.load(f)
            if "/aspect/" in data["@id"]:
                filetype = "aspect"
            elif "/data/" in data["@id"]:
                filetype = "data"
            elif "/facet/" in data["@id"]:
                filetype = "facet"

            if adddatafile({"path": filename}, filetype):
                print("Imported " + filename)


# ----- MySQL Functions -----

# used in datasets/mysql.py:getcodenames
def getdatasetnames():
    """ retrieve the shortnames of all the datasets """
    qset = Datasets.objects.all().values_list(
        'datasetname', flat=True).order_by('id')
    lst = list(qset)
    return lst


# used in datasets/mysql.py:getcodenames
def getsourcecodes():
    """ retrieve the shortnames of all the datasets """
    qset = Datasets.objects.all().values_list(
        'sourcecode', flat=True).order_by('id')
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


# used to update dataset stats
def updatestats():
    """update the number of files for each different dataset"""
    # data
    sets = Datasets.objects.exclude(sourcecode='chalklab').\
        values_list('id', flat=True)
    for setid in sets:
        count = JsonLookup.objects.filter(dataset_id=setid).count()
        sett = Datasets.objects.get(id=setid)
        sett.count = count
        sett.save()

    # facets
    dnames = Datasets.objects.filter(sourcecode='chalklab').\
        values_list('id', 'datasetname')
    for setid, dname in dnames:
        count = FacetLookup.objects.filter(type=dname).count()
        sett = Datasets.objects.get(id=setid)
        sett.count = count
        sett.save()
    return
