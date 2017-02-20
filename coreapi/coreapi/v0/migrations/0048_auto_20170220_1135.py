# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0047_auto_20170220_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryactivityimage',
            name='actual_activity_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
