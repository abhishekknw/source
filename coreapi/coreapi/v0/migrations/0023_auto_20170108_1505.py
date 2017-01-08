# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0022_auto_20170108_1447'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='campaignassignment',
            table='campaign_assignment',
        ),
    ]
