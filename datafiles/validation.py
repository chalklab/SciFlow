""" validation of SciData JSON-LD files """
# from datasets.ds_functions import *
# import json
#
#
# # TODO: Needed?
# def validate(file):
#     """
#     all-in-one validation function.
#     Includes every check that we would want to do on a file
#     """
#
#     validity = {}
#
#     # runs a check to make sure the file is in proper scidata format
#     # check_scidata(file, validity)
#
#     # TODO: See check_type function below
#     # Specialized checks for each dataset type
#     # searchstrings = getcodesnames()
#     # string = searchstrings[filetype]
#     # check_type(path, validity, loginfo, filetype, string)
#
#     # Validity Check
#     if all(validity.values()):
#         return True
#     else:
#         return False
#
#
# # TODO: Needed?
# def check_type(path, validity, loginfo, filetype, string):
#     """
#     generic function to check for a specific type of SciData file.
#     assumes that scidata check has been done
#     """
#     found = False
#     with open(path) as file:
#         if string in file.read():
#             found = True
#
#     if found:
#         print('Found!')
#         # logwrite("act", loginfo, "\t- " + filetype + ": Valid\n")
#     else:
#         print('Not found')
#         # logwrite("act", loginfo, "\t- " + filetype + ": Invalid!\n")
#         # logwrite("err", loginfo, "- " + " not found!\n")
#
#     validity.update({"is" + filetype: found})
