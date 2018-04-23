# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0083_gatewayarchinventory'),
    ]

    operations = [
        migrations.AddField(
            model_name='leads',
            name='date1',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='leads',
            name='date2',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='leads',
            name='number1',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='leads',
            name='number2',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='adinventorylocationmapping',
            name='adinventory_name',
            field=models.CharField(default='POSTER', max_length=10, db_column='ADINVENTORY_NAME', choices=[('POSTER', 'Poster'), ('STANDEE', 'Standee'), ('STALL', 'Stall'), ('CAR DISPLAY', 'Car Display'), ('FLIER', 'Flier'), ('BANNER', 'Banner'), ('POSTER LIFT', 'Poster Lift'), ('GLASS_FACADE', 'GLASS_FACADE'), ('HOARDING', 'HOARDING'), ('DROPDOWN', 'DROPDOWN'), ('STANDEE', 'STANDEE'), ('PROMOTION_DESK', 'PROMOTION_DESK'), ('PILLAR', 'PILLAR'), ('TROLLEY', 'TROLLEY'), ('WALL_INVENTORY', 'WALL_INVENTORY'), ('FLOOR_INVENTORY', 'FLOOR_INVENTORY'), ('GATEWAY ARCH', 'GATEWAY ARCH')]),
        ),
        migrations.AlterField(
            model_name='adinventorytype',
            name='adinventory_name',
            field=models.CharField(default='POSTER', max_length=20, db_column='ADINVENTORY_NAME', choices=[('POSTER', 'Poster'), ('STANDEE', 'Standee'), ('STALL', 'Stall'), ('CAR DISPLAY', 'Car Display'), ('FLIER', 'Flier'), ('BANNER', 'Banner'), ('POSTER LIFT', 'Poster Lift'), ('GLASS_FACADE', 'GLASS_FACADE'), ('HOARDING', 'HOARDING'), ('DROPDOWN', 'DROPDOWN'), ('STANDEE', 'STANDEE'), ('PROMOTION_DESK', 'PROMOTION_DESK'), ('PILLAR', 'PILLAR'), ('TROLLEY', 'TROLLEY'), ('WALL_INVENTORY', 'WALL_INVENTORY'), ('FLOOR_INVENTORY', 'FLOOR_INVENTORY'), ('GATEWAY ARCH', 'GATEWAY ARCH')]),
        ),
    ]
