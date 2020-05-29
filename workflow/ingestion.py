import pathlib
import shutil
from .validation import*
from .normalization import*
from .logwriter import*
from .updatedb import*
from .ingestiondir import*

actlog = {}


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
    logdir = str(root_path+'/'+type+'/04 '+type+' log')

    for file in input.iterdir():
        if str(file).endswith('.jsonld'):
            path = str(file)
            filename = str(file).split("\\")[-1]
            actlog.update({"Filename":filename})

            validate(path, type) #validate.py
            actlog.update({"Validity":validity})

            if validate(path, type) is True:
                normalize(path) #normalization.py

                if normalize(path) is True:
                    updatedb() #updatedb.py

            finalize(path, output, error, logdir, validity, errorlog, actlog)


#finalizes the ingestion, determining whether it was successful, and printing all logs:
def finalize(path, output, error, logdir, validity, errorlog, actlog):
    i = 0
    for value in validity.values():
        if value is False:
            i += 1

    #Detemines whether the ingestion was successful or not, and counts the errors if it was not
    if i == 0:
        dest = output
        status = "SCS-"
        shutil.move(path, dest)
    else:
        dest = error
        status = "ERR-"
        shutil.move(path, dest)

    #printing and resetting of logs (logwriter.py)
    actlog.update({"Status":status})
    printactivitylog('t', path, actlog)
    printerrorlog(i, status, path, errorlog, logdir)
    actlog.clear()
    errorlog.clear()
    validity.clear()
