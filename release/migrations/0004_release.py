# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0003_auto_20151012_1053'),
    ]

    operations = [
        migrations.CreateModel(
            name='release',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('retime', models.CharField(max_length=200)),
                ('releaser', models.CharField(max_length=200)),
                ('restatus', models.CharField(max_length=200)),
                ('relog', models.CharField(max_length=800)),
            ],
        ),
    ]
