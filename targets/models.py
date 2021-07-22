"""import models"""
from django.db import models

class Targets(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=1024)
    type = models.CharField(max_length=32, blank=True, null=True)
    organism = models.CharField(max_length=32, blank=True, null=True)
    tax_id = models.CharField(max_length=8, blank=True, null=True)
    chembl_id = models.CharField(max_length=16, blank=True, null=True)
    graphdb = models.CharField(max_length=256, blank=True, null=True)
    facet_lookup_id = models.IntegerField(blank=True, null=True)
    comments = models.CharField(max_length=256, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'targets'


class Identifiers(models.Model):
    CHEMBL = 'chembl'
    TYPE_CHOICES = [
        (CHEMBL, 'ChEMBL ID')
    ]
    target = models.ForeignKey(Targets, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=CHEMBL)
    value = models.CharField(max_length=768, default='')
    #iso might just be a way to make canonical SMILES format pseudo unique, might not be needed for targets
    #iso = models.CharField(max_length=5, default=None)
    source = models.CharField(max_length=64, default='')
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'identifiers'

class Descriptors(models.Model):
    """ accessing the descriptors DB table"""
    target = models.ForeignKey(Targets, on_delete=models.CASCADE)
    type = models.CharField(max_length=128, default='')
    value = models.CharField(max_length=768, default='')
    source = models.CharField(max_length=64, default='')
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'descriptors'

class Sources(models.Model):
    """ get data from the sources DB table"""
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    substance = models.ForeignKey('Targets', models.DO_NOTHING)
    source = models.CharField(max_length=32)
    result = models.CharField(max_length=1)
    notes = models.CharField(max_length=2000, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'sources'