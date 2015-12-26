# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0011_projectinfo_recounts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectinfo',
            name='recounts',
            field=models.IntegerField(),
        ),
    ]
