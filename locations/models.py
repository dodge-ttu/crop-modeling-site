from django.db import models
from datetime import datetime


class Location(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    site_id = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(max_length=500, null=True)
    latitude = models.FloatField(default=33.88, blank=False, null=True)
    longitude = models.FloatField(default=-101.22, blank=False, null=True)
    is_published = models.BooleanField(default=False, null=True)
    post_date = models.DateTimeField(default=datetime.now, null=True)

    def __str__(self):
        return self.name
