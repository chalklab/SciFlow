""" django views file for the datafiles app """
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.paginator import Paginator
from datafiles.df_serializers import *
from datafiles.forms import UploadFileForm
from workflow.wf_functions import ingest
from datetime import datetime
from sciflow import gvars
from django.http import HttpResponse


def ingestion(request):
    """ ingestion SciData JSON-LD file """
    user = request.user
    if request.method == "POST":
        gvars.init()
        now = datetime.now()
        gvars.ingest_session = datetime.timestamp(now)
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file')
            for file in files:
                ingest(file, user)
    else:
        form = UploadFileForm()
    context = {'form': form}
    return render(request, 'datafiles/ingestion.html', context)


def viewfile(request, fileid):
    """view to generate list of substances on homepage"""
    file = JsonLookupSerializer(JsonLookup.objects.get(id=fileid))
    return render(request, "datafiles/viewfile.html", {'file': file.data})


def clean(request, fileid):
    """remove (clean) a datafile and its related data from the system"""
    # delete datafile record => json_lookup (others deleted on cascade)
    # TODO: current default in models is model.PROTECT not CASCADE
    JsonLookup.objects.filter(id=fileid).delete()
    return render(request, "datafiles/cleaned.html", {'fileid': fileid})


def jsonld(request, fileid):
    """send JSON-LD file to browser"""
    data = JsonFiles.objects.get(id=fileid)
    return HttpResponse(data.file, content_type="application/ld+json")


# references related
def getrefs(request):
    refs = References.objects.all().order_by('title')
    paginator = Paginator(refs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "references/index.html", {'page_obj': page_obj})


def viewref(request, refid):
    ref = References.objects.get(id=refid)
    return render(request, "references/view.html", {'ref': ref})


def search(request, query):
    """ search for a reference """
    if request.method == "POST":
        query = request.POST.get('q')
        return redirect('/references/search/' + str(query))

    refs = References.objects.filter(title__icontains=query).values_list('id', 'title').order_by('title')
    return render(request, "references/search.html", {"refs": refs})
