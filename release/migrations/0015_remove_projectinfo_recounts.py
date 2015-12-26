# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0014_projectinfo_isinit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectinfo',
            name='recounts',
        ),
    ]
