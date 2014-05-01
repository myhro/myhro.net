# -*- coding: utf-8 -*-

from django import test
from .forms import URLForm
from .models import URL


class URLFormTestCase(test.TestCase):
    def test_invalid_url(self):
        num_urls = URL.objects.count()
        form = URLForm(data={'longurl': 'ftp://cdrom.com'})
        form.instance.ip = '127.0.0.1'
        if form.is_valid():
            form.save()
        self.assertEqual(URL.objects.count(), num_urls)

    def test_new_url(self):
        num_urls = URL.objects.count()
        form = URLForm(data={'longurl': 'http://google.com'})
        form.instance.ip = '127.0.0.1'
        if form.is_valid():
            form.save()
        self.assertEqual(URL.objects.count(), num_urls + 1)

    def test_properly_saved_url(self):
        new_url = 'http://google.com'
        num_urls = URL.objects.count()
        form = URLForm(data={'longurl': new_url})
        form.instance.ip = '127.0.0.1'
        if form.is_valid():
            form.save()
        self.assertEqual(URL.objects.last().longurl, new_url)

    def test_same_url_twice(self):
        num_urls = URL.objects.count()
        form = URLForm(data={'longurl': 'http://google.com'})
        form.instance.ip = '127.0.0.1'
        if form.is_valid():
            form.save()
        form = URLForm(data={'longurl': 'http://google.com'})
        form.instance.ip = '127.0.0.1'
        if form.is_valid():
            form.save()
        self.assertEqual(URL.objects.count(), num_urls + 1)
