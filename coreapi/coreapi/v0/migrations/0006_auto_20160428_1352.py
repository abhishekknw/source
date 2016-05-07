# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0005_auto_20160428_1038'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlierThroughLobbyInfo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('adinventory_id', models.CharField(max_length=22, null=True, db_column='ADINVENTORY_ID', blank=True)),
                ('flier_distribution_frequency_lobby', models.CharField(max_length=20, null=True, db_column='FLIER_DISTRIBUTION_FREQUENCY_LOBBY', blank=True)),
                ('flier_lobby_inventory_status', models.CharField(max_length=15, null=True, db_column='FLIER_LOBBY_INVENTORY_STATUS', blank=True)),
                ('flier_lobby_price_society', models.FloatField(default=0.0, null=True, db_column='FLIER_LOBBY_PRICE_SOCIETY', blank=True)),
                ('flier_lobby_price_business', models.FloatField(default=0.0, null=True, db_column='FLIER_LOBBY_PRICE_BUSINESS', blank=True)),
                ('master_flier_lobby_price_society', models.FloatField(default=0.0, null=True, db_column='MASTER_FLIER_LOBBY_PRICE_SOCIETY', blank=True)),
                ('master_flier_lobby_price_business', models.FloatField(default=0.0, null=True, db_column='MASTER_FLIER_LOBBY_PRICE_BUSINESS', blank=True)),
                ('supplier', models.ForeignKey(related_name='flier_lobby', db_column='SUPPLIER_ID', blank=True, to='v0.SupplierTypeSociety', null=True)),
            ],
            options={
                'db_table': 'flier_through_lobby_info',
            },
        ),
        migrations.AlterField(
            model_name='societymajorevents',
            name='past_major_events',
            field=models.IntegerField(null=True, db_column='PAST_MAJOR_EVENTS', blank=True),
        ),
    ]
