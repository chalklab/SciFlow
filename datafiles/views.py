""" django views file for the datafiles app """
from django.shortcuts import render
from datasets.serializer import *


def view(request, fileid):
    """view to generate list of substances on homepage"""
    file = JsonLookupSerializer(JsonLookup.objects.get(id=fileid))
    return render(request, "files/view.html", {'file': file.data})
