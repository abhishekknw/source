# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-07 14:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0111_leadsformitems_campaign_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='leadsformitems',
            name='supplier_id',
            field=models.CharField(blank=True, max_length=70, null=True),
        ),
    ]
