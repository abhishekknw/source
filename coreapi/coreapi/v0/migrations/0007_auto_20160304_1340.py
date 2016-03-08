# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0006_auto_20160229_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doortodoorinfo',
            name='leaflet_handover',
            field=models.CharField(max_length=50, null=True, db_column='LEAFLET_HANDOVER', blank=True),
        ),
    ]
