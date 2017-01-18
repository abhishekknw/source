# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0034_auto_20170117_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='shortlistedspaces',
            name='payment_method',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='shortlistedspaces',
            name='payment_status',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='shortlistedspaces',
            name='total_negotiated_price',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
