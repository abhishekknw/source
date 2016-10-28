# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0034_auto_20161020_1659'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SupplierTypeGym',
        ),
        migrations.DeleteModel(
            name='SupplierTypeSalon',
        ),
    ]
