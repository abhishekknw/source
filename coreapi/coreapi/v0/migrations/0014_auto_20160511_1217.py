# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0013_jmn_society'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commonareadetails',
            name='supplier_id',
        ),
        migrations.AddField(
            model_name='commonareadetails',
            name='supplier',
            field=models.ForeignKey(related_name='ca', db_column='SUPPLIER_ID', blank=True, to='v0.SupplierTypeSociety', null=True),
        ),
    ]
