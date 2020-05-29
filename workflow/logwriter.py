from datetime import datetime
time = datetime.today().strftime('%Y%m%d_%H%M%S-')
actlogdir = str('/Users/Caleb Desktop/Desktop/sciflow ingestion/activitylogs')


#prints a log based on the values added to errorlog dictionary
def printerrorlog(i, status, source, errorlog, errlogdir):
    logname = time + status + source.split("\\")[-1].split(".")[0]
    log = open(str(errlogdir + '/' + logname + '.txt'), "w+")
    if status == "SCS-":
        log.write("This file was ingested successfully!")
    if status == "ERR-":
        log.write(str(i) + " error(s) were encountered while ingesting this file! \n\n")
        for value in errorlog.values():
            log.write("- " + value + "\n")


#prints a log based on the values added to the actlog dictionary. Can be set to print in the terminal (t) or to a file (f)
def printactivitylog(printtype, source, actlog):
    if printtype == "t":
        for key, value in actlog.items():
            print(str(key) + ": " + str(value))
    if printtype == "f":
        logname = "ACT-" + time + source.split("\\")[-1].split(".")[0]
        log = open(str(actlogdir + '/' + logname + '.txt'), "w+")
        log.write("activitylog")
