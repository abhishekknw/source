# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0014_auto_20160511_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventorysummary',
            name='supplier',
            field=models.ForeignKey(related_name='inventoy_summary', null=True, db_column='SUPPLIER_ID', blank=True, to='v0.SupplierTypeSociety', unique=True),
        ),
    ]
