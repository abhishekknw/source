# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('v0', '0025_auto_20160611_1014'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliertypesociety',
            name='society_subarea',
            field=models.CharField(max_length=50, null=True, db_column='SOCIETY_SUBAREA', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='created_by',
            field=models.ForeignKey(db_column='created_by', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_normal_user',
            field=models.BooleanField(default=False, db_column='is_normal_user'),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='society_locality',
            field=models.CharField(max_length=50, null=True, db_column='SOCIETY_LOCALITY', blank=True),
        ),
    ]
