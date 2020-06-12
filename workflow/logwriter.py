from .ingestion import*
from slacker import Slacker

from requests.sessions import Session
with Session() as session:
    slack = Slacker('xoxb-4596507645-1171034330099-eP4swGipytYQHLnomPvBoOPO', session=session)


# creates an errorlog, triggered by the detection of an error
def errloginit(loginfo):
    errlog = open(loginfo["errlogdir"]+'/'+loginfo["logname"]+'.txt', "w+")
    errlog.write("The following error(s) were encountered while ingesting this file: \n\n")
    errlog.close()


# dictates whether the activity log will print to the terminal (t) or a file (f)
def actloginit(loginfo):
    actlog = open(loginfo["actlogdir"]+'/'+loginfo["logname"]+'.txt', "w+")
    actlog.write("-----------Activity Log-----------\n")
    actlog.write("Filename: " + loginfo["logname"].split("-")[1] + "\n")
    actlog.close()
    # slack.chat.post_message('#workflow-updates', "Filename: " + loginfo["logname"].split("-")[1])


# writes to a log depending on the type. Whatever is placed into the input arguement will be added to the log.
def logwrite(log, loginfo, content):

    # if an error log does not exist, it will be created
    if log == "err":
        try:
            open(loginfo[log+"logdir"]+'/'+loginfo["logname"]+'.txt', "r").close()
        except:
            errloginit(loginfo)
        logname = open(loginfo[log+"logdir"]+'/'+loginfo["logname"]+'.txt', "a+")
        logname.write(content + '\n')
        logname.close()

    # if an activity log does not exist, it will instead print to the console. To print to a file, change the printtype arg in actloginit to "f" (located in ingestion.py)
    if log == "act":
        try:
            logname = open(loginfo[log+"logdir"]+'/'+loginfo["logname"]+'.txt', "a+")
            logname.write(content + '\n')
            logname.close()
        except:
            pass


def logprint(loginfo):
    try:
        with open(loginfo["actlogdir"]+'/'+loginfo["logname"]+'.txt', "r") as file:
            actlog = file.read()
            print(actlog)
            actcontent = actlog
            file.close()
    except:
        actcontent = "No Activity Log was found for this file!"
    # slack.chat.post_message('#workflow-updates', actcontent)
    try:
        with open(loginfo["errlogdir"]+'/'+loginfo["logname"]+'.txt', "r") as file:
            errlog = file.read()
            print(errlog)
            errcontent = errlog
            file.close()
    except:
        errcontent = "No Errors were encountered!"
    # slack.chat.post_message('#workflow-updates', errcontent)
    # slack.chat.post_message('#workflow-updates', "-------------End Log-------------")
