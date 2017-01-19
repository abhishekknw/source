# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0035_auto_20170118_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adinventorylocationmapping',
            name='adinventory_name',
            field=models.CharField(default='POSTER', max_length=10, db_column='ADINVENTORY_NAME', choices=[('POSTER', 'Poster'), ('STANDEE', 'Standee'), ('STALL', 'Stall'), ('CAR DISPLAY', 'Car Display'), ('FLIER', 'Flier'), ('BANNER', 'Banner'), ('POSTER LIFT', 'Poster Lift')]),
        ),
        migrations.AlterField(
            model_name='adinventorytype',
            name='adinventory_name',
            field=models.CharField(default='POSTER', max_length=20, db_column='ADINVENTORY_NAME', choices=[('POSTER', 'Poster'), ('STANDEE', 'Standee'), ('STALL', 'Stall'), ('CAR DISPLAY', 'Car Display'), ('FLIER', 'Flier'), ('BANNER', 'Banner'), ('POSTER LIFT', 'Poster Lift')]),
        ),
    ]
