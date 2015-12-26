# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0005_release_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='release',
            name='name',
            field=models.ForeignKey(related_name='project_release', to='release.projectinfo'),
        ),
    ]
