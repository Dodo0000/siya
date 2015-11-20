from django.db import models

from django.contrib.auth.models import Group, Permission

# Create your models here.


class AlmsGroup(models.Model):
    group = Group
    name = models.CharField(max_length=255)
