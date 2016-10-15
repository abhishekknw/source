# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('v0', '0024_auto_20160929_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='flattype',
            name='content_type',
            field=models.ForeignKey(default=None, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='flattype',
            name='object_id',
            field=models.CharField(max_length=12, null=True),
        ),
    ]
