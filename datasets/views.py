""" django views file for the datasets app """
from datasets.ds_functions import *
from django.shortcuts import render
from django.core.paginator import Paginator


def home(request):
    """view to generate list of substances on homepage"""
    updatestats()
    sets = Datasets.objects.exclude(count=0)
    return render(request, "datasets/home.html", {'sets': sets})


def index(request):
    """view to generate list of substances on homepage"""
    datasets = Datasets.objects.exclude(sourcecode='chalklab')
    return render(request, "datasets/index.html", {'datasets': datasets})


def viewdataset(request, setid):
    """view a dataset list of files"""
    files = JsonLookup.objects.filter(dataset_id=setid).order_by('title').values_list('id', 'title').distinct()
    paginator = Paginator(files, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    dataset = Datasets.objects.get(id=setid)
    return render(request, "datasets/viewdataset.html",
                  {'page_obj': page_obj, 'dataset': dataset})
