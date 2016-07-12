# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0002_auto_20160709_0723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposalinfoversion',
            name='proposal',
            field=models.ForeignKey(related_name='proposal_versions', db_column='PROPOSAL', to='v0.ProposalInfo'),
        ),
    ]
