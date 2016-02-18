# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0019_auto_20160212_0648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactdetails',
            name='landline',
            field=models.BigIntegerField(null=True, db_column='CONTACT_LANDLINE', blank=True),
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='mobile',
            field=models.BigIntegerField(null=True, db_column='CONTACT_MOBILE', blank=True),
        ),
    ]
