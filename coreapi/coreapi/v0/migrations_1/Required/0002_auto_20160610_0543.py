# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignInventoryPrice',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('master_factor', models.IntegerField(null=True, db_column='MASTER_FACTOR')),
                ('business_price', models.IntegerField(null=True, db_column='BUSINESS_PRICE')),
                ('campaign', models.ForeignKey(related_name='campaign', db_column='CAMPAIGN_ID', to='v0.Campaign', null=True)),
                ('supplier', models.ForeignKey(related_name='inventoryprice', null=True, db_column='SUPPLIER_ID', blank=True, to='v0.SupplierTypeSociety', unique=True)),
            ],
            options={
                'db_table': 'campaign_inventory_price',
            },
        ),
        migrations.CreateModel(
            name='CampaignOtherCost',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('content_dev_cost', models.IntegerField(null=True, db_column='CONTENT_DEV_COST')),
                ('pm_cost', models.IntegerField(null=True, db_column='PROJECT_MGMT_COST')),
                ('data_analytics', models.IntegerField(null=True, db_column='DATA_ANALYTICS')),
                ('printing_cost', models.IntegerField(null=True, db_column='PRINTING_COST')),
                ('digital_camp_cost', models.IntegerField(null=True, db_column='DIGITAL_CAMP_COST')),
                ('campaign', models.ForeignKey(related_name='campaign_cost', db_column='CAMPAIGN_ID', to='v0.Campaign', null=True)),
            ],
            options={
                'db_table': 'campaign_other_cost',
            },
        ),
        migrations.RenameField(
            model_name='businesssubtypes',
            old_name='business',
            new_name='business_type',
        ),
        migrations.RemoveField(
            model_name='business',
            name='type',
        ),
        migrations.AddField(
            model_name='business',
            name='type_name',
            field=models.ForeignKey(related_name='type_set', db_column='TYPE', default=None, to='v0.BusinessTypes'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='business',
            name='sub_type',
            field=models.ForeignKey(related_name='sub_type_set', db_column='SUB_TYPE', to='v0.BusinessSubTypes'),
        ),
    ]
