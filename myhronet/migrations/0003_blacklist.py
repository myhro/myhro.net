# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'myhronet', b'0002_auto_20140501_1545'),
    ]

    operations = [
        migrations.CreateModel(
            name=b'Blacklist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'domain', models.CharField(max_length=255, unique=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
