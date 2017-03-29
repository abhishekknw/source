# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0052_suppliertypesociety_total_tenant_flat_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricemappingdefault',
            name='object_id',
            field=models.CharField(max_length=12, null=True, db_index=True),
        ),
    ]
