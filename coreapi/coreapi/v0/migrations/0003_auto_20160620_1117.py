# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0002_auto_20160620_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='society_subarea',
            field=models.CharField(max_length=50, null=True, db_column='SOCIETY_SUBAREA', blank=True),
        ),
    ]
