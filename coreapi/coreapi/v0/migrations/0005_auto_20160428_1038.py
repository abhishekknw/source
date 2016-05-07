# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0004_auto_20160428_0757'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventorysummary',
            name='flier_watchman_allowed',
        ),
        migrations.RemoveField(
            model_name='inventorysummary',
            name='pricing_confidence',
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='flier_price_confidence',
            field=models.CharField(max_length=20, null=True, db_column='FLIER_PRICE_CONFIDENCE', blank=True),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='largeStall_price_confidence',
            field=models.CharField(max_length=20, null=True, db_column='LARGESTALL_PRICE_CONFIDENCE', blank=True),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='lift_price_confidence',
            field=models.CharField(max_length=20, null=True, db_column='LIFT_PRICE_CONFIDENCE', blank=True),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='nb_price_confidence',
            field=models.CharField(max_length=20, null=True, db_column='NB_PRICE_CONFIDENCE', blank=True),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='premium_price_confidence',
            field=models.CharField(max_length=20, null=True, db_column='PREMIUM_PRICE_CONFIDENCE', blank=True),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='smallStall_price_confidence',
            field=models.CharField(max_length=20, null=True, db_column='SMALLSTALL_PRICE_CONFIDENCE', blank=True),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='standard_price_confidence',
            field=models.CharField(max_length=20, null=True, db_column='STANDARD_PRICE_CONFIDENCE', blank=True),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='standee_price_confidence',
            field=models.CharField(max_length=20, null=True, db_column='STANDEE_PRICE_CONFIDENCE', blank=True),
        ),
    ]
