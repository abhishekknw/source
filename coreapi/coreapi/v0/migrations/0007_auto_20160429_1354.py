# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0006_auto_20160428_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventorysummary',
            name='poster_count_per_tower',
            field=models.IntegerField(null=True, db_column='POSTER_COUNT_PER_TOWER'),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='standee_count_per_tower',
            field=models.IntegerField(null=True, db_column='STANDEE_COUNT_PER_TOWER'),
        ),
    ]
