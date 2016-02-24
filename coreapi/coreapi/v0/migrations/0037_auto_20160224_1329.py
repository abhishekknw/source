# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0036_auto_20160223_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='average_rent',
            field=models.FloatField(null=True, db_column='AVERAGE_RENT', blank=True),
        ),
    ]
