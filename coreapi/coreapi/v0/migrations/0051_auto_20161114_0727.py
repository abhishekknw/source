# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0050_auto_20161114_0706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genericexportfilename',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
