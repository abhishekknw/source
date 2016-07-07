# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0005_suppliertypesociety_banner_allowed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesssubtypes',
            name='business_sub_type_code',
            field=models.CharField(max_length=3, db_column='SUBTYPE_CODE'),
        ),
    ]
