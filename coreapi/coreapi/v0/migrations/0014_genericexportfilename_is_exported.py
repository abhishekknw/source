# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0013_auto_20161213_0746'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericexportfilename',
            name='is_exported',
            field=models.BooleanField(default=False),
        ),
    ]
