# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0013_auto_20160206_0805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticeboarddetails',
            name='adinventory_id',
            field=models.CharField(max_length=20, null=True, db_column='ADINVENTORY_ID', blank=True),
        ),
    ]
