# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0015_shortlistedspacesversion_dummy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shortlistedspacesversion',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='shortlistedspacesversion',
            name='space_mapping_version',
        ),
        migrations.DeleteModel(
            name='ShortlistedSpacesVersion',
        ),
    ]
