# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0023_auto_20160929_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventorysummary',
            name='content_type',
            field=models.ForeignKey(default=None, to='contenttypes.ContentType', null=True),
        ),
    ]
