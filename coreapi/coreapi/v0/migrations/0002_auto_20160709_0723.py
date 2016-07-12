# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventorytypeversion',
            old_name='space_mapping',
            new_name='space_mapping_version',
        ),
        migrations.RenameField(
            model_name='proposalcentermappingversion',
            old_name='proposal',
            new_name='proposal_version',
        ),
        migrations.RenameField(
            model_name='shortlistedspacesversion',
            old_name='space_mapping',
            new_name='space_mapping_version',
        ),
        migrations.RenameField(
            model_name='spacemappingversion',
            old_name='center',
            new_name='center_version',
        ),
        migrations.RenameField(
            model_name='spacemappingversion',
            old_name='proposal',
            new_name='proposal_version',
        ),
        migrations.AlterUniqueTogether(
            name='proposalcentermappingversion',
            unique_together=set([('proposal_version', 'center_name')]),
        ),
    ]
