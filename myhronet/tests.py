# -*- coding: utf-8 -*-

import random
import string
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
        self.assertEqual(URL.objects.count(), num_urls + 1)
        self.assertEqual(URL.objects.last().longurl, new_url)

    def test_same_url_twice(self):
        num_urls = URL.objects.count()
        form = URLForm(data={'longurl': 'http://google.com'})
        form.instance.ip = '127.0.0.1'
        if form.is_valid():
            form.save()
        self.assertEqual(URL.objects.count(), num_urls + 1)
        form = URLForm(data={'longurl': 'http://google.com'})
        form.instance.ip = '127.0.0.1'
        if form.is_valid():
            form.save()
        self.assertEqual(URL.objects.count(), num_urls + 1)


class ViewsTestCase(test.TestCase):
    def setUp(self):
        self.client = test.client.Client()
        self.post_valid_url = {'longurl': 'http://google.com'}

    def test_invalid_longurl(self):
        response = self.client.post('/', {'longurl': 'not.a.valid/url'})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'longurl', 'Invalid URL.')
        self.assertTemplateUsed(response, 'home.html')

    def test_invalid_shorturl(self):
        response = self.client.get('/dontexist')
        self.assertEqual(response.status_code, 404)

    def test_multiple_urls_to_check_base36_conversion(self):
        for i in xrange(36):
            random_domain = ''.join(
                [random.choice(string.ascii_lowercase) for x in xrange(10)]
            )
            random_url = 'http://{domain}.com/'.format(domain=random_domain)
            response = self.client.post('/', {'longurl': random_url})
            self.assertContains(response, random_url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'done.html')

    def test_same_url_twice(self):
        num_urls = URL.objects.count()
        # Save a new URL
        response = self.client.post('/', self.post_valid_url)
        self.assertEqual(URL.objects.count(), num_urls + 1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'done.html')
        # Load an existing URL
        response = self.client.post('/', self.post_valid_url)
        # It shouldn't save a new URL on the second try
        self.assertEqual(URL.objects.count(), num_urls + 1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'done.html')

    def test_stats_valid_url(self):
        response = self.client.post('/', self.post_valid_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'done.html')
        response = self.client.get('/1-')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stats.html')

    def test_valid_shorturl(self):
        response = self.client.post('/', self.post_valid_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'done.html')
        response = self.client.get('/1')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.post_valid_url['longurl'])

    def test_valid_longurl(self):
        response = self.client.post('/', self.post_valid_url)
        self.assertContains(response, self.post_valid_url['longurl'])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'done.html')
