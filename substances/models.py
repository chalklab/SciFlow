"""import models"""
from django.db import models


class Substances(models.Model):
    """ getting data from the substances DB table"""
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=256, default='')
    formula = models.CharField(max_length=256, default='')
    monomass = models.FloatField(default=0.00)
    molweight = models.FloatField(default=0.00)
    casrn = models.CharField(max_length=16, default='')
    graphdb = models.CharField(max_length=256, null=True)
    facet_lookup_id = models.IntegerField(blank=True, null=True)
    comments = models.CharField(max_length=256, null=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'substances'


class Identifiers(models.Model):
    """ accessing the identifiers DB table"""
    CASRN = 'casrn'
    INCHI = 'inchi'
    INCHIKEY = 'inchikey'
    CSMILES = 'csmiles'
    ISMILES = 'ismiles'
    CSPR = 'chemspider'
    PUBCHEM = 'pubchem'
    INAME = 'iupacname'
    SPRNGR = 'springer'
    OTHER = 'othername'
    ATC = 'atc'
    REAXYS = 'reaxys'
    GMELIN = 'gmelin'
    CHEBI = 'chebi'
    CHEMBL = 'chembl'
    RTECS = 'rtecs'
    DSSTOX = 'dsstox'
    TYPE_CHOICES = [
        (CASRN, 'CAS Registry Number'), (INCHI, 'IUPAC InChI String'), (INCHIKEY, 'IUPAC InChI Key'),
        (CSMILES, 'Canonical SMILES'), (ISMILES, 'Isomeric SMILES'), (CSPR, 'Chemspider ID'),
        (PUBCHEM, 'PubChem Compound ID'), (INAME, 'IUPAC Name'), (SPRNGR, 'Springer ID'),
        (OTHER, 'Other Name'), (ATC, 'ATC Code'), (REAXYS, 'Reaxys ID'),
        (GMELIN, 'Gmelin ID'), (CHEBI, 'ChEBI ID'), (CHEMBL, 'ChEMBL ID'),
        (RTECS, 'RTECS ID'), (DSSTOX, 'DSSTOX ID')
    ]

    substance = models.ForeignKey(Substances, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=CASRN)
    value = models.CharField(max_length=768, default='')
    iso = models.CharField(max_length=5, default=None)
    source = models.CharField(max_length=64, default='')
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'identifiers'


class Sources(models.Model):
    """ get data from the sources DB table"""
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    substance = models.ForeignKey('Substances', models.DO_NOTHING)
    source = models.CharField(max_length=32)
    result = models.CharField(max_length=1)
    notes = models.CharField(max_length=2000, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'sources'


class Systems(models.Model):
    """ getting data from the identifiers DB table"""
    class CompTypes(models.TextChoices):
        """list of different composition types"""
        PURE = 'PS', 'pure compound'
        BINARY = 'BM', 'binary mixture'
        TERNARY = 'TM', 'ternary mixture'
        QUANARY = 'QM', 'quaternary mixture',
        QUINARY = 'NM', 'quinternary mixture'

    name = models.CharField(max_length=1024, default='')
    composition = models.CharField(max_length=2, choices=CompTypes.choices, default=CompTypes.PURE)
    identifier = models.CharField(max_length=128, default='')
    substance1 = models.ForeignKey(Substances, null=True, related_name='substance1', on_delete=models.CASCADE)
    substance2 = models.ForeignKey(Substances, null=True, related_name='substance2', on_delete=models.CASCADE)
    substance3 = models.ForeignKey(Substances, null=True, related_name='substance3', on_delete=models.CASCADE)
    substance4 = models.ForeignKey(Substances, null=True, related_name='substance4', on_delete=models.CASCADE)
    substance5 = models.ForeignKey(Substances, null=True, related_name='substance5', on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'systems'


class Templates(models.Model):
    """ getting data from the template """
    type = models.CharField(max_length=16)
    json = models.TextField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'templates'


class Descriptors(models.Model):
    """ accessing the descriptors DB table"""
    substance = models.ForeignKey(Substances, on_delete=models.CASCADE)
    type = models.CharField(max_length=128, default='')
    value = models.CharField(max_length=768, default='')
    source = models.CharField(max_length=64, default='')
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'descriptors'


class SubstancesSystems(models.Model):
    """ getting data from the substances_systems join table """
    substance = models.ForeignKey(Substances, null=True, related_name='substance_id', on_delete=models.CASCADE)
    system = models.ForeignKey(Systems, null=True, related_name='system_id', on_delete=models.CASCADE)
    role = models.CharField(max_length=13, blank=True, null=True)
    constituent = models.PositiveIntegerField(blank=True, null=True)
    mixture_id = models.IntegerField(blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'substances_systems'
