# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0011_auto_20160914_1910'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shortlistedspacesversion',
            name='space_mapping_version',
        ),
    ]
