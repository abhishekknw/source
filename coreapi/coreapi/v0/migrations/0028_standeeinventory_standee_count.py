# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0027_auto_20160219_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='standeeinventory',
            name='standee_count',
            field=models.IntegerField(null=True, db_column='STANDEE_COUNT', blank=True),
        ),
    ]
