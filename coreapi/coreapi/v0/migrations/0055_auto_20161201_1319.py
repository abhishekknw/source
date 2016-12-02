# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0054_auto_20161121_1531'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShortlistedInventoryPricingDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('supplier_id', models.CharField(max_length=100)),
                ('inventory_price', models.FloatField(default=0.0, null=True)),
                ('inventory_count', models.IntegerField(default=0, null=True)),
                ('factor', models.IntegerField(default=0.0, null=True)),
                ('supplier_type_code', models.CharField(max_length=255, null=True)),
                ('ad_inventory_duration', models.ForeignKey(to='v0.DurationType', null=True)),
                ('ad_inventory_type', models.ForeignKey(to='v0.AdInventoryType', null=True)),
                ('center', models.ForeignKey(to='v0.ProposalCenterMapping')),
                ('proposal', models.ForeignKey(to='v0.ProposalInfo')),
            ],
            options={
                'db_table': 'shortlisted_inventory_pricing_details',
            },
        ),
        migrations.RemoveField(
            model_name='shortlistedinventorydetails',
            name='inventory_type',
        ),
        migrations.DeleteModel(
            name='ShortlistedInventoryDetails',
        ),
    ]
