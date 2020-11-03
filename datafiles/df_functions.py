""" functions file for the datafiles app"""
from datafiles.models import *
from django.core.exceptions import ValidationError
import json
import re


# Variant that only adds the lookup info so errors can be stored. Upon validation addfile is run and the file is actually added.
def adddatafile(jsonld, uploading_user=None):
    """
    Add data jsonld metadata to the database
    :param jsonld: data jsonld file
    :param uploading_user: user id
    :return: boolean
    """

    # save metadata
    if JsonLookup.objects.filter(uniqueid=jsonld['@graph']['uid']):
        m = JsonLookup.objects.get(uniqueid=jsonld['@graph']['uid'])
    else:
        m = JsonLookup()
        uid = jsonld['@graph']['uid']
        parts = uid.split(":")

        # get dataset_id
        dset = Datasets.objects.get(source__exact=parts[0], datasetname=parts[1])

        if dset.id:
            m.dataset_id = dset.id
        else:
            m.dataset_id = 0
        m.uniqueid = uid
        m.title = jsonld['@graph']['title']
        m.graphname = jsonld['@id']
        m.type = parts[1]
        m.currentversion = 1
        if uploading_user is None:
            m.auth_user_id = 1
        else:
            m.auth_user_id = uploading_user.id
        m.save()

    if m.id:
        return True
    else:
        return False


def updatedatafile(jsonld):
    """
    Add a data jsonld file to the database
    :param jsonld: data jsonld file information
    :return: boolean
    """

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


def addfacetfile(jsonld=None, uploading_user=None):
    """
    Add a facet jsonld file to the database
    :param jsonld: data jsonld file information
    :param uploading_user: user id
    :return: boolean
    """

    # check for valid file
    if jsonld is None or jsonld == "":
        return False

    # save metadata
    if FacetLookup.objects.filter(uniqueid=jsonld['@graph']['uid']):
        m = FacetLookup.objects.get(uniqueid=jsonld['@graph']['uid'])
    else:
        m = FacetLookup()

        uid = jsonld['@graph']['uid']
        parts = uid.split(":")

        # get dataset_id
        dset = Datasets.objects.get(sourcecode__exact=parts[0], datasetname=parts[1])

        if dset.id:
            m.dataset_id = dset.id
        else:
            m.dataset_id = 0
        m.uniqueid = uid
        m.title = jsonld['@graph']['title']
        m.type = parts[1]
        m.graphname = jsonld['@id']
        m.currentversion = 0  # because adding the file to facet_files will increment
        if uploading_user is None:
            m.auth_user_id = 1
        else:
            m.auth_user_id = uploading_user.id
        m.save()

    if m.id:
        return m.id
    else:
        return False


def updatefacetfile(jsonld=None):
    """
    Add a facet jsonld file to the database
    :param jsonld: data jsonld file information
    :return: boolean
    """

    # check for valid file
    if jsonld is None or jsonld == "":
        raise ValidationError("no jsonld file provided")

    # get metadata
    m = FacetLookup.objects.get(uniqueid=jsonld['@graph']['uid'])

    if m:
        m.currentversion += 1
        m.save()
    else:
        raise ValidationError("the jsonld file has not been added yet")

    # get latest version of file and check that is different
    j = FacetFiles.objects.filter(facet_lookup_id=m.id).latest('updated')
    jsonld = json.dumps(jsonld, separators=(',', ':'))
    tmp1 = re.sub(r'"generatedAt":".*?"', '"generatedAt": ""', jsonld)
    tmp2 = re.sub(r'"generatedAt":".*?"', '"generatedAt": ""', j.file)
    if tmp1 == tmp2:
        return False

    # save json file
    f = FacetFiles()
    f.facet_lookup_id = m.id
    f.file = jsonld
    f.type = "raw"
    f.version = m.currentversion
    f.save()

    if m.id and f.id:
        return True
    else:
        return False


# ----- Validation -----
def json_validator(json_file):
    """
    Validate a SciData JSON-LD file
    :param json_file: jsonld file to be validated
    :return: boolean
    """
    json_file_content = json.load(json_file)
    keys_a = []
    keys_b = []
    isscidata = True
    if not str(json_file).endswith('.jsonld'):
        isscidata = False
    if not get_graphuid(json_file):
        isscidata = False
    for k, v in json_file_content.items():
        keys_a.append(k)
        if k == '@graph':
            for y, z in v.items():
                keys_b.append(y)
    for y in ['@context', '@id', '@graph']:
        if y not in keys_a:
            isscidata = False
    for y in ['scidata', 'uid', 'sourcecode', 'datasetname']:
        if y not in keys_b:
            isscidata = False
    if not isscidata:
        raise ValidationError("Not Valid SciData JSON-LD")

def get_graphuid(json_file):
    try:
        json_file.seek(0)
        json_file_content = json.load(json_file)
        guid = json_file_content['@graph']['uid']
        return guid
    except:
        return False