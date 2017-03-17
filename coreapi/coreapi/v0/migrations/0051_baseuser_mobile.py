# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0050_posterinventory_tower'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='mobile',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
