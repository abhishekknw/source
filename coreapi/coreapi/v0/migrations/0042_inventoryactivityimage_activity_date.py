# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0041_inventoryactivityimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryactivityimage',
            name='activity_date',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
    ]
