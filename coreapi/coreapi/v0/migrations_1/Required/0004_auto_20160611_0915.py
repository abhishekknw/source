# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0003_auto_20160610_1143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='business',
        ),
        migrations.AddField(
            model_name='campaign',
            name='account',
            field=models.ForeignKey(related_name='campaigns', db_column='BUSINESS_ID', to='v0.Account', null=True),
        ),
    ]
