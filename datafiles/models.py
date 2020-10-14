""" django database models file """
from django.db import models
from datasets.models import Datasets


class JsonLookup(models.Model):
    """ class for the json_lookup DB table """
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
    """ class for the json_files DB table """
    json_lookup = models.ForeignKey(JsonLookup, on_delete=models.PROTECT)
    file = models.TextField(default='')
    filefield = models.TextField(default='')
    type = models.CharField(max_length=32, default='')
    version = models.IntegerField(default='')
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'json_files'


class JsonErrors(models.Model):
    """ class for the json_errors DB table """
    json_lookup = models.ForeignKey(JsonLookup, on_delete=models.PROTECT, default='')
    json_file = models.ForeignKey(JsonFiles, on_delete=models.PROTECT, default='')
    errorcode = models.CharField(max_length=128, default='')
    comment = models.CharField(max_length=256, default='')
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'json_errors'


class JsonActlog(models.Model):
    """ class for the json_errors DB table """
    json_lookup = models.ForeignKey(JsonLookup, on_delete=models.PROTECT, null=True)
    json_file_id = models.ForeignKey(JsonFiles, on_delete=models.PROTECT, null=True)
    activitycode = models.CharField(max_length=2048, default='')
    comment = models.CharField(max_length=256, default='')
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'json_actlog'
