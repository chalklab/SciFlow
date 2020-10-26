""" functions file for the datafiles app"""
import json
from datafiles.models import *
from django.contrib.auth.models import *
from django.core.exceptions import ValidationError
import json

testpath = "C:/Users/Caleb Desktop/PycharmProjects/sciflow/datafiles/test.jsonld"

# Variant that only adds the lookup info so errors can be stored. Upon validation addfile is run and the file is actually added.
def initfile(jsonld, uploading_user):
    """
    Add a data jsonld file to the database
    Required dictionary entries
        dataset_id: id of dataset to which the data belongs
        path: path to data jsonld file (OR file)
        file: file contents (OR path)
    :param finfo: data jsonld file information
    :return: boolean
    """
    finfo=None
    if finfo is None:
        #  use the test input
        finfo = {
            "dataset_id": 1
        }

    # return error is required files not included
    if 'dataset_id' not in finfo:
        return "error: required fields not provided"


    # save metadata
    if JsonLookup.objects.filter(uniqueid = jsonld['@graph']['uid']):
        m = JsonLookup.objects.get(uniqueid = jsonld['@graph']['uid'])
    else:
        m = JsonLookup()

    if finfo['dataset_id']:
        m.dataset_id = finfo['dataset_id']
    m.uniqueid = jsonld['@graph']['uid']
    m.title = jsonld['@graph']['title']
    m.graphname = jsonld['@id']
    m.auth_user_id = uploading_user.id
    m.save()

    if m.id:
        return True
    else:
        return False


def updatefile(jsonld):
    """
    Add a data jsonld file to the database
    Requires metadata to be previously established in the lookups table
    Required dictionary entries
        dataset_id: id of dataset to which the data belongs
        path: path to data jsonld file
    :param finfo: data jsonld file information
    :return: boolean
    """

    finfo=None
    if finfo is None:
        #  use the test input
        finfo = {
            "dataset_id": 1
        }

    # return error is required files not included
    if 'dataset_id' not in finfo:
        return "error: required fields not provided"

    # get metadata
    m = JsonLookup.objects.get(uniqueid=jsonld['@graph']['uid'])
    m.currentversion += 1
    m.save()

    # save json file
    f = JsonFiles()
    f.json_lookup_id = m.id
    f.file = json.dumps(jsonld, separators=(',', ':'))
    f.type = "raw"
    f.version = m.currentversion
    f.save()


    if m.id and f.id:
        return True
    else:
        return False


# ----- Validation -----
def json_validator(json_file):
    json_file_content = json.load(json_file)
    keys_a = []
    keys_b = []
    isscidata = True
    if not str(json_file).endswith('.jsonld'):
        isscidata = False
    for k, v in json_file_content.items():
        keys_a.append(k)
        if k == '@graph':
            for y, z in v.items():
                keys_b.append(y)
    for y in ['@context', '@id', '@graph']:
        if y not in keys_a:
            isscidata = False
    for y in ['scidata']:
        if y not in keys_b:
            isscidata = False
    if not isscidata:
        raise ValidationError("Not Valid SciData JSON-LD")
