"""import models"""
from django.db import models
from datafiles.models import FacetLookup


class Targets(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=1024)
    type = models.CharField(max_length=32, blank=True, null=True)
    organism = models.CharField(max_length=32, blank=True, null=True)
    tax_id = models.CharField(max_length=8, blank=True, null=True)
    chembl_id = models.CharField(max_length=16, blank=True, null=True)
    graphdb = models.CharField(max_length=256, blank=True, null=True)
    facetlookup = models.ForeignKey(FacetLookup, on_delete=models.DO_NOTHING, db_column='facet_lookup_id')
    comments = models.CharField(max_length=256, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'targets'


class Targids(models.Model):
    target = models.ForeignKey(Targets, models.DO_NOTHING, db_column='target_id')
    type = models.CharField(max_length=128)
    value = models.CharField(max_length=750)
    source = models.CharField(max_length=16, blank=True, null=True)
    comment = models.CharField(max_length=128, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'targids'


class Targdescs(models.Model):
    target = models.ForeignKey(Targets, models.DO_NOTHING, db_column='target_id')
    type = models.CharField(max_length=128)
    value = models.CharField(max_length=500)
    source = models.CharField(max_length=16, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'targdescs'
        unique_together = (('target_id', 'type', 'value', 'source'),)


class Targsrcs(models.Model):
    target = models.ForeignKey(Targets, models.DO_NOTHING, db_column='target_id')
    source = models.CharField(max_length=32)
    result = models.CharField(max_length=1)
    notes = models.TextField(blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'targsrcs'
