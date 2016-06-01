# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0021_account_accountcontact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posterinventory',
            name='adinventory_id',
            field=models.CharField(max_length=25, serialize=False, primary_key=True, db_column='ADINVENTORY_ID'),
        ),
    ]
