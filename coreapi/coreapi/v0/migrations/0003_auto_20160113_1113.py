# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0002_load_intial_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannerinventory',
            name='adinventory_id',
            field=models.CharField(max_length=20, null=True, db_column='ADINVENTORY_ID', blank=True),
        ),
        migrations.AlterField(
            model_name='standeeinventory',
            name='adinventory_id',
            field=models.CharField(max_length=20, null=True, db_column='ADINVENTORY_ID', blank=True),
        ),
    ]
