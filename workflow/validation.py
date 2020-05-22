from .scidataschema import schema
from .ingestion import*
import json
import jsonschema
from jsonschema import validate

hergvalidity = {}
hergerrorlog = {}
cifvalidity = {}
ciferrorlog = {}


#valdity check: if file is valid, i = 1 at the end. It is invalid, it should equal 0
def hergcheck(path):
    searchfile = open('C:' + path,"r")
    #checking if it is actually herg
    a = 0
    b = 0
    for line in searchfile:
        #checking if it is actually herg
        if "\"CHEMBL240\"" in line:
            a += 1
        #verifying author (an example used for testing purposes)
        if "Fray MJ" in line:
            b += 1
    if a > 0:
        isherg = True
    else:
        isherg = False
        hergerrorlog.update({"a":"No instance of CHEMBL240 found!"})

    if b > 0:
        author = True
    else:
        author = False
        hergerrorlog.update({"b":"Incorrect Author! (needs to be written by Fray MJ)"})

    hergvalidity.update({"isherg":isherg, "author":author})
    searchfile.close()


def cifcheck(path):
    searchfile = open('C:' + path,"r")
    i = 0
    for line in searchfile:
        if "potato" in line:
            i += 1
    if i > 0:
        valid = True
    else:
        valid = False
    return valid
    searchfile.close()





def validateJson(jsonData):
    try:
        validate(instance=jsonData, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True
