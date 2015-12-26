# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0007_auto_20151013_0625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectinfo',
            name='name',
            field=models.CharField(unique=True, max_length=200),
        ),
    ]
