# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0029_auto_20160217_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignedaudits',
            name='ad_inventory_type',
            field=models.CharField(max_length=50, db_column='AD_INVENTORY_TYPE', blank=True),
        ),
    ]
