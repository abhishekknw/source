# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0045_amenity_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryActivityAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('activity_type', models.CharField(max_length=255, choices=[('RELEASE', 'RELEASE'), ('CLOSURE', 'CLOSURE'), ('AUDIT', 'AUDIT')])),
                ('activity_date', models.CharField(max_length=255)),
                ('assigned_by', models.ForeignKey(related_name='activity_assigned_by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('assigned_to', models.ForeignKey(related_name='activity_assigned_to', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('shortlisted_inventory_details', models.ForeignKey(to='v0.ShortlistedInventoryPricingDetails')),
            ],
            options={
                'db_table': 'inventory_activity_assignment',
            },
        ),
        migrations.RemoveField(
            model_name='inventoryactivityimage',
            name='activity_date',
        ),
        migrations.RemoveField(
            model_name='inventoryactivityimage',
            name='activity_type',
        ),
        migrations.RemoveField(
            model_name='inventoryactivityimage',
            name='shortlisted_inventory_details',
        ),
        migrations.AddField(
            model_name='inventoryactivityimage',
            name='activity_by',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='inventoryactivityimage',
            name='actual_activity_date',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='inventoryactivityimage',
            name='inventory_activity_assignment',
            field=models.ForeignKey(blank=True, to='v0.InventoryActivityAssignment', null=True),
        ),
        # migrations.AlterUniqueTogether(
        #     name='inventoryactivityassignment',
        #     unique_together=set([('shortlisted_inventory_details', 'activity_type', 'activity_date')]),
        # ),
    ]
