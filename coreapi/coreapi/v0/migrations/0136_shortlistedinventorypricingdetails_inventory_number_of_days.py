# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-15 15:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0135_shortlistedspaces_stall_locations'),
    ]

    operations = [
        migrations.AddField(
            model_name='shortlistedinventorypricingdetails',
            name='inventory_number_of_days',
            field=models.IntegerField(null=True),
        ),
    ]