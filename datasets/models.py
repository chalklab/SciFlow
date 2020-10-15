"""import models"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Datasets(models.Model):
    """model for the datasets table"""

    class Protected(models.TextChoices):
        """ choice for protected field """
        YES = 'yes', _('Yes')
        NO = 'no', _('No')

    name = models.CharField(max_length=64, default='')
    sourcecode = models.CharField(max_length=16, null=True)
    source = models.CharField(max_length=64, default='')
    sourceurl = models.CharField(max_length=256, default='')
    datasetname = models.CharField(max_length=16, null=True)
    uniqueidformat = models.CharField(max_length=128, null=True)
    protected = models.CharField(max_length=16, choices=Protected.choices, default='no')
    count = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'datasets'


class JsonActlog(models.Model):
    """model for the json_actlogs table"""
    json_lookup_id = models.IntegerField()
    json_file_id = models.IntegerField()
    activitycode = models.CharField(max_length=16)
    comment = models.CharField(max_length=256)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'json_actlog'


class JsonAspects(models.Model):
    """model for the json_aspects join table"""
    json_lookup_id = models.IntegerField()
    aspects_lookup_id = models.IntegerField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'json_aspects'


class JsonErrors(models.Model):
    """model for the json_errors table"""
    json_lookup_id = models.IntegerField()
    json_file_id = models.IntegerField()
    errorcode = models.CharField(max_length=16)
    comment = models.CharField(max_length=256)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'json_errors'


class JsonFacets(models.Model):
    """model for the json_facets join table"""

    json_lookup_id = models.IntegerField()
    facets_lookup_id = models.IntegerField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'json_facets'


class JsonLookup(models.Model):
    """model for the json_lookup table"""
    dataset = models.ForeignKey(Datasets, models.DO_NOTHING, db_column="dataset_id")
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
    """model for the json_files table"""
    meta = models.ForeignKey(JsonLookup, models.DO_NOTHING, db_column="json_lookup_id")

    file = models.TextField()
    type = models.CharField(max_length=32)
    version = models.IntegerField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'json_files'
