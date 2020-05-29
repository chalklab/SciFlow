import os
import json
#Compound Conveyor
compounds = {}

sddir = '/Users/n01448636/Documents/PycharmProjects/chembl_django/scidata/JSON_dumps/'
def findcomp(sdfile):
    output = {}
    if sdfile.endswith('.jsonld'):
        x = json.loads(open(sddir+sdfile).read())
        for k,v in json.loads(open(sddir+sdfile).read()).items():
            if k == '@graph':
                for a in x['@graph']['scidata']['system']['facets']:
                    for b,c in a.items():
                        if b == '@id' and c.startswith('target'):
                            output.update({'targetchembl':(a['chembl_id'])})
                        if b == '@id' and c.startswith('compound'):
                            output.update({'inchi':(a['identifiers']['standard_inchi'])})
    if output:
        return output


for sdfile in os.listdir(sddir):
    print(findcomp(sdfile))


def findprofile(compounds):
    print("search for existing profile in the database")
    inchi = compounds.value()
    if "exists" == True:
        getprofile()
    else:
        makeprofile()
    addprofile()

def getprofile():
    print("get existing profile")

def makeprofile():
    print("make a new profile")

def addprofile():
    print("add profile to file being ingested")
