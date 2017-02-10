# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0043_amenity_supplieramenitiesmap'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='supplieramenitiesmap',
            table='supplier_amenities_map',
        ),
    ]
