# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0015_auto_20160326_1029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventorysummary',
            name='poster_per_nb',
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='car_display_allowed',
            field=models.BooleanField(default=False, db_column='CAR_DISPLAY_ALLOWED'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='cd_premium',
            field=models.BooleanField(default=False, db_column='CD_PREMIUM'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='cd_price_day',
            field=models.IntegerField(null=True, db_column='CD_PRICE_DAY'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='cd_standard',
            field=models.BooleanField(default=False, db_column='CD_STANDARD'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='d2d_allowed',
            field=models.BooleanField(default=False, db_column='D2D_ALLOWED'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='flier_allowed',
            field=models.BooleanField(default=False, db_column='FLIER_ALLOWED'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='flier_price_day',
            field=models.IntegerField(null=True, db_column='FLIER_PRICE_DAY'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='mailbox_allowed',
            field=models.BooleanField(default=False, db_column='MAILBOX_ALLOWED'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='poster_price_week',
            field=models.IntegerField(null=True, db_column='POSTER_PRICE_WEEK'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='stall_price_day',
            field=models.IntegerField(null=True, db_column='STALL_PRICE_DAY'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='standee_price_week',
            field=models.IntegerField(null=True, db_column='STANDEE_PRICE_WEEK'),
        ),
    ]
