# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0004_auto_20160119_0838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poleinventory',
            name='pole_lit_status',
            field=models.CharField(max_length=5, db_column='POLE_LIT_STATUS', blank=True),
        ),
        migrations.AlterField(
            model_name='poleinventory',
            name='pole_monthly_price_business',
            field=models.FloatField(null=True, db_column='POLE_MONTHLY_PRICE_BUSINESS'),
        ),
        migrations.AlterField(
            model_name='poleinventory',
            name='pole_monthly_price_society',
            field=models.FloatField(null=True, db_column='POLE_MONTHLY_PRICE_SOCIETY'),
        ),
        migrations.AlterField(
            model_name='poleinventory',
            name='pole_quarterly_price_business',
            field=models.FloatField(null=True, db_column='POLE_QUARTERLY_PRICE_BUSINESS'),
        ),
        migrations.AlterField(
            model_name='poleinventory',
            name='pole_quarterly_price_society',
            field=models.FloatField(null=True, db_column='POLE_QUARTERLY_PRICE_SOCIETY'),
        ),
        migrations.AlterField(
            model_name='wallinventory',
            name='inventory_type_id',
            field=models.CharField(max_length=20, db_column='INVENTORY_TYPE_ID', blank=True),
        ),
        migrations.AlterField(
            model_name='wallinventory',
            name='wall_paint_allowed',
            field=models.CharField(max_length=5, null=True, db_column='WALL_PAINT_ALLOWED', blank=True),
        ),
    ]
