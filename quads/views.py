"""django views file for the quads app"""
from django.shortcuts import render
from datafiles.forms import UploadFileForm
from quads.qd_functions import ingest
from datetime import datetime
from sciflow import gvars
from django.http import HttpResponse


def ingestion(request):
    """ ingest SciData JSON-LD file for conversion to quads """
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
    return render(request, 'quads/ingestion.html', context)
