# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0025_auto_20161007_0646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposalcentermappingversion',
            name='area',
            field=models.CharField(max_length=35, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='proposalcentermappingversion',
            name='city',
            field=models.CharField(max_length=35, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='proposalcentermappingversion',
            name='latitude',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='proposalcentermappingversion',
            name='longitude',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='proposalcentermappingversion',
            name='pincode',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='proposalcentermappingversion',
            name='radius',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='proposalcentermappingversion',
            name='subarea',
            field=models.CharField(max_length=35, null=True, blank=True),
        ),
    ]
