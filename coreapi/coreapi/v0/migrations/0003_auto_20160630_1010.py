# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0002_auto_20160628_0631'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliertypesociety',
            name='flier_allowed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='poster_allowed_lift',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='poster_allowed_nb',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='stall_allowed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='standee_allowed',
            field=models.BooleanField(default=False),
        ),
    ]
