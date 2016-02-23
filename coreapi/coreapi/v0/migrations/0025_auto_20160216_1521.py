# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0024_auto_20160215_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='audits',
            name='image_url',
            field=models.CharField(max_length=100, null=True, db_column='IMAGE_URL'),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='total_ad_spaces',
            field=models.IntegerField(null=True, db_column='TOTAL_AD_SPACES'),
        ),
    ]
