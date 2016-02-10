# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0010_auto_20160123_0843'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditorSocietyMapping',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('user_id', models.IntegerField(null=True, db_column='USER_ID')),
                ('society', models.ForeignKey(related_name='auditors', db_column='SUPPLIER_ID', to='v0.SupplierTypeSociety', null=True)),
            ],
            options={
                'db_table': 'auditor_society_mapping',
            },
        ),
        migrations.CreateModel(
            name='audits',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('latitude', models.FloatField(null=True, db_column='LATITUDE')),
                ('longitude', models.FloatField(null=True, db_column='LONGITUDE')),
                ('timestamp', models.DateTimeField(null=True, db_column='TIMESTAMP')),
                ('barcode', models.FloatField(null=True, db_column='BARCODE')),
                ('audited_by', models.IntegerField(null=True, db_column='USER_ID')),
                ('audit_type', models.CharField(max_length=20, db_column='AUDIT_TYPE', blank=True)),
            ],
            options={
                'db_table': 'audits',
            },
        ),
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('name', models.CharField(max_length=50, db_column='NAME', blank=True)),
                ('business_type', models.CharField(max_length=20, db_column='TYPE', blank=True)),
                ('phone', models.IntegerField(null=True, db_column='PHONE')),
                ('email', models.CharField(max_length=50, db_column='EMAILID', blank=True)),
                ('address', models.CharField(max_length=100, db_column='ADDRESS', blank=True)),
            ],
            options={
                'db_table': 'business',
            },
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('business', models.ForeignKey(related_name='campaigns', db_column='BUSINESS_ID', to='v0.Business', null=True)),
            ],
            options={
                'db_table': 'campaign',
            },
        ),
        migrations.CreateModel(
            name='CampaignBookingInfo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('booking_id', models.IntegerField(null=True, db_column='BOOKING_ID')),
                ('campaign_amount', models.FloatField(null=True, db_column='CAMPAIGN_AMOUNT')),
                ('campaign', models.ForeignKey(related_name='bookings', db_column='CAMPAIGN_ID', to='v0.Campaign', null=True)),
            ],
            options={
                'db_table': 'campaign_booking_info',
            },
        ),
        migrations.CreateModel(
            name='CampaignSocietyMapping',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('campaign', models.ForeignKey(related_name='societies', db_column='CAMPAIGN_ID', to='v0.Campaign', null=True)),
                ('society', models.ForeignKey(related_name='campaigns', db_column='SUPPLIER_ID', to='v0.SupplierTypeSociety', null=True)),
            ],
            options={
                'db_table': 'campaign_society_mapping',
            },
        ),
        migrations.CreateModel(
            name='CampaignTypes',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('type_name', models.CharField(max_length=20, db_column='TYPE_NAME', blank=True)),
            ],
            options={
                'db_table': 'campaign_types',
            },
        ),
        migrations.CreateModel(
            name='SocietyInventoryBooking',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('start_date', models.DateField(null=True, db_column='START_DATE')),
                ('end_date', models.DateField(null=True, db_column='END_DATE')),
                ('campaign_status', models.CharField(max_length=20, db_column='CAMPAIGN_STATUS', blank=True)),
                ('adinventory_id', models.ForeignKey(related_name='inventory_bookings', db_column='ADINVENTORY_LOCATION_MAPPING_ID', to='v0.AdInventoryLocationMapping', null=True)),
                ('campaign', models.ForeignKey(related_name='inventory_bookings', db_column='CAMPAIGN_ID', to='v0.Campaign', null=True)),
                ('society', models.ForeignKey(related_name='inventory_bookings', db_column='SUPPLIER_ID', to='v0.SupplierTypeSociety', null=True)),
            ],
            options={
                'db_table': 'society_inventory_booking',
            },
        ),
        migrations.AddField(
            model_name='campaign',
            name='campaign_type',
            field=models.ForeignKey(related_name='campaigns', db_column='CAMPAIGN_TYPE_ID', to='v0.CampaignTypes', null=True),
        ),
        migrations.AddField(
            model_name='audits',
            name='society_booking',
            field=models.ForeignKey(related_name='audits', db_column='SOCIETY_BOOKING_ID', to='v0.SocietyInventoryBooking', null=True),
        ),
    ]
