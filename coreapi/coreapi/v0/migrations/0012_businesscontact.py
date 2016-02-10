# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0011_auto_20160201_1240'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessContact',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('name', models.CharField(max_length=50, db_column='NAME', blank=True)),
                ('designation', models.CharField(max_length=20, db_column='DESIGNATION', blank=True)),
                ('phone', models.IntegerField(null=True, db_column='PHONE')),
                ('email', models.CharField(max_length=50, db_column='EMAILID', blank=True)),
                ('business', models.ForeignKey(related_name='contacts', db_column='BUSINESS_ID', to='v0.Business', null=True)),
            ],
            options={
                'db_table': 'business_contact',
            },
        ),
    ]
