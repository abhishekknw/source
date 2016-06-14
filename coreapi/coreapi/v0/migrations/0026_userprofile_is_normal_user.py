# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0025_auto_20160611_1014'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_normal_user',
            field=models.BooleanField(default=False, db_column='is_normal_user'),
        ),
    ]
