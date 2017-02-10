# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0044_auto_20170210_0719'),
    ]

    operations = [
        migrations.AddField(
            model_name='amenity',
            name='code',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
    ]
