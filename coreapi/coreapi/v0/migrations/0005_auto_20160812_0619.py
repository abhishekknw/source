# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0004_auto_20160812_0535'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailboxinfo',
            name='tower',
        ),
        migrations.AddField(
            model_name='mailboxinfo',
            name='tower_id',
            field=models.CharField(max_length=20, null=True, db_column='TOWER_ID', blank=True),
        ),
        migrations.AddField(
            model_name='mailboxinfo',
            name='tower_name',
            field=models.CharField(max_length=20, null=True, db_column='TOWER_NAME', blank=True),
        ),
    ]
