# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='disable',
        ),
        migrations.AddField(
            model_name='citysubarea',
            name='locality_rating',
            field=models.CharField(max_length=100, null=True, db_column='LOCALITY_RATING'),
        ),
    ]
