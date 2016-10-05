# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0022_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flattype',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='flattype',
            name='object_id',
        ),
    ]
