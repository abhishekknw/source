# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('v0', '0016_auto_20160922_0659'),
    ]

    operations = [
        migrations.AddField(
            model_name='pricemappingdefault',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='pricemappingdefault',
            name='object_id',
            field=models.CharField(max_length=12, null=True),
        ),
    ]
