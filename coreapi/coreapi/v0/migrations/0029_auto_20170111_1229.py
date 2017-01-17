# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0028_auto_20170110_1056'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='auditdate',
            table='audit_date',
        ),
    ]
