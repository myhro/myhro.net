# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myhronet', '0004_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='country_code',
            field=models.CharField(max_length=2, unique=True, null=True),
            preserve_default=True,
        ),
    ]
