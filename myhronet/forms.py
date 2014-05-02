# -*- coding: utf-8 -*-

import re
from django import forms
from django.utils.translation import ugettext as _
from .models import URL


class URLForm(forms.ModelForm):
    def clean_longurl(self, *args, **kwargs):
        cleaned_data = super(URLForm, self).clean(*args, **kwargs)
        if not re.match('^https?://.*\.[a-z]{2,}', cleaned_data['longurl']):
            raise forms.ValidationError(_('Invalid URL.'))
        return cleaned_data['longurl']

    class Meta:
        model = URL
        fields = ('longurl',)
        labels = {
            'longurl': '',
        }
        widgets = {
            'longurl': forms.TextInput(attrs={'size': '50'}),
        }
