# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0020_auto_20160212_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactdetails',
            name='country_code',
            field=models.IntegerField(null=True, db_column='COUNTRY_CODE', blank=True),
        ),
        migrations.AddField(
            model_name='contactdetails',
            name='salutation',
            field=models.CharField(max_length=50, null=True, db_column='SALUTATION', blank=True),
        ),
        migrations.AddField(
            model_name='contactdetails',
            name='std_code',
            field=models.IntegerField(null=True, db_column='STD_CODE', blank=True),
        ),
    ]
