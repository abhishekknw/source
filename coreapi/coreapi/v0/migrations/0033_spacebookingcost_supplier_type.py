# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('v0', '0032_auto_20161017_0633'),
    ]

    operations = [
        migrations.AddField(
            model_name='spacebookingcost',
            name='supplier_type',
            field=models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True),
        ),
    ]
