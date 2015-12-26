# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0010_auto_20151013_0712'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectinfo',
            name='recounts',
            field=models.IntegerField(default=0, max_length=10),
            preserve_default=False,
        ),
    ]
