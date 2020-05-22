"""imports"""
from django.shortcuts import redirect
from django.shortcuts import render
from .models import Datasets



def home(request):
    """view to generate list of substances on homepage"""
    dscount = Datasets.objects.count()
    return render(request, "datasets/home.html", {'dscount': dscount})
