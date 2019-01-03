# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0007_auto_20161209_1001'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountinfo',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AddField(
            model_name='proposalinfo',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE),
        ),
    ]
