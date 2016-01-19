# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0006_auto_20160119_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemapping',
            name='location_id',
            field=models.CharField(max_length=20, null=True, db_column='LOCATION_ID', blank=True),
        ),
    ]
