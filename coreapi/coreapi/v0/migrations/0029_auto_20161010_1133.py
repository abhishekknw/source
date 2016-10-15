# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0028_auto_20161010_1055'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='shortlistedinventorydetails',
            table='shortlisted_inventory_details',
        ),
    ]
