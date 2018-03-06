# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('v0', '0080_baseuser_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeadAlias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('original_name', models.CharField(max_length=255)),
                ('alias', models.CharField(max_length=255)),
                ('campaign', models.ForeignKey(to='v0.ProposalInfo')),
            ],
            options={
                'db_table': 'lead_alias',
            },
        ),
        migrations.CreateModel(
            name='Leads',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('object_id', models.CharField(max_length=20)),
                ('firstname1', models.CharField(max_length=20, null=True, blank=True)),
                ('lastname1', models.CharField(max_length=20, null=True, blank=True)),
                ('firstname2', models.CharField(max_length=20, null=True, blank=True)),
                ('lastname2', models.CharField(max_length=20, null=True, blank=True)),
                ('mobile1', models.BigIntegerField(null=True, blank=True)),
                ('mobile2', models.BigIntegerField(null=True, blank=True)),
                ('phone', models.BigIntegerField(null=True, blank=True)),
                ('email1', models.EmailField(max_length=50, null=True, blank=True)),
                ('email2', models.EmailField(max_length=50, null=True, blank=True)),
                ('address', models.CharField(max_length=250, null=True, blank=True)),
                ('alphanumeric1', models.CharField(max_length=50, null=True, blank=True)),
                ('alphanumeric2', models.CharField(max_length=50, null=True, blank=True)),
                ('alphanumeric3', models.CharField(max_length=50, null=True, blank=True)),
                ('alphanumeric4', models.CharField(max_length=50, null=True, blank=True)),
                ('boolean1', models.BooleanField(default=False)),
                ('boolean2', models.BooleanField(default=False)),
                ('boolean3', models.BooleanField(default=False)),
                ('boolean4', models.BooleanField(default=False)),
                ('float1', models.FloatField(null=True, blank=True)),
                ('float2', models.FloatField(null=True, blank=True)),
                ('campaign', models.ForeignKey(to='v0.ProposalInfo')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', null=True)),
            ],
            options={
                'db_table': 'leads',
            },
        ),
    ]
