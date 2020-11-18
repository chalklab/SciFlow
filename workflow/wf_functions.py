"""workflow functions"""
import ast
from slacker import Slacker
from requests.sessions import Session
from .gdb_functions import *
from datafiles.df_functions import *
from substances.sub_functions import *
import json
import time
from datafiles.models import *


# ----- Ingestion -----
def ingest(upload, user):
    """ ingest SciData JSON-LD file """
    if str(upload).endswith('.jsonld'):
        upload.seek(0)
        text = upload.read()
        file = json.loads(text)

        # TODO: Extra validation steps here
        adddatafile(file, user)
        jl, jf = updatedatafile(file)
        aid = loginit(jl, jf)
        addentry(aid, "UID", JsonLookup.objects.get(id=jl).uniqueid)


        sections = {}
        types = ['compound']  # this would be expanded as we get me code written for other unique types...
        for systype in types:
            found = getfacet(file, systype)
            if found:
                sections.update({systype: found[systype]})


        if sections:
            addentry(aid, "SECTIONS", sections)
            # TODO: Normalization
            # if normalize(file) is True:  # normalization.py
        else:
            addentry(aid, "ERROR", "No sections found!")

        # TODO confirm normalization


# ----- Normalization -----

normcheck = {}

# previously used the variables path and loginfo. File has replaced path, and aid is the new loginfo
def normalize(file, sections, aid):
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
        for k, v in file.items():
            if k == '@graph':
                for a in v['scidata']['system']['facets']:
                    for b, c in a.items():
                        if b == '@type' and c.startswith('sci:' + systype):
                            output.update({systype: a})
        if output:
            return output
        else:
            return False
    except FileNotFoundError:
        pass


# ----- Logwriter -----

with Session() as session:
    slack = Slacker('xoxb-4596507645-1171034330099-eP4swGipytYQHLnomPvBoOPO', session=session)
    # slack.chat.post_message('#workflow-updates', "Filename: " + loginfo["logname"].split("-")[1])


def loginit(json_lookup_id, json_file_id):
    a = JsonActlog.objects.create(json_lookup_id=json_lookup_id, json_file_id=json_file_id, activitylog='{"ERROR":"[]"}')
    a.save()
    return a.id


def addentry(actlogid, ekey, evalue):
    a = JsonActlog.objects.get(id=actlogid)
    s_dict = a.activitylog
    d_dict = ast.literal_eval(s_dict)
    if ekey is not "ERROR":
        d_dict.update({ekey:evalue})
    else:
        elist = d_dict["ERROR"]
        elist.append(evalue)

    a.activitylog = d_dict
    a.save()
