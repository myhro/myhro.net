# -*- coding: utf-8 -*-

from django.db import models


class URL(models.Model):
    hashcode = models.CharField(max_length=10, unique=True, db_index=True)
    longurl = models.CharField(max_length=1024, unique=True, db_index=True)
    views = models.IntegerField(default=0)
    ip = models.GenericIPAddressField()
    data = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return ' - '.join([self.hashcode, self.longurl])
