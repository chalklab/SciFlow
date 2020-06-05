""" scratch file """
from substances.sources import *
from substances.models import Identifiers


def cmpddata(identifier):
    """ searches for compound in database and gets its data or adds new compound with data"""

    # id the compound in the database?
    substance = Identifiers.objects.get(value=identifier)
    print(substance)
    exit()

    if substance.rowcount == 0:
        print("Not found")
    else:
        print(substance)

    exit()
    # meta = {}
    # ids = {}
    # descs = {}
    #
    # pubchem("aspirin", meta, ids, descs)
    # classyfire("BSYNRYMUTXBXSQ-UHFFFAOYSA-N", meta, ids, descs)
    # wikidata("BSYNRYMUTXBXSQ-UHFFFAOYSA-N", meta, ids, descs)
    # print(meta)
    # print(ids)
    # print(descs)


cmpddata("109-69-3")
