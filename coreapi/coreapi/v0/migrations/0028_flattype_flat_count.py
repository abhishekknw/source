# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0027_auto_20160218_1237'),
    ]

    operations = [
        migrations.AddField(
            model_name='flattype',
            name='flat_count',
            field=models.IntegerField(null=True, db_column='FLAT_COUNT', blank=True),
        ),
    ]
