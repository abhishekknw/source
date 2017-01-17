# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0029_auto_20170111_1229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shortlistedinventorypricingdetails',
            name='audit_dates',
        ),
    ]
