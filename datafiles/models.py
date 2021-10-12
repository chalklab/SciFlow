"""import models"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class References(models.Model):
    id = models.SmallAutoField(primary_key=True)
    journal = models.CharField(max_length=256, blank=True, null=True)
    authors = models.CharField(max_length=2048, blank=True, null=True)
    aulist = models.CharField(max_length=1024, blank=True, null=True)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    volume = models.CharField(max_length=12, blank=True, null=True)
    issue = models.CharField(max_length=16, blank=True, null=True)
    startpage = models.CharField(max_length=16, blank=True, null=True)
    endpage = models.CharField(max_length=16, blank=True, null=True)
    title = models.CharField(max_length=512, blank=True, null=True)
    url = models.CharField(max_length=256, blank=True, null=True)
    doi = models.CharField(max_length=256)
    count = models.SmallIntegerField(blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'references'


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


class JsonLookup(models.Model):
    """ model for the json_lookup DB table """
    dataset = models.ForeignKey(Datasets, on_delete=models.PROTECT, db_column='dataset_id')
    reference = models.ForeignKey(References, on_delete=models.PROTECT, db_column='reference_id')
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
    jhash = models.CharField(max_length=52, blank=True, null=True)
    comments = models.CharField(max_length=32, blank=True, null=True)
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
    aspect_lookup = models.ForeignKey(AspectLookup, on_delete=models.PROTECT)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'json_aspects'


class JsonFacets(models.Model):
    """model for the json_facets join table"""
    json_lookup = models.ForeignKey(JsonLookup, on_delete=models.PROTECT)
    facet_lookup = models.ForeignKey(FacetLookup, on_delete=models.PROTECT)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'json_facets'
