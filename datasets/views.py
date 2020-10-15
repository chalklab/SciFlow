""" django views file for the datasets app """
from django.shortcuts import render, redirect
from datasets.serializer import *
from .forms import *
from workflow.ingestion import *
from django.shortcuts import render


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


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            ingest(request.FILES['file'])
            return redirect('home')
    else:
        form = UploadFileForm()
    return render(request, 'datasets/model_form_upload.html', {'form': form})















