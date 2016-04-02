# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0016_auto_20160330_1413'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cityarea',
            old_name='area_name',
            new_name='label',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='count_0_6',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='count_16_30',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='count_31_45',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='count_46_60',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='count_7_15',
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='avg_household_occupants',
            field=models.IntegerField(null=True, db_column='AVG_HOUSEHOLD_OCCUPANTS'),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='avg_pg_occupancy',
            field=models.IntegerField(null=True, db_column='AVG_PG_OCCUPANCY'),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='bachelor_tenants_allowed',
            field=models.BooleanField(default=False, db_column='BACHELOR_TENANTS_ALLOWED'),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='count_0_5',
            field=models.IntegerField(null=True, db_column='COUNT_0-5', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='count_15_25',
            field=models.IntegerField(null=True, db_column='COUNT_15-25', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='count_25_60',
            field=models.IntegerField(null=True, db_column='COUNT_25-60', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='count_5_15',
            field=models.IntegerField(null=True, db_column='COUNT_5-15', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='past_campaign_occurred',
            field=models.BooleanField(default=False, db_column='PAST_CAMPAIGN_OCCURRED'),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='pg_flat_count',
            field=models.IntegerField(null=True, db_column='PG_FLAT_COUNT'),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='service_household_count',
            field=models.IntegerField(null=True, db_column='SERVICE_HOUSEHOLD_COUNT'),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='society_weekly_off',
            field=models.CharField(max_length=30, null=True, db_column='SOCIETY_WEEKLY_OFF', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='vacant_flat_count',
            field=models.IntegerField(null=True, db_column='VACANT_FLAT_COUNT'),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='women_occupants',
            field=models.IntegerField(null=True, db_column='WOMEN_OCCUPANTS'),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='working_women_count',
            field=models.IntegerField(null=True, db_column='WORKING_WOMEN_COUNT'),
        ),
        migrations.AlterField(
            model_name='inventorysummary',
            name='timing',
            field=models.CharField(max_length=20, null=True, db_column='STALL_TIMING', blank=True),
        ),
    ]
