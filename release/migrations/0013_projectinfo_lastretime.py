# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0012_auto_20151013_0732'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectinfo',
            name='lastretime',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 13, 8, 15, 17, 106590, tzinfo=utc), max_length=200),
            preserve_default=False,
        ),
    ]
