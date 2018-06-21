# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0090_auto_20180518_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliertypesociety',
            name='representative',
            field=models.ForeignKey(blank=True, to='v0.Organisation', null=True),
        ),
    ]
