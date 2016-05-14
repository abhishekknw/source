# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('v0', '0013_jmn_society'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAreas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('area', models.ForeignKey(related_name='areas', db_column='area_id', to='v0.CityArea')),
                ('user', models.ForeignKey(related_name='clusters', db_column='user_id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_areas',
            },
        ),
        migrations.CreateModel(
            name='UserCities',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.ForeignKey(db_column='city_id', to='v0.City', null=True)),
                ('user', models.ForeignKey(related_name='cities', db_column='user_id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_cities',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_city_manager', models.BooleanField(default=False, db_column='is_city_manager')),
                ('is_cluster_manager', models.BooleanField(default=False, db_column='is_cluster_manager')),
                ('user', models.ForeignKey(related_name='profile', db_column='user_id', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'db_table': 'user_profile',
            },
        ),
    ]
