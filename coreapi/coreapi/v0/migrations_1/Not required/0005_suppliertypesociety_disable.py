# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0004_auto_20160611_0915'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliertypesociety',
            name='disable',
            field=models.BooleanField(default=False, db_column='DISABLED'),
        ),
    ]
