# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0051_auto_20161114_0727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricemappingdefault',
            name='business_price',
            field=models.IntegerField(null=True, db_column='ACTUAL_SOCIETY_PRICE', blank=True),
        ),
        migrations.AlterField(
            model_name='pricemappingdefault',
            name='supplier_price',
            field=models.IntegerField(null=True, db_column='SUGGESTED_SOCIETY_PRICE', blank=True),
        ),
    ]
