# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0030_auto_20161010_1803'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplierTypeBusShelter',
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
                ('lit_status', models.CharField(max_length=255, null=True, blank=True)),
                ('halt_buses_count', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'supplier_bus_shelter',
            },
        ),
    ]
