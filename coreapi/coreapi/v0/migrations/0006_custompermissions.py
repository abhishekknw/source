# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0005_genericexportfilename_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomPermissions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('extra_permission_code', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=1000, null=True)),
                ('user', models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
