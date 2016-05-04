# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0018_societytower_standee_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cityarea',
            old_name='area_name',
            new_name='label',
        ),
        migrations.RemoveField(
            model_name='campaignbookinginfo',
            name='instrument_no',
        ),
        migrations.RemoveField(
            model_name='campaignbookinginfo',
            name='instrument_type',
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
