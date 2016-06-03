# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0016_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userareas',
            name='area',
            field=models.ForeignKey(to='v0.CityArea', db_column='area_id'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.ForeignKey(related_name='user_profile', db_column='user_id', to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
