# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0014_remove_shortlistedspacesversion_dummy'),
    ]

    operations = [
        migrations.AddField(
            model_name='shortlistedspacesversion',
            name='dummy',
            field=models.BooleanField(default=False),
        ),
    ]
