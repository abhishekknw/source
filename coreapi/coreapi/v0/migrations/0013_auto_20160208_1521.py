# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0012_businesscontact'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignTypeMapping',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('type', models.CharField(max_length=20, db_column='TYPE', blank=True)),
                ('sub_type', models.CharField(max_length=20, db_column='SUB_TYPE', blank=True)),
            ],
            options={
                'db_table': 'campaign_type_mapping',
            },
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='campaign_type',
        ),
        migrations.RemoveField(
            model_name='campaignbookinginfo',
            name='campaign_amount',
        ),
        migrations.RemoveField(
            model_name='societyinventorybooking',
            name='adinventory_id',
        ),
        migrations.RemoveField(
            model_name='societyinventorybooking',
            name='campaign_status',
        ),
        migrations.AddField(
            model_name='business',
            name='business_sub_type',
            field=models.CharField(max_length=20, db_column='SUB_TYPE', blank=True),
        ),
        migrations.AddField(
            model_name='business',
            name='comments',
            field=models.TextField(max_length=100, db_column='COMMENTS', blank=True),
        ),
        migrations.AddField(
            model_name='business',
            name='reference',
            field=models.CharField(max_length=50, db_column='REFERENCE', blank=True),
        ),
        migrations.AddField(
            model_name='businesscontact',
            name='comments',
            field=models.TextField(max_length=100, db_column='COMMENTS', blank=True),
        ),
        migrations.AddField(
            model_name='businesscontact',
            name='spoc',
            field=models.BooleanField(default=False, db_column='SPOC'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='booking_status',
            field=models.CharField(max_length=20, db_column='BOOKING_STATUS', blank=True),
        ),
        migrations.AddField(
            model_name='campaign',
            name='end_date',
            field=models.DateField(null=True, db_column='END_DATE'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='start_date',
            field=models.DateField(null=True, db_column='START_DATE'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='tentative_cost',
            field=models.IntegerField(null=True, db_column='TENTATIVE_COST'),
        ),
        migrations.AddField(
            model_name='campaignbookinginfo',
            name='booking_amount',
            field=models.FloatField(null=True, db_column='BOKING_AMOUNT'),
        ),
        migrations.AddField(
            model_name='campaignbookinginfo',
            name='date_received',
            field=models.DateField(null=True, db_column='DATE_RECEIVED'),
        ),
        migrations.AddField(
            model_name='campaignbookinginfo',
            name='instrument_no',
            field=models.CharField(max_length=20, db_column='INSTRUMENT_NO', blank=True),
        ),
        migrations.AddField(
            model_name='campaignbookinginfo',
            name='instrument_type',
            field=models.CharField(max_length=20, db_column='INSTRUMENT_TYPE', blank=True),
        ),
        migrations.AddField(
            model_name='campaignsocietymapping',
            name='booking_status',
            field=models.CharField(max_length=20, db_column='BOOKING_STATUS', blank=True),
        ),
        migrations.AddField(
            model_name='societyinventorybooking',
            name='adinventory_type',
            field=models.CharField(max_length=20, db_column='ADINVENTORY_TYPE', blank=True),
        ),
        migrations.AddField(
            model_name='societyinventorybooking',
            name='audit_date',
            field=models.DateField(null=True, db_column='AUDIT_DATE'),
        ),
        migrations.AddField(
            model_name='societyinventorybooking',
            name='comments',
            field=models.TextField(max_length=100, db_column='COMMENTS', blank=True),
        ),
        migrations.AddField(
            model_name='campaigntypemapping',
            name='campaign',
            field=models.ForeignKey(related_name='types', db_column='CAMPAIGN_ID', to='v0.Campaign', null=True),
        ),
    ]
