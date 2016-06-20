# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0005_suppliertypesociety_society_subarea'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='daily_electricity_charges',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='electricity_available',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='sound_available',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='stall_timing',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='street_furniture_available',
        ),
    ]
