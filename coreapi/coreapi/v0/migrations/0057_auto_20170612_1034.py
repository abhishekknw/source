# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0056_data_migration_unique_campaign_id_campaign_assignment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaignassignment',
            name='campaign',
            field=models.OneToOneField(to='v0.ProposalInfo'),
        ),
    ]
