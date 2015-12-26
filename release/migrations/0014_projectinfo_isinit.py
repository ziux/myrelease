# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0013_projectinfo_lastretime'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectinfo',
            name='isinit',
            field=models.BooleanField(default=datetime.datetime(2015, 10, 15, 8, 37, 48, 120648, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
