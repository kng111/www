from django.db import models
from django.contrib.auth.models import Permission


class Role(models.Model):
    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField(Permission)

    def __str__(self):
        return self.name


class MyGroup(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
