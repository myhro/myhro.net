# -*- coding: utf-8 -*-

import string
from django.db import models


class Blacklist(models.Model):
    domain = models.CharField(max_length=255, unique=True, null=True)

    def __unicode__(self):
        return self.domain


class Country(models.Model):
    country_code = models.CharField(max_length=2, unique=True, null=True)

    def __unicode__(self):
        return self.country_code


class URL(models.Model):
    hashcode = models.CharField(max_length=10, unique=True,
                                db_index=True, null=True)
    longurl = models.CharField(max_length=1024, unique=True,
                               db_index=True, null=True)
    views = models.IntegerField(default=0)
    ip = models.GenericIPAddressField(null=True)
    data = models.DateTimeField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            if URL.objects.count():
                last = URL.objects.latest('id').pk + 1
                alphabet = string.digits + string.ascii_lowercase
                base36 = ''
                while last != 0:
                    last, i = divmod(last, len(alphabet))
                    base36 = alphabet[i] + base36
                self.hashcode = base36
            else:
                self.hashcode = '1'
        return super(URL, self).save(*args, **kwargs)

    def short_url(self, request):
        return ''.join([
            request.scheme,
            '://', request.get_host(),
            '/', self.hashcode,
        ])

    def __unicode__(self):
        return ' - '.join([self.hashcode, self.longurl])
