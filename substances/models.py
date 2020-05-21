"""import models"""
from django.db import models

# Create your models here.


class Substances(models.Model):
    """ getting data from the substances DB table"""
    name = models.CharField(max_length=256, default='')
    formula = models.CharField(max_length=256, default='')
    molweight = models.FloatField(default=0.00)
    casrn = models.CharField(max_length=16, default='')

    class Meta:
        managed = False
        db_table = 'substances'


class Identifiers(models.Model):
    """ getting data from the identifiers DB table"""
    class IDTypes(models.TextChoices):
        """list of different identifier types"""
        CASRN = 'CA', 'CAS RN'
        INCHI = 'IN', 'InChi String'
        INCHIKEY = 'IK', 'InChi Key'
        SMILES = 'SM', 'SMILES'

    substance = models.ForeignKey(Substances, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=IDTypes.choices, default=IDTypes.CASRN)
    value = models.CharField(max_length=1024, default='')

    class Meta:
        managed = False
        db_table = 'identifiers'


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


