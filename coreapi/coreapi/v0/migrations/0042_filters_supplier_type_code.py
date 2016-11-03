# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0041_auto_20161022_0840'),
    ]

    operations = [
        migrations.AddField(
            model_name='filters',
            name='supplier_type_code',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
