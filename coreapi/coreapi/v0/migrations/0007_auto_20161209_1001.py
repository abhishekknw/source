# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0006_custompermissions'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='custompermissions',
            table='custom_permissions',
        ),
    ]
