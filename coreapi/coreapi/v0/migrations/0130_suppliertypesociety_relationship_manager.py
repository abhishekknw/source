# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-10 12:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0129_auto_20181005_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliertypesociety',
            name='relationship_manager',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]