# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0026_remove_flattype_flat_type_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flattype',
            name='flat_count',
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='flat_type_count',
            field=models.IntegerField(null=True, db_column='FLAT_TYPE_COUNT', blank=True),
        ),
    ]
