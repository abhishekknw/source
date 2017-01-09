# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0021_auto_20170108_1322'),
    ]

    operations = [
        migrations.RenameField(
            model_name='campaignassignment',
            old_name='campaign_id',
            new_name='campaign',
        ),
    ]
