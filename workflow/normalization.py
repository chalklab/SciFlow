from .ingestion import*
import os
import json

normcheck = {}
compound = {}
target = {}

def normalize(path):
    getsystem(path)
    findprofile(path, compound)
    normalizationcheck(path)

    i = 0
    for value in normcheck.values():
        if value is False:
            i += 1

    if i == 0:
        return True
    else:
        return False


#gets the compound and target within the scidata file
#sddir = '/Users/n01448636/Documents/PycharmProjects/chembl_django/scidata/JSON_dumps/'
def getsystem(path):
    x = json.loads(open(path).read())
    for k,v in x.items():
        if k == '@graph':
            for a in x['@graph']['scidata']['system']['facets']:
                for b,c in a.items():
                    if b == '@id' and c.startswith('target'):
                        target.update({'targetchembl':(a['chembl_id'])})
                    if b == '@id' and c.startswith('compound'):
                        compound.update({'inchi':(a['identifiers']['standard_inchi'])})


#for sdfile in os.listdir(sddir):
    #print(findcomp(sdfile))


#searches the database for a profile matching the found inchi key
def findprofile(path, compound):
    inchi = compound.get("inchi")
    if "exists" == True:
        getprofile(inchi)
    else:
        makeprofile(inchi)
    addprofile(inchi)

#if the profile is found, this pulls it
def getprofile(inchi):
    print("get existing profile")

#if the profile is not found, this creates it
def makeprofile(inchi):
    print("make a new profile")

#once the profile has been created or obtained, this integrates it to the main file
def addprofile(inchi):
    print("add profile to file being ingested")


#checks to make sure the file has been correctly normalized
def normalizationcheck(path):
    normalized = True
    if normalized == True:
        isnormalized = True
    else:
        isnormalized = False
        errorlog.update({"e":"File was not properly normalized!"})
    validity.update({"isnormalized": isnormalized})
