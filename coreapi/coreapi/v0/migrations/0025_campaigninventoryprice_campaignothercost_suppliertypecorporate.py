# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0024_auto_20160602_1135'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignInventoryPrice',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('master_factor', models.IntegerField(null=True, db_column='MASTER_FACTOR')),
                ('business_price', models.IntegerField(null=True, db_column='BUSINESS_PRICE')),
                ('campaign', models.ForeignKey(related_name='campaign', db_column='CAMPAIGN_ID', to='v0.Campaign', null=True)),
                ('supplier', models.ForeignKey(related_name='inventoryprice', null=True, db_column='SUPPLIER_ID', blank=True, to='v0.SupplierTypeSociety', unique=True)),
            ],
            options={
                'db_table': 'campaign_inventory_price',
            },
        ),
        migrations.CreateModel(
            name='CampaignOtherCost',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('content_dev_cost', models.IntegerField(null=True, db_column='CONTENT_DEV_COST')),
                ('pm_cost', models.IntegerField(null=True, db_column='PROJECT_MGMT_COST')),
                ('data_analytics', models.IntegerField(null=True, db_column='DATA_ANALYTICS')),
                ('printing_cost', models.IntegerField(null=True, db_column='PRINTING_COST')),
                ('digital_camp_cost', models.IntegerField(null=True, db_column='DIGITAL_CAMP_COST')),
                ('campaign', models.ForeignKey(related_name='campaign_cost', db_column='CAMPAIGN_ID', to='v0.Campaign', null=True)),
            ],
            options={
                'db_table': 'campaign_other_cost',
            },
        ),
        migrations.CreateModel(
            name='SupplierTypeCorporate',
            fields=[
                ('supplier_id', models.CharField(max_length=20, serialize=False, primary_key=True, db_column='SUPPLIER_ID')),
                ('supplier_code', models.CharField(max_length=3, null=True, db_column='SUPPLIER_CODE')),
                ('corporate_name', models.CharField(max_length=70, null=True, db_column='CORPORATE_NAME', blank=True)),
                ('corporate_address1', models.CharField(max_length=250, null=True, db_column='CORPORATE_ADDRESS1', blank=True)),
                ('corporate_address2', models.CharField(max_length=250, null=True, db_column='CORPORATE_ADDRESS2', blank=True)),
                ('corporate_zip', models.IntegerField(null=True, db_column='CORPORATE_ZIP', blank=True)),
                ('corporate_city', models.CharField(max_length=250, null=True, db_column='CORPORATE_CITY', blank=True)),
                ('corporate_state', models.CharField(max_length=250, null=True, db_column='CORPORATE_STATE', blank=True)),
                ('corporate_longitude', models.FloatField(default=0.0, null=True, db_column='CORPORATE_LONGITUDE', blank=True)),
                ('corporate_locality', models.CharField(max_length=30, null=True, db_column='CORPORATE_LOCALITY', blank=True)),
                ('corporate_latitude', models.FloatField(default=0.0, null=True, db_column='CORPORATE_LATITUDE', blank=True)),
                ('corporate_location_type', models.CharField(max_length=50, null=True, db_column='CORPORATE_LOCATION_TYPE', blank=True)),
                ('corporate_type', models.CharField(max_length=10, db_column='CORPORATE_TYPE')),
                ('corporate_industry_segment', models.CharField(max_length=30, null=True, db_column='CORPORATE_INDUSTRY_SEGMENT', blank=True)),
                ('corporate_age', models.PositiveSmallIntegerField(null=True, db_column='CORPORATE_AGE', blank=True)),
                ('corporate_building_count', models.IntegerField(null=True, db_column='CORPORATE_BUILDING_COUNT', blank=True)),
                ('corporate_floorperbuilding_count', models.IntegerField(null=True, db_column='CORPORATE_FLOORPERBUILDING_COUNT', blank=True)),
                ('corporate_totalcompanies_count', models.IntegerField(null=True, db_column='CORPORATE_TOTALCOMPANIES_COUNT', blank=True)),
                ('corporate_totalemployees_count', models.IntegerField(null=True, db_column='CORPORATE_TOTALEMPLOYEES_COUNT', blank=True)),
                ('corporate_isrealestateallowed', models.BooleanField(default=False, db_column='CORPORATE_ISREALESTATEALLOWED')),
            ],
            options={
                'db_table': 'supplier_corporate',
            },
        ),
    ]
