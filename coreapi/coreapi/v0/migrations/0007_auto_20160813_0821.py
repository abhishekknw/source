# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0006_remove_mailboxinfo_tower_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlyerInventory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('adinventory_id', models.CharField(unique=True, max_length=22, db_column='ADINVENTORY_ID')),
                ('flat_count', models.IntegerField(null=True, db_column='FLAT_COUNT', blank=True)),
                ('mailbox_allowed', models.BooleanField(default=False, db_column='MAILBOX_ALLOWED')),
                ('d2d_allowed', models.BooleanField(default=False, db_column='D2D_ALLOWED')),
                ('lobbytolobby_allowed', models.BooleanField(default=False, db_column='LOBBYTOLOBBY_ALLOWED')),
                ('supplier', models.ForeignKey(related_name='flyers', db_column='SUPPLIER_ID', blank=True, to='v0.SupplierTypeSociety', null=True)),
            ],
            options={
                'db_table': 'flyer_inventory',
            },
        ),
        migrations.AlterField(
            model_name='stallinventory',
            name='electricity_charges_daily',
            field=models.FloatField(max_length=50, null=True, db_column='E LECTRICITY_CHARGES_DAILY', blank=True),
        ),
    ]
