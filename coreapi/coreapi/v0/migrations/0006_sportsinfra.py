# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0005_auto_20160113_1223'),
    ]

    operations = [
        migrations.CreateModel(
            name='SportsInfra',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('sports_infrastructure_id', models.CharField(max_length=20, null=True, db_column='SPORTS_INFRASTRUCTURE_ID', blank=True)),
                ('stall_spaces_count', models.IntegerField(db_column='STALL_SPACES_COUNT', blank=True)),
                ('banner_spaces_count', models.IntegerField(db_column='BANNER_SPACES_COUNT', blank=True)),
                ('poster_spaces_count', models.IntegerField(db_column='POSTER_SPACES_COUNT', blank=True)),
                ('standee_spaces_count', models.IntegerField(db_column='STANDEE_SPACES_COUNT', blank=True)),
                ('sponsorship_amount_society', models.IntegerField(db_column='SPONSORSHIP_AMOUNT_SOCIETY', blank=True)),
                ('sponsorship_amount_business', models.IntegerField(db_column='SPONSORSHIP_AMOUNT_BUSINESS)', blank=True)),
                ('start_date', models.DateField(null=True, db_column='START_DATE', blank=True)),
                ('end_date', models.DateField(null=True, db_column='END_DATE', blank=True)),
                ('outside_participants_allowed', models.CharField(max_length=5, null=True, db_column='OUTSIDE_PARTICIPANTS_ALLOWED', blank=True)),
                ('lit_unlit', models.CharField(max_length=5, null=True, db_column='LIT_UNLIT', blank=True)),
                ('daily_infra_charges_society', models.IntegerField(db_column='DAILY_INFRA_CHARGES_SOCIETY', blank=True)),
                ('daily_infra_charges_business', models.IntegerField(db_column='DAILY_INFRA_CHARGES_BUSINESS', blank=True)),
                ('play_areas_count', models.IntegerField(db_column='PLAY_AREAS_COUNT', blank=True)),
                ('play_area_size', models.IntegerField(db_column='PLAY_AREA_SIZE', blank=True)),
                ('sports_type', models.CharField(max_length=20, null=True, db_column='SPORTS_TYPE', blank=True)),
                ('photograph_1', models.CharField(max_length=45, null=True, db_column='PHOTOGRAPH_1', blank=True)),
                ('photograph_2', models.CharField(max_length=45, null=True, db_column='PHOTOGRAPH_2', blank=True)),
                ('supplier', models.ForeignKey(related_name='sports', db_column='SUPPLIER_ID', blank=True, to='v0.SupplierTypeSociety', null=True)),
            ],
            options={
                'db_table': 'sports_infra',
            },
        ),
    ]
