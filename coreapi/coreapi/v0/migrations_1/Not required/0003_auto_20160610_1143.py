# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0002_auto_20160610_0543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='business',
            field=models.ForeignKey(related_name='accounts', db_column='BUSINESS_ID', to='v0.Business', null=True),
        ),
    ]
