# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0003_auto_20160730_2205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailboxinfo',
            name='tower_id',
        ),
        migrations.AddField(
            model_name='mailboxinfo',
            name='tower',
            field=models.ForeignKey(related_name='fliers', db_column='TOWER_ID', blank=True, to='v0.SocietyTower', null=True),
        ),
    ]
