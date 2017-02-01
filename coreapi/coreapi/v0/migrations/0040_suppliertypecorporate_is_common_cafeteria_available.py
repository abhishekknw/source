# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0039_auto_20170201_0611'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliertypecorporate',
            name='is_common_cafeteria_available',
            field=models.BooleanField(default=False),
        ),
    ]
