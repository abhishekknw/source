# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0015_auto_20160512_0711'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliertypesociety',
            name='account_no',
            field=models.IntegerField(null=True, db_column='ACCOUNT_NUMBER', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='bank_name',
            field=models.CharField(max_length=100, null=True, db_column='BANK_NAME', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='ifsc_code',
            field=models.CharField(max_length=100, null=True, db_column='IFSC_CODE', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='name_for_payment',
            field=models.CharField(max_length=100, null=True, db_column='NAME_FOR_PAYMENT', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='payment_details_available',
            field=models.BooleanField(default=True, db_column='PAYMENT_DETAILS_AVAILABLE'),
        ),
    ]
