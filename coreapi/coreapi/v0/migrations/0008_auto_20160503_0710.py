# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0007_auto_20160429_1354'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stallinventory',
            old_name='stall_furniture_details',
            new_name='furniture_details',
        ),
        migrations.RemoveField(
            model_name='stallinventory',
            name='electricity_available_stalls',
        ),
        migrations.RemoveField(
            model_name='stallinventory',
            name='stall_availability',
        ),
        migrations.RemoveField(
            model_name='stallinventory',
            name='stall_furniture_available',
        ),
        migrations.RemoveField(
            model_name='stallinventory',
            name='stall_inventory_status',
        ),
        migrations.RemoveField(
            model_name='stallinventory',
            name='type',
        ),
        migrations.AddField(
            model_name='stallinventory',
            name='car_premium',
            field=models.BooleanField(default=False, db_column='CAR_PREMIUM'),
        ),
        migrations.AddField(
            model_name='stallinventory',
            name='car_standard',
            field=models.BooleanField(default=False, db_column='CAR_STANDARD'),
        ),
        migrations.AddField(
            model_name='stallinventory',
            name='electricity_available',
            field=models.BooleanField(default=False, db_column='ELECTRICITY_AVAILABLE_STALLS'),
        ),
        migrations.AddField(
            model_name='stallinventory',
            name='furniture_available',
            field=models.BooleanField(default=False, db_column='STALL_FURNITURE_AVAILABLE'),
        ),
        migrations.AddField(
            model_name='stallinventory',
            name='stall_canopy',
            field=models.BooleanField(default=False, db_column='STALL_CANOPY'),
        ),
        migrations.AddField(
            model_name='stallinventory',
            name='stall_evening',
            field=models.BooleanField(default=False, db_column='STALL_EVENING'),
        ),
        migrations.AddField(
            model_name='stallinventory',
            name='stall_medium',
            field=models.BooleanField(default=False, db_column='STALL_MEDIUM'),
        ),
        migrations.AddField(
            model_name='stallinventory',
            name='stall_morning',
            field=models.BooleanField(default=False, db_column='STALL_MORNING'),
        ),
        migrations.AddField(
            model_name='stallinventory',
            name='stall_small',
            field=models.BooleanField(default=False, db_column='STALL_SMALL'),
        ),
        migrations.AddField(
            model_name='stallinventory',
            name='stall_time_both',
            field=models.BooleanField(default=False, db_column='STALL_TIME_BOTH'),
        ),
        migrations.AlterField(
            model_name='stallinventory',
            name='sound_system_allowed',
            field=models.BooleanField(default=False, db_column='SOUND_SYSTEM_ALLOWED'),
        ),
        migrations.AlterField(
            model_name='stallinventory',
            name='stall_timing',
            field=models.CharField(max_length=20, null=True, db_column='STALL_TIMINGS', blank=True),
        ),
    ]
