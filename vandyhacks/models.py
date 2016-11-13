import datetime

from django.db import models
from django.utils import timezone

import retrival.py as ret
class Graph(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=10000, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    industries = models.ManyToManyField(Industry)
    
    def __unicode__(self):
        return unicode(self.title)


class Industry(models.Model):
    name = models.CharField(max_length = 60)
    url = models.URLField()

    def __unicode__(self):
        return unicode(self.name)

