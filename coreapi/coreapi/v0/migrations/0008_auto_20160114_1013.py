# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0007_auto_20160113_1735'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bannerinventory',
            old_name='banner_type',
            new_name='type',
        ),
        migrations.RenameField(
            model_name='stallinventory',
            old_name='stall_types',
            new_name='type',
        ),
        migrations.RemoveField(
            model_name='standeeinventory',
            name='standee_area',
        ),
        migrations.AddField(
            model_name='standeeinventory',
            name='type',
            field=models.CharField(max_length=10, null=True, db_column='STANDEE_TYPE', blank=True),
        ),
    ]
