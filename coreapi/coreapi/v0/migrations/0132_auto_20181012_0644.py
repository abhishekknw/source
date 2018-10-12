# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-12 06:44
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0131_auto_20181011_1008'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('email_type', models.CharField(choices=[(b'WEEKLY_LEADS', b'WEEKLY_LEADS'), (b'WEEKLY_LEADS_GRAPH', b'WEEKLY_LEADS_GRAPH'), (b'BOOKING_DETAILS_BASIC', b'BOOKING_DETAILS_BASIC'), (b'BOOKING_DETAILS_ADV', b'BOOKING_DETAILS_ADV')], max_length=70, null=True)),
                ('is_allowed', models.BooleanField(default=False)),
                ('last_sent', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'email_settings',
            },
        ),
        migrations.AlterUniqueTogether(
            name='emailsettings',
            unique_together=set([('user', 'email_type')]),
        ),
    ]