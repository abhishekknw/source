# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-18 10:34
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('v0', '0098_hashtagimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='leadsformdata',
            name='status',
            field=models.CharField(choices=[(b'ACTIVE', b'ACTIVE'), (b'INACTIVE', b'INACTIVE')], max_length=70, null=True),
        ),
    ]