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
        adddatafile(file, user)
        """
        if adddatafile(file, user):
            if not updatedatafile(file):
                raise DatabaseError("Could not save data file to JsonFiles")
        else:
            raise DatabaseError("Could not save data file metadata to JsonLookup")
        """
        jl, jf = updatedatafile(file)
        print(jl,jf)
        actlog(jl, jf, "UID: "+JsonLookup.objects.get(id=jl).uniqueid)


        sections = {}
        mettypes = ['procedure']  # this would be expanded as we get me code written for other unique types...
        systypes = ['compound']  # this would be expanded as we get me code written for other unique types...

        for mettype in mettypes:
            found = getaspect(file, mettype)
            if found:
                sections.update({mettype: found})

        for systype in systypes:
            found = getfacet(file, systype)
            if found:
                sections.update({systype: found})


        if sections:
            actlog(jl, jf, "SECTIONS: "+ sections)
            if normalize(file, sections, user, jl, jf) is True:  # normalization.py
                errorlog(jl, jf, "WF_51: This is just a test.")
                return True
            else:
                errorlog(jl, jf, "WF_54: File could not be normalized!")
        else:
            errorlog(jl, jf, "WF_56: No sections found!")
            return True


# ----- Normalization -----
def normalize(dfile, sections, user, jl, jf):
    """
    normalize a file by replacing out unique things (e.g. compounds, organisms, targets, etc.)
    :param dfile - datafile to be normalized (as dict)
    :param sections - sections of the file that need to be normalized
    :param user - user that submitted the file via the form
    """

    # use the metadata from a section to find the compound in the database
    for section, entries in sections.items():
        if section == "compound":
            for entry in entries:
                subid = getaddsub(section, entry)

                if subid:
                    key = getinchikey(subid)
                    # substance is already in MySQL
                    ffileid = subinfiles(subid)
                    graphid = subingraph(subid)
                    if not ffileid:
                        # not in graph or in facet_lookup (but in DB) so create sd file and add to both
                        ffile = createsubjld(key)
                        # add facet file to DB
                        ffileid = addfacetfile(ffile, user)
                        if not ffileid:
                            errorlog(jl, jf, "WF_86: Compound file metadata not added to facet_lookup")
                        if not updatefacetfile(ffile):
                            errorlog(jl, jf, "WF_88: Compound file not added to facet_files")
                        # now that facet file has be added link to DB table
                        updatesubstance(subid, 'facet_lookup_id', ffileid)
                    if not graphid:
                        # has the jsonld file been save in the DB but not added to the graph?
                        if addgraph('facet', ffileid):
                            # update ftype table with id
                            sub = Substances.objects.get(id=subid)
                            sub.graphdb = 'https://scidata.unf.edu/facet/' + str(ffileid)
                            sub.save()
                        else:
                            errorlog(jl, jf, "WF_99: Compound not added to GraphDB")

                    # load facet file to extract @id for compound
                    fobjt = FacetFiles.objects.get(facet_lookup_id=ffileid)
                    ffile = json.loads(fobjt.file)
                    normid = ffile['@graph']['@id'] + 'compound/1/'

                    # substance already in graph so update facet entry with link to facet in graph
                    facets = dfile['@graph']['scidata']['system']['facets']
                    facetid = entry[section]['@id']
                    for fidx, facet in enumerate(facets):
                        if facet['@id'] == facetid:
                            # update datafile facet entry
                            finfo = {"@id": normid, "@type": "sci:" + section}
                            dfile['@graph']['scidata']['system']['facets'][fidx] = finfo
                            break
                else:
                    errorlog(jl, jf, "WF_116: Compound not found in or added to DB")

    # update file in DB
    updated = updatedatafile(dfile, 'normalized')
    if updated:
        atid = dfile['@id']
        parts = atid.split('/')
        if addgraph('data', parts[4]):
            return True
        else:
            errorlog(jl, jf, "WF_126: Could not save normlized version of data file")
    return True


def getfacet(file, systype):
    """gets the facet data within the scidata system section of a file"""
    output = []
    sd = file['@graph']['scidata']  # can rely on this based on validation
    if 'system' in sd.keys():
        for a in sd['system']['facets']:
            if a['@type'] == 'sdo:' + systype:
                output.append({systype: a})
        if output:
            return output
        else:
            return False
    else:
        return False


def getaspect(file, mettype):
    """gets the aspect data within the scidata methodology section of a file"""
    output = []
    sd = file['@graph']['scidata']  # can rely on this based on validation
    if 'methodology' in sd.keys():
        for a in sd['methodology']['aspects']:
            if a['@type'] == 'sdo:' + mettype:
                output.append({mettype: a})
        if output:
            return output
        else:
            return False
    else:
        return False


# ----- Logwriter -----

with Session() as session:
    slack = Slacker('xoxb-4596507645-1171034330099-eP4swGipytYQHLnomPvBoOPO', session=session)
    # slack.chat.post_message('#workflow-updates', "Filename: " + loginfo["logname"].split("-")[1])


def actlog(json_lookup_id, json_file_id, content):
    a = JsonActlog.objects.create(json_lookup_id=json_lookup_id, json_file_id=json_file_id, activitylog=content)
    a.save()

def errorlog(json_lookup_id, json_file_id, content):
    e = JsonErrors.objects.create(json_lookup_id=json_lookup_id, json_file_id=json_file_id, errorcode=content)
    e.save()

