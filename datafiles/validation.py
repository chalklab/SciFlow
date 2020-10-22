""" validation of SciData JSON-LD files """
from datasets.ds_functions import *
import json


def validate(file):
    """all-in-one validation function. Includes every check that we would want to do on a file"""

    validity = {}

    # runs a check to make sure the file is in proper scidata format
    # check_scidata(file, validity)

    # TODO: See check_type function below
    # Specialized checks for each dataset type
    # searchstrings = getcodesnames()
    # string = searchstrings[filetype]
    # check_type(path, validity, loginfo, filetype, string)

    # Validity Check
    if all(validity.values()):
        return True
    else:
        return False


def check_scidata(file, validity):
    """ checks that file is present, is valid json, and conforms to the SciData specification """
    try:
        with file as json_file:
            data = json.load(json_file)
            keys_a = []
            keys_b = []
            isscidata = True
            for k, v in data.items():
                keys_a.append(k)
                if k == '@graph':
                    for y, z in v.items():
                        keys_b.append(y)
            for y in ['@context', '@id', '@graph']:
                if y not in keys_a:
                    isscidata = False
            for y in ['scidata']:
                if y not in keys_b:
                    isscidata = False
            # write to logs
            if isscidata is True:
                print("valid!")
                # logwrite("act", loginfo, "\t- Scidata: Valid")
            else:
                print("invalid!")
                # logwrite("act", loginfo, "\t- Scidata: Invalid!")
                # logwrite("err", loginfo, "- Invalid Scidata Format!\n")
            # update validity
            validity.update({"isscidata": isscidata})
    except FileNotFoundError as ex:
        # logwrite("err", loginfo, str(ex) + "\n")
        print("Error: file not found!")
        validity.update({"validfile": False})


# TODO: Needs rewritten using the new uniqueid system
def check_type(path, validity, loginfo, filetype, string):
    """ generic function to check for a specific type of SciData file. assumes that scidata check has been done """
    found = False
    with open(path) as file:
        if string in file.read():
            found = True
    if found:
        print('Found!')
        # logwrite("act", loginfo, "\t- " + filetype + ": Valid\n")
    else:
        print('Not found')
        # logwrite("act", loginfo, "\t- " + filetype + ": Invalid!\n")
        # logwrite("err", loginfo, "- " + " not found!\n")

    validity.update({"is" + filetype: found})
