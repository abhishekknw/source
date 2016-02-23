# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0021_auto_20160213_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactdetails',
            name='country_code',
            field=models.CharField(max_length=10, null=True, db_column='COUNTRY_CODE', blank=True),
        ),
    ]
