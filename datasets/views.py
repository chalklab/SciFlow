"""imports"""
from django.shortcuts import redirect
from django.shortcuts import render
from .models import Datasets
from datasets.ingestion import *



def home(request):
    """view to generate list of substances on homepage"""
    dscount = Datasets.objects.count()
    return render(request, "datasets/home.html", {'dscount': dscount})

#Sciflow Ingestion

def ingestion(response):
    getfiles(herginput, herginputfiles)
    getfiles(cifinput, cifinputfiles)

    #herg submit button press:
    if(response.POST.get('herg')):
        ingest("herg", "m")
        return redirect('/ingestion/results')

    #cif submit button press:
    if(response.POST.get('cif')):
        ingest("cif", "m")
        return redirect('/ingestion/results')

    return render(response, 'datasets/ingestion.html', {"herginputfiles":herginputfiles, "cifinputfiles":cifinputfiles})


#Sciflow Ingestion Results
def ingestionresults(response):
    getfiles(herginput, herginputfiles)
    getfiles(hergoutput, hergoutputfiles)
    getfiles(hergerror, hergerrorfiles)
    getfiles(cifinput, cifinputfiles)
    getfiles(cifoutput, cifoutputfiles)
    getfiles(ciferror, ciferrorfiles)

    #herg submit button press:
    if(response.POST.get('herg')):
        ingest("herg", "m")
        return redirect('/ingestion/results')

    #cif submit button press:
    if(response.POST.get('cif')):
        ingest("herg", "m")
        return redirect('/ingestion/results')


    return render(response, 'datasets/ingestionresults.html', {"herginputfiles":herginputfiles, "cifinputfiles":cifinputfiles, "hergoutputfiles":hergoutputfiles, "cifoutputfiles":cifoutputfiles, "hergerrorfiles":hergerrorfiles, "ciferrorfiles":ciferrorfiles,})
