# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0040_proposalcentersuppliers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposalinfo',
            name='account',
            field=models.ForeignKey(related_name='proposals', to='v0.AccountInfo'),
        ),
        migrations.AlterField(
            model_name='proposalinfo',
            name='name',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='proposalinfo',
            name='payment_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='proposalinfo',
            name='proposal_id',
            field=models.CharField(max_length=15, serialize=False, primary_key=True),
        ),
    ]
