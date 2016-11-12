# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0047_auto_20161110_0751'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='city',
            unique_together=set([('state_code', 'city_code')]),
        ),
    ]
