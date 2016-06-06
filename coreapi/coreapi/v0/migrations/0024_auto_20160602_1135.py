# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0023_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business',
            name='type',
        ),
        migrations.AddField(
            model_name='business',
            name='type_name',
            field=models.CharField(max_length=100, db_column='TYPE', blank=True),
        ),
    ]
