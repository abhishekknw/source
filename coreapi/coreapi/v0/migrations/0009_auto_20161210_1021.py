# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0008_auto_20161210_0640'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalcentermapping',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AddField(
            model_name='proposalcentersuppliers',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE),
        ),
    ]
