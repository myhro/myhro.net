# -*- coding: utf-8 -*-

import re
from django import forms
from django.conf import settings
from django.contrib.gis import geoip
from django.utils.translation import ugettext as _
from .models import Blacklist, Country, URL


class URLForm(forms.ModelForm):
    def clean_ip(self, *args, **kwargs):
        cleaned_data = super(URLForm, self).clean(*args, **kwargs)
        if geoip.HAS_GEOIP:
            g = geoip.GeoIP(settings.GEOIP_PATH)
            country = g.country_code(cleaned_data['ip'])
            if country and not Country.objects.filter(country_code=country):
                raise forms.ValidationError(_('Forbidden Country'))
        return cleaned_data['ip']

    def clean_longurl(self, *args, **kwargs):
        cleaned_data = super(URLForm, self).clean(*args, **kwargs)
        if not re.match('^https?://.*\.[a-z]{2,}', cleaned_data['longurl']):
            raise forms.ValidationError(_('Invalid URL'))
        for i in Blacklist.objects.all():
            if i.domain in cleaned_data['longurl']:
                raise forms.ValidationError(_('Forbidden URL'))
        return cleaned_data['longurl']

    class Meta:
        model = URL
        fields = ('ip', 'longurl')
        labels = {
            'longurl': '',
        }
        widgets = {
            'longurl': forms.TextInput(attrs={'size': '50'}),
        }
