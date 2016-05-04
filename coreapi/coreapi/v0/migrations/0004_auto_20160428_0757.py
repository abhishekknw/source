# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0003_auto_20160428_0719'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventorysummary',
            name='poster_price_week',
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='poster_price_week_lift',
            field=models.IntegerField(null=True, db_column='POSTER_PRICE_WEEK_LIFT'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='poster_price_week_nb',
            field=models.IntegerField(null=True, db_column='POSTER_PRICE_WEEK_NB'),
        ),
    ]
