# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0014_auto_20160322_1232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='standeeinventory',
            name='supplier',
        ),
        migrations.AddField(
            model_name='standeeinventory',
            name='tower',
            field=models.ForeignKey(related_name='standees', db_column='TOWER_ID', blank=True, to='v0.SocietyTower', null=True),
        ),
        migrations.AlterField(
            model_name='societytower',
            name='flat_type_count',
            field=models.IntegerField(default=0, db_column='FLAT_TYPE_COUNT'),
        ),
        migrations.AlterField(
            model_name='societytower',
            name='lift_count',
            field=models.IntegerField(default=0, db_column='LIFT_COUNT'),
        ),
        migrations.AlterField(
            model_name='societytower',
            name='notice_board_count_per_tower',
            field=models.IntegerField(default=0, db_column='NOTICE_BOARD_COUNT_PER_TOWER'),
        ),
        migrations.AlterField(
            model_name='societytower',
            name='standee_count',
            field=models.IntegerField(default=0, db_column='STANDEE_COUNT'),
        ),
    ]
