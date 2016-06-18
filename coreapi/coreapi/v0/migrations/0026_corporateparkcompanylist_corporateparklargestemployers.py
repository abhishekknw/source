# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0025_campaigninventoryprice_campaignothercost_suppliertypecorporate'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorporateParkCompanyList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length='50', db_column='NAME')),
                ('supplier_id', models.ForeignKey(to='v0.SupplierTypeCorporate', db_column='SUPPLIER_ID')),
            ],
            options={
                'db_table': 'corporateparkcompanylist',
            },
        ),
        migrations.CreateModel(
            name='CorporateParkLargestEmployers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length='50', db_column='NAME')),
                ('supplier_id', models.ForeignKey(to='v0.SupplierTypeCorporate', db_column='SUPPLIER_ID')),
            ],
            options={
                'db_table': 'corporateparklargestemployers',
            },
        ),
    ]
