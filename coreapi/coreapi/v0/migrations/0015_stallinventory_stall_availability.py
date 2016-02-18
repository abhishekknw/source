# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0014_auto_20160206_0830'),
    ]

    operations = [
        migrations.AddField(
            model_name='stallinventory',
            name='stall_availability',
            field=models.CharField(max_length=10, null=True, db_column='STALL_AVAILABILITY', blank=True),
        ),
    ]
