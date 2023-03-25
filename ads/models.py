import json

from django.db import models


class Ad(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=250)
    address = models.CharField(max_length=100, blank=True)
    is_published = models.BooleanField()


class Category(models.Model):
    name = models.CharField(max_length=100)


