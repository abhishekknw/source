# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-25 13:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0105_shortlistedspaces_transaction_or_check_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplierPhase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False)),
                ('phase_no', models.CharField(blank=True, default=b'', max_length=10, null=True)),
                ('start_date', models.DateTimeField(null=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('comments', models.CharField(blank=True, max_length=255, null=True)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='v0.ProposalInfo')),
            ],
            options={
                'db_table': 'supplier_phase',
            },
        ),
    ]