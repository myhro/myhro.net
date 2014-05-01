# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'myhronet', b'0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name=b'url',
            name=b'ip',
            field=models.GenericIPAddressField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name=b'url',
            name=b'longurl',
            field=models.CharField(max_length=1024, unique=True, null=True, db_index=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name=b'url',
            name=b'data',
            field=models.DateTimeField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name=b'url',
            name=b'views',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name=b'url',
            name=b'hashcode',
            field=models.CharField(max_length=10, unique=True, null=True, db_index=True),
            preserve_default=True,
        ),
    ]
