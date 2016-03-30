# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0013_auto_20160314_0705'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventorySummary',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('poster_allowed_nb', models.BooleanField(default=False, db_column='POSTER_ALLOWED_NB')),
                ('poster_allowed_lift', models.BooleanField(default=False, db_column='POSTER_ALLOWED_LIFT')),
                ('standee_allowed', models.BooleanField(default=False, db_column='STANDEE_ALLOWED')),
                ('stall_allowed', models.BooleanField(default=False, db_column='STALL_ALLOWED')),
                ('nb_A4_allowed', models.BooleanField(default=False, db_column='NB_A4_ALLOWED')),
                ('nb_A3_allowed', models.BooleanField(default=False, db_column='NB_A3_ALLOWED')),
                ('nb_count', models.IntegerField(null=True, db_column='NB_COUNT')),
                ('poster_per_nb', models.IntegerField(null=True, db_column='POSTER_PER_NB')),
                ('total_poster_nb', models.IntegerField(null=True, db_column='TOTAL_POSTERS_NB')),
                ('lift_count', models.IntegerField(null=True, db_column='LIFT_COUNT')),
                ('total_poster_count', models.IntegerField(null=True, db_column='TOTAL_POSTER_COUNT')),
                ('total_poster_campaigns', models.IntegerField(null=True, db_column='TOTAL_POSTER_CAMPAIGNS')),
                ('standee_small', models.BooleanField(default=False, db_column='STANDEE_SMALL')),
                ('standee_medium', models.BooleanField(default=False, db_column='STANDEE_MEDIUM')),
                ('total_standee_count', models.IntegerField(null=True, db_column='TOTAL_STANDEE_COUNT')),
                ('total_standee_campaigns', models.IntegerField(null=True, db_column='TOTAL_STANDEE_CAMPAIGNS')),
                ('stall_canopy', models.BooleanField(default=False, db_column='STALL_CANOPY')),
                ('stall_small', models.BooleanField(default=False, db_column='STALL_SMALL')),
                ('stall_large', models.BooleanField(default=False, db_column='STALL_LARGE')),
                ('total_stall_count', models.IntegerField(null=True, db_column='TOTAL_STALL_COUNT')),
                ('timing', models.CharField(max_length=20, null=True, db_column='STALL_TIMING')),
                ('furniture_available', models.BooleanField(default=False, db_column='FURNITURE_AVAILABLE')),
                ('electricity_available', models.BooleanField(default=False, db_column='ELECTRICITY_SEPARATE')),
            ],
            options={
                'db_table': 'inventory_summary',
            },
        ),
        migrations.AddField(
            model_name='societytower',
            name='standee_count',
            field=models.IntegerField(null=True, db_column='STANDEE_COUNT', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='supplier_code',
            field=models.CharField(max_length=3, null=True, db_column='SUPPLIER_CODE'),
        ),
        migrations.AlterModelTable(
            name='campaignsuppliertypes',
            table='campaign_supplier_types',
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='supplier',
            field=models.ForeignKey(related_name='inventoy_summary', db_column='SUPPLIER_ID', blank=True, to='v0.SupplierTypeSociety', null=True),
        ),
    ]
