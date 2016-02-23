# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0010_auto_20160123_0843'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliertypesociety',
            name='tower_count',
            field=models.IntegerField(null=True, db_column='TOWER_COUNT', blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='total_ad_spaces',
            field=models.IntegerField(null=True, db_column='TOTAL_AD_SPACES'),
        ),
    ]
