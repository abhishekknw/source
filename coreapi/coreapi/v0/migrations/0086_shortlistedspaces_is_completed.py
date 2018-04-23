# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0085_leads_is_from_sheet'),
    ]

    operations = [
        migrations.AddField(
            model_name='shortlistedspaces',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]
