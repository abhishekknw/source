# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0059_inventoryactivityimage_distance_from_supplier'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventoryactivityimage',
            old_name='distance_from_supplier',
            new_name='latitude',
        ),
        migrations.AddField(
            model_name='inventoryactivityimage',
            name='longitude',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
