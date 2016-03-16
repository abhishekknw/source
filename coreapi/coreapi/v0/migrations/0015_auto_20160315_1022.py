# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0014_inventorysummary'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventorysummary',
            old_name='total_posters_nb',
            new_name='total_poster_nb',
        ),
    ]
