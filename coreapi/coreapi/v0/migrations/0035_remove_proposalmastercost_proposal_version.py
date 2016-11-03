# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0034_auto_20161019_0728'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposalmastercost',
            name='proposal_version',
        ),
    ]
