"""import models"""
from django.db import models
from datasets.models import *


# data tables
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
    session = models.CharField(max_length=24, default=None)
    json_lookup = models.ForeignKey(JsonLookup, on_delete=models.PROTECT)
    json_file = models.ForeignKey(JsonFiles, on_delete=models.PROTECT)
    errorcode = models.CharField(max_length=128, default='')
    comment = models.CharField(max_length=256, default=None)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'json_errors'


class JsonActlog(models.Model):
    """ model for the json_errors DB table """
    session = models.CharField(max_length=24, default=None)
    json_lookup = models.ForeignKey(JsonLookup, on_delete=models.PROTECT)
    json_file = models.ForeignKey(JsonFiles, on_delete=models.PROTECT)
    activitylog = models.CharField(max_length=2048, default='')
    comment = models.CharField(max_length=256, default=None)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'json_actlog'


# facet tables
class FacetLookup(models.Model):
    """ model for the facet_lookup DB table """
    uniqueid = models.CharField(max_length=128)
    title = models.CharField(max_length=256)
    type = models.CharField(max_length=16)
    graphname = models.CharField(max_length=256)
    currentversion = models.IntegerField()
    auth_user_id = models.PositiveIntegerField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'facet_lookup'


class FacetFiles(models.Model):
    """ model for the facet_files DB table """
    facet_lookup = models.ForeignKey(FacetLookup, on_delete=models.PROTECT)
    file = models.TextField()
    type = models.CharField(max_length=32)
    version = models.IntegerField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'facet_files'


class FacetActlog(models.Model):
    """ model for the facet_actlog DB table """
    facet_lookup = models.ForeignKey(FacetLookup, on_delete=models.PROTECT)
    facet_file = models.ForeignKey(FacetFiles, on_delete=models.PROTECT)
    activitycode = models.CharField(max_length=16)
    comment = models.CharField(max_length=256)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'facet_actlog'


class FacetErrors(models.Model):
    """ model for the facet_errors DB table """
    facet_lookup = models.ForeignKey(FacetLookup, on_delete=models.PROTECT)
    facet_file = models.ForeignKey(FacetFiles, on_delete=models.PROTECT)
    errorcode = models.CharField(max_length=16)
    comment = models.CharField(max_length=256)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'facet_errors'


# aspect files
class AspectLookup(models.Model):
    """ model for the aspect_lookup DB table """
    uniqueid = models.CharField(max_length=128)
    title = models.CharField(max_length=256)
    type = models.CharField(max_length=16)
    graphname = models.CharField(max_length=256)
    currentversion = models.IntegerField()
    auth_user_id = models.PositiveIntegerField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'aspect_lookup'


class AspectFiles(models.Model):
    """ model for the aspect_files DB table """
    aspect_lookup = models.ForeignKey(AspectLookup, on_delete=models.PROTECT)
    file = models.TextField()
    type = models.CharField(max_length=32)
    version = models.IntegerField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'aspect_files'


class AspectActlog(models.Model):
    """ model for the aspect_actlog DB table """
    aspect_lookup = models.ForeignKey(AspectLookup, on_delete=models.PROTECT)
    aspect_file = models.ForeignKey(AspectFiles, on_delete=models.PROTECT)
    activitycode = models.CharField(max_length=16)
    comment = models.CharField(max_length=256)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'aspect_actlog'


class AspectErrors(models.Model):
    """ model for the aspect_errors DB table """
    aspect_lookup = models.ForeignKey(AspectLookup, on_delete=models.PROTECT)
    aspect_file = models.ForeignKey(AspectFiles, on_delete=models.PROTECT)
    errorcode = models.CharField(max_length=16)
    comment = models.CharField(max_length=256)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'aspect_errors'


# join tables
class JsonAspects(models.Model):
    """model for the json_aspects join table"""
    json_lookup = models.ForeignKey(JsonLookup, on_delete=models.PROTECT)
    aspects_lookup = models.ForeignKey(AspectLookup, on_delete=models.PROTECT)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'json_aspects'


class JsonFacets(models.Model):
    """model for the json_facets join table"""
    json_lookup = models.ForeignKey(JsonLookup, on_delete=models.PROTECT)
    facets_lookup = models.ForeignKey(FacetLookup, on_delete=models.PROTECT)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'json_facets'
