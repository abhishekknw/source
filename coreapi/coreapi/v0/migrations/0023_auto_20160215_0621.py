# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0022_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='societyinventorybooking',
            name='ad_location',
            field=models.CharField(max_length=50, db_column='AD_LOCATION', blank=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='phone',
            field=models.CharField(max_length=10, db_column='PHONE', blank=True),
        ),
        migrations.AlterField(
            model_name='businesscontact',
            name='phone',
            field=models.CharField(max_length=10, db_column='PHONE', blank=True),
        ),
        migrations.AlterField(
            model_name='societyinventorybooking',
            name='end_date',
            field=models.DateField(null=True, db_column='END_DATE'),
        ),
        migrations.AlterField(
            model_name='societyinventorybooking',
            name='start_date',
            field=models.DateField(null=True, db_column='START_DATE'),
        ),
    ]
