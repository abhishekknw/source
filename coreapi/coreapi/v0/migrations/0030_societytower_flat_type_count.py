# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0029_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='societytower',
            name='flat_type_count',
            field=models.IntegerField(null=True, db_column='FLAT_TYPE_COUNT', blank=True),
        ),
    ]
