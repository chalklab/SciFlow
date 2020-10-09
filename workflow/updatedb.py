from .validation import *
from .logwriter import logwrite


# function to attempt to push things to the mysql and graph databases. If either fail, the update is reverted to prevent inconsistencies.
def updatedb(compound, loginfo):
    updatemysql(compound)
    try:
        updategraphdb()
        # updatemysql(compound)
        logwrite("act", loginfo, "Update: Valid\n")
    except:
        logwrite("act", loginfo, "Update: Invalid!\n")
        logwrite("err", loginfo, "- An issue was encountered while updating a database!\n")


def updategraphdb():
    print("")


def updatemysql(compound):
    # inchikey = compound["inchikey"]
    print("")

