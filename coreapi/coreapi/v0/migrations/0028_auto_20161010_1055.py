# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('v0', '0027_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShortlistedInventoryDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('supplier_id', models.CharField(max_length=100, null=True)),
                ('inventory_price', models.FloatField(default=0.0)),
                ('inventory_count', models.IntegerField(default=0)),
                ('factor', models.IntegerField(default=0.0)),
                ('inventory_type', models.ForeignKey(to='contenttypes.ContentType', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='inventorytype',
            name='banner_count',
        ),
        migrations.RemoveField(
            model_name='inventorytype',
            name='banner_price',
        ),
        migrations.RemoveField(
            model_name='inventorytype',
            name='flier_count',
        ),
        migrations.RemoveField(
            model_name='inventorytype',
            name='flier_price',
        ),
        migrations.RemoveField(
            model_name='inventorytype',
            name='poster_count',
        ),
        migrations.RemoveField(
            model_name='inventorytype',
            name='poster_price',
        ),
        migrations.RemoveField(
            model_name='inventorytype',
            name='stall_count',
        ),
        migrations.RemoveField(
            model_name='inventorytype',
            name='stall_price',
        ),
        migrations.RemoveField(
            model_name='inventorytype',
            name='standee_count',
        ),
        migrations.RemoveField(
            model_name='inventorytype',
            name='standee_price',
        ),
        migrations.AlterField(
            model_name='proposalcentermappingversion',
            name='area',
            field=models.CharField(default='', max_length=35),
        ),
        migrations.AlterField(
            model_name='proposalcentermappingversion',
            name='city',
            field=models.CharField(default='', max_length=35),
        ),
        migrations.AlterField(
            model_name='proposalcentermappingversion',
            name='latitude',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='proposalcentermappingversion',
            name='longitude',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='proposalcentermappingversion',
            name='pincode',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='proposalcentermappingversion',
            name='radius',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='proposalcentermappingversion',
            name='subarea',
            field=models.CharField(default='', max_length=35),
        ),
        migrations.AlterModelTable(
            name='accountinfo',
            table='account_info',
        ),
        migrations.AlterModelTable(
            name='businessaccountcontact',
            table='business_account_contact',
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
