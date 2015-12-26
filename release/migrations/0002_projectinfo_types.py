# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectinfo',
            name='types',
            field=models.CharField(default=datetime.datetime(2015, 10, 12, 3, 41, 27, 567548, tzinfo=utc), max_length=100),
            preserve_default=False,
        ),
    ]
