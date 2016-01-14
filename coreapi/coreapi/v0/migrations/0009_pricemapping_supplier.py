# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0008_auto_20160114_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='pricemapping',
            name='supplier',
            field=models.ForeignKey(related_name='inv_prices', db_column='SUPPLIER_ID', blank=True, to='v0.SupplierTypeSociety', null=True),
        ),
    ]
