""" views for substances """
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.contrib import messages
from workflow.gdb_functions import *
from substances.sub_functions import *
from sciflow.settings import BASE_DIR
from zipfile import ZipFile
from django.http import HttpResponse
from os import path
import requests


def molfile(request, subid):
    file = Structures.objects.get(substance_id=subid)
    return HttpResponse(str(file.molfile), content_type="text/plain")


def newjld(request, subid):
    """create a new version of the substance json_ld file"""
    sub = Substances.objects.get(id=subid)
    if sub.inchikey is not None:
        # generate new json-ld file (as python dictionary)
        jld = createsubjld(subid)
        # add entry in facet_lookup if no graphdb
        if sub.graphdb is None:
            title = jld["@graph"]["title"]
            uid = jld["@graph"]["uid"]
            lookup = FacetLookup(uniqueid=uid, title=title, type='substance', currentversion=1, auth_user_id=2)
            lookup.save()
            lookup.graphname = 'https://scidata.unf.edu/facet/' + str(lookup.id).zfill(8)
            lookup.save()
            sub.graphdb = lookup.graphname
            sub.facet_lookup_id = str(lookup.id).zfill(8)
            sub.save()
        # update new file @id
        jld["@id"] = sub.graphdb
        # get the latest version of this file from facet_files
        found = FacetFiles.objects.filter(facet_lookup_id=sub.facet_lookup_id)
        if not found:
            newver = 1
        else:
            lastver = FacetFiles.objects.filter(facet_lookup_id=sub.facet_lookup_id).order_by('-version')[0]
            newver = lastver.version + 1
        # load into facet_files
        file = FacetFiles(facet_lookup_id=sub.facet_lookup_id,
                          file=json.dumps(jld, separators=(',', ':')), type='raw', version=newver)
        file.save()
        # add json-ld to the graph replacing the old version if present
        addgraph('facet', sub.facet_lookup_id, 'remote', sub.graphdb)
        # update facet_lookup
        lookup = FacetLookup.objects.get(id=sub.facet_lookup_id)
        lookup.currentversion = newver
        lookup.save()
        # session message
        messages.add_message(request, messages.INFO, 'Compound twin added')
    else:
        messages.add_message(request, messages.INFO, 'Compound twin could not be added (no inchikey)')
    return subview(request, subid)


def sublist(request):
    """view to generate list of substances on homepage"""
    if request.method == "POST":
        query = request.POST.get('q')
        return redirect('/substances/search/' + str(query))

    substances = Substances.objects.all().order_by('name')
    return render(request, "substances/list.html", {'substances': substances})


def home(response):
    """present an overview page about the substance in sciflow"""
    subcount = Substances.objects.count()
    idcount = Identifiers.objects.count()
    descount = Descriptors.objects.count()

    return render(response, "substances/home.html",
                  {'subcount': subcount, 'idcount': idcount, 'descount': descount})


def subview(request, subid):
    """present an overview page about the substance in sciflow"""
    substance = Substances.objects.get(id=subid)
    ids = substance.identifiers_set.values_list('type', 'value', 'source')
    descs = substance.descriptors_set.values_list('type', 'value', 'source')
    srcs = substance.sources_set.all()
    inchikey = getinchikey(substance.id)
    baseimage = 'https://cactus.nci.nih.gov/chemical/structure/{}/file?format=sdf&get3d=true'

    image_url = baseimage.format(inchikey)
    testvar = path.exists("/static/Jsmol/JSmol.min.js")
    print(substance)
    print('js path is ' + str(testvar))
    print(inchikey)

    r = requests.get(image_url)
    print(str(r.status_code))
    if r.status_code == 200:
        image_found = ''
    else:
        image_found = 'Error Model not Found'
        image_url = ''
    print(image_found)
    print(image_url)
    if not descs:
        key = ""
        for i in ids:
            if i.type == 'inchikey':
                key = i.value
                break
        m, i, descs, srcs = getsubdata(key)
        savedescs(subid, descs)
    idlist = {}
    for idtype, value, src in ids:
        if idtype not in idlist.keys():
            idlist.update({idtype: {}})
        if value not in idlist[idtype].keys():
            idlist[idtype].update({value: []})
        idlist[idtype][value].append(src)
    dlist = {}
    for desc, value, src in descs:
        if desc not in dlist.keys():
            dlist.update({desc: {}})
        if value not in dlist[desc].keys():
            dlist[desc].update({value: []})
        dlist[desc][value].append(src)

    # related data files
    files = substance.jsonlookupsubstances_set.all()
    # print(json.dumps(dlist, indent=4))
    # print(descs)
    # print(srcs)
    # exit()
    return render(request, "substances/subview.html",
                  {'substance': substance, "ids": idlist, "descs": dlist, "srcs": srcs, "files": files,
                   "image_url": image_url, "image_found": image_found, "inchikey": inchikey})


def subids(request, subid):
    """present an overview page about the substance in sciflow"""
    substance = Substances.objects.get(id=subid)
    ids = substance.identifiers_set.all()
    return render(request, "substances/subids.html", {'substance': substance, "ids": ids})


def subdescs(request, subid):
    """present an overview page about the substance in sciflow"""
    substance = Substances.objects.get(id=subid)
    ids = substance.identifiers_set.all()
    descs = substance.descriptors_set.all()
    if not descs:
        key = ""
        for i in ids:
            if i.type == 'inchikey':
                key = i.value
                break
        m, i, descs = getsubdata(key)
        savedescs(subid, descs)
    return render(request, "substances/subdescs.html",
                  {'substance': substance, "descs": descs})


