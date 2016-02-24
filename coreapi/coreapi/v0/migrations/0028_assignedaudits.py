# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0025_auto_20160216_1521'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignedAudits',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('ad_inventory_id', models.CharField(max_length=50, db_column='AD_INVENTORY_ID', blank=True)),
                ('supplier_name', models.CharField(max_length=50, db_column='SUPPLIER_NAME', blank=True)),
                ('ad_location', models.CharField(max_length=50, db_column='AD_LOCATION', blank=True)),
                ('address', models.CharField(max_length=100, db_column='ADDRESS', blank=True)),
                ('date', models.DateField(null=True, db_column='DATE')),
                ('business_name', models.CharField(max_length=50, db_column='BUSINESS_NAME', blank=True)),
                ('audit_type', models.CharField(max_length=20, db_column='AUDIT_TYPE', blank=True)),
                ('image_url', models.CharField(max_length=100, null=True, db_column='IMAGE_URL')),
            ],
            options={
                'db_table': 'assigned_audits',
            },
        ),
    ]
