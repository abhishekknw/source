# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0003_auto_20160405_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliertypesociety',
            name='society_off',
            field=models.BooleanField(default=False, db_column='SOCIETY_OFF'),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='bachelor_tenants_allowed',
            field=models.CharField(max_length=5, null=True, db_column='BACHELOR_TENANTS_ALLOWED'),
        ),
    ]
