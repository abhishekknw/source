# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('v0', '0070_data_migration_copy_organisation_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralUserPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=1000, null=True, blank=True)),
                ('is_allowed', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'general_user_permission',
            },
        ),
        migrations.CreateModel(
            name='ObjectLevelPermission',
            fields=[
                ('permission_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='auth.Permission')),
                ('view', models.BooleanField(default=False)),
                ('update', models.BooleanField(default=False)),
                ('create', models.BooleanField(default=False)),
                ('delete', models.BooleanField(default=False)),
                ('view_all', models.BooleanField(default=False)),
                ('update_all', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=1000, null=True, blank=True)),
            ],
            options={
                'db_table': 'object_level_permission',
            },
            bases=('auth.permission',),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('name', models.CharField(max_length=255)),
                ('is_standard', models.BooleanField(default=False)),
                ('organisation', models.ForeignKey(to='v0.Organisation')),
            ],
            options={
                'db_table': 'profile',
            },
        ),
        migrations.AddField(
            model_name='objectlevelpermission',
            name='profile',
            field=models.ForeignKey(to='v0.Profile'),
        ),
        migrations.AddField(
            model_name='generaluserpermission',
            name='profile',
            field=models.ForeignKey(to='v0.Profile'),
        ),
    ]
