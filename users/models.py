from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user', default='', blank=True, null=True)
    type = models.CharField(max_length=200)
    action = models.CharField(max_length=200)
    content = models.CharField(max_length=200)
    object = models.CharField(max_length=200)
