""" view definitions for the workflow app """
import ast
from zipfile import ZipFile

from django.shortcuts import redirect
from django.shortcuts import render
from .ingestion import *
from .models import *
from substances.forms import *

# Sciflow ingestion variables
herginputfiles = {}
hergoutputfiles = {}
hergerrorfiles = {}
cifinputfiles = {}
cifoutputfiles = {}
ciferrorfiles = {}


def dashboard(response):
    """ main view of workflow activity """
    # TODO add dashboard page


def ingestion(request):
    """ ingestion SciData JSON-LD file """
    user = request.user
    if request.method == "POST":
        file = request.FILES['upload']
        print(file)
        if "jsonld" in file.name:
            ingest(file, user)
            # data = file.readlines()
            # print(data)

        if "zip" in file.name:
            with ZipFile(file, 'r') as zip:
                filenames = []
                for info in zip.infolist():
                    name = info.filename
                    filenames.append(name)
                for file in filenames:
                    ingest(file, user)
                    # data = file.readlines()
                    # print(data)

    context = {}
    return render(request, 'workflow/ingestion.html', context)


def ingestionresults(response):
    """ ingestion results """
    user = response.user
    getfiles(herginput, herginputfiles)
    getfiles(hergoutput, hergoutputfiles)
    getfiles(hergerror, hergerrorfiles)
    getfiles(cifinput, cifinputfiles)
    getfiles(cifoutput, cifoutputfiles)
    getfiles(ciferror, ciferrorfiles)

    # TODO ingestionresults definition needs to be generic

    # herg submit button press:
    if response.POST.get('herg'):
        ingest("herg", "m", user)
        return redirect('/ingestion/results')

    # cif submit button press:
    if response.POST.get('cif'):
        ingest("herg", "m", user)
        return redirect('/ingestion/results')

    return render(response, 'workflow/ingestionresults.html', {
        "herginputfiles": herginputfiles, "cifinputfiles": cifinputfiles,
        "hergoutputfiles": hergoutputfiles, "cifoutputfiles": cifoutputfiles,
        "hergerrorfiles": hergerrorfiles, "ciferrorfiles": ciferrorfiles})


def test(response):
    """ retrieve the shortnames of all the datasets """
    qset = Datasets.objects.all().values_list('sourcecode', flat=True).order_by('id')
    lst = list(qset)
    print(lst)
    return render(response, "substances/add.html", {"lst": lst})

def errors(response):
    """ for testing and displaying errorcodes"""

    if response.method == "POST":
        if 'errortest' in response.POST:
            errorcode = response.POST.get('errortest')
            adderror(2,errorcode)

    errors = readerrors(1)

    context = {"errors":errors}
    return render(response, "workflow/errors.html", context)
