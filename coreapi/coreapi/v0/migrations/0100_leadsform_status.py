# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-18 10:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0099_auto_20180818_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='leadsform',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'ACTIVE'), ('INACTIVE', 'INACTIVE')], max_length=70, null=True),
        ),
    ]
