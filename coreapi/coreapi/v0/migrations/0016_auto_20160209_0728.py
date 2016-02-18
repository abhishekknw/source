# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0015_stallinventory_stall_availability'),
    ]

    operations = [
        migrations.AlterField(
            model_name='societyflat',
            name='flat_size_per_sq_feet_builtup_area',
            field=models.FloatField(null=True, db_column='FLAT_SIZE_PER_SQ_FEET_BUILTUP_AREA', blank=True),
        ),
        migrations.AlterField(
            model_name='societyflat',
            name='flat_size_per_sq_feet_carpet_area',
            field=models.FloatField(null=True, db_column='FLAT_SIZE_PER_SQ_FEET_CARPET_AREA', blank=True),
        ),
        migrations.AlterField(
            model_name='stallinventory',
            name='stall_size',
            field=models.CharField(max_length=20, null=True, db_column='STALL_SIZE', blank=True),
        ),
    ]
