# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('v0', '0026_userprofile_is_normal_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='created_by',
            field=models.ForeignKey(db_column='created_by', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
