""" django views file for the datasets app """
from django.shortcuts import render
from .models import *


def home(request):
    """view to generate list of substances on homepage"""
    dscount = Datasets.objects.count()
    return render(request, "datasets/home.html", {'dscount': dscount})

def jsonlds(request):
    """view to generate list of substances on homepage"""
    jsonldlist = JsonFiles.objects.filter()
    return render(request, "datasets/jsonlds.html", {'jsonldlist': jsonldlist})
    # return render(request, "datasets/jsonlds.html")

def jsonldview(request, jsonldid):
    """view to generate list of substances on homepage"""
    jsonld= JsonFiles.objects.get(id=jsonldid)
    return render(request, "datasets/jsonldview.html", {'jsonld': jsonld})
    # return render(request, "datasets/jsonlds.html")