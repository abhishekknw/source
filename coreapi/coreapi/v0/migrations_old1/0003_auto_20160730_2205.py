# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0002_auto_20160729_1628'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='accountinfo',
            table='account_info',
        ),
        migrations.AlterModelTable(
            name='businessaccountcontact',
            table='business_account_conatct',
        ),
        migrations.AlterModelTable(
            name='businessinfo',
            table='business_info',
        ),
        migrations.AlterModelTable(
            name='businesssubtypes',
            table='business_subtypes',
        ),
        migrations.AlterModelTable(
            name='businesstypes',
            table='business_types',
        ),
        migrations.AlterModelTable(
            name='inventorytype',
            table='inventory_type',
        ),
        migrations.AlterModelTable(
            name='proposalinfo',
            table='proposal_info',
        ),
    ]
