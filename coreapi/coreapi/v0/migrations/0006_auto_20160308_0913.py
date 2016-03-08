# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0005_assignedaudits'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignSupplierTypes',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('supplier_type', models.CharField(max_length=20, db_column='SUPPLIER_TYPE', blank=True)),
                ('count', models.IntegerField(null=True, db_column='COUNT')),
                ('campaign', models.ForeignKey(related_name='supplier_types', db_column='CAMPAIGN_ID', to='v0.Campaign', null=True)),
            ],
            options={
                'db_table': 'campaign_supplier_types',
            },
        ),
        migrations.RenameField(
            model_name='business',
            old_name='business_sub_type',
            new_name='sub_type',
        ),
        migrations.RenameField(
            model_name='business',
            old_name='business_type',
            new_name='type',
        ),
        migrations.RemoveField(
            model_name='business',
            name='reference',
        ),
        migrations.AddField(
            model_name='business',
            name='reference_email',
            field=models.CharField(max_length=50, db_column='REFERENCE_EMAIL', blank=True),
        ),
        migrations.AddField(
            model_name='business',
            name='reference_name',
            field=models.CharField(max_length=50, db_column='REFERENCE_NAME', blank=True),
        ),
        migrations.AddField(
            model_name='business',
            name='reference_phone',
            field=models.CharField(max_length=10, db_column='REFERENCE_PHONE', blank=True),
        ),
        migrations.AddField(
            model_name='businesscontact',
            name='department',
            field=models.CharField(max_length=20, db_column='DEPARTMENT', blank=True),
        ),
    ]
