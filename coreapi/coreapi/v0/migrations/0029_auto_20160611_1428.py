# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0028_auto_20160611_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='corporate_type',
            field=models.CharField(max_length=25, db_column='CORPORATE_TYPE'),
        ),
    ]
