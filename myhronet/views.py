# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, redirect, render
from .forms import URLForm
from .models import URL
from .utils import get_client_ip


def home(request):
    form = URLForm()
    if request.method == 'POST':
        # Necessary to create a copy, as this QueryDict instance is immutable
        data = request.POST.copy()
        data['ip'] = get_client_ip(request)
        form = URLForm(data)
        valid_url = True
        if form.is_valid():
            form.save()
            hashcode = form.instance.hashcode
            new_url = form.instance.short_url(request)
            orig_url = form.instance.longurl
        elif 'longurl' in form.errors:
            # Check if the error was caused by a repeated URL...
            url_db = URL.objects.filter(longurl=form.instance.longurl).first()
            if url_db:
                hashcode = url_db.hashcode
                new_url = url_db.short_url(request)
                orig_url = url_db.longurl
            # Or it is just invalid.
            else:
                valid_url = False
        else:
            valid_url = False
        if not valid_url:
            return render(request, 'home.html', locals())
        orig_size = len(orig_url)
        new_size = len(new_url)
        if new_size < orig_size:
            diff_chars = orig_size - new_size
            diff_percent = int(
                round(100 - (100 * (new_size / float(orig_size))))
            )
        elif new_size > orig_size:
            diff_chars = new_size - orig_size
            diff_percent = int(
                round((new_size * 100 / float(orig_size)) - 100)
            )
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
