"""workflow functions"""
from workflow.gdb_functions import *
from datafiles.df_functions import *
from substances.sub_functions import *
from datafiles.models import *
from sciflow import gvars
import json


# ----- Ingestion -----
def ingest(upload, user):
    """ ingest SciData JSON-LD file """
    actlog("WF_A01: Ingest initiated")

    if str(upload).endswith('.jsonld'):
        upload.seek(0)
        text = upload.read()
        file = json.loads(text)
        mid = adddatafile(file, user)
        if mid:
            if not updatedatafile(file):
                errorlog("WF_E01: File was not updated (added to json_files)")
        else:
            errorlog("WF_E02: File was not added to json_lookup")

        ids = updatedatafile(file)
        gvars.ingest_data_lookup_id = ids['mid']
        gvars.ingest_data_file_id = ids['fid']
        actlog("WF_A02: UID is "+JsonLookup.objects.get(id=ids['mid']).uniqueid)

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
            actlog("WF_A03: Sections:" + str(sections.keys()))
            if normalize(file, sections, user, ids['mid']) is True:  # normalization.py
                actlog("WF_A04: File normalized!")
                return True
            else:
                errorlog("WF_E03: File was not normalized!")
        else:
            errorlog("WF_E04: No sections found to normalize!")
            return True
    actlog("WF_A05: Ingest completed!")


# ----- Normalization -----
def normalize(dfile, sections, user, jl):
    """
    normalize a file by replacing out unique things (e.g. compounds, organisms, targets, etc.)
    :param dfile - datafile to be normalized (as dict)
    :param sections - sections of the file that need to be normalized
    :param user - user that submitted the file via the form
    :param jl - json_lookup table id
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
                            errorlog("WF_E05: Compound file metadata for substance id "+subid+" not added to facet_lookup")
                        if not updatefacetfile(ffile):
                            errorlog("WF_E06: Compound file id "+ffileid+" was not added to facet_files")
                        # now that facet file has be added link to DB table
                        updatesubstance(subid, 'facet_lookup_id', ffileid)
                        actlog("WF_A06: Created compound facet file id "+ffileid+" and added to DB")
                    if not graphid:
                        # has the jsonld file been saved in the DB but not added to the graph?
                        if addgraph('facet', ffileid):
                            # update ftype table with id
                            sub = Substances.objects.get(id=subid)
                            sub.graphdb = 'https://scidata.unf.edu/facet/' + str(ffileid)
                            sub.save()
                            actlog("WF_A07:Compound file id "+ffileid+" added to GraphDB")
                        else:
                            errorlog("WF_E07: Compound file id "+ffileid+" was not added to GraphDB")

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

                    # add entry into json_facets
                    link = JsonFacets()
                    link.json_lookup_id = jl
                    link.facets_lookup_id = ffileid
                    link.save()
                    actlog("WF_A08: Compound found in DB: ( "+section+", "+entry+", "+ffileid+" )")
                else:
                    errorlog("WF_E08: Compound not found in or added to DB ( "+section+", "+entry+" )")

    # update file in DB
    updated = updatedatafile(dfile, 'normalized')
    if updated:
        atid = dfile['@id']
        parts = atid.split('/')
        if addgraph('data', parts[4]):
            actlog("WF_A09: Normalized version of data file added to Graph DB: "+parts[4])
            return True
        else:
            errorlog("WFE09: Could not save normalized version of data file to Graph DB")
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

# with Session() as session:
# slack = Slacker('xoxb-4596507645-1171034330099-eP4swGipytYQHLnomPvBoOPO', session=session)
# slack.chat.post_message('#workflow-updates', "Filename: " + loginfo["logname"].split("-")[1])
