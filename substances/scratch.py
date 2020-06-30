""" scratch file """
from sciflow.settings import BASE_DIR


def addlist(request):
    """ add many compounds from a text file list of identifiers """
    path = BASE_DIR + "/json/herg_chemblids.txt"
    file = open(path)
    lines = file.readlines()
    for line in lines:
        print(line)
        exit()


addlist('fake')
