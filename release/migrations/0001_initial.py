# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='projectinfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('devsvnurl', models.CharField(max_length=300)),
                ('devsvnuser', models.CharField(max_length=100)),
                ('devsvnpasswd', models.CharField(max_length=200)),
                ('releasesvnurl', models.CharField(max_length=300)),
                ('releasesvnuser', models.CharField(max_length=100)),
                ('releasesvnpasswd', models.CharField(max_length=200)),
                ('proxybasedirectory', models.CharField(max_length=200)),
                ('releasebasedirectory', models.CharField(max_length=200)),
            ],
        ),
    ]
