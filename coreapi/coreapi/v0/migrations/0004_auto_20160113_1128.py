# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0003_auto_20160113_1113'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bannerinventory',
            old_name='banner_display_location',
            new_name='banner_location',
        ),
    ]
