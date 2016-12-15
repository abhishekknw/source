# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0016_auto_20161215_0741'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalinfo',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='proposalinfo',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
    ]
