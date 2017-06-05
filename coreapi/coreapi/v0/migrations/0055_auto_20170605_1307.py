# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0054_auto_20170417_1354'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pricemappingdefault',
            old_name='business_price',
            new_name='actual_supplier_price',
        ),
        migrations.RenameField(
            model_name='pricemappingdefault',
            old_name='supplier_price',
            new_name='suggested_supplier_price',
        ),
    ]
