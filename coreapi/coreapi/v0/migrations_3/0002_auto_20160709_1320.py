# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='spacemapping',
            old_name='saloon_allowed',
            new_name='salon_allowed',
        ),
        migrations.RenameField(
            model_name='spacemapping',
            old_name='saloon_buffer_count',
            new_name='salon_buffer_count',
        ),
        migrations.RenameField(
            model_name='spacemapping',
            old_name='saloon_count',
            new_name='salon_count',
        ),
    ]
