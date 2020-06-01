from .validation import*
from .ingestion import*

#function to attempt to push things to the mysql and graph databases. If either fail, the update is reverted to prevent inconsistencies.
def updatedb(loginfo):
    try:
        updatemysql()
        updategraphdb()
        logwrite("act", loginfo, "Update: Valid\n")
    except:
        revertupdatemysql()
        revertupdategraphdb()
        logwrite("act", loginfo, "Update: Invalid!\n")
        logwrite("err", loginfo, "- An issue was encountered while updating a database!\n")

def updatemysql():
    print("")


def updategraphdb():
    print("")


def revertupdatemysql():
    print("")


def revertupdategraphdb():
    print("")
