# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0051_auto_20161114_0727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposalinfo',
            name='proposal_id',
            field=models.CharField(max_length=255, serialize=False, primary_key=True),
        ),
    ]
