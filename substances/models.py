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

    substance_id = models.ForeignKey(Substances, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=IDTypes.choices, default=IDTypes.CASRN)
    value = models.CharField(max_length=1024, default='')
