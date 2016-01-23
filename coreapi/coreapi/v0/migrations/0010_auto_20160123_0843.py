# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('v0', '0009_auto_20160120_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliertypesociety',
            name='created_by',
            field=models.ForeignKey(related_name='societies', db_column='CREATED_BY', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 23, 8, 43, 21, 413391, tzinfo=utc), auto_now_add=True, db_column='CREATED_ON'),
            preserve_default=False,
        ),
    ]
