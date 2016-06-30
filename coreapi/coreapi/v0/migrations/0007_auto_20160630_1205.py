# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0006_auto_20160630_1201'),
    ]

    operations = [
        migrations.RenameField(
            model_name='suppliertypesociety',
            old_name='cd_allowed',
            new_name='car_display_allowed',
        ),
    ]
