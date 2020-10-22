import ast
from slacker import Slacker
from requests.sessions import Session
from .gdb_functions import *
from substances.sub_functions import *
import json
import time
from datafiles.models import *

# ----- Ingestion -----

def ingest(file, user):
    """ ingest SciData JSON-LD file """
    if str(file).endswith('.jsonld'):
        # initfile(file, user)
        # addfile(file, user)
        sections = {}
        types = ['compound']  # this would be expanded as we get me code written for other unique types...
        for systype in types:
            found = getfacet(file, systype)
            if found:
                sections.update({systype: found[systype]})

        if sections:
            print(sections)
            # if normalize(file) is True:  # normalization.py
            # addfile(file, user)
            #     print("finished!")
            #     #finalize(path, outputdir, errordir, loginfo)
            # else:
            #     print("file could not be normalized")  # convert to act/err log entries
        else:
            print("no system sections found!")  # convert to act/err log entries

        # TODO confirm normalization


def finalize(path, outputdir, errordir, loginfo):
    """ finalizes the ingestion, determining whether it was successful, and moving the file """
    # Detemines whether the ingestion was successful or not
    logname = loginfo["errlogdir"]+'/'+loginfo["logname"]+'.txt'
    i = 0
    try:
        # if the file is found then it has not been successfully ingested
        file = open(logname)
        file.close()
        logwrite("act", loginfo, "Status: Failed!")
        i += 1
    except FileNotFoundError:
        # if the file is not present then it has been successfully ingested
        logwrite("act", loginfo, "Status: Success!")
    logprint("act", loginfo)

    # move the file
    if i == 0:
        shutil.move(path, outputdir)
    else:
        shutil.move(path, errordir)


# ----- Normalization -----

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
        for x in file.chunks():
            y = json.loads(x)
            for k,v in y.items():
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

# old
def errloginit(loginfo):
    """ creates an error log, triggered by the detection of an error """
    errlog = open(loginfo["errlogdir"]+'/'+loginfo["logname"]+'.txt', "w+")
    errlog.write("The following error(s) were encountered while ingesting this file: \n\n")
    errlog.close()

# old
def actloginit(loginfo):
    """ creates an activity log, triggered by the detection of an activity """
    actlog = open(loginfo["actlogdir"]+'/'+loginfo["logname"]+'.txt', "w+")
    actlog.write("-----------Activity Log-----------\n")
    actlog.write("Filename: " + loginfo["logname"].split("-")[1] + "\n")
    actlog.close()
    # slack.chat.post_message('#workflow-updates', "Filename: " + loginfo["logname"].split("-")[1])

# old
def logwrite(logtype, loginfo, content):
    """ writes to a log depending on the type. Whatever is placed into the input arguement will be added to the log. """
    # if a log file does not exist, it will be created
    # To print to a file, change the printtype arg in actloginit to "f" (located in ingestion.py)
    try:
        logname = open(loginfo[logtype+"logdir"]+'/'+loginfo["logname"]+'.txt', "a+")
        logname.write(content + '\n')
        logname.close()
    except FileNotFoundError as fnf_error:
        print(fnf_error)
        pass

# old
def logprint(logtype, loginfo):
    """ prints a log file to the screen """
    try:
        with open(loginfo[logtype+"logdir"]+'/'+loginfo["logname"]+'.txt') as file:
            log = file.read()
            print(log)
            # actcontent = log  # needed?
            file.close()
    except FileNotFoundError as fnf_error:
        print(fnf_error)
        pass
        # actcontent = "No " + logtype + " log was found for this file!"  # needed?

    # slack.chat.post_message('#workflow-updates', actcontent)
    # slack.chat.post_message('#workflow-updates', errcontent)
    # slack.chat.post_message('#workflow-updates', "-------------End Log-------------")


def adderror(errorid, errorcode):
    e = JsonErrors.objects.get(id=errorid)
    s_list = e.errorcode
    l_list = ast.literal_eval(s_list)
    l_list.append(str(errorcode))
    e.errorcode = l_list
    e.save()

def readerrors(eid):
    e = JsonErrors.objects.get(id=eid)
    ec = e.errorcode
    ecl = ast.literal_eval(ec)
    print(type(ecl))
    print(ecl)
    reports = []
    for error in ecl:
        print(error)
        x=int(str(error)[0])
        y=int(str(error)[1])

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
                      uploaderrors[y],]

        print(errorcodes[x])
        report = errorcodes[x]
        reports.append(report)
    return reports
