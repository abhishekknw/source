# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spacemapping',
            name='inventory_type_count',
            field=models.IntegerField(default=0),
        ),
    ]
