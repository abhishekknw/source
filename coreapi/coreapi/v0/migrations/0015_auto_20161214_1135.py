# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0014_genericexportfilename_is_exported'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genericexportfilename',
            name='is_exported',
            field=models.BooleanField(default=True),
        ),
    ]
