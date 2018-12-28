# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0049_inventoryactivityassignment_reassigned_activity_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='posterinventory',
            name='tower',
            field=models.ForeignKey(blank=True, to='v0.SocietyTower', null=True, on_delete=django.db.models.deletion.CASCADE),
        ),
    ]
