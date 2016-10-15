# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0029_auto_20161010_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposalcentermapping',
            name='latitude',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='proposalcentermapping',
            name='longitude',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='proposalcentermapping',
            name='radius',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='proposalcentermappingversion',
            name='latitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='proposalcentermappingversion',
            name='longitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='proposalcentermappingversion',
            name='radius',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='shortlistedinventorydetails',
            name='factor',
            field=models.IntegerField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='shortlistedinventorydetails',
            name='inventory_count',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='shortlistedinventorydetails',
            name='inventory_price',
            field=models.FloatField(default=0.0, null=True),
        ),
    ]
