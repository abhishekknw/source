# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0029_remove_standeeinventory_standee_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliertypesociety',
            name='banner_count',
            field=models.IntegerField(null=True, db_column='BANNER_COUNT', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='stall_count',
            field=models.IntegerField(null=True, db_column='STALL_COUNT', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='standee_count',
            field=models.IntegerField(null=True, db_column='STANDEE_COUNT', blank=True),
        ),
    ]
