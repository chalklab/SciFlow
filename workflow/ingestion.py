import pathlib
import shutil
from .validation import*
from .normalization import*
from .logwriter import*
from .updatedb import*
from .ingestiondir import*


#functions
def getfiles(folder, dict):
    for file in folder.iterdir():
        if str(file).endswith('.jsonld'):
            filename = str(file).split("\\")[-1]
            dict.update({filename:filename})


#ingestion script
def ingest(type, auto):
    if auto == "a":
        input = pathlib.Path(root_path+'/'+type+'/00 '+type+' auto input')
    if auto == "m":
        input = pathlib.Path(root_path+'/'+type+'/01 '+type+' input')
    output = pathlib.Path(root_path+'/'+type+'/02 '+type+' output')
    error = pathlib.Path(root_path+'/'+type+'/03 '+type+' error')


    for file in input.iterdir():
        if str(file).endswith('.jsonld'):
            path = str(file)
            filename = str(file).split("\\")[-1]

            loginfo = {
                "errlogdir":str(root_path+'/'+type+'/04 '+type+' log'),
                "actlogdir":str(root_path+'/activitylogs'),
                "logname":time + filename.split(".")[0],
             }
            actloginit("t", loginfo)

            if validate(path, type, loginfo) is True: #validate.py

                if normalize(path, loginfo) is True: #normalization.py
                    updatedb(loginfo) #updatedb.py

            finalize(path, output, error, loginfo)


#finalizes the ingestion, determining whether it was successful, and moving the file
def finalize(path, output, error, loginfo):
    #Detemines whether the ingestion was successful or not
    logname = loginfo["errlogdir"]+'/'+loginfo["logname"]+'.txt'
    i = 0
    try:
        open(logname, "r")
        logwrite("act", loginfo, "Status: Failed!")
        i += 1
    except:
        logwrite("act", loginfo, "Status: Success!")

    #Moves the file
    if i == 0:
        dest = output
        #shutil.move(path, dest)
    else:
        dest = error
        #shutil.move(path, dest)

