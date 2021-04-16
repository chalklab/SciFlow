""" django views file for the datafiles app """
from django.shortcuts import render
from datasets.serializer import *
from datafiles.forms import UploadFileForm
from workflow.wf_functions import ingest
from datetime import datetime
from sciflow import gvars
from django.http import HttpResponse


def ingestion(request):
    """ ingestion SciData JSON-LD file """
    user = request.user
    if request.method == "POST":
        gvars.init()
        now = datetime.now()
        gvars.ingest_session = datetime.timestamp(now)
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file')
            for file in files:
                ingest(file, user)
    else:
        form = UploadFileForm()
    context = {'form': form}
    return render(request, 'datafiles/ingestion.html', context)


def viewfile(request, fileid):
    """view to generate list of substances on homepage"""
    file = JsonLookupSerializer(JsonLookup.objects.get(id=fileid))
    return render(request, "datafiles/viewfile.html", {'file': file.data})


def clean(request, fileid):
    """remove (clean) a datafile and its related data from the system"""
    # delete datafile record => json_lookup (others deleted on cascade)
    # TODO: current default in modesl is model.PROTECT not CASCADE
    JsonLookup.objects.filter(id=fileid).delete()
    return render(request, "datafiles/cleaned.html", {'fileid': fileid})


def jsonld(request, fileid):
    """send JSON-LD file to browser"""
    data = JsonFiles.objects.get(id=fileid)
    return HttpResponse(data.file, content_type="application/ld+json")
