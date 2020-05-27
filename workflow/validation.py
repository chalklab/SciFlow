# from .ingestion import *
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


#Validate scidata jsonld format
x = '/Users/n01448636/Documents/PycharmProjects/chembl_django/scidata/JSON_dumps/51366_CHEMBL1086273.jsonld'

def validateSciData(input):
    with open(input) as json_file:
        data = json.load(json_file)
        keycheckA = ['@context', '@id', '@graph']
        keycheckB = ['scidata']
        keysA = []
        keysB = []
        for k,v in data.items():
            keysA.append(k)
            if k == '@graph':
                for y,z in v.items():
                    keysB.append(y)
                for x in keycheckB:
                    if x not in keysB:
                        return False
        for x in keycheckA:
            if x not in keysA:
                return False
        return True

print(validateSciData(x))
