# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0002_auto_20161206_1201'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='businessaccountcontact',
            name='user',
        ),
    ]
