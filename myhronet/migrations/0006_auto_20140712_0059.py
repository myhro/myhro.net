# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myhronet', '0005_country_country_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='ip',
            field=models.GenericIPAddressField(null=True, blank=True),
        ),
    ]
