""" django database models file """
from django.db import models


class JsonLookup(models.Model):
    """ class for the json_lookup DB table """
    dataset_id = models.IntegerField()
    uniqueid = models.CharField(max_length=128)
    title = models.CharField(max_length=256)
    graphname = models.CharField(max_length=256)
    currentversion = models.IntegerField()
    auth_user_id = models.PositiveIntegerField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'json_lookup'


class JsonFiles(models.Model):
    """ class for the json_files DB table """
    json_lookup_id = models.IntegerField()
    file = models.TextField()
    type = models.CharField(max_length=32)
    version = models.IntegerField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'json_files'


class JsonErrors(models.Model):
    """ class for the json_errors DB table """
    json_lookup_id = models.IntegerField()
    json_file_id = models.IntegerField()
    errorcode = models.CharField(max_length=16)
    comment = models.CharField(max_length=256)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'json_errors'


class JsonActlog(models.Model):
    """ class for the json_actlog DB table """
    json_lookup_id = models.IntegerField()
    json_file_id = models.IntegerField()
    activitycode = models.CharField(max_length=16)
    comment = models.CharField(max_length=256)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'json_actlog'
