# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('v0', '0082_auto_20180301_1355'),
    ]

    operations = [
        migrations.CreateModel(
            name='GatewayArchInventory',
            fields=[
                ('created_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('adinventory_id', models.CharField(unique=True, max_length=22, db_column='ADINVENTORY_ID')),
                ('object_id', models.CharField(max_length=20, null=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', null=True, on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'db_table': 'gateway_arch_inventory',
            },
        ),
    ]
