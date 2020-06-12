import os
import time
from datetime import datetime
import shutil
from .validation import *
from .normalization import *
from .logwriter import logwrite, logprint
from .updatedb import *
from .ingestiondir import *



# functions
def getfiles(folder, dirdict):
    for file in folder.iterdir():
        if str(file).endswith('.jsonld'):
            filename = str(file).split("\\")[-1]
            dirdict.update({filename: filename})


# ingestion script
def ingest(filetype, auto):
    if auto == "a":
        inputdir = pathlib.Path(root_path+'/'+filetype+'/00 '+filetype+' auto input')
    if auto == "m":
        inputdir = pathlib.Path(root_path+'/'+filetype+'/01 '+filetype+' input')
    outputdir = pathlib.Path(root_path+'/'+filetype+'/02 '+filetype+' output')
    errordir = pathlib.Path(root_path+'/'+filetype+'/03 '+filetype+' error')

    for file in inputdir.iterdir():
        now = datetime.today().strftime('%Y%m%d_%H%M%S-')
        if str(file).endswith('.jsonld'):
            path = str(file)
            filename = str(file).split("\\")[-1]

            loginfo = {
                "errlogdir": str(root_path+'/'+filetype+'/04 '+filetype+' log'),
                "actlogdir": str(root_path+'/activitylogs'),
                "logname": now + filename.split(".")[0],
             }
            actloginit(loginfo)
            if validate(path, filetype, loginfo) is True:  # validate.py
                compound, target = getsystem(path)
                if normalize(path, compound, target, loginfo) is True:  # normalization.py
                    updatedb(compound, loginfo)  # updatedb.py

            finalize(path, outputdir, errordir, loginfo)


# finalizes the ingestion, determining whether it was successful, and moving the file
def finalize(path, outputdir, errordir, loginfo):
    # Detemines whether the ingestion was successful or not
    logname = loginfo["errlogdir"]+'/'+loginfo["logname"]+'.txt'
    i = 0
    try:
        file = open(logname, "r")
        file.close()
        logwrite("act", loginfo, "Status: Failed!")
        i += 1
    except:
        logwrite("act", loginfo, "Status: Success!")
    logprint(loginfo)
    # Moves the file
    if i == 0:
        dest = outputdir
        # shutil.move(path, dest)
    else:
        dest = errordir
        # shutil.move(path, dest)


def autoingest(filetype):
    try:
        ingest(filetype, "a")
    except:
        pass
    wait(type)


def wait(filetype):
    time.sleep(10)
    autoingest(filetype)

autodir = os.listdir(hergautoinput)
if len(autodir) > 1:
    autoingest("herg")
else:
    print("no files detected in auto input; auto input disabled")
