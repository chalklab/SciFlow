"""workflow functions"""
import ast
from slacker import Slacker
from requests.sessions import Session
from workflow.gdb_functions import *
from datafiles.df_functions import *
from substances.sub_functions import *
from datafiles.models import *
from django.db import *


# ----- Ingestion -----
def ingest(upload, user):
    """ ingest SciData JSON-LD file """
    if str(upload).endswith('.jsonld'):
        upload.seek(0)
        text = upload.read()
        file = json.loads(text)
        if adddatafile(file, user):
            if not updatedatafile(file):
                raise DatabaseError("Could not save data file to JsonFiles")
        else:
            raise DatabaseError("Could not save data file metadata to JsonLookup")
        # identify parts of the aspects and facets section of the jld file to normalize
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
            if normalize(file, sections, user) is True:  # normalization.py
                return True
            else:
                raise ValueError("Data file could not be normalized")  # convert to act/err log entries
        else:
            return True


# old
# def finalize(path, outputdir, errordir, loginfo):
#     """ finalizes the ingestion, determining whether it was successful, and moving the file """
#     # Detemines whether the ingestion was successful or not
#     logname = loginfo["errlogdir"]+'/'+loginfo["logname"]+'.txt'
#     i = 0
#     try:
#         # if the file is found then it has not been successfully ingested
#         file = open(logname)
#         file.close()
#         logwrite("act", loginfo, "Status: Failed!")
#         i += 1
#     except FileNotFoundError:
#         # if the file is not present then it has been successfully ingested
#         logwrite("act", loginfo, "Status: Success!")
#     logprint("act", loginfo)
#
#     # move the file
#     # if i == 0:
#     #     shutil.move(path, outputdir)
#     # else:
#     #     shutil.move(path, errordir)


# ----- Normalization -----
def normalize(dfile, sections, user):
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
                            raise ValidationError("Compound file metadata not added to facet_lookup")
                        if not updatefacetfile(ffile):
                            raise ValidationError("Compound file not added to facet_files")
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
                            raise DatabaseError("Compound not added to GraphDB")

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
                    raise DatabaseError("Compound not found in or added to DB")

    # update file in DB
    updated = updatedatafile(dfile, 'normalized')
    if updated:
        atid = dfile['@id']
        parts = atid.split('/')
        if addgraph('data', parts[4]):
            return True
        else:
            raise DatabaseError("Could not save normlized version of data file")
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
#
#
# # old
# def errloginit(loginfo):
#     """ creates an error log, triggered by the detection of an error """
#     errlog = open(loginfo["errlogdir"]+'/'+loginfo["logname"]+'.txt', "w+")
#     errlog.write("The following error(s) were encountered while ingesting this file: \n\n")
#     errlog.close()
#
#
# # old
# def actloginit(loginfo):
#     """ creates an activity log, triggered by the detection of an activity """
#     actlog = open(loginfo["actlogdir"]+'/'+loginfo["logname"]+'.txt', "w+")
#     actlog.write("-----------Activity Log-----------\n")
#     actlog.write("Filename: " + loginfo["logname"].split("-")[1] + "\n")
#     actlog.close()
#     # slack.chat.post_message('#workflow-updates', "Filename: " + loginfo["logname"].split("-")[1])
#
#
# # old
# def logwrite(logtype, loginfo, content):
#     """ writes to a log depending on the type. Whatever is placed into the input arguement will be added to the log. """
#     # if a log file does not exist, it will be created
#     # To print to a file, change the printtype arg in actloginit to "f" (located in ingestion.py)
#     try:
#         logname = open(loginfo[logtype+"logdir"]+'/'+loginfo["logname"]+'.txt', "a+")
#         logname.write(content + '\n')
#         logname.close()
#     except FileNotFoundError as fnf_error:
#         print(fnf_error)
#         pass
#
#
# # old
# def logprint(logtype, loginfo):
#     """ prints a log file to the screen """
#     try:
#         with open(loginfo[logtype+"logdir"]+'/'+loginfo["logname"]+'.txt') as file:
#             log = file.read()
#             print(log)
#             # actcontent = log  # needed?
#             file.close()
#     except FileNotFoundError as fnf_error:
#         print(fnf_error)
#         pass
#         # actcontent = "No " + logtype + " log was found for this file!"  # needed?
#
#     # slack.chat.post_message('#workflow-updates', actcontent)
#     # slack.chat.post_message('#workflow-updates', errcontent)
#     # slack.chat.post_message('#workflow-updates', "-------------End Log-------------")


def adderror(errorid, errorcode):
    """add error function"""

    # TODO I think one entry in table per error
    # also we should add more details like variables and code line (new fields)

    e = JsonErrors.objects.get(id=errorid)
    s_list = e.errorcode
    l_list = ast.literal_eval(s_list)
    l_list.append(str(errorcode))
    e.errorcode = l_list
    e.save()


def geterror(eid):
    """get error function"""
    e = JsonErrors.objects.get(id=eid)
    ec = e.errorcode
    ecl = ast.literal_eval(ec)
    print(type(ecl))
    print(ecl)
    reports = []
    for error in ecl:
        print(error)
        x = int(str(error)[0])
        y = int(str(error)[1])

        ingesterrors = ["The first ingestion error!",
                        "The second ingestion error!"]

        verificationerrors = ["The first verification error!",
                              "The second verification error!"]

        normalizationerrors = ["The first normalization error!",
                               "The second normalization error!"]

        uploaderrors = ["The first upload error!",
                        "The second upload error!"]

        errorcodes = [ingesterrors[y],
                      verificationerrors[y],
                      normalizationerrors[y],
                      uploaderrors[y]]

        print(errorcodes[x])
        report = errorcodes[x]
        reports.append(report)
    return reports


def addentry(actlogid, ekey, evalue):
    """what doed this do?"""
    a = JsonActlog.objects.get(id=actlogid)
    s_dict = a.activitylog
    d_dict = ast.literal_eval(s_dict)
    if ekey != "ERROR":
        d_dict.update({ekey: evalue})
    else:
        elist = d_dict["ERROR"]
        elist.append(evalue)

    a.activitylog = d_dict
    a.save()
