from datetime import datetime
time = datetime.today().strftime('%Y%m%d_%H%M%S-')
from .ingestiondir import*
from .ingestion import*


def errloginit(loginfo):
    errlog = open(loginfo["errlogdir"]+'/'+loginfo["logname"]+'.txt', "w+")
    errlog.write("The following error(s) were encountered while ingesting this file: \n\n")
    errlog.close()

def actloginit(printtype, loginfo):
    if printtype == "t":
        logwrite("act", loginfo, "Filename: " + loginfo["logname"].split("-")[1])
    if printtype == "f":
        actlog = open(loginfo["actlogdir"]+'/'+loginfo["logname"]+'.txt', "w+")
        actlog.write("Filename: " + loginfo["logname"].split("-")[1] + "\n")
        actlog.close()

def logwrite(log, loginfo, input):

    if log == "err":
        try:
            open(loginfo[log+"logdir"]+'/'+loginfo["logname"]+'.txt', "r")
        except:
            errloginit(loginfo)
        logname = open(loginfo[log+"logdir"]+'/'+loginfo["logname"]+'.txt', "a+")
        logname.write(input + '\n')

    if log == "act":
        try:
            open(loginfo[log+"logdir"]+'/'+loginfo["logname"]+'.txt', "r")
        except:
            print(input)
