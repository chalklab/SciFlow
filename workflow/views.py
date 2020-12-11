""" view definitions for the workflow app """
from django.shortcuts import render
from .wf_functions import *
from datetime import time


def viewlog(response, lid):
    """ for testing and displaying errorcodes"""
    if not JsonActlog.objects.filter(json_lookup_id=lid):
        context = {"notfound": "This lookup does not have an activity log!"}
    else:
        lookup = JsonActlog.objects.filter(json_lookup_id=lid).all()
        fileids = []
        for entry in lookup:
            id = entry.json_file_id
            if id not in fileids:
                fileids.append(id)
        print(fileids)
        entries = {}
        errors = {}
        for fid in fileids:
            uid = JsonLookup.objects.get(id=lid).uniqueid
            finfo = "Version: "+str(JsonFiles.objects.get(id=fid).version)+", Upload Time: "+str(JsonFiles.objects.get(id=fid).updated)
            entries.update({finfo:[]})
            errors.update({finfo:[]})
            act = JsonActlog.objects.filter(json_file_id=fid)
            err = JsonErrors.objects.filter(json_file_id=fid)
            for entry in act:
                entries[finfo].append(entry.activitylog)
            for entry in err:
                errors[finfo].append(entry.errorcode)
        print(entries)
        print(errors)
        context = {"uid":uid,"lookup":lookup,"entries":entries,"errors":errors}
    return render(response, "workflow/viewlog.html", context)


def logs(response):
    """ for seeing all the logs"""
    lookups = JsonLookup.objects.all()
    rarror =  ValidationError("This is an error!")
    print(rarror.params)
    context = {"lookups":lookups, "rarror":rarror}
    return render(response, "workflow/logs.html", context)
