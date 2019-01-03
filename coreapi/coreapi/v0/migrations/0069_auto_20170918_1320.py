# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0068_data_migration_for_contacts'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountinfo',
            name='organisation',
            field=models.ForeignKey(blank=True, to='v0.Organisation', null=True, on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AddField(
            model_name='genericexportfilename',
            name='organisation',
            field=models.ForeignKey(blank=True, to='v0.Organisation', null=True, on_delete=django.db.models.deletion.CASCADE),
        ),
    ]
