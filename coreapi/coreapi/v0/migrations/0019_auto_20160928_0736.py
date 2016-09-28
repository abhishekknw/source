# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('v0', '0018_auto_20160927_1744'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pricemappingdefault',
            old_name='society_price',
            new_name='supplier_price',
        ),

    ]
