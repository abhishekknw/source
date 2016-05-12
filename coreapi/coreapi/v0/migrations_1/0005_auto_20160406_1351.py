# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0004_auto_20160406_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='past_campaign_occurred',
            field=models.CharField(max_length=5, null=True, db_column='PAST_CAMPAIGN_OCCURRED'),
        ),
    ]
