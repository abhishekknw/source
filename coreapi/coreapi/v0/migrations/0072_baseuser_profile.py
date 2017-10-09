# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0071_auto_20170919_0623'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='profile',
            field=models.ForeignKey(blank=True, to='v0.Profile', null=True),
        ),
    ]
