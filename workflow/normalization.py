""" functions to normalize SciData JSON-LD files """
from .ingestion import *
from .graphdb import *
from .logwriter import logwrite
from sciflow.settings import gdrivesds
from substances.functions import *
import json
import time

normcheck = {}


def normalize(path, sections, loginfo):
    """ normalize a file by replacing out unique things (e.g. compounds, organisms, targets, etc.) """

    # use the metadata from a section to find the compound in the database
    section = ""
    found = False
    for section, meta in sections.items():
        if section == "compound":
            found = findsub(section, meta)

    # either add a new compound or find out of the compound is in the graph database
    if found:
        if ingraph(found):  # find if compound is already in the graph (uses graphdb field in substances)
            # Ok now update to the JSON-LD to point to the graph of the substance
            # normalize data file
            print("in graph")
        else:
            # not in graph (but in DB) so create sd file and add to graphDB
            key = getinchikey(found)
            jldfilename = createsubjld(key)
            if jldfilename:
                # file path is different on the sds server therefore we need the gdrivesds path
                time.sleep(3)
                added = addgraph(gdrivesds + jldfilename, 'local')
                if added:
                    # update substance entry in table
                    gname = getgraphname(key)
                    # normalize data file
                    print(gname)

    else:
        # compound not found in DB
        print("not found in DB")
    print(section)

    # needed?
    # logwrite("act", loginfo, "System:")
    # try:
    #     logwrite("act", loginfo, "\t- Compound: " + str(section))
    #     logwrite("act", loginfo, "\t- Target: " + str(section)+"\n")
    # except FileNotFoundError:
    #     pass
    #
    # normalizationcheck(path, loginfo)
    # i = 0
    # for value in normcheck.values():
    #     if value is False:
    #         i += 1
    #
    # if i == 0:
    #     return True
    # else:
    #     return False


def findsub(section, meta):
    """ take an array of metadata from a compounds section and find out if it is the database """
    terms = searchterms[section]
    for key, value in meta.items():
        for term in terms:
            if term in key:
                subid = getsubid(value)
                if subid:
                    return subid
    return False


def getfacet(path, systype):
    """ gets the compound and target within the scidata file """
    output = {}
    try:
        x = json.loads(open(path).read())
        for k, v in x.items():
            if k == '@graph':
                for a in x['@graph']['scidata']['system']['facets']:
                    for b, c in a.items():
                        if b == '@type' and c.startswith('sdo:' + systype):
                            output.update({systype: a})
        if bool(output):
            return output
        else:
            return False
    except FileNotFoundError:
        pass


# move profile definitions to profile.py file

def findprofile(path, compound, loginfo):
    """ searches the database for a profile matching the found inchikey """
    inchi = compound.get("inchi")
    if Identifiers.objects.all().filter(value=inchi).exists() is True:
        getprofile(inchi, loginfo)
    else:
        makeprofile(inchi, loginfo)
    addprofile(inchi, loginfo)


def getprofile(inchi, loginfo):
    """ if the profile is found, this pulls it """
    subid = Identifiers.objects.get(value=inchi).substance_id
    substance = Substances.objects.get(id=subid)
    logwrite("act", loginfo, "Substance Name: " + substance.name)


def makeprofile(inchi, loginfo):
    """ if the profile is not found, this creates it """
    print("no inchi found")


def addprofile(inchi, loginfo):
    """ once the profile has been created or obtained, this integrates it to the main file """
    print("adding...")


def normalizationcheck(path, loginfo):
    """ # checks to make sure the file has been correctly normalized """
    normalized = True
    if normalized is True:
        logwrite("act", loginfo, "Normalization: Valid")
    else:
        logwrite("act", loginfo, "Normalization: Invalid!")
        logwrite("err", loginfo, "- File was not properly normalized!")
