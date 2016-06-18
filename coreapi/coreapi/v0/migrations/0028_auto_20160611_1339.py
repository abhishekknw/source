# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0027_auto_20160610_1516'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='corporateparkcompanylist',
            name='largestemployers',
        ),
        migrations.AddField(
            model_name='corporateparkcompanylist',
            name='largest_employers',
            field=models.BooleanField(default=False, db_column='LARGEST_EMPLOYERS'),
        ),
    ]
