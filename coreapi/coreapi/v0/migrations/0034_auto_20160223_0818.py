# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0033_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adinventorytype',
            name='adinventory_name',
            field=models.CharField(default='POSTER', max_length=20, db_column='ADINVENTORY_NAME', choices=[('POSTER', 'Poster'), ('STANDEE', 'Standee'), ('STALL', 'Stall'), ('BANNER', 'Banner')]),
        ),
        migrations.AlterField(
            model_name='durationtype',
            name='days_count',
            field=models.CharField(max_length=10, db_column='DAYS_COUNT'),
        ),
    ]
