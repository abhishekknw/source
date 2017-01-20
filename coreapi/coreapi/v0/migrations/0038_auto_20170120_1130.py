# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0037_auto_20170120_1127'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shortlistedinventorypricingdetails',
            old_name='comments',
            new_name='comment',
        ),
    ]
