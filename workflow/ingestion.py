import pathlib
import shutil
from .validation import*
from .normalization import*
from .logwriter import*
from .updatedb import*


#directories:

#herg
hergautoinput = pathlib.Path('/Users/Caleb Desktop/Desktop/sciflow ingestion/herg/00 herg auto input')
herginput = pathlib.Path('/Users/Caleb Desktop/Desktop/sciflow ingestion/herg/01 herg input')
hergoutput = pathlib.Path('/Users/Caleb Desktop/Desktop/sciflow ingestion/herg/02 herg output')
hergerror = pathlib.Path('/Users/Caleb Desktop/Desktop/sciflow ingestion/herg/03 herg error')
herglog = pathlib.Path('/Users/Caleb Desktop/Desktop/sciflow ingestion/herg/04 herg log')
herginputfiles = {}
hergoutputfiles = {}
hergerrorfiles = {}



#cif
cifautoinput = pathlib.Path('/Users/Caleb Desktop/Desktop/sciflow ingestion/cif/00 cif auto input')
cifinput = pathlib.Path('/Users/Caleb Desktop/Desktop/sciflow ingestion/cif/01 cif input')
cifoutput = pathlib.Path('/Users/Caleb Desktop/Desktop/sciflow ingestion/cif/02 cif output')
ciferror = pathlib.Path('/Users/Caleb Desktop/Desktop/sciflow ingestion/cif/03 cif error')
ciflog = pathlib.Path('/Users/Caleb Desktop/Desktop/sciflow ingestion/cif/04 cif log')
cifinputfiles = {}
cifoutputfiles = {}
ciferrorfiles = {}

actlog = {}

#functions
def getfiles(folder, dict):
    for file in folder.iterdir():
        filename = str(file).split("\\")[-1]
        dict.update({filename:filename})


#ingestion script
def ingest(type, auto):
    if auto == "a":
        input = pathlib.Path('/Users/Caleb Desktop/Desktop/sciflow ingestion/'+type+'/00 '+type+' auto input')
    if auto == "m":
        input = pathlib.Path('/Users/Caleb Desktop/Desktop/sciflow ingestion/'+type+'/01 '+type+' input')
    output = pathlib.Path('/Users/Caleb Desktop/Desktop/sciflow ingestion/'+type+'/02 '+type+' output')
    error = pathlib.Path('/Users/Caleb Desktop/Desktop/sciflow ingestion/'+type+'/03 '+type+' error')
    logdir = str('/Users/Caleb Desktop/Desktop/sciflow ingestion/'+type+'/04 '+type+' log')

    for file in input.iterdir():
        path = str(file)
        filename = str(file).split("\\")[-1]
        actlog.update({"Filename":filename})

        validate(path, type) #validate.py
        actlog.update({"Validity":validity})

        if validate(path, type) is True:
            normalize(path) #normalization.py
            actlog.update({"Compound":compound})
            actlog.update({"Target":target})

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
        #shutil.move('C:' + source, dest)
    else:
        dest = error
        status = "ERR-"
        #shutil.move('C:' + source, dest)

    #printing and resetting of logs (logwriter.py)
    actlog.update({"Status":status})
    printactivitylog('t', path, actlog)
    printerrorlog(i, status, path, errorlog, logdir)
    actlog.clear()
    errorlog.clear()
    validity.clear()
