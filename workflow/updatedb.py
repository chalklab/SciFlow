from .validation import*
from .ingestion import*

#function to attempt to push things to the mysql and graph databases. If either fail, the update is reverted to prevent inconsistencies.
def updatedb():
    try:
        updatemysql()
        updategraphdb()
        validity.update({"Update Successful":True})
    except:
        revertupdatemysql()
        revertupdategraphdb()
        validity.update({"Update Successful":False})
        errorlog.update({"f":"An issue was encountered while updating a database!"})

def updatemysql():
    print("")


def updategraphdb():
    print("")


def revertupdatemysql():
    print("")


def revertupdategraphdb():
    print("")
