# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0019_auto_20160516_1206'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessSubTypes',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('sub_type', models.CharField(max_length=100, db_column='SUBTYPE', blank=True)),
            ],
            options={
                'db_table': 'business_subtypes',
            },
        ),
        migrations.CreateModel(
            name='BusinessTypes',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('type_name', models.CharField(max_length=100, db_column='BUSINESS_TYPE', blank=True)),
            ],
            options={
                'db_table': 'business_types',
            },
        ),
        migrations.AlterField(
            model_name='business',
            name='sub_type',
            field=models.CharField(max_length=100, db_column='SUB_TYPE', blank=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='type',
            field=models.CharField(max_length=100, db_column='TYPE', blank=True),
        ),
        migrations.AddField(
            model_name='businesssubtypes',
            name='business',
            field=models.ForeignKey(related_name='business_subtypes', db_column='BUSINESS_TYPE', to='v0.BusinessTypes', null=True),
        ),
    ]
