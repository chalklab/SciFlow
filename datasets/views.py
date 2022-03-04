""" django views file for the datasets app """
from datasets.ds_functions import *
from datafiles.df_serializers import *
from django.shortcuts import render
from django.core.paginator import Paginator
from sciflow.settings import authorized_users


def home(response):
    """view to generate list of substances on homepage"""
    updatestats()
    sets = Datasets.objects.exclude(count=0)

    user = response.user
    message = 'Welcome to SciFlow'

    if not user.is_anonymous:
        if user.email in authorized_users:
            message = 'Hello ' + user.first_name + ', Welcome to SciFlow.'

        else:
            message = 'You are not an approved user! Please contact Dr. Chalk to become authorized to use this site.'
            user.delete()

    return render(response, "datasets/home.html", {'sets': sets, 'message': message})


def index(request):
    """view to generate list of substances on homepage"""
    datasets = Datasets.objects.exclude(sourcecode='chalklab')
    return render(request, "datasets/index.html", {'datasets': datasets})


def view(request, setid):
    """view a dataset list of files (by reference)"""
    refids = JsonLookup.objects.filter(dataset_id=setid).values('reference_id').distinct()
    refs = References.objects.filter(id__in=refids)
    paginator = Paginator(refs, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    dataset = Datasets.objects.get(id=setid)

    return render(request, "datasets/view.html", {'page_obj': page_obj, 'dataset': dataset})
