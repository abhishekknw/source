# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0058_data_migration_for_updating_space_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryactivityimage',
            name='distance_from_supplier',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
