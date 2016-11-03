# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0042_filters_supplier_type_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='shortlistedinventorydetails',
            name='supplier_type_code',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
