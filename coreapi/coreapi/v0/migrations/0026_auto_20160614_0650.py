# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0025_auto_20160614_0550'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='corporate_form_access',
            field=models.BooleanField(default=False, db_column='corporate_form_access'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='society_form_access',
            field=models.BooleanField(default=False, db_column='society_form_access'),
        ),
    ]
