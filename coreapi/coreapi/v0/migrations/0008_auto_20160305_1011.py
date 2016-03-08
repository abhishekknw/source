# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0007_auto_20160304_1340'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='count_0to6',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='count_19_35',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='count_36_50',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='count_50to65',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='count_65above',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='count_6_18',
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='count_0_6',
            field=models.IntegerField(null=True, db_column='COUNT_0-6', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='count_16_30',
            field=models.IntegerField(null=True, db_column='COUNT_16-30', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='count_31_45',
            field=models.IntegerField(null=True, db_column='COUNT_31-45', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='count_46to60',
            field=models.IntegerField(null=True, db_column='COUNT_46to60', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='count_60above',
            field=models.IntegerField(null=True, db_column='count_60above', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='count_7_15',
            field=models.IntegerField(null=True, db_column='COUNT_7-15', blank=True),
        ),
    ]
