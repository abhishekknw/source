# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('v0', '0073_auto_20170919_1307'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjectLevelPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=50)),
                ('view', models.BooleanField(default=False)),
                ('update', models.BooleanField(default=False)),
                ('create', models.BooleanField(default=False)),
                ('delete', models.BooleanField(default=False)),
                ('view_all', models.BooleanField(default=False)),
                ('update_all', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=1000, null=True, blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('profile', models.ForeignKey(to='v0.Profile')),
            ],
            options={
                'db_table': 'object_level_permission',
            },
        ),
    ]
