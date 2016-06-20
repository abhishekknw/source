# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0003_auto_20160620_1117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='society_subarea',
        ),
    ]
