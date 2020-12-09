""" functions to log workflow activity and errors """
from datafiles.models import *
from sciflow import gvars


def actlog(content):
    """add entry to activity log"""
    ts = gvars.ingest_session
    jli = gvars.ingest_data_lookup_id
    jfi = gvars.ingest_data_file_id
    a = JsonActlog.objects.create(session=ts, json_lookup_id=jli, json_file_id=jfi, activitylog=content)
    a.save()


def errorlog(content):
    """add entry to error log"""
    ts = gvars.ingest_session
    jli = gvars.ingest_data_lookup_id
    jfi = gvars.ingest_data_file_id
    e = JsonErrors.objects.create(session=ts, json_lookup_id=jli, json_file_id=jfi, errorcode=content)
    e.save()
