# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0026_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactdetails',
            name='std_code',
            field=models.CharField(max_length=6, null=True, db_column='STD_CODE', blank=True),
        ),
    ]
