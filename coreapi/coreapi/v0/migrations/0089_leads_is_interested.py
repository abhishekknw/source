# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0088_suppliertypesociety_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='leads',
            name='is_interested',
            field=models.BooleanField(default=False),
        ),
    ]
