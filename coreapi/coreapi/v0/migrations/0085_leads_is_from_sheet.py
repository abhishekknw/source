# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0084_auto_20180320_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='leads',
            name='is_from_sheet',
            field=models.BooleanField(default=False),
        ),
    ]
