from django.db import models
from datasets.models import Datasets
class JsonLookup(models.Model):
    """ table for errorcodes"""
    dataset = models.ForeignKey(Datasets, on_delete=models.PROTECT)
    uniqueid = models.CharField(max_length=128, default='')
    title = models.CharField(max_length=256, default='')
    graphname = models.CharField(max_length=256, default='')
    currentversion = models.IntegerField(default='')
    auth_user_id = models.IntegerField(default='')
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        managed = False
        db_table = 'json_lookup'


class JsonFiles(models.Model):
    """ table for errorcodes"""
    json_lookup = models.ForeignKey(JsonLookup, on_delete=models.PROTECT)
    file = models.TextField(default='')
    type = models.CharField(max_length=32, default='')
    version = models.IntegerField(default='')
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'json_files'


class JsonErrors(models.Model):
    """ table for errorcodes"""
    json_lookup = models.ForeignKey(JsonLookup, on_delete=models.PROTECT, null=True)
    json_file = models.ForeignKey(JsonFiles, on_delete=models.PROTECT, null=True)
    errorcode = models.CharField(max_length=128, default='')
    comment = models.CharField(max_length=256, default='')
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'json_errors'

