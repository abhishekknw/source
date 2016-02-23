# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0031_remove_societyflat_flat_type_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='flattype',
            name='flat_type_count',
            field=models.IntegerField(null=True, db_column='FLAT_TYPE_COUNT', blank=True),
        ),
        migrations.AlterField(
            model_name='societyflat',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True, db_column='ID'),
        ),
    ]
