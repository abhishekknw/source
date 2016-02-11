# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0010_auto_20160123_0843'),
    ]

    operations = [
        migrations.AddField(
            model_name='liftdetails',
            name='inventory_size',
            field=models.CharField(max_length=30, null=True, db_column='INVENTORY_SIZE', blank=True),
        ),
        migrations.AddField(
            model_name='liftdetails',
            name='inventory_status_lift',
            field=models.CharField(max_length=20, null=True, db_column='INVENTORY_STATUS_LIFT', blank=True),
        ),
    ]
