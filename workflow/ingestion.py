""" ingestion functions """
from .normalization import *
from .updatedb import *
from .settings import *
from datafiles.functions import *
from datetime import datetime
import os
import time
import shutil
import platform


def getfiles(folder, dirdict):
    """ get a list of files in a folder """
    for file in folder.iterdir():
        if str(file).endswith('.jsonld'):
            filename = str(file).split("\\")[-1]
            dirdict.update({filename: filename})



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


def autoingest(filetype):
    """ autoingest files """
    try:
        ingest(filetype, "a", "bot")
    except FileNotFoundError as fnf_error:
        print(fnf_error)
        pass
    wait(type)


def wait(filetype):
    """ to ingest file """
    time.sleep(10)
    autoingest(filetype)


# autodir = os.listdir(hergautoinput)
# if len(autodir) > 1:
#     autoingest("herg")
# else:
#     print("no files detected in auto input; auto input disabled")
