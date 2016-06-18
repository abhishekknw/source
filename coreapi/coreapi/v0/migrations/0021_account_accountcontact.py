# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0020_auto_20160519_0937'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('name', models.CharField(max_length=50, db_column='NAME', blank=True)),
                ('phone', models.CharField(max_length=10, db_column='PHONE', blank=True)),
                ('email', models.CharField(max_length=50, db_column='EMAILID', blank=True)),
                ('address', models.CharField(max_length=100, db_column='ADDRESS', blank=True)),
                ('reference_name', models.CharField(max_length=50, db_column='REFERENCE_NAME', blank=True)),
                ('reference_phone', models.CharField(max_length=10, db_column='REFERENCE_PHONE', blank=True)),
                ('reference_email', models.CharField(max_length=50, db_column='REFERENCE_EMAIL', blank=True)),
                ('comments', models.TextField(max_length=100, db_column='COMMENTS', blank=True)),
                ('business', models.ForeignKey(related_name='business', db_column='BUSINESS_ID', to='v0.Business', null=True)),
            ],
            options={
                'db_table': 'account',
            },
        ),
        migrations.CreateModel(
            name='AccountContact',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('name', models.CharField(max_length=50, db_column='NAME', blank=True)),
                ('designation', models.CharField(max_length=20, db_column='DESIGNATION', blank=True)),
                ('department', models.CharField(max_length=20, db_column='DEPARTMENT', blank=True)),
                ('phone', models.CharField(max_length=10, db_column='PHONE', blank=True)),
                ('email', models.CharField(max_length=50, db_column='EMAILID', blank=True)),
                ('spoc', models.BooleanField(default=False, db_column='SPOC')),
                ('comments', models.TextField(max_length=100, db_column='COMMENTS', blank=True)),
                ('account', models.ForeignKey(related_name='contacts', db_column='ACCOUNT_ID', to='v0.Account', null=True)),
            ],
            options={
                'db_table': 'account_contact',
            },
        ),
    ]
