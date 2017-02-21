# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0046_auto_20170217_0740'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryActivity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('activity_type', models.CharField(max_length=255, null=True, choices=[('RELEASE', 'RELEASE'), ('CLOSURE', 'CLOSURE'), ('AUDIT', 'AUDIT')])),
                ('shortlisted_inventory_details', models.ForeignKey(to='v0.ShortlistedInventoryPricingDetails')),
            ],
            options={
                'db_table': 'inventory_activity',
            },
        ),
        migrations.AlterField(
            model_name='inventoryactivityassignment',
            name='activity_date',
            field=models.DateTimeField(max_length=255, null=True, blank=True),
        ),
        # migrations.AlterUniqueTogether(
        #     name='inventoryactivityassignment',
        #     unique_together=set([]),
        # ),
        migrations.RemoveField(
            model_name='inventoryactivityassignment',
            name='activity_type',
        ),
        migrations.RemoveField(
            model_name='inventoryactivityassignment',
            name='shortlisted_inventory_details',
        ),
        migrations.AddField(
            model_name='inventoryactivityassignment',
            name='inventory_activity',
            field=models.ForeignKey(blank=True, to='v0.InventoryActivity', null=True),
        ),
    ]
