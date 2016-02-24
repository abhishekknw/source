# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0022_auto_20160213_1057'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlatType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('flat_type_count', models.IntegerField(null=True, db_column='FLAT_TYPE_COUNT', blank=True)),
                ('size_carpet_area', models.FloatField(null=True, db_column='SIZE_CARPET_AREA', blank=True)),
                ('size_builtup_area', models.FloatField(null=True, db_column='SIZE_BUILTUP_AREA', blank=True)),
                ('flat_rent', models.IntegerField(null=True, db_column='FLAT_RENT', blank=True)),
                ('rent_per_sqft', models.FloatField(null=True, db_column='RENT_PER_SQFT', blank=True)),
                ('average_rent_per_sqft_tower', models.FloatField(null=True, db_column='AVERAGE_RENT_PERS_SQFT_TOWER', blank=True)),
                ('society', models.ForeignKey(related_name='flatTypes', db_column='SUPPLIER_ID', blank=True, to='v0.SupplierTypeSociety', null=True)),
            ],
            options={
                'db_table': 'flat_type',
            },
        ),
        migrations.RemoveField(
            model_name='societyflat',
            name='average_rent_pers_sqft_tower',
        ),
        migrations.RemoveField(
            model_name='societyflat',
            name='flat_rent',
        ),
        migrations.RemoveField(
            model_name='societyflat',
            name='flat_size_per_sq_feet_builtup_area',
        ),
        migrations.RemoveField(
            model_name='societyflat',
            name='flat_size_per_sq_feet_carpet_area',
        ),
        migrations.RemoveField(
            model_name='societyflat',
            name='rent_per_sqft',
        ),
    ]
