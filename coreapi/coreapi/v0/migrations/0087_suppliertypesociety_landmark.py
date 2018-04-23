# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0086_shortlistedspaces_is_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliertypesociety',
            name='landmark',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
