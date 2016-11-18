# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0012_auto_20160914_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='shortlistedspacesversion',
            name='space_mapping_version',
            field=models.ForeignKey(related_name='spaces_version', default=1, to='v0.SpaceMappingVersion'),
        ),
    ]
