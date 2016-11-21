# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0010_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, db_column='CREATED_ON'),
        ),
    ]
