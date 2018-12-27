# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0040_suppliertypecorporate_is_common_cafeteria_available'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryActivityImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('image_path', models.CharField(max_length=1000, null=True, blank=True)),
                ('comment', models.CharField(max_length=1000, null=True, blank=True)),
                ('activity_type', models.CharField(max_length=1000, choices=[('RELEASE', 'RELEASE'), ('CLOSURE', 'CLOSURE'), ('AUDIT', 'AUDIT')])),
                ('shortlisted_inventory_details', models.ForeignKey(to='v0.ShortlistedInventoryPricingDetails', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'db_table': 'inventory_activity_image',
            },
        ),
    ]
