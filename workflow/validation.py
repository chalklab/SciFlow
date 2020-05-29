# from .ingestion import *
# from .logwriter import*
import json
# import jsonschema
# from jsonschema import validate
import os

validity = {}
errorlog = {}

#all-in-one validation function. Includes every check that we would want to do on a file.
def validate(path, type):
    #runs a check to make sure the file is in proper scidata format
    validatescidata(path)
    if validatescidata(path) is True:
        isscidata = True
    else:
        isscidata = False
        errorlog.update({"a": "Invalid Scidata Format!"})
    validity.update({"isscidata":isscidata})

    #Specialized checks for each dataset type
    if type == "herg":
        hergcheck(path)
    if type == "cif":
        cifcheck(path)

    #Validity Check
    i = 0
    for value in validity.values():
        if value is False:
            i += 1

    if i == 0:
        return True
    else:
        return False





def validatescidata(path):
    """ validation script """
    try:
        with open(path) as json_file:
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
    except Exception as ex:
        return False



#Specialized checks for each dataset type
def hergcheck(path):
    """ check that this is a herg file"""
    searchfile = open(path)
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
        errorlog.update({"b": "No instance of CHEMBL240 found!"})

    if b > 0:
        author = True
    else:
        author = False
        errorlog.update({"c": "Incorrect Author! (needs to be written by Fray MJ)"})

    validity.update({"isherg": isherg, "author": author})
    searchfile.close()


def cifcheck(path):
    """ check that this is a CIF file"""
    searchfile = open(path)
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
