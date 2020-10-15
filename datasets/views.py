""" django views file for the datasets app """
from django.shortcuts import render
from datasets.serializer import *


def home(request):
    """view to generate list of substances on homepage"""
    dscount = Datasets.objects.exclude(sourcecode='chalklab').count()
    return render(request, "datasets/home.html", {'dscount': dscount})


def index(request):
    """view to generate list of substances on homepage"""
    datasets = Datasets.objects.exclude(sourcecode='chalklab')
    return render(request, "datasets/index.html", {'datasets': datasets})


def view(request, setid):
    """view a dataset list of files"""
    dataset = DatasetSerializer(Datasets.objects.get(id=setid))
    return render(request, "datasets/view.html", {'dataset': dataset.data})
