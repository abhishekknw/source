# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0046_auto_20161110_0739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposalmetrics',
            name='proposal_master_cost',
            field=models.ForeignKey(blank=True, to='v0.ProposalMasterCost', null=True),
        ),
    ]
