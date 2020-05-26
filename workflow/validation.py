""" SciData validation functions"""
# from .ingestion import *
from django.conf import settings
import os
import json
# import jsonschema
# from jsonschema import validate

hergvalidity = {}
hergerrorlog = {}
cifvalidity = {}
ciferrorlog = {}


# valdity check: if file is valid, i = 1 at the end. It is invalid, it should equal 0
def hergcheck(path):
    """ check that this is a herg file"""
    searchfile = open('C:' + path)
    # checking if it is actually herg
    a = 0
    b = 0
    for line in searchfile:
        # checking if it is actually herg
        if "\"CHEMBL240\"" in line:
            a += 1
        # verifying author (an example used for testing purposes)
        if "Fray MJ" in line:
            b += 1
    if a > 0:
        isherg = True
    else:
        isherg = False
        hergerrorlog.update({"a": "No instance of CHEMBL240 found!"})

    if b > 0:
        author = True
    else:
        author = False
        hergerrorlog.update({"b": "Incorrect Author! (needs to be written by Fray MJ)"})

    hergvalidity.update({"isherg": isherg, "author": author})
    searchfile.close()


def cifcheck(path):
    """ check that this is a CIF file"""
    searchfile = open('C:' + path)
    i = 0
    for line in searchfile:
        if "potato" in line:
            i += 1
    if i > 0:
        valid = True
    else:
        valid = False
    searchfile.close()
    return valid


def validatescidata(sdfile):
    """ validation script """
    with open(sdfile) as json_file:
        data = json.load(json_file)
        keys_a = []
        keys_b = []
        for k, v in data.items():
            keys_a.append(k)
            if k == '@graph':
                for y, z in v.items():
                    keys_b.append(y)
        for y in ['@context', '@id', '@graph']:
            if y not in keys_a:
                return False
        for y in ['scidata']:
            if y not in keys_b:
                return False
        return True


def validatefiles():
    """look in the json folder and validate any files present"""
    jpath = settings.BASE_DIR + '/json/'
    for dirpath, dirs, files in os.walk(jpath):
        if len(files) > 0:
            for filename in files:
                valid = validatescidata(jpath + filename)
                print(filename + ": " + str(valid))
        else:
            return "No files to validate"
    return "Files validated"


print(validatefiles())
