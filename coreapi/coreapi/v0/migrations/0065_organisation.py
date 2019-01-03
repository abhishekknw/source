# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
from django.utils.timezone import utc
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0064_suppliertypebusdepot'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('created_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('organisation_id', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255, blank=True)),
                ('phone', models.CharField(max_length=12, blank=True)),
                ('email', models.CharField(max_length=50, blank=True)),
                ('address', models.CharField(max_length=255, blank=True)),
                ('reference_name', models.CharField(max_length=50, blank=True)),
                ('reference_phone', models.CharField(max_length=10, blank=True)),
                ('reference_email', models.CharField(max_length=50, blank=True)),
                ('comments', models.TextField(max_length=100, blank=True)),
                ('category', models.CharField(default='BUSINESS', max_length=30, choices=[('MACHADALO', 'MACHADALO'), ('BUSINESS', 'BUSINESS'), ('BUSINESS_AGENCY', 'BUSINESS_AGENCY'), ('SUPPLIER_AGENCY', 'SUPPLIER_AGENCY'), ('SUPPLIER', 'SUPPLIER')])),
                ('sub_type', models.ForeignKey(blank=True, to='v0.BusinessSubTypes', null=True, on_delete=django.db.models.deletion.CASCADE)),
                ('type_name', models.ForeignKey(blank=True, to='v0.BusinessTypes', null=True, on_delete=django.db.models.deletion.CASCADE)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'db_table': 'organisation',
            },
        ),
    ]
