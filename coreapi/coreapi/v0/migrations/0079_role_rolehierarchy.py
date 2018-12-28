# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0078_data_migration_for_initial_general_permission_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=255)),
                ('organisation', models.ForeignKey(to='v0.Organisation', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'db_table': 'role',
            },
        ),
        migrations.CreateModel(
            name='RoleHierarchy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('depth', models.IntegerField(default=0)),
                ('child', models.ForeignKey(to='v0.Role', on_delete=django.db.models.deletion.CASCADE)),
                ('parent', models.ForeignKey(related_name='parent', to='v0.Role', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'db_table': 'role_hierarchy',
            },
        ),
    ]
