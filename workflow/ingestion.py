import pathlib
import shutil
from .validation import*
from .normalization import*
from .logwriter import*


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
        actlog.update({"Filename":filename})


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
        searchfile = open('C:' + path,"r")
        if type == "herg":
            findcomp(path)
            hergcheck(path)
            actlog.update({"Validity":hergvalidity})
            actlog.update({"Compounds":compounds})
            movefile(path, output, error, logdir, hergvalidity, hergerrorlog)
        if type == "cif":
            cifcheck(searchfile)
            findcomp(searchfile)
            searchfile.close()
            movefile(path, output, error, logdir, cifvalidity, ciferrorlog)



#move the file further down the pipeline depending on the vailidity, and prints a log depending on it's destination:
def movefile(source, output, error, logdir, dict, errorlog):
    i = 0
    for value in dict.values():
        if value is False:
            i += 1

    if i == 0:
        dest = output
        status = "SCS-"
        #shutil.move('C:' + source, dest)
    else:
        dest = error
        status = "ERR-"
        #shutil.move('C:' + source, dest)
    printerrorlog(i, status, source, errorlog, logdir)
    actlog.update({"Status":status})
    printactivitylog('t', source, actlog)

