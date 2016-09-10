# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0005_auto_20160812_0619'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailboxinfo',
            name='tower_name',
        ),
    ]
