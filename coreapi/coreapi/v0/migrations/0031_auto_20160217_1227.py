# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0030_assignedaudits_ad_inventory_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignedaudits',
            name='ad_inventory_type',
            field=models.CharField(max_length=50, null=True, db_column='AD_INVENTORY_TYPE', blank=True),
        ),
    ]
