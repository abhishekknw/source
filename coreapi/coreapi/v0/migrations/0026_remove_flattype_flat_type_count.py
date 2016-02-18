# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0025_auto_20160218_0708'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flattype',
            name='flat_type_count',
        ),
    ]
