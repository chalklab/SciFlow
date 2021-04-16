""" views for substances """
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.paginator import Paginator
from substances.sub_functions import *
from sciflow.settings import BASE_DIR
from zipfile import ZipFile


def sublist(request):
    """view to generate list of substances on homepage"""
    if request.method == "POST":
        query = request.POST.get('q')
        return redirect('/substances/search/' + str(query))

    substances = Substances.objects.all().order_by('name')
    return render(request, "substances/list.html", {'substances': substances})


def home(request):
    """present an overview page about the substance in sciflow"""
    subcount = Substances.objects.count()
    idcount = Identifiers.objects.count()
    descount = Descriptors.objects.count()
    return render(request, "substances/home.html",
                  {'subcount': subcount, 'idcount': idcount, 'descount': descount})


def subview(request, subid):
    """present an overview page about the substance in sciflow"""
    substance = Substances.objects.get(id=subid)
    ids = substance.identifiers_set.values_list('type', 'value', 'source')
    descs = substance.descriptors_set.values_list('type', 'value', 'source')
    srcs = substance.sources_set.all()
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

    # print(json.dumps(dlist, indent=4))
    # print(descs)
    # print(srcs)
    # exit()
    return render(request, "substances/subview.html",
                  {'substance': substance, "ids": idlist,
                   "descs": dlist, "srcs": srcs})


def subids(request, subid):
    """present an overview page about the substance in sciflow"""
    substance = Substances.objects.get(id=subid)
    ids = substance.identifiers_set.all()
    return render(request, "substances/subids.html",
                  {'substance': substance, "ids": ids})


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
    return render(request, "substances/ingest.html",)


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
