# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0004_auto_20160705_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliertypesociety',
            name='banner_allowed',
            field=models.BooleanField(default=False, db_column='BANNER_ALLOWED'),
        ),
    ]
