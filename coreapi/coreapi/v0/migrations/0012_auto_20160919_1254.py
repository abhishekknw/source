# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0011_auto_20160919_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventorysummary',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True),
        ),
    ]
