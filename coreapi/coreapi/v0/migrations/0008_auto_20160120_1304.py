# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0007_auto_20160119_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticeboarddetails',
            name='notice_board_lit',
            field=models.BooleanField(default=True, db_column='NOTICE_BOARD_LIT'),
        ),
    ]
