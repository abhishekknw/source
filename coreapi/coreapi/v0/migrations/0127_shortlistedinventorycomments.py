# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-26 17:12
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0126_auto_20180926_1125'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShortlistedInventoryComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('comment', models.CharField(blank=True, max_length=500, null=True)),
                ('campaign_id', models.CharField(blank=True, max_length=70, null=True)),
                ('shortlisted_inventory_details', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='v0.ShortlistedInventoryPricingDetails')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'shortlisted_inventory_comments',
            },
        ),
    ]
