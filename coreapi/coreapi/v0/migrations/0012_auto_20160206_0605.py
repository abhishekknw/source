# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0011_auto_20160205_1101'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stallinventory',
            name='current_price_stall',
        ),
        migrations.AddField(
            model_name='stallinventory',
            name='stall_size',
            field=models.CharField(default=0.0, max_length=20, null=True, db_column='STALL_SIZE', blank=True),
        ),
        migrations.AddField(
            model_name='stallinventory',
            name='stall_timing',
            field=models.CharField(max_length=10, null=True, db_column='STALL_TIMINGS', blank=True),
        ),
        migrations.AlterField(
            model_name='stallinventory',
            name='electricity_charges_daily',
            field=models.FloatField(max_length=50, null=True, db_column='ELECTRICITY_CHARGES_DAILY', blank=True),
        ),
    ]
