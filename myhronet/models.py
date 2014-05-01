# -*- coding: utf-8 -*-

from django.db import models


class URL(models.Model):
    hashcode = models.CharField(max_length=10, unique=True, db_index=True, null=True)
    longurl = models.CharField(max_length=1024, unique=True, db_index=True, null=True)
    views = models.IntegerField(default=0)
    ip = models.GenericIPAddressField(null=True)
    data = models.DateTimeField(auto_now_add=True, null=True)

    def short_url(self, request):
        return ''.join([request.scheme, '://', request.get_host(), '/', self.hashcode])

    def __unicode__(self):
        return ' - '.join([self.hashcode, self.longurl])
