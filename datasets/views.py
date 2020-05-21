"""imports"""
from django.shortcuts import render
from .models import Datasets


def home(request):
    """view to generare list of substances on homepage"""
    dscount = Datasets.objects.count()
    return render(request, "home.html", {'dscount': dscount})
