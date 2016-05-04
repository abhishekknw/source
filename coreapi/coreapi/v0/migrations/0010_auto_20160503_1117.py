# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0009_auto_20160503_0752'),
    ]

    operations = [
        migrations.CreateModel(
            name='StallInventory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('adinventory_id', models.CharField(max_length=22, db_column='ADINVENTORY_ID')),
                ('stall_small', models.BooleanField(default=False, db_column='STALL_SMALL')),
                ('stall_canopy', models.BooleanField(default=False, db_column='STALL_CANOPY')),
                ('stall_medium', models.BooleanField(default=False, db_column='STALL_MEDIUM')),
                ('car_standard', models.BooleanField(default=False, db_column='CAR_STANDARD')),
                ('car_premium', models.BooleanField(default=False, db_column='CAR_PREMIUM')),
                ('stall_morning', models.BooleanField(default=False, db_column='STALL_MORNING')),
                ('stall_evening', models.BooleanField(default=False, db_column='STALL_EVENING')),
                ('stall_time_both', models.BooleanField(default=False, db_column='STALL_TIME_BOTH')),
                ('stall_location', models.CharField(max_length=50, null=True, db_column='STALL_LOCATION', blank=True)),
                ('electricity_available', models.BooleanField(default=False, db_column='ELECTRICITY_AVAILABLE_STALLS')),
                ('electricity_charges_daily', models.FloatField(max_length=50, null=True, db_column='ELECTRICITY_CHARGES_DAILY', blank=True)),
                ('sound_system_allowed', models.BooleanField(default=False, db_column='SOUND_SYSTEM_ALLOWED')),
                ('furniture_available', models.BooleanField(default=False, db_column='STALL_FURNITURE_AVAILABLE')),
                ('furniture_details', models.CharField(max_length=50, null=True, db_column='STALL_FURNITURE_DETAILS', blank=True)),
                ('stall_size', models.CharField(max_length=20, null=True, db_column='STALL_SIZE', blank=True)),
                ('stall_timing', models.CharField(max_length=20, null=True, db_column='STALL_TIMINGS', blank=True)),
                ('supplier', models.ForeignKey(related_name='stalls', db_column='SUPPLIER_ID', blank=True, to='v0.SupplierTypeSociety', null=True)),
            ],
            options={
                'db_table': 'stall_inventory',
            },
        ),
        migrations.RemoveField(
            model_name='stallcarinventory',
            name='supplier',
        ),
        migrations.DeleteModel(
            name='StallCarInventory',
        ),
    ]
