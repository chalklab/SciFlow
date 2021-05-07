""" models for the crosswalks DB """

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Nspaces(models.Model):
    """ crosswalks nspaces table """
    name = models.CharField(max_length=64)
    ns = models.CharField(max_length=8)
    path = models.CharField(unique=True, max_length=64)
    homepage = models.CharField(max_length=128)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'nspaces'


class Ontterms(models.Model):
    """ crosswalks ontterms table """
    title = models.CharField(max_length=256)
    definition = models.CharField(max_length=2048, blank=True, null=True)
    code = models.CharField(max_length=64)
    nspace = models.ForeignKey(Nspaces, on_delete=models.DO_NOTHING)
    sdsection = models.CharField(max_length=11, blank=True, null=True)
    sdsubsection = models.CharField(max_length=64, blank=True, null=True)
    to_remove = models.CharField(max_length=8, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ontterms'


class Metadata(models.Model):
    """ crosswalks metadata table """
    table = models.CharField(max_length=128)
    field = models.CharField(max_length=128)
    label = models.CharField(max_length=16, blank=True, null=True)
    ontterm = models.ForeignKey(Ontterms, on_delete=models.DO_NOTHING)
    sdsection = models.CharField(max_length=11, blank=True, null=True)
    sdsubsection = models.CharField(max_length=32, blank=True, null=True)
    sdsubsubsection = models.CharField(max_length=64, blank=True, null=True)
    category = models.CharField(max_length=64, blank=True, null=True)
    unit = models.CharField(max_length=32, blank=True, null=True)
    datatype = models.CharField(max_length=22, blank=True, null=True)
    output = models.CharField(max_length=10, blank=True, null=True)
    group = models.CharField(max_length=512, blank=True, null=True)
    intlinks = models.CharField(max_length=1024, blank=True, null=True)
    meta = models.CharField(max_length=64, blank=True, null=True)
    ignore = models.CharField(max_length=32, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'metadata'
