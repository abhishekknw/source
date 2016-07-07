# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0003_auto_20160705_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spacemapping',
            name='corporate_buffer_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='spacemapping',
            name='corporate_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='spacemapping',
            name='gym_buffer_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='spacemapping',
            name='gym_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='spacemapping',
            name='saloon_buffer_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='spacemapping',
            name='saloon_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='spacemapping',
            name='society_buffer_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='spacemapping',
            name='society_count',
            field=models.IntegerField(default=0),
        ),
    ]
