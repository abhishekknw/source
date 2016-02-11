# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0012_auto_20160206_0605'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stallinventory',
            name='photograph_1',
        ),
        migrations.RemoveField(
            model_name='stallinventory',
            name='photograph_2',
        ),
        migrations.RemoveField(
            model_name='stallinventory',
            name='stall_size_area',
        ),
        migrations.RemoveField(
            model_name='stallinventory',
            name='stall_timings_evening',
        ),
        migrations.RemoveField(
            model_name='stallinventory',
            name='stall_timings_morning',
        ),
        migrations.AlterField(
            model_name='events',
            name='past_gathering_per_event',
            field=models.IntegerField(null=True, db_column='PAST_GATHERING_PER_EVENT', blank=True),
        ),
    ]
