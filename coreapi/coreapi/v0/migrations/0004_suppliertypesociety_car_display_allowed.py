# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0003_auto_20160630_1010'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliertypesociety',
            name='car_display_allowed',
            field=models.BooleanField(default=False),
        ),
    ]
