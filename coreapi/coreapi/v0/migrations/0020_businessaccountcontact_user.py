# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0019_auto_20161215_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessaccountcontact',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE),
        ),
    ]
