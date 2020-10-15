""" functions file for the datafiles app"""
import json
from datasets.models import *
from django.contrib.auth.models import *


testpath = "C:/Users/Caleb Desktop/PycharmProjects/sciflow/datafiles/test.jsonld"

# Variant that only adds the lookup info so errors can be stored. Upon validation addfile is run and the file is actually added.
def initfile(finfo=None):
    """
    Add a data jsonld file to the database
    Required dictionary entries
        dataset_id: id of dataset to which the data belongs
        path: path to data jsonld file (OR file)
        file: file contents (OR path)
    :param finfo: data jsonld file information
    :return: boolean
    """

    if finfo is None:
        #  use the test input
        finfo = {
            "dataset_id": 1, "auth_user_id": 2, "path": testpath
        }

    # return error is required files not included
    if 'dataset_id' not in finfo and 'path' not in finfo:
        return "error: required fields not provided"

    # load jsonld file if path present (overrides data in finfo['file'])
    if finfo['path']:
        with open(finfo['path']) as ld:
            jsonld = json.load(ld)
            finfo['file'] = json.dumps(jsonld, separators=(',', ':'))

    # get current user
    # TODO get access to authenticated user configured
    # current_user = User

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
    if finfo['auth_user_id']:
        m.auth_user_id = finfo['auth_user_id']
    m.save()


    if m.id:
        return True
    else:
        return False


def addfile(finfo=None):
    """
    Add a data jsonld file to the database
    Requires metadata to be previously established in the lookups table
    Required dictionary entries
        dataset_id: id of dataset to which the data belongs
        path: path to data jsonld file
    :param finfo: data jsonld file information
    :return: boolean
    """

    if finfo is None:
        #  use the test input
        finfo = {
            "dataset_id": 1, "auth_user_id": 2, "path": testpath
        }

    # return error is required files not included
    if 'dataset_id' not in finfo and 'path' not in finfo:
        return "error: required fields not provided"

    # load jsonld file if path present (overrides data in finfo['file'])
    if finfo['path']:
        with open(finfo['path']) as ld:
            jsonld = json.load(ld)
            finfo['file'] = json.dumps(jsonld, separators=(',', ':'))

    # get current user
    # TODO get access to authenticated user configured
    # current_user = User


    # get metadata
    m = JsonLookup.objects.get(uniqueid=jsonld['@graph']['uid'])
    m.currentversion += 1
    m.save()

    # save json file
    f = JsonFiles()
    f.json_lookup_id = m.id
    if finfo['file']:
        f.file = json.dumps(jsonld, separators=(',', ':'))
    f.type = "raw"
    f.version = m.currentversion
    f.save()


    if m.id and f.id:
        return True
    else:
        return False
