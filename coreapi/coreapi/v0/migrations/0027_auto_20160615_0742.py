# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0026_auto_20160614_0700'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='societytower',
            unique_together=set([('tower_tag', 'supplier')]),
        ),
    ]
