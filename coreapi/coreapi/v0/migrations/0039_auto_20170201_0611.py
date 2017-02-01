# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0038_auto_20170120_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliertypebusshelter',
            name='food_tasting_allowed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='suppliertypebusshelter',
            name='sales_allowed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='suppliertypecorporate',
            name='food_tasting_allowed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='suppliertypecorporate',
            name='sales_allowed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='suppliertypegym',
            name='food_tasting_allowed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='suppliertypegym',
            name='sales_allowed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='suppliertypesalon',
            name='food_tasting_allowed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='suppliertypesalon',
            name='sales_allowed',
            field=models.BooleanField(default=False),
        ),
    ]
