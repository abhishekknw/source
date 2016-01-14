# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0006_sportsinfra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sportsinfra',
            name='banner_spaces_count',
            field=models.IntegerField(null=True, db_column='BANNER_SPACES_COUNT', blank=True),
        ),
        migrations.AlterField(
            model_name='sportsinfra',
            name='daily_infra_charges_business',
            field=models.IntegerField(null=True, db_column='DAILY_INFRA_CHARGES_BUSINESS', blank=True),
        ),
        migrations.AlterField(
            model_name='sportsinfra',
            name='daily_infra_charges_society',
            field=models.IntegerField(null=True, db_column='DAILY_INFRA_CHARGES_SOCIETY', blank=True),
        ),
        migrations.AlterField(
            model_name='sportsinfra',
            name='play_area_size',
            field=models.IntegerField(null=True, db_column='PLAY_AREA_SIZE', blank=True),
        ),
        migrations.AlterField(
            model_name='sportsinfra',
            name='play_areas_count',
            field=models.IntegerField(null=True, db_column='PLAY_AREAS_COUNT', blank=True),
        ),
        migrations.AlterField(
            model_name='sportsinfra',
            name='poster_spaces_count',
            field=models.IntegerField(null=True, db_column='POSTER_SPACES_COUNT', blank=True),
        ),
        migrations.AlterField(
            model_name='sportsinfra',
            name='sponsorship_amount_business',
            field=models.IntegerField(null=True, db_column='SPONSORSHIP_AMOUNT_BUSINESS)', blank=True),
        ),
        migrations.AlterField(
            model_name='sportsinfra',
            name='sponsorship_amount_society',
            field=models.IntegerField(null=True, db_column='SPONSORSHIP_AMOUNT_SOCIETY', blank=True),
        ),
        migrations.AlterField(
            model_name='sportsinfra',
            name='stall_spaces_count',
            field=models.IntegerField(null=True, db_column='STALL_SPACES_COUNT', blank=True),
        ),
        migrations.AlterField(
            model_name='sportsinfra',
            name='standee_spaces_count',
            field=models.IntegerField(null=True, db_column='STANDEE_SPACES_COUNT', blank=True),
        ),
    ]
