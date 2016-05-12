# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0006_auto_20160413_1345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='standeeinventory',
            name='sides',
        ),
        migrations.RemoveField(
            model_name='standeeinventory',
            name='standee_inventory_status',
        ),
        migrations.RemoveField(
            model_name='standeeinventory',
            name='standee_location_in_tower',
        ),
    ]
