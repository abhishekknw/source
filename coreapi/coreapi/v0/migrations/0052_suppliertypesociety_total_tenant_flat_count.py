# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0051_baseuser_mobile'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliertypesociety',
            name='total_tenant_flat_count',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
