# -*- coding: utf-8 -*-

from django.shortcuts import redirect, render
from .forms import URLForm
from .models import URL


def home(request):
    form = URLForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.ip = request.META['REMOTE_ADDR']
            form.save()
            hashcode = form.instance.hashcode
            orig_url = form.instance.longurl
        elif 'longurl' in form.errors:
            url_bd = URL.objects.get(longurl=form.instance.longurl)
            hashcode = url_bd.hashcode
            orig_url = url_bd.longurl
        else:
            return render(request, 'home.html', locals())
        new_url = ''.join([request.META['wsgi.url_scheme'], '://', request.get_host(), request.path, hashcode])
        orig_size = len(orig_url)
        new_size = len(new_url)
        if new_size < orig_size:
            diff_chars = orig_size - new_size
            diff_percent = int(round(100 - (100 * (new_size / float(orig_size)))))
        elif new_size > orig_size:
            diff_chars = new_size - orig_size
            diff_percent = int(round((new_size * 100 / float(orig_size)) - 100))
        return render(request, 'done.html', locals())
    return render(request, 'home.html', locals())
