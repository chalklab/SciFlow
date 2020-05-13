"""imports"""
from django.shortcuts import render
from .models import Substances
from itertools import cycle
import os


def home(request):
    """view to generare list of substances on homepage"""
    substances = Substances.objects.all().filter(name__contains='benzene').order_by('name')
    return render(request, "home.html", {'substances': substances})


def chunk(request):
    """take an SDF file and chunk out the molecules"""
    path = r"/Users/n00002621/PycharmProjects/chemicals/files"
    os.chdir(path)

    subs = open('antiviral_with_properties.sdf')
    lines = subs.readlines()

    substance = []
    name = ''
    formula = ''
    casrn = ''
    mol = ''
    nxt = ''
    iname = ''
    mw = 0.0
    for line in lines:
        line = line.strip()
        if line == '$$$$':
            """organize data"""
            name = substance.pop(0)
            formula = substance.pop(0)
            casrn = substance.pop(0).replace(" Copyright (C) 2020 ACS", "")
            temp = substance[:]
            for molstr in temp:
                if molstr.find("M  END") == -1:
                    mol = mol + molstr + '\n'
                    substance.pop(0)
                else:
                    substance.pop(0)
                    break

            subcycle = cycle(substance[:])
            for subline in subcycle:
                if subline.startswith("> <cas.index.name>"):
                    iname = next(subcycle)

            nxt = substance.pop(0)
            break
        elif line == '':
            continue
        else:
            substance.append(line)

    return render(request, "chunk.html",
                  {'substance': substance, 'name': name, 'formula': formula, 'casrn': casrn, 'mol': mol, 'iname': iname})
