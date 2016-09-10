# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0007_auto_20160813_0821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stallinventory',
            name='electricity_charges_daily',
            field=models.FloatField(max_length=50, null=True, db_column='ELECTRICITY_CHARGES_DAILY', blank=True),
        ),
    ]
