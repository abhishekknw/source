# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='society_subarea',
            field=models.CharField(default=None, max_length=50, null=True, db_column='SOCIETY_SUBAREA', blank=True),
        ),
    ]
