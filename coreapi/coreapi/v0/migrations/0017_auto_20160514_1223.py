# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0016_auto_20160514_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='payment_details_available',
            field=models.BooleanField(default=False, db_column='PAYMENT_DETAILS_AVAILABLE'),
        ),
    ]
