# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0008_auto_20151013_0647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='release',
            name='retime',
            field=models.TimeField(max_length=200),
        ),
    ]
