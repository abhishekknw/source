# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0012_proposalinfo_invoice_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposalinfo',
            name='account',
            field=models.ForeignKey(related_name='proposals', to='v0.AccountInfo', null=True),
        ),
    ]
