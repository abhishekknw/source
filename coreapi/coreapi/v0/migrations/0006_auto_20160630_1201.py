# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0005_remove_suppliertypesociety_car_display_allowed'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliertypesociety',
            name='cd_allowed',
            field=models.BooleanField(default=False, db_column='CAR_DISPLAY_ALLOWED'),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='flier_allowed',
            field=models.BooleanField(default=False, db_column='FLIER_ALLOWED'),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='poster_allowed_lift',
            field=models.BooleanField(default=False, db_column='POSTER_ALLOWED_LIFT'),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='poster_allowed_nb',
            field=models.BooleanField(default=False, db_column='POSTER_ALLOWED_NB'),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='stall_allowed',
            field=models.BooleanField(default=False, db_column='STALL_ALLOWED'),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='standee_allowed',
            field=models.BooleanField(default=False, db_column='STANDEE_ALLOWED'),
        ),
    ]
