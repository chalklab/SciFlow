""" view definitions for the workflow app """
from django.shortcuts import render
from .wf_functions import *


def actlog(response, fid):
    """ for testing and displaying errorcodes"""
    if not JsonActlog.objects.filter(json_file_id=fid):
        context = {"notfound": "This file does not have an activity log!"}
    else:
        log = ast.literal_eval(JsonActlog.objects.get(json_file_id=fid).activitylog)
        print(log["UID"])
        context = {"log":log}
    return render(response, "workflow/actlog.html", context)
