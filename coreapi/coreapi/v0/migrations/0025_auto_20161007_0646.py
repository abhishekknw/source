# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0024_auto_20160929_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventorytype',
            name='banner_count',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='inventorytype',
            name='banner_price',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='inventorytype',
            name='flier_count',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='inventorytype',
            name='flier_price',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='inventorytype',
            name='poster_count',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='inventorytype',
            name='poster_price',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='inventorytype',
            name='stall_count',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='inventorytype',
            name='stall_price',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='inventorytype',
            name='standee_count',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='inventorytype',
            name='standee_price',
            field=models.FloatField(default=0.0, null=True),
        ),
    ]
