# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0028_standeeinventory_standee_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='standeeinventory',
            name='standee_count',
        ),
    ]
