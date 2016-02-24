# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0034_auto_20160223_0818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adinventorylocationmapping',
            name='adinventory_name',
            field=models.CharField(default='POSTER', max_length=10, db_column='ADINVENTORY_NAME', choices=[('POSTER', 'Poster'), ('STANDEE', 'Standee'), ('STALL', 'Stall'), ('CAR DISPLAY', 'Car Display'), ('FLIER', 'Flier'), ('BANNER', 'Banner')]),
        ),
        migrations.AlterField(
            model_name='adinventorytype',
            name='adinventory_name',
            field=models.CharField(default='POSTER', max_length=20, db_column='ADINVENTORY_NAME', choices=[('POSTER', 'Poster'), ('STANDEE', 'Standee'), ('STALL', 'Stall'), ('CAR DISPLAY', 'Car Display'), ('FLIER', 'Flier'), ('BANNER', 'Banner')]),
        ),
        migrations.AlterField(
            model_name='pricemappingdefault',
            name='business_price',
            field=models.IntegerField(db_column='ACTUAL_SOCIETY_PRICE'),
        ),
        migrations.AlterField(
            model_name='pricemappingdefault',
            name='society_price',
            field=models.IntegerField(db_column='SUGGESTED_SOCIETY_PRICE'),
        ),
    ]
