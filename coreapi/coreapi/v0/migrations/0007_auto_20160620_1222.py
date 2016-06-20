# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0006_auto_20160620_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliertypesociety',
            name='daily_electricity_charges',
            field=models.IntegerField(default=0, null=True, db_column='DAILY_ELECTRICITY_CHARGES', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='electricity_available',
            field=models.BooleanField(default=False, db_column='ELECTRICITY_AVAILABLE'),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='sound_available',
            field=models.BooleanField(default=False, db_column='SOUND_AVAILABLE'),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='stall_timing',
            field=models.CharField(max_length=10, null=True, db_column='STALL_TIMING', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='street_furniture_available',
            field=models.BooleanField(default=False, db_column='STREET_FURNITURE_AVAILABLE'),
        ),
    ]
