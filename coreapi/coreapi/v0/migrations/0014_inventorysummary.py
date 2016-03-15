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
                ('posterAllowedNB', models.BooleanField(default=False, db_column='POSTER_ALLOWED_NB')),
                ('posterAllowedLift', models.BooleanField(default=False, db_column='POSTER_ALLOWED_LIFT')),
                ('poster_type_nb', models.CharField(max_length=5, null=True, db_column='POSTER_TYPE_NB')),
                ('nb_count', models.IntegerField(null=True, db_column='NB_COUNT')),
                ('poster_per_nb', models.IntegerField(null=True, db_column='POSTER_PER_NB')),
                ('total_posters_nb', models.IntegerField(null=True, db_column='TOTAL_POSTERS_NB')),
                ('poster_type_lift', models.CharField(max_length=5, null=True, db_column='POSTER_TYPE_LIFT')),
                ('lift_count', models.IntegerField(null=True, db_column='LIFT_COUNT')),
                ('total_poster_count', models.IntegerField(null=True, db_column='TOTAL_POSTER_COUNT')),
                ('total_campaigns', models.IntegerField(null=True, db_column='TOTAL_CAMPAIGNS')),
                ('supplier', models.ForeignKey(related_name='tower', db_column='SUPPLIER_ID', blank=True, to='v0.SupplierTypeSociety', null=True)),
            ],
        ),
    ]
