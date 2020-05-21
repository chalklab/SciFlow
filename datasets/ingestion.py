import pathlib
import shutil
import json
import jsonschema
from jsonschema import validate
from datetime import datetime
time = datetime.today().strftime('-%Y%m%d-%H%M%S-')

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
hergvalidity = {}
hergerrorlog = {}


#cif
cifautoinput = pathlib.Path('/Users/Caleb Desktop/Desktop/sciflow ingestion/cif/00 cif auto input')
cifinput = pathlib.Path('/Users/Caleb Desktop/Desktop/sciflow ingestion/cif/01 cif input')
cifoutput = pathlib.Path('/Users/Caleb Desktop/Desktop/sciflow ingestion/cif/02 cif output')
ciferror = pathlib.Path('/Users/Caleb Desktop/Desktop/sciflow ingestion/cif/03 cif error')
ciflog = pathlib.Path('/Users/Caleb Desktop/Desktop/sciflow ingestion/cif/04 cif log')
cifinputfiles = {}
cifoutputfiles = {}
ciferrorfiles = {}
cifvalidity = {}
ciferrorlog = {}


#functions
def getfiles(folder, dict):
    for file in folder.iterdir():
        filename = str(file).split("\\")[-1]
        dict.update({filename:filename})

from .chemblschema import schema
def validateJson(jsonData):
    try:
        validate(instance=jsonData, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True

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
        searchfile = open(path,"r")
        if type == "herg":
            hergcheck(searchfile)
            searchfile.close()
            movefile(path, output, error, logdir, hergvalidity, hergerrorlog)
        if type == "cif":
            cifcheck(searchfile)
            searchfile.close()
            movefile(path, output, error, logdir, cifvalidity, ciferrorlog)

#valdity check: if file is valid, i = 1 at the end. It is invalid, it should equal 0
def hergcheck(searchfile):

    #checking if it is actually herg
    a = 0
    b = 0
    for line in searchfile:
        #checking if it is actually herg
        if "\"CHEMBL240\"" in line:
            a += 1
        #verifying author (an example used for testing purposes)
        if "Fray MJ" in line:
            b += 1

    if a > 0:
        isherg = True
    else:
        isherg = False
        hergerrorlog.update({"a":"No instance of CHEMBL240 found!"})

    if b > 0:
        author = True
    else:
        author = False
        hergerrorlog.update({"b":"Incorrect Author! (needs to be written by Fray MJ)"})



    hergvalidity.update({"isherg":isherg, "author":author})




def cifcheck(searchfile):
    i = 0
    for line in searchfile:
        if "potato" in line:
            i += 1
    if i > 0:
        valid = True
    else:
        valid = False
    return valid

#move the file further down the pipeline depending on the vailidity, and prints a log depending on it's destination:
def movefile(source, output, error, logdir, dict, errorlog):
    i = 0
    for value in dict.values():
        print(value)
        if value is False:
            i += 1
    print("int: " + str(i))

    if i == 0:
        dest = output
        status = "Scs"
        #shutil.move('C:' + source, dest)
    else:
        dest = error
        status = "Err"
        #shutil.move('C:' + source, dest)

    #Log Printing:
    logname = status + time + source.split("\\")[-1].split(".")[0]
    log = open(str(logdir + '/' + logname + '.txt'), "w+")
    if status == "Scs":
        log.write("This file was ingested successfully!")
    if status == "Err":
        log.write(str(i) + " error(s) were encountered while ingesting this file! \n\n")
        for value in errorlog.values():
            log.write("- " + value + "\n")
