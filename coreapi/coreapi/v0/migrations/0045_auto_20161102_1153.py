# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0044_auto_20161102_1140'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lead',
            old_name='status',
            new_name='lead_status',
        ),
        migrations.RenameField(
            model_name='lead',
            old_name='type',
            new_name='lead_type',
        ),
    ]
