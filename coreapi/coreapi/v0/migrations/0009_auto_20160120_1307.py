# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0008_auto_20160120_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticeboarddetails',
            name='notice_board_lit',
            field=models.CharField(max_length=5, null=True, db_column='NOTICE_BOARD_LIT', blank=True),
        ),
    ]
