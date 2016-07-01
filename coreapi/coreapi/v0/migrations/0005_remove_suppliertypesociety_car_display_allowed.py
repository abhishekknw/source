# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0004_suppliertypesociety_car_display_allowed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='car_display_allowed',
        ),
    ]
