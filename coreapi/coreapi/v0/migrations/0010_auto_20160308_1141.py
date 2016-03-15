# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0009_auto_20160305_1037'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('city_name', models.CharField(max_length=20, null=True, db_column='CITY_NAME')),
                ('city_code', models.CharField(max_length=5, null=True, db_column='CITY_CODE')),
            ],
            options={
                'db_table': 'city',
            },
        ),
        migrations.CreateModel(
            name='CityArea',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('area_name', models.CharField(max_length=20, null=True, db_column='AREA_NAME')),
                ('area_code', models.CharField(max_length=5, null=True, db_column='AREA_CODE')),
                ('city_code', models.ForeignKey(related_name='citycode', db_column='CITY_CODE', to='v0.City', null=True)),
            ],
            options={
                'db_table': 'city_area',
            },
        ),
        migrations.CreateModel(
            name='CitySubArea',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('subarea_name', models.CharField(max_length=20, null=True, db_column='SUBAREA_NAME')),
                ('subarea_code', models.CharField(max_length=5, null=True, db_column='SUBAREA_CODE')),
                ('area_code', models.ForeignKey(related_name='areacode', db_column='AREA_CODE', to='v0.CityArea', null=True)),
            ],
            options={
                'db_table': 'city_area_subarea',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('state_name', models.CharField(max_length=20, null=True, db_column='STATE_NAME')),
                ('state_code', models.CharField(max_length=5, null=True, db_column='STATE_CODE')),
            ],
            options={
                'db_table': 'state',
            },
        ),
        migrations.CreateModel(
            name='SupplierType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('supplier_type_name', models.CharField(max_length=20, null=True, db_column='SUPPLIER_TYPE_NAME')),
                ('supplier_type_code', models.CharField(max_length=5, null=True, db_column='SUPPLIER_TYPE_CODE')),
            ],
            options={
                'db_table': 'supplier_type',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='state_code',
            field=models.ForeignKey(related_name='citycode', db_column='STATE_CODE', to='v0.State', null=True),
        ),
    ]