def add(request, identifier):
    """ check identifier to see if compound already in system and if not add """
    # id the compound in the database?
    hits = Substances.objects.all().filter(
        identifiers__value__exact=identifier).count()
    if hits == 0:
        meta, ids, descs, srcs = addsubstance(identifier, 'all')
    else:
        subid = getsubid(identifier)
        return redirect("/substances/view/" + str(subid))

    return render(request, "substances/add.html",
                  {"hits": hits, "meta": meta, "ids": ids, "descs": descs})


def ingest(request):
    """ingest a new substance"""
    if request.method == "POST":
        if 'ingest' in request.POST:
            inchikey = request.POST.get('ingest')
            matchgroup = re.findall('[A-Z]{14}-[A-Z]{10}-[A-Z]', inchikey)
            for match in matchgroup:
                hits = Substances.objects.all().filter(identifiers__value__exact=match).count()
                if hits == 0:
                    meta, ids, descs, srcs = addsubstance(match, 'all')
                else:
                    subid = getsubid(match)
        elif 'upload' in request.FILES.keys():
            file = request.FILES['upload']
            fname = file.name
            subs = []
            if fname.endswith('.json'):
                jdict = json.loads(file.read())
                for key in jdict['keys']:
                    subid = getsubid(key)
                    status = None
                    if not subid:
                        status = 'new'
                        sub = addsubstance(key, 'sub')
                        subid = sub.id
                    else:
                        status = 'present'
                    meta = getmeta(subid)
                    subs.append(
                        {'id': meta['id'], 'name': meta['name'],
                         'status': status})
                    request.session['subs'] = subs
                return redirect("/substances/list/")
            elif fname.endswith('.zip'):
                with ZipFile(file) as zfile:
                    filenames = []
                    for info in zfile.infolist():
                        name = info.filename
                        filenames.append(name)
                    for file in filenames:
                        data = zfile.read(file)
                        m = re.search('^[A-Z]{14}-[A-Z]{10}-[A-Z]$', str(data))
                        if m:
                            print(m)
                        else:
                            print(':(')
    return render(request, "substances/ingest.html", )


def ingestlist(request):
    """ add many compounds from a text file list of identifiers """
    path = BASE_DIR + "/json/herg_chemblids.txt"
    file = open(path)
    lines = file.readlines()
    # get a list of all chemblids currently in the DB
    qset = Identifiers.objects.all().filter(
        type__exact='chembl').values_list(
        'value', flat=True)
    chemblids = sublist(qset)
    count = 0
    names = []
    for identifier in lines:
        identifier = identifier.rstrip("\n")
        if identifier not in chemblids:
            meta, ids, descs, srcs = addsubstance(identifier, 'all')
            names.append(ids['pubchem']['iupacname'])
        count += 1
        if count == 1:
            break
    return names


def normalize(request, identifier):
    """
    create a SciData JSON-LD file for a compound, ingest in the graph
    and update data file with graph location
    """
    subid = getsubid(identifier)
    success = createsubjld(subid)
    return render(request, "substances/normalize.html", {"success": success})


def list(request):
    """emtpy view to be accessed via redirect from ingest above"""
    if 'subs' in request.session:
        subs = request.session['subs']
    else:
        subs = Substances.objects.all().order_by('name')

    paginator = Paginator(subs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "substances/list.html", {"page_obj": page_obj, "facet": "Substances"})


def search(request, query):
    """ search for a substance """
    context = subsearch(query)

    if request.method == "POST":
        query = request.POST.get('q')

        return redirect('/substances/search/' + str(query))

    return render(request, "substances/search.html", context)


def subcheck(request, action="view"):
    errors = []
    if action == "inkcheck":  # checks identifiers table for the presence of CASRN and InChIKey
        subs = Substances.objects.all().values_list('id', 'inchikey')
        for subid, key in subs:
            gotkey = Identifiers.objects.filter(substance_id=subid, type='inchikey').exclude(source='comchem').values_list('value', flat=True).distinct()
            if gotkey:
                if len(gotkey) == 1:
                    if str(gotkey[0]) != key:
                        errors.append('InChIKey ' + key + ' (substance ' + str(subid) + ') does not match')
                else:
                    errors.append('Multiple InChIKeys found for ' + key + ' (substance ' + str(subid) + ')')
            else:
                errors.append('InChIKey ' + key + ' (substance ' + str(subid) + ') not found in Identifiers table')
    elif action == "cascheck":
        subs = Substances.objects.all().values_list('id', 'casrn')
        for subid, casrn in subs:
            if casrn:
                gotcas = Identifiers.objects.filter(substance_id=subid, type='casrn').values_list('value', flat=True).distinct()
                if gotcas:
                    if len(gotcas) == 1:
                        if str(gotcas[0]) != casrn:
                            errors.append('CASRN ' + casrn + ' (substance ' + str(subid) + ') does not match')
                    else:
                        errors.append('Multiple CASRNs found for ' + casrn + ' (substance ' + str(subid) + ')')
                else:
                    errors.append('CASRN ' + casrn + ' (substance ' + str(subid) + ') not found in Identifiers table')
            else:
                errors.append('No CASRN for substance ' + str(subid))

    return render(request, "substances/check.html", {"errors": errors})


def showfacet(request, facetid):
    latest = FacetFiles.objects.filter(facet_lookup_id=facetid).latest('updated')
    return HttpResponse(latest.file, content_type="application/ld+json")


def showdata(request, dataid):
    latest = JsonFiles.objects.filter(json_lookup_id=dataid, type='normalized').latest('updated')
    return HttpResponse(latest.file, content_type="application/ld+json")
