# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0033_auto_20170116_0656'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposalinfo',
            name='is_campaign',
        ),
        migrations.AddField(
            model_name='proposalinfo',
            name='campaign_state',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
    ]
