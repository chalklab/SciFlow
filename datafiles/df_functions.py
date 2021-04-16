""" functions file for the datafiles app"""
from django.core.exceptions import ValidationError
from workflow.log_functions import *
import json
import re


# Variant that only adds the lookup info so errors can be stored.
# Upon validation addfile is run and the file is actually added.
def adddatafile(dfile, uploading_user=None):
    """
    Add data jsonld metadata to the database
    :param dfile: data jsonld file
    :param uploading_user: user id
    :return: boolean
    """

    # save metadata
    if JsonLookup.objects.filter(uniqueid=dfile['@graph']['uid']):
        m = JsonLookup.objects.get(uniqueid=dfile['@graph']['uid'])
    else:
        m = JsonLookup()
        uid = dfile['@graph']['uid']
        parts = None
        if ':' in uid:
            parts = uid.split(":")
        elif '_' in uid:
            parts = uid.split("_")

        # get dataset_id
        dset = Datasets.objects.get(
            sourcecode__exact=parts[0], datasetname=parts[1])

        if dset.id:
            m.dataset_id = dset.id
        else:
            m.dataset_id = 0
        m.uniqueid = uid
        m.title = dfile['@graph']['title']
        m.type = parts[1]
        m.currentversion = 0
        if uploading_user is None:
            m.auth_user_id = 1
        else:
            m.auth_user_id = uploading_user.id
        m.save()

    if m.id:
        # update the graphname in the file and DB
        dataid = str(m.id).rjust(8, '0')  # creates id with the right length
        dfile['@id'] = "https://scidata.unf.edu/data/" + dataid
        m.graphname = dfile['@id']
        m.save()
        return m.id
    else:
        return False


def updatedatafile(dfile=None, form='raw'):
    """
    Add a data jsonld file to the database
    :param dfile: data jsonld file information
    :param form: what type of file format this is (raw/normalized)
    :return: boolean
    """

    # check for valid file
    if dfile is None or dfile == "":
        errorlog("DF_E01: No data file to work with!")

    # get metadata
    m = JsonLookup.objects.get(uniqueid=dfile['@graph']['uid'])
    if not m:
        errorlog("DF_E02: The jsonld data file has not yet been added")
    else:
        actlog("DF_A01: Found file in json_lookup (id: " + str(m.id) + ")")

    # get latest version of file (if it exists) and check that is different
    dstr = json.dumps(dfile, separators=(',', ':'))
    f = JsonFiles.objects.filter(json_lookup=m.id)
    if f:  # if there is a version in json_files then check against current
        actlog("DF_A04: Found data file in json_files")
        latest = f.latest('updated')
        genatrpl = '"generatedAt": ""'
        tmp1 = re.sub(r'"generatedAt":"[0-9:\s\-]*"', genatrpl, dstr)
        tmp2 = re.sub(r'"generatedAt":"[0-9:\s\-]*"', genatrpl, latest.file)
        if tmp1 == tmp2:  # checking files are same except for creation date
            actlog("DF_05: Datafile is the same as last version - not adding")
            return {"mid": m.id, "fid": latest.id}

    actlog("DF_A02: Data file is different than last version - adding " + str(m.currentversion + 1) + "...")

    # update file version
    m.currentversion += 1
    m.save()

    # save json file
    f = JsonFiles()
    f.json_lookup_id = m.id
    f.file = dstr
    f.type = form
    f.version = m.currentversion
    f.save()

    # return
    if m.id and f.id:
        return {"mid": m.id, "fid": f.id}
    else:
        return False


def addfacetfile(ffile=None, uploading_user=None):
    """
    Add a facet jsonld file to the database
    :param ffile: data jsonld file information
    :param uploading_user: user id
    :return: boolean
    """

    # check for valid file
    if ffile is None or ffile == "":
        return False

    # save metadata
    if FacetLookup.objects.filter(uniqueid=ffile['@graph']['uid']):
        m = FacetLookup.objects.get(uniqueid=ffile['@graph']['uid'])
    else:
        m = FacetLookup()

        uid = ffile['@graph']['uid']
        parts = None
        if ':' in uid:
            parts = uid.split(":")
        elif '_' in uid:
            parts = uid.split("_")

        # get dataset_id
        dset = Datasets.objects.get(
            sourcecode__exact=parts[0], datasetname=parts[1])

        if dset.id:
            m.dataset_id = dset.id
        else:
            m.dataset_id = 0
        m.uniqueid = uid
        m.title = ffile['@graph']['title']
        m.type = parts[1]
        m.graphname = ffile['@id']
        m.currentversion = 0  # adding the file to facet_files will increment
        if uploading_user is None:
            m.auth_user_id = 1
        else:
            m.auth_user_id = uploading_user.id
        m.save()

    if m.id:
        # update the graphname in the file and DB
        gname = str(ffile['@id'])
        facetid = str(m.id).rjust(8, '0')  # creates id with the right length
        ffile['@id'] = gname.replace("<facetid>", facetid)
        m.graphname = ffile['@id']
        return m.id
    else:
        return False


def updatefacetfile(ffile=None):
    """
    Add a facet jsonld file to the database
    :param ffile: data jsonld file information
    :return: boolean
    """

    # check for valid file
    if ffile is None or ffile == "":
        raise ValidationError("No facet file provided")

    # get metadata
    m = FacetLookup.objects.get(uniqueid=ffile['@graph']['uid'])
    if not m:
        raise ValidationError("The facet file has not yet been added")

    # get latest version of file (if it exists) and check that is different
    ffile = json.dumps(ffile, separators=(',', ':'))
    j = FacetFiles.objects.filter(facet_lookup_id=m.id)
    if j:  # if there is a version in facet_files then check against current
        latest = j.latest('updated')
        genatrpl = '"generatedAt": ""'
        tmp1 = re.sub(r'"generatedAt":".*?"', genatrpl, ffile)
        tmp2 = re.sub(r'"generatedAt":".*?"', genatrpl, latest.file)
        if tmp1 == tmp2:  # checking files are same except for creation date
            return True

    # update file version
    m.currentversion += 1
    m.save()

    # save json file
    f = FacetFiles()
    f.facet_lookup_id = m.id
    f.file = ffile
    f.type = "raw"
    f.version = m.currentversion
    f.save()

    # return
    if m.id and f.id:
        return m.id, f.id
    else:
        return False


def infacetfiles(facetid):
    """
    find out if a facet with this id has been saved to the facet_files table
    """
    found = FacetLookup.objects.all().values_list(
        'graphdb', flat=True).get(id=facetid)
    if found:
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
    """
    try:
        jsonld.to_rdf(json_file_content, {"processingMode": "json-ld-1.0"})
    except ValidationError:
        isscidata = False
    """
    if not str(json_file).endswith('.jsonld'):
        isscidata = False
    if not get_graphuid(json_file):
        isscidata = False
    for k, v in json_file_content.items():
        keys_a.append(k)
        if k == '@graph':
            for y, z in v.items():
                keys_b.append(y)
    for y in ['@context', '@id', 'generatedAt', '@graph']:
        if y not in keys_a:
            isscidata = False
    for y in ['scidata', 'uid']:
        if y not in keys_b:
            isscidata = False
    if not isscidata:
        raise ValidationError("Not a valid SciData JSON-LD")


def get_graphuid(json_file):
    """ get uid from json file"""
    try:
        json_file.seek(0)
        json_file_content = json.load(json_file)
        guid = json_file_content['@graph']['uid']
        return guid
    except LookupError:
        return False
