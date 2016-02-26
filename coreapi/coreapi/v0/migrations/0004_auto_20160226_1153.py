# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0003_auto_20160224_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='average_rent',
            field=models.FloatField(null=True, db_column='AVERAGE_RENT', blank=True),
        ),
    ]
