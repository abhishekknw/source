# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0089_leads_is_interested'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='account_no',
            field=models.BigIntegerField(null=True, db_column='ACCOUNT_NUMBER', blank=True),
        ),
    ]
