# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0048_auto_20170220_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryactivityassignment',
            name='reassigned_activity_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
