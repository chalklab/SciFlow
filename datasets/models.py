"""import models"""
from django.db import models

# Create your models here.


class Datasets(models.Model):
    """ getting data from the substances DB table"""
    name = models.CharField(max_length=64, default='')
    source = models.CharField(max_length=64, default='')
    sourceurl = models.CharField(max_length=256, default='')
    count = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'datasets'
