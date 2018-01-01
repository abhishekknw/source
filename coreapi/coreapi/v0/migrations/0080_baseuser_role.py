# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0079_role_rolehierarchy'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='role',
            field=models.ForeignKey(blank=True, to='v0.Role', null=True),
        ),
    ]
