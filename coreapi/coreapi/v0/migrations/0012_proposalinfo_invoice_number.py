# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0011_auto_20161212_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalinfo',
            name='invoice_number',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
    ]
