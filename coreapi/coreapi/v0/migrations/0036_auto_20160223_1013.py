# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0035_auto_20160223_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricemapping',
            name='business_price',
            field=models.IntegerField(db_column='ACTUAL_SOCIETY_PRICE'),
        ),
        migrations.AlterField(
            model_name='pricemapping',
            name='society_price',
            field=models.IntegerField(db_column='SUGGESTED_SOCIETY_PRICE'),
        ),
    ]
