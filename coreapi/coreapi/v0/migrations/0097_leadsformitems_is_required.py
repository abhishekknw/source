# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-16 17:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0096_auto_20180816_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='leadsformitems',
            name='is_required',
            field=models.BooleanField(default=False),
        ),
    ]
