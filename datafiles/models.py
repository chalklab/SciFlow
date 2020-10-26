"""import models"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from datasets.models import *

class JsonLookup(models.Model):
    """ model for the json_lookup DB table """
    dataset = models.ForeignKey(Datasets, on_delete=models.PROTECT)
    uniqueid = models.CharField(max_length=128, unique=True, default='')
    title = models.CharField(max_length=256, default='')
    graphname = models.CharField(max_length=256, default='')
    currentversion = models.IntegerField(default=0)
    auth_user_id = models.IntegerField(default='')
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        managed = False
        db_table = 'json_lookup'


class JsonFiles(models.Model):
    """ model for the json_files DB table """
    json_lookup = models.ForeignKey(JsonLookup, on_delete=models.PROTECT)
    file = models.TextField(default='')
    type = models.CharField(max_length=32, default='')
    version = models.IntegerField(default='')
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'json_files'


class JsonErrors(models.Model):
    """ model for the json_errors DB table """
    json_lookup = models.ForeignKey(JsonLookup, on_delete=models.PROTECT, default='')
    json_file = models.ForeignKey(JsonFiles, on_delete=models.PROTECT, default='')
    errorcode = models.CharField(max_length=128, default='')
    comment = models.CharField(max_length=256, default='')
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'json_errors'


class JsonActlog(models.Model):
    """ model for the json_errors DB table """
    json_lookup = models.ForeignKey(JsonLookup, on_delete=models.PROTECT, null=True)
    json_file_id = models.ForeignKey(JsonFiles, on_delete=models.PROTECT, null=True)
    activitycode = models.CharField(max_length=2048, default='')
    comment = models.CharField(max_length=256, default='')
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'json_actlog'


class JsonAspects(models.Model):
    """model for the json_aspects join table"""
    json_lookup = models.ForeignKey(JsonLookup, on_delete=models.PROTECT)
    aspects_lookup_id = models.IntegerField()  # needs to match syntax of the above once the AspectsLookup model is created
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'json_aspects'


class JsonFacets(models.Model):
    """model for the json_facets join table"""

    json_lookup = models.ForeignKey(JsonLookup, on_delete=models.PROTECT)
    facets_lookup_id = models.IntegerField()  # needs to match syntax of the above once the FacetsLookup model is created
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'json_facets'

