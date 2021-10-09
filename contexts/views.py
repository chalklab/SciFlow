""" django view file """
import json

from django.shortcuts import render, redirect
from datasets.ds_functions import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from contexts.ctx_functions import *
from contexts.git_functions import *
from datetime import datetime

# Contexts


def ctxlist(request):
    ctxs = getctxs()
    return render(request, "contexts/list.html", {'contexts': ctxs})


def ctxview(request, ctxid):
    ctx = getctx(ctxid)
    ds = getset(ctx.dataset_id)
    cws = ctx.crosswalks_set.all().order_by('table', 'field')
    onts = getonts()
    return render(request, "contexts/view.html",
                  {'context': ctx, 'dataset': ds, 'crosswalks': cws, 'onts': onts})


def ctxadd(request):
    """view to add data about a context"""
    if request.method == "POST":
        # save new namespace
        data = request.POST
        ctx = Contexts()
        ctx.dataset_id = data['dataset_id']
        ctx.name = data['name']
        ctx.description = data['description']
        ctx.filename = data['filename']
        ctx.save()
        # save crosswalk entries that have not been saved
        return redirect('/contexts/view/' + str(ctx.id))

    sets = setlist()
    trms = getonts()
    return render(request, "contexts/add.html", {'sets': sets, 'trms': trms})


# Crosswalks


def cwklist(request, cwkid=''):
    """view to generate list of namespaces"""
    crosswalks = getcwks(cwkid)
    return render(request, "crosswalks/list.html", {'crosswalks': crosswalks})


def cwkview(request, cwkid):
    """view to show all data about a namespace"""
    crosswalk = getcwk(cwkid)
    return render(request, "crosswalks/view.html", {'crosswalk': crosswalk})


# Namespaces


def nsplist(request):
    """view to generate list of namespaces"""
    spaces = getnsps()
    return render(request, "nspaces/list.html", {'spaces': spaces})


def nspview(request, nspid):
    """view to show all data about a namespace"""
    space = getnsp(nspid)
    terms = onttermsbyns(nspid)
    return render(request, "nspaces/view.html", {'space': space, 'terms': terms})


def nspadd(request):
    """view to add data about a namespace"""
    if request.method == "POST":
        # save new namespace
        data = request.POST
        nspace = Nspaces()
        nspace.name = data['name']
        nspace.ns = data['alias']
        nspace.path = data['path']
        nspace.homepage = data['homepage']
        nspace.save()
        return redirect('/nspaces/')

    aliases = nsaliases()
    oonts = olsonts()  # list of tuples (four values)
    oonts.sort(key=lambda tup: tup[1])
    return render(request, "nspaces/add.html", {'aliases': aliases, 'onts': oonts})


# Ontterms


def ontlist(request):
    """view to generate list of namespaces"""
    terms = getonts()
    return render(request, "ontterms/list.html", {'ontterms': terms})


def ontview(request, ontid):
    """view to show all data about an ont term"""
    term = getont(ontid)
    space = getnsp(term.nspace_id)
    uri = term.url.replace(space.ns + ':', space.path)
    return render(request, "ontterms/view.html", {'term': term, 'uri': uri})


def ontadd(request):
    """view to show all data about a ontterms"""
    if request.method == "POST":
        # save new namespace
        data = request.POST
        ontterm = Ontterms()
        ontterm.title = data['title']
        ontterm.definition = data['definition']
        ontterm.code = data['code']
        ontterm.nspace_id = data['nsid']
        ns = Nspaces.objects.get(id=data['nsid'])
        ontterm.url = ns.ns + ':' + data['code']
        ontterm.sdsection = data['sdsubsection']
        ontterm.sdsubsection = data['sdsubsection']
        ontterm.save()
        return redirect('/ontterms/')

    sdsects = [('methodology', 'Methodology (the "how" section)'), ('system', 'System (the "what" section)'),
               ('dataset', 'Dataset (the "data" section)')]
    subsects = [('procedure', 'methodology', 'Procedure'), ('chemical', 'system', 'Chemical'),
                ('exptdata', 'dataset', 'Experimental data')]

    nss = Nspaces.objects.all().values_list('id', 'name').order_by('name')
    aliases = nsaliases()
    onts = olsonts()  # list of tuples (four elements)
    kept = []
    onts.sort(key=lambda tup: tup[0])
    # remove entries that are not in the namespace list
    for i, ont in enumerate(onts):
        if ont[0] in aliases:
            kept.append(ont)
    return render(request, "ontterms/add.html",
                  {'nss': nss, 'sdsects': sdsects, 'subsects': subsects, 'onts': kept, 'aliases': aliases})


# ajax functions (wrappers)


@csrf_exempt
def ontterms(request, ontid):
    oterms = olsont(ontid)
    return JsonResponse({"ontterms": oterms}, status=200)


@csrf_exempt
def jscwkadd(request):
    if request.method == "POST":
        data = request.POST
        cwkid = data['cwkid']
        cxtid = data['cxtid']
        if cwkid == "" and cxtid != "":
            cwk = Crosswalks()
            cxt = Contexts.objects.get(id=cxtid)
            cwk.context_id = cxtid
            cwk.dataset_id = cxt.dataset_id
            if data['field'] != 'ontterm_id':
                cwk.ontterm = None
            cwk.datatype = 'string'  # default option
        else:
            cwk = Crosswalks.objects.get(id=cwkid)
        cwk.__dict__[data['field']] = data['value']
        cwk.save()
        if cwk.ontterm_id:
            cwk.temp = cwk.ontterm.title + '|' + cwk.ontterm.url
    return JsonResponse(model_to_dict(cwk), status=200)


@csrf_exempt
def jsdelcwk(request):
    if request.method == "POST":
        data = request.POST
        cwkid = data['cwkid']
        Crosswalks.objects.get(id=cwkid).delete()
        response = {}
        try:
            Crosswalks.objects.get(id=cwkid)
            response.update({"response": "failure"})
        except Crosswalks.DoesNotExist:
            response.update({"response": "success"})
    return JsonResponse(response, status=200)


@csrf_exempt
def jscwkread(request, cwkid=""):
    cwk = Crosswalks.objects.get(id=cwkid)
    return JsonResponse(model_to_dict(cwk), status=200)


@csrf_exempt
def jswrtctx(request, ctxid: int):
    ctx = Contexts.objects.get(id=ctxid)
    tpl = '{"@vocab": "https://www.w3.org/2001/XMLSchema#",' \
          '"sdo": "https://stuchalk.github.io/scidata/ontology/scidata.owl#"}'
    cdict = json.loads(tpl)
    nss = {}
    # add namespaces
    for cwk in ctx.crosswalks_set.all():
        nss.update({cwk.ontterm.nspace.ns: cwk.ontterm.nspace.path})
    for key in nss:
        cdict.update({key: nss[key]})
    # add entries
    for cwk in ctx.crosswalks_set.all():
        tmp = {}
        tmp.update({"@id": cwk.ontterm.url, "@type": cwk.datatype})
        if cwk.newname:
            cdict.update({cwk.newname: tmp})
        else:
            cdict.update({cwk.field: tmp})
    jld = {"@context": cdict}
    text = json.dumps(jld, separators=(',', ':'))
    resp = addctxfile('contexts/' + ctx.filename + '.jsonld', 'commit via API', text)
    return JsonResponse({"response": resp}, status=200)
