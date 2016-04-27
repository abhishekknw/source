# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0002_load_intial_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventorysummary',
            name='cd_price_day',
        ),
        migrations.RemoveField(
            model_name='inventorysummary',
            name='stall_price_day',
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='cd_price_day_premium',
            field=models.IntegerField(null=True, db_column='CD_PRICE_DAY_PREMIUM'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='cd_price_day_standard',
            field=models.IntegerField(null=True, db_column='CD_PRICE_DAY_STANDARD'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='flier_frequency',
            field=models.IntegerField(null=True, db_column='FLIER_FREQUENCY'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='stall_price_day_large',
            field=models.IntegerField(null=True, db_column='STALL_PRICE_DAY_LARGE'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='stall_price_day_small',
            field=models.IntegerField(null=True, db_column='STALL_PRICE_DAY_SMALL'),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='society_count',
            field=models.BooleanField(default=True, db_column='SOCIETY_COUNT'),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='society_ratings',
            field=models.BooleanField(default=True, db_column='SOCIETY_RATINGS'),
        ),
    ]
