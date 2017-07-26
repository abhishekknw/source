# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0060_auto_20170714_1017'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplierTypeRetailShop',
            fields=[
                ('created_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('supplier_id', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('supplier_code', models.CharField(max_length=3, null=True)),
                ('name', models.CharField(max_length=70, null=True, blank=True)),
                ('address1', models.CharField(max_length=250, null=True, blank=True)),
                ('address2', models.CharField(max_length=250, null=True, blank=True)),
                ('area', models.CharField(max_length=255, null=True, blank=True)),
                ('subarea', models.CharField(max_length=30, null=True, blank=True)),
                ('city', models.CharField(max_length=250, null=True, blank=True)),
                ('state', models.CharField(max_length=250, null=True, blank=True)),
                ('zipcode', models.IntegerField(null=True, blank=True)),
                ('latitude', models.FloatField(default=0.0, null=True, blank=True)),
                ('longitude', models.FloatField(default=0.0, null=True, blank=True)),
                ('locality_rating', models.CharField(max_length=50, null=True, blank=True)),
                ('quality_rating', models.CharField(max_length=50, null=True, blank=True)),
                ('machadalo_index', models.CharField(max_length=30, null=True, blank=True)),
                ('bank_account_name', models.CharField(max_length=250, null=True, blank=True)),
                ('bank_name', models.CharField(max_length=250, null=True, blank=True)),
                ('ifsc_code', models.CharField(max_length=30, null=True, blank=True)),
                ('account_number', models.CharField(max_length=250, null=True, blank=True)),
                ('food_tasting_allowed', models.BooleanField(default=False)),
                ('sales_allowed', models.BooleanField(default=False)),
                ('retail_shop_type', models.CharField(max_length=255, choices=[('GROCERY_STORE', 'GROCERY_STORE'), ('ELECTRONIC_STORE', 'ELECTRONIC_STORE'), ('SANITARY_STORE', 'SANITARY_STORE'), ('STATIONARY_STORE', 'STATIONARY_STORE')])),
                ('size', models.FloatField()),
                ('is_modern_trade', models.BooleanField(default=False)),
                ('is_traditional', models.BooleanField(default=False)),
                ('category_name', models.CharField(max_length=255)),
                ('user', models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'supplier_type_retail_shop',
            },
        ),
        migrations.AlterField(
            model_name='adinventorylocationmapping',
            name='adinventory_name',
            field=models.CharField(default='POSTER', max_length=10, db_column='ADINVENTORY_NAME', choices=[('POSTER', 'Poster'), ('STANDEE', 'Standee'), ('STALL', 'Stall'), ('CAR DISPLAY', 'Car Display'), ('FLIER', 'Flier'), ('BANNER', 'Banner'), ('POSTER LIFT', 'Poster Lift'), ('GLASS_FACADE', 'GLASS_FACADE'), ('HOARDING', 'HOARDING'), ('DROPDOWN', 'DROPDOWN'), ('STANDEE', 'STANDEE'), ('PROMOTION_DESK', 'PROMOTION_DESK'), ('PILLAR', 'PILLAR'), ('TROLLEY', 'TROLLEY'), ('WALL_INVENTORY', 'WALL_INVENTORY'), ('FLOOR_INVENTORY', 'FLOOR_INVENTORY')]),
        ),
        migrations.AlterField(
            model_name='adinventorytype',
            name='adinventory_name',
            field=models.CharField(default='POSTER', max_length=20, db_column='ADINVENTORY_NAME', choices=[('POSTER', 'Poster'), ('STANDEE', 'Standee'), ('STALL', 'Stall'), ('CAR DISPLAY', 'Car Display'), ('FLIER', 'Flier'), ('BANNER', 'Banner'), ('POSTER LIFT', 'Poster Lift'), ('GLASS_FACADE', 'GLASS_FACADE'), ('HOARDING', 'HOARDING'), ('DROPDOWN', 'DROPDOWN'), ('STANDEE', 'STANDEE'), ('PROMOTION_DESK', 'PROMOTION_DESK'), ('PILLAR', 'PILLAR'), ('TROLLEY', 'TROLLEY'), ('WALL_INVENTORY', 'WALL_INVENTORY'), ('FLOOR_INVENTORY', 'FLOOR_INVENTORY')]),
        ),
    ]
