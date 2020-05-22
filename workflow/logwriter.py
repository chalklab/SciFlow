from datetime import datetime
time = datetime.today().strftime('%Y%m%d_%H%M%S-')


#Log Printing:
def printerrorlog(i, status, source, errorlog, logdir):
    logname = time + status + source.split("\\")[-1].split(".")[0]
    log = open(str(logdir + '/' + logname + '.txt'), "w+")
    if status == "SCS-":
        log.write("This file was ingested successfully!")
    if status == "ERR-":
        log.write(str(i) + " error(s) were encountered while ingesting this file! \n\n")
        for value in errorlog.values():
            print(value)
            log.write("- " + value + "\n")
