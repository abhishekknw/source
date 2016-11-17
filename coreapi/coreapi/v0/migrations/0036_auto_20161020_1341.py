# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0035_remove_proposalmastercost_proposal_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shortlistedspaces',
            name='space_mapping',
            field=models.ForeignKey(related_name='spaces', blank=True, to='v0.SpaceMapping', null=True),
        ),
        migrations.AlterField(
            model_name='shortlistedspaces',
            name='supplier_code',
            field=models.CharField(max_length=4, null=True, blank=True),
        ),
    ]
