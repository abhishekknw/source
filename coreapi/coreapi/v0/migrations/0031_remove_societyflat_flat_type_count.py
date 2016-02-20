# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0030_societytower_flat_type_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='societyflat',
            name='flat_type_count',
        ),
    ]
