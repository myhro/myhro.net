# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, redirect, render
from .forms import URLForm
from .models import URL


def home(request):
    form = URLForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.ip = request.META['REMOTE_ADDR']
            form.save()
            hashcode = form.instance.hashcode
            new_url = form.instance.short_url(request)
            orig_url = form.instance.longurl
        elif 'longurl' in form.errors:
            # Verifica se o erro foi causado por uma URL repetida...
            url_db = URL.objects.filter(longurl=form.instance.longurl).first()
            if url_db:
                hashcode = url_db.hashcode
                new_url = url_db.short_url(request)
                orig_url = url_db.longurl
            # Ou simplesmente inválida.
            else:
                return render(request, 'home.html', locals())
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

def retrieve(request, hashcode):
    stats = False
    if hashcode.endswith('-'):
        hashcode = hashcode[:-1]
        stats = True
    url_db = get_object_or_404(URL, hashcode=hashcode)
    if stats:
        num_views = url_db.views
        orig_url = url_db.longurl
        short_url = url_db.short_url(request)
        return render(request, 'stats.html', locals())
    url_db.views = url_db.views + 1
    url_db.save()
    return redirect(url_db.longurl)
