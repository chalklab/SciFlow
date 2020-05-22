"""imports"""
from django.shortcuts import redirect
from django.shortcuts import render
from .models import Substances
from .models import Identifiers
from .models import Systems


def home(request):
    """view to generare list of substances on homepage"""
    substances = Substances.objects.all().filter(name__contains='benzene').order_by('name')
    return render(request, "substances/home.html", {'substances': substances})


def index(request):
    """present an overview page about the substance in sciflow"""
    subcount = Substances.objects.count()
    idcount = Identifiers.objects.count()
    syscount = Systems.objects.count()

    return render(request, "substances/index.html", {'subcount': subcount, 'idcount': idcount, 'syscount': syscount})


def view(request, subid):
    """present an overview page about the substance in sciflow"""
    substance = Substances.objects.get(id=subid)
    ids = Substances.objects.select_related('identifiers').get(id=subid)
    return render(request, "substances/view.html", {'substance': substance, 'ids': ids})
