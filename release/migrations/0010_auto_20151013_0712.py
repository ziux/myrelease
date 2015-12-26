# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0009_auto_20151013_0706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='release',
            name='retime',
            field=models.DateTimeField(max_length=200),
        ),
    ]
