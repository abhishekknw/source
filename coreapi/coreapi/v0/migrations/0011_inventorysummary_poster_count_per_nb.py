# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0010_auto_20160503_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventorysummary',
            name='poster_count_per_nb',
            field=models.IntegerField(null=True, db_column='POSTER_COUNT_PER_NB'),
        ),
    ]
