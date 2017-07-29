# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0061_auto_20170726_0829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suppliertyperetailshop',
            name='category_name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertyperetailshop',
            name='retail_shop_type',
            field=models.CharField(blank=True, max_length=255, null=True, choices=[('GROCERY_STORE', 'GROCERY_STORE'), ('ELECTRONIC_STORE', 'ELECTRONIC_STORE'), ('SANITARY_STORE', 'SANITARY_STORE'), ('STATIONARY_STORE', 'STATIONARY_STORE')]),
        ),
        migrations.AlterField(
            model_name='suppliertyperetailshop',
            name='size',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
