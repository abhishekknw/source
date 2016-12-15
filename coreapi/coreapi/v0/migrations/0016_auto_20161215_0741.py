# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0015_auto_20161214_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericexportfilename',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='genericexportfilename',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
    ]
