""" functions to log workflow activity and errors """
from datafiles.models import *
from sciflow import gvars
from inspect import currentframe


def actlog(content):
    """add entry to activity log"""
    tag = " [Line: " + str(currentframe().f_back.f_lineno) + "]"
    ts = gvars.ingest_session
    jli = gvars.ingest_data_lookup_id
    jfi = gvars.ingest_data_file_id
    a = JsonActlog.objects.create(
        session=ts,
        json_lookup_id=jli,
        json_file_id=jfi,
        activitylog=content + tag)
    a.save()


def errorlog(content):
    """add entry to error log"""
    tag = " [Line: " + str(currentframe().f_back.f_lineno) + "]"
    ts = gvars.ingest_session
    jli = gvars.ingest_data_lookup_id
    jfi = gvars.ingest_data_file_id
    e = JsonErrors.objects.create(
        session=ts,
        json_lookup_id=jli,
        json_file_id=jfi,
        errorcode=content + tag)
    e.save()
