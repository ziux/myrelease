# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0004_release'),
    ]

    operations = [
        migrations.AddField(
            model_name='release',
            name='comments',
            field=models.CharField(default=datetime.datetime(2015, 10, 13, 1, 36, 58, 300775, tzinfo=utc), max_length=800),
            preserve_default=False,
        ),
    ]
