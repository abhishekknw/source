# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0003_auto_20160709_0916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposalinfoversion',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
