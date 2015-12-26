# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0002_projectinfo_types'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectinfo',
            name='proxybasedirectory',
        ),
        migrations.RemoveField(
            model_name='projectinfo',
            name='releasebasedirectory',
        ),
    ]
