# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0008_auto_20160305_1011'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='count_46to60',
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='count_46_60',
            field=models.IntegerField(null=True, db_column='COUNT_46-60', blank=True),
        ),
    ]
