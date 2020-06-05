from substances.models import*

#For a given inchi, it will change the provided field with the content given
def updateSubstanceField(inchikey, field, content):
    subid = Identifiers.objects.get(value=inchikey).substance_id
    substance = Substances.objects.filter(id=subid)
    substance.update(**{field : content})


#For a given inchi, it will change the provided field to NULL
def clearSubstanceField(inchikey, field):
    subid = Identifiers.objects.get(value=inchikey).substance_id
    substance = Substances.objects.filter(id=subid)
    substance.update(**{field : None})


#For a given inchi, designate the identifier type and value to add it for that substance. Source may be set to None
def addIdentifier(inchikey, type, value, source):
    subid = Identifiers.objects.get(value=inchikey).substance_id
    Identifiers.objects.create(substance_id=subid, type=type, value=value, source=source)


#Creates an entry in the substance table from the provided information
def createSubstance(inchikey, name, formula):
    Substances.objects.create(name=name, formula=formula)
    subid = Substances.objects.get(name=name, formula=formula).id
    Identifiers.objects.create(substance_id=subid, type="inchikey", value=inchikey)

def populateSubstance(inchikey):
    name = "name"
    formula = "formula"
    createSubstance(inchikey, name, formula)
    identifiers = {}
    casrn = "casrn"
    pubchem = "pubchem"
    iupacname = "iupacname"
    inchi = "inchi"
    chemspider = "chemspider"
    csmiles = "csmiles"
    for k, v in identifiers:
        addIdentifier(inchi, k, v)
