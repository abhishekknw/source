# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0023_auto_20160217_1350'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flattype',
            old_name='rent_per_sqft',
            new_name='average_rent_per_sqft',
        ),
        migrations.RemoveField(
            model_name='flattype',
            name='average_rent_per_sqft_tower',
        ),
        migrations.AddField(
            model_name='flattype',
            name='flat_type',
            field=models.CharField(default=0, max_length=20, db_column='FLAT_TYPE'),
            preserve_default=False,
        ),
    ]
