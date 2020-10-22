""" django views file for the datasets app """
from django.shortcuts import redirect
from datasets.serializer import *
from datafiles.forms import *
from django.shortcuts import render


def home(request):
    """view to generate list of substances on homepage"""
    dscount = Datasets.objects.exclude(sourcecode='chalklab').count()
    return render(request, "datasets/home.html", {'dscount': dscount})


def index(request):
    """view to generate list of substances on homepage"""
    datasets = Datasets.objects.exclude(sourcecode='chalklab')
    return render(request, "datasets/index.html", {'datasets': datasets})


def viewdataset(request, setid):
    """view a dataset list of files"""
    dataset = DatasetSerializer(Datasets.objects.get(id=setid))
    return render(request, "datasets/viewdataset.html", {'dataset': dataset.data})













