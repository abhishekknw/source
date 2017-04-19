# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0053_auto_20170328_0852'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliertypesociety',
            name='age_group_0_6',
            field=models.IntegerField(default=0, blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='age_group_7_18',
            field=models.IntegerField(default=0, blank=True),
        ),
    ]
