# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0003_auto_20160118_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannerinventory',
            name='adinventory_id',
            field=models.CharField(max_length=20, db_column='ADINVENTORY_ID', blank=True),
        ),
        migrations.AlterField(
            model_name='bannerinventory',
            name='banner_location',
            field=models.CharField(max_length=50, db_column='BANNER_DISPLAY_LOCATION', blank=True),
        ),
        migrations.AlterField(
            model_name='bannerinventory',
            name='banner_size',
            field=models.CharField(max_length=10, db_column='BANNER_SIZE', blank=True),
        ),
        migrations.AlterField(
            model_name='bannerinventory',
            name='inventory_status',
            field=models.CharField(max_length=15, db_column='INVENTORY_STATUS', blank=True),
        ),
        migrations.AlterField(
            model_name='bannerinventory',
            name='photograph_1',
            field=models.CharField(max_length=45, db_column='PHOTOGRAPH_1', blank=True),
        ),
        migrations.AlterField(
            model_name='bannerinventory',
            name='photograph_2',
            field=models.CharField(max_length=45, db_column='PHOTOGRAPH_2', blank=True),
        ),
        migrations.AlterField(
            model_name='bannerinventory',
            name='type',
            field=models.CharField(max_length=20, db_column='BANNER_TYPE', blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='past_collections_banners',
            field=models.IntegerField(null=True, db_column='PAST_YEAR_COLLECTIONS_BANNERS'),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='past_collections_car',
            field=models.IntegerField(null=True, db_column='PAST_YEAR_COLLECTIONS_CAR'),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='past_collections_poster',
            field=models.IntegerField(null=True, db_column='PAST_YEAR_COLLECTIONS_POSTER'),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='past_collections_stalls',
            field=models.IntegerField(null=True, db_column='PAST_YEAR_COLLECTIONS_STALLS'),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='past_collections_standee',
            field=models.IntegerField(null=True, db_column='PAST_YEAR_COLLECTIONS_STANDEE'),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='past_sponsorship_collection_events',
            field=models.IntegerField(null=True, db_column='PAST_YEAR_SPONSORSHIP_COLLECTION_EVENTS'),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='past_total_sponsorship',
            field=models.IntegerField(null=True, db_column='PAST_YEAR_TOTAL_SPONSORSHIP'),
        ),
        migrations.AlterField(
            model_name='wallinventory',
            name='wall_paint_allowed',
            field=models.BooleanField(default=False, db_column='WALL_PAINT_ALLOWED'),
        ),
    ]
