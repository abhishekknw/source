# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('v0', '0072_baseuser_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='objectlevelpermission',
            name='permission_ptr',
        ),
        migrations.RemoveField(
            model_name='objectlevelpermission',
            name='profile',
        ),
        migrations.DeleteModel(
            name='ObjectLevelPermission',
        ),
    ]
