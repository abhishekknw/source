# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0036_auto_20170119_0926'),
    ]

    operations = [
        migrations.AddField(
            model_name='shortlistedinventorypricingdetails',
            name='comments',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='shortlistedspaces',
            name='booking_status',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
    ]
