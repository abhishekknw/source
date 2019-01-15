# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0023_auto_20170108_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='stallinventory',
            name='status',
            field=models.CharField(default='F', max_length=10),
        ),
        migrations.AddField(
            model_name='standeeinventory',
            name='status',
            field=models.CharField(default='F', max_length=10),
        ),
    ]
