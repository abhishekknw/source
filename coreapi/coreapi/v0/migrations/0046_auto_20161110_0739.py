# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0045_auto_20161102_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasciencescost',
            name='proposal_master_cost',
            field=models.ForeignKey(blank=True, to='v0.ProposalMasterCost', null=True),
        ),
        migrations.AlterField(
            model_name='eventstaffingcost',
            name='proposal_master_cost',
            field=models.ForeignKey(blank=True, to='v0.ProposalMasterCost', null=True),
        ),
        migrations.AlterField(
            model_name='ideationdesigncost',
            name='proposal_master_cost',
            field=models.ForeignKey(blank=True, to='v0.ProposalMasterCost', null=True),
        ),
        migrations.AlterField(
            model_name='logisticoperationscost',
            name='proposal_master_cost',
            field=models.ForeignKey(blank=True, to='v0.ProposalMasterCost', null=True),
        ),
        migrations.AlterField(
            model_name='printingcost',
            name='proposal_master_cost',
            field=models.ForeignKey(blank=True, to='v0.ProposalMasterCost', null=True),
        ),
        migrations.AlterField(
            model_name='spacebookingcost',
            name='proposal_master_cost',
            field=models.ForeignKey(blank=True, to='v0.ProposalMasterCost', null=True),
        ),
    ]
