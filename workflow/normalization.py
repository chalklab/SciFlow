""" functions to normalize SciData JSON-LD files """
from .ingestion import *
from .graphdb import *
from .logwriter import logwrite
from sciflow.settings import gdrivesds
from substances.functions import *
from substances.models import Substances
from substances.models import Identifiers
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


def getfacet(file, systype):
    """ gets the compound and target within the scidata file """
    output = {}
    try:
        # x = json.loads(open(path).read())
        x = json.loads(file)
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


url = "https://stuchalk.github.io/scidata/examples/cif/1000118.jsonld"
cifs = '/Users/n01448636/Documents/Google Drive/CIF_scidata_jsonlds/'
directory = os.fsencode(cifs)


def graph_link_a(file):
    jsonfile = json.load(file)
    try:
        for group in jsonfile['@graph']['scidata']['system']['facets']:
            if group['@id'].startswith(('compound/', 'crystal/')):
                newgroup = graph_link_b(group)
                group.clear()
                group.update(newgroup)
    except:
        pass
    return jsonfile


def graph_link_b(group):
    # group = {'@id': 'compound/1/', '@type': 'cif:compound', '_chemical_formula_moiety': 'C12 H8', '_chemical_name_systematic': 'Q194207'}
    tablematch = {"compound": [Identifiers, Substances, 'substance_id'], "crystal": [Identifiers, Substances, 'substance_id']}
    identifier = {'@id': group['@id']}
    category = group['@id'].split('/')[0]
    for line in list(tablematch[category][0].objects.values()):
        try:
            if any(line['value'] in q for q in group.values()):
                if line['value'] in group.values():
                    group = identifier
                    group.update(tablematch[category][1].objects.values('graphdb').get(id=line[tablematch[category][2]]))
                    # Post(y)
            else:
                # compound/crystal/etc not found in database. Needs to be added first in order to link
                # then GraphLinkB(group)
                pass
        except:
            print('exception')
    return group


def normalizationcheck(path, loginfo):
    """ # checks to make sure the file has been correctly normalized """
    normalized = True
    if normalized is True:
        logwrite("act", loginfo, "Normalization: Valid")
    else:
        logwrite("act", loginfo, "Normalization: Invalid!")
        logwrite("err", loginfo, "- File was not properly normalized!")
