#Compound Conveyor
compounds = {}

def findcomp(path):
    searchfile = open('C:' + path,"r")
    for line in searchfile:
        if "inchi_key" in line:
            loc = line
            pos = loc.find("standard_inchi_key")
            inchi = loc[pos+22:pos+49]
            compounds.update({inchi:inchi})
    searchfile.close()


def findprofile(compounds):


    print("search for existing profile")

def getprofile():
    print("get existing profile")

def makeprofile():
    print("make a new profile")
