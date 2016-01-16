# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0010_auto_20160115_0910'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagemapping',
            name='name',
            field=models.CharField(max_length=50, null=True, db_column='NAME', blank=True),
        ),
        migrations.AlterField(
            model_name='imagemapping',
            name='comments',
            field=models.CharField(max_length=100, null=True, db_column='COMMENTS', blank=True),
        ),
        migrations.AlterField(
            model_name='societyflat',
            name='flat_size_per_sq_feet_builtup_area',
            field=models.FloatField(default=0.0, null=True, db_column='FLAT_SIZE_PER_SQ_FEET_BUILTUP_AREA', blank=True),
        ),
        migrations.AlterField(
            model_name='societyflat',
            name='flat_size_per_sq_feet_carpet_area',
            field=models.FloatField(default=0.0, null=True, db_column='FLAT_SIZE_PER_SQ_FEET_CARPET_AREA', blank=True),
        ),
    ]
