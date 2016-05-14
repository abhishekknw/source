# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0009_auto_20160420_0753'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaignbookinginfo',
            name='instrument_no',
        ),
        migrations.RemoveField(
            model_name='campaignbookinginfo',
            name='instrument_type',
        ),
        migrations.AddField(
            model_name='campaign',
            name='amount_payable',
            field=models.IntegerField(null=True, db_column='AMOUNT_PAYABLE'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='discount_given',
            field=models.IntegerField(null=True, db_column='DISCOUNT'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='total_amount_paid',
            field=models.IntegerField(null=True, db_column='TOTAL_AMOUNT_PAID'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='total_campaign_cost',
            field=models.IntegerField(null=True, db_column='TOTAL_CAMPAIGN_COST'),
        ),
        migrations.AddField(
            model_name='campaignbookinginfo',
            name='payment_mode',
            field=models.CharField(max_length=20, db_column='PAYMENT_MODE', blank=True),
        ),
        migrations.AddField(
            model_name='campaignbookinginfo',
            name='payment_no',
            field=models.CharField(max_length=20, db_column='PAYMENT_NO', blank=True),
        ),
        migrations.AlterField(
            model_name='campaignbookinginfo',
            name='booking_amount',
            field=models.FloatField(null=True, db_column='BOOKING_AMOUNT'),
        ),
    ]
