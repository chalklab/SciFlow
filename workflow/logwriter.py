""" logging activity in sciflow """
import ast

from .models import *
from slacker import Slacker
from requests.sessions import Session
with Session() as session:
    slack = Slacker('xoxb-4596507645-1171034330099-eP4swGipytYQHLnomPvBoOPO', session=session)


def errloginit(loginfo):
    """ creates an error log, triggered by the detection of an error """
    errlog = open(loginfo["errlogdir"]+'/'+loginfo["logname"]+'.txt', "w+")
    errlog.write("The following error(s) were encountered while ingesting this file: \n\n")
    errlog.close()


def actloginit(loginfo):
    """ creates an activity log, triggered by the detection of an activity """
    actlog = open(loginfo["actlogdir"]+'/'+loginfo["logname"]+'.txt', "w+")
    actlog.write("-----------Activity Log-----------\n")
    actlog.write("Filename: " + loginfo["logname"].split("-")[1] + "\n")
    actlog.close()
    # slack.chat.post_message('#workflow-updates', "Filename: " + loginfo["logname"].split("-")[1])


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
        x=str(error)[0]
        y=str(error)[1]

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
