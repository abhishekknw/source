# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0017_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliertypesociety',
            name='society_locality',
            field=models.CharField(max_length=30, null=True, db_column='SOCIETY_LOCALITY', blank=True),
        ),
    ]
