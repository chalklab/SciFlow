from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from .ingestion import*
# Create your views here.

#Sciflow Ingestion
herginputfiles = {}
hergoutputfiles = {}
hergerrorfiles = {}
cifinputfiles = {}
cifoutputfiles = {}
ciferrorfiles = {}

def ingestion(response):
    user = response.user
    getfiles(herginput, herginputfiles)
    getfiles(cifinput, cifinputfiles)

    #herg submit button press:
    if(response.POST.get('herg')):
        ingest("herg", "m", user)
        return redirect('/ingestion/results')

    #cif submit button press:
    if(response.POST.get('cif')):
        ingest("cif", "m", user)
        return redirect('/ingestion/results')

    return render(response, 'workflow/ingestion.html', {"herginputfiles":herginputfiles, "cifinputfiles":cifinputfiles})


#Sciflow Ingestion Results
def ingestionresults(response):
    user = response.user
    getfiles(herginput, herginputfiles)
    getfiles(hergoutput, hergoutputfiles)
    getfiles(hergerror, hergerrorfiles)
    getfiles(cifinput, cifinputfiles)
    getfiles(cifoutput, cifoutputfiles)
    getfiles(ciferror, ciferrorfiles)

    #herg submit button press:
    if(response.POST.get('herg')):
        ingest("herg", "m", user)
        return redirect('/ingestion/results')

    #cif submit button press:
    if(response.POST.get('cif')):
        ingest("herg", "m", user)
        return redirect('/ingestion/results')

    return render(response, 'workflow/ingestionresults.html', {"herginputfiles":herginputfiles, "cifinputfiles":cifinputfiles, "hergoutputfiles":hergoutputfiles, "cifoutputfiles":cifoutputfiles, "hergerrorfiles":hergerrorfiles, "ciferrorfiles":ciferrorfiles,})
