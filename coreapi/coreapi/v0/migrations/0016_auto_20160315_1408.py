# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0015_auto_20160315_1022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventorysummary',
            name='total_campaigns',
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='electricity',
            field=models.BooleanField(default=False, db_column='ELECTRICITY_SEPARATE'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='furniture',
            field=models.BooleanField(default=False, db_column='FURNITURE_AVAILABLE'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='stallAllowed',
            field=models.BooleanField(default=False, db_column='STALL_ALLOWED'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='stall_type',
            field=models.CharField(max_length=20, null=True, db_column='STALL_TYPE'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='standeeAllowed',
            field=models.BooleanField(default=False, db_column='STANDEE_ALLOWED'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='standee_type',
            field=models.CharField(max_length=20, null=True, db_column='STANDEE_TYPE'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='timing',
            field=models.CharField(max_length=20, null=True, db_column='STALL_TIMING'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='total_poster_campaigns',
            field=models.IntegerField(null=True, db_column='TOTAL_POSTER_CAMPAIGNS'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='total_stall_count',
            field=models.IntegerField(null=True, db_column='TOTAL_STALL_COUNT'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='total_standee_campaigns',
            field=models.IntegerField(null=True, db_column='TOTAL_STANDEE_CAMPAIGNS'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='total_standee_count',
            field=models.IntegerField(null=True, db_column='TOTAL_STANDEE_COUNT'),
        ),
    ]
