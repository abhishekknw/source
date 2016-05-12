# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0011_inventorysummary_poster_count_per_nb'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posterinventory',
            name='notice_board_id',
        ),
        migrations.AddField(
            model_name='posterinventory',
            name='location_id',
            field=models.CharField(max_length=20, null=True, db_column='LOCATION_ID', blank=True),
        ),
        migrations.AddField(
            model_name='posterinventory',
            name='tower_name',
            field=models.CharField(max_length=20, null=True, db_column='TOWER_NAME', blank=True),
        ),
    ]
