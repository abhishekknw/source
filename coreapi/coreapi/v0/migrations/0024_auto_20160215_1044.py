# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0023_auto_20160215_0621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='end_date',
            field=models.DateTimeField(null=True, db_column='END_DATE'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='start_date',
            field=models.DateTimeField(null=True, db_column='START_DATE'),
        ),
    ]
