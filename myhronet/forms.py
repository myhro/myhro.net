# -*- coding: utf-8 -*-

import re
from django import forms
from .models import URL


class URLForm(forms.ModelForm):
    def clean(self, *args, **kwargs):
        cleaned_data = super(URLForm, self).clean(*args, **kwargs)
        if not re.match('^https?://.*\.[a-z]{2,}', cleaned_data['longurl']):
            raise forms.ValidationError('URL inválida.')
        return cleaned_data

    def save(self, *args, **kwargs):
        if URL.objects.count():
            last = URL.objects.latest('id').pk + 1
            alphabet='0123456789abcdefghijklmnopqrstuvwxyz'
            base36 = ''
            if last < len(alphabet):
                self.instance.hashcode = alphabet[last]
            while last != 0:
                last, i = divmod(last, len(alphabet))
                base36 = alphabet[i] + base36
            self.instance.hashcode = base36
        else:
            self.instance.hashcode = '1'
        super(URLForm, self).save(*args, **kwargs)

    class Meta:
        model = URL
        fields = ('longurl',)
