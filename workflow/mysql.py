""" functions to interact with MySQL """
from substances.models import *


def update_substance_field(inchikey, field, content):
    """ For a given InChIKey, it will change the provided field with the content given """
    subid = Identifiers.objects.get(value=inchikey).substance_id
    substance = Substances.objects.filter(id=subid)
    substance.update(**{field: content})


def clear_substance_field(inchikey, field):
    """ For a given InChIKey, it will change the provided field to NULL """
    subid = Identifiers.objects.get(value=inchikey).substance_id
    substance = Substances.objects.filter(id=subid)
    substance.update(**{field: None})


def add_identifier(inchikey, idtype, value, source):
    """ For a given InChIKey, add identifier (type & value) to that substance. Source may be set to None """
    subid = Identifiers.objects.get(value=inchikey).substance_id
    Identifiers.objects.create(substance_id=subid, type=idtype, value=value, source=source)


def create_substance(inchikey, name, formula):
    """ add substance table using the provided information """
    Substances.objects.create(name=name, formula=formula)
    subid = Substances.objects.get(name=name, formula=formula).id
    Identifiers.objects.create(substance_id=subid, type="inchikey", value=inchikey)
