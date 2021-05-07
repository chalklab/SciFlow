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
