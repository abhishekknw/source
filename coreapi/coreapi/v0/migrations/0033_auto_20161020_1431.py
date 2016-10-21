# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0032_auto_20161020_1426'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyFloor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('floor_number', models.IntegerField(null=True, db_column='FLOOR_NUMBER', blank=True)),
            ],
            options={
                'db_table': 'corporate_building_floors',
            },
        ),
        migrations.CreateModel(
            name='CorporateBuilding',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('building_name', models.CharField(max_length=50, null=True, db_column='BUILDING_NAME', blank=True)),
                ('number_of_wings', models.IntegerField(null=True, db_column='NUMBER_OF_WINGS', blank=True)),
            ],
            options={
                'db_table': 'corporate_building',
            },
        ),
        migrations.CreateModel(
            name='CorporateBuildingWing',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('wing_name', models.CharField(max_length=50, null=True, db_column='WING_NAME', blank=True)),
                ('number_of_floors', models.IntegerField(null=True, db_column='NUMBER_OF_FLOORS', blank=True)),
                ('building_id', models.ForeignKey(related_name='buildingwing', db_column='BUILDING_ID', blank=True, to='v0.CorporateBuilding', null=True)),
            ],
            options={
                'db_table': 'corporate_building_wing',
            },
        ),
        migrations.CreateModel(
            name='CorporateCompanyDetails',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('building_name', models.CharField(max_length=20, null=True, db_column='BUILDING_NAME', blank=True)),
                ('wing_name', models.CharField(max_length=20, null=True, db_column='WING_NAME', blank=True)),
            ],
            options={
                'db_table': 'corporate_company_details',
            },
        ),
        migrations.CreateModel(
            name='CorporateParkCompanyList',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('name', models.CharField(max_length='50', null=True, db_column='COMPANY_NAME', blank=True)),
            ],
            options={
                'db_table': 'corporateparkcompanylist',
            },
        ),
        migrations.CreateModel(
            name='SupplierTypeCorporate',
            fields=[
                ('supplier_id', models.CharField(max_length=20, serialize=False, primary_key=True)),
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
                ('supplier_code', models.CharField(max_length=3, null=True, db_column='SUPPLIER_CODE')),
                ('corporate_type', models.CharField(max_length=25, null=True, db_column='CORPORATE_TYPE', blank=True)),
                ('industry_segment', models.CharField(max_length=30, null=True, db_column='CORPORATE_INDUSTRY_SEGMENT', blank=True)),
                ('possession_year', models.CharField(max_length=5, null=True, db_column='CORPORATE_AGE', blank=True)),
                ('building_count', models.IntegerField(null=True, db_column='CORPORATE_BUILDING_COUNT', blank=True)),
                ('floorperbuilding_count', models.IntegerField(null=True, db_column='CORPORATE_FLOORPERBUILDING_COUNT', blank=True)),
                ('totalcompanies_count', models.IntegerField(null=True, db_column='CORPORATE_TOTALCOMPANIES_COUNT', blank=True)),
                ('totalemployees_count', models.IntegerField(null=True, db_column='CORPORATE_TOTALEMPLOYEES_COUNT', blank=True)),
                ('isrealestateallowed', models.BooleanField(default=False, db_column='CORPORATE_ISREALESTATEALLOWED')),
                ('total_area', models.FloatField(default=0.0, null=True, db_column='TOTAL_AREA', blank=True)),
                ('quantity_rating', models.CharField(max_length=50, null=True, db_column='QUANTITY_RATING', blank=True)),
                ('luxurycars_count', models.IntegerField(null=True, db_column='LUXURYCARS_COUNT', blank=True)),
                ('standardcars_count', models.IntegerField(null=True, db_column='STANDARDCARS_COUNT', blank=True)),
                ('totallift_count', models.IntegerField(null=True, db_column='TOTALLIFT_COUNT', blank=True)),
                ('parkingspaces_count', models.IntegerField(null=True, db_column='PARKINGSPACES_COUNT', blank=True)),
                ('entryexit_count', models.IntegerField(null=True, db_column='ENTRYEXIT_COUNT', blank=True)),
                ('openspaces_count', models.IntegerField(null=True, db_column='OPENSPACES_COUNT', blank=True)),
                ('constructionspaces_count', models.IntegerField(null=True, db_column='CONSTRUCTIONSPACES_COUNT', blank=True)),
                ('constructedspace', models.FloatField(default=0.0, null=True, db_column='CONSTRUCTEDSPACE', blank=True)),
                ('parkingspace', models.FloatField(default=0.0, null=True, db_column='PARKINGSPACE', blank=True)),
                ('openspace', models.FloatField(default=0.0, null=True, db_column='OPENSPACE', blank=True)),
                ('averagerent', models.FloatField(default=0.0, null=True, db_column='AVERAGERENT', blank=True)),
                ('corporate_name', models.CharField(max_length=30, null=True, db_column='CORPORATE_NAME_PAYMENT', blank=True)),
                ('bank_name', models.CharField(max_length=30, null=True, db_column='BANK_NAME', blank=True)),
                ('ifsc_code', models.CharField(max_length=30, null=True, db_column='IFSC_CODE', blank=True)),
                ('account_number', models.CharField(max_length=30, null=True, db_column='ACCOUNT_NUMBER', blank=True)),
            ],
            options={
                'db_table': 'supplier_corporate',
            },
        ),
        migrations.AddField(
            model_name='corporateparkcompanylist',
            name='supplier_id',
            field=models.ForeignKey(related_name='corporatecompany', db_column='CORPORATEPARK_ID', blank=True, to='v0.SupplierTypeCorporate', null=True),
        ),
        migrations.AddField(
            model_name='corporatecompanydetails',
            name='company_id',
            field=models.ForeignKey(related_name='companydetails', db_column='COMPANY_ID', blank=True, to='v0.CorporateParkCompanyList', null=True),
        ),
        migrations.AddField(
            model_name='corporatebuilding',
            name='corporatepark_id',
            field=models.ForeignKey(related_name='corporatebuilding', db_column='CORPORATE_ID', blank=True, to='v0.SupplierTypeCorporate', null=True),
        ),
        migrations.AddField(
            model_name='companyfloor',
            name='company_details_id',
            field=models.ForeignKey(related_name='wingfloor', db_column='COMPANY_DETAILS_ID', blank=True, to='v0.CorporateCompanyDetails', null=True),
        ),
    ]
