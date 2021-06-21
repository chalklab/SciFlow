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

