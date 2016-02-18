# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0024_auto_20160217_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='flattype',
            name='flat_count',
            field=models.IntegerField(null=True, db_column='FLAT_COUNT', blank=True),
        ),
        migrations.AlterField(
            model_name='flattype',
            name='average_rent_per_sqft',
            field=models.FloatField(null=True, db_column='AVERAGE_RENT_PER_SQFT', blank=True),
        ),
    ]
