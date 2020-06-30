""" view definitions for the workflow app """
from django.shortcuts import redirect
from django.shortcuts import render
from .ingestion import *


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


def ingestion(response):
    """ ingestion SciData JSON-LD file """
    user = response.user
    getfiles(herginput, herginputfiles)
    getfiles(cifinput, cifinputfiles)

    # TODO ingestion definition needs to be generic

    # herg submit button press:
    if response.POST.get('herg'):
        ingest("herg", "m", user)
        return redirect('/workflow/results')

    # cif submit button press:
    if response.POST.get('cif'):
        ingest("cif", "m", user)
        return redirect('/workflow/results')

    return render(response, 'workflow/ingestion.html', {
        "herginputfiles": herginputfiles, "cifinputfiles": cifinputfiles})


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
    x = 0
    return render(response, "substances/add.html", {"lst": lst})
