# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0009_pricemapping_supplier'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageMapping',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('location_id', models.CharField(max_length=20, db_column='LOCATION_ID')),
                ('location_type', models.CharField(max_length=20, null=True, db_column='LOCATION_TYPE', blank=True)),
                ('image_url', models.CharField(max_length=100, db_column='IMAGE_URL')),
                ('comments', models.CharField(max_length=100, db_column='COMMENTS')),
                ('supplier', models.ForeignKey(related_name='images', db_column='SUPPLIER_ID', blank=True, to='v0.SupplierTypeSociety', null=True)),
            ],
            options={
                'db_table': 'image_mapping',
            },
        ),
        migrations.RemoveField(
            model_name='contactdetails',
            name='supplier_id',
        ),
        migrations.AddField(
            model_name='contactdetails',
            name='supplier',
            field=models.ForeignKey(related_name='contacts', db_column='SUPPLIER_ID', blank=True, to='v0.SupplierTypeSociety', null=True),
        ),
        migrations.AlterField(
            model_name='adinventorylocationmapping',
            name='adinventory_name',
            field=models.CharField(default='POSTER', max_length=10, db_column='ADINVENTORY_NAME', choices=[('POSTER', 'Poster'), ('STANDEE', 'Standee'), ('STALL', 'Stall'), ('BANNER', 'Banner')]),
        ),
        migrations.AlterField(
            model_name='adinventorytype',
            name='adinventory_name',
            field=models.CharField(default='POSTER', max_length=10, db_column='ADINVENTORY_NAME', choices=[('POSTER', 'Poster'), ('STANDEE', 'Standee'), ('STALL', 'Stall'), ('BANNER', 'Banner')]),
        ),
        migrations.AlterField(
            model_name='societyflat',
            name='average_rent_pers_sqft_tower',
            field=models.IntegerField(null=True, db_column='AVERAGE_RENT_PERS_SQFT_TOWER', blank=True),
        ),
        migrations.AlterField(
            model_name='societyflat',
            name='flat_rent',
            field=models.IntegerField(null=True, db_column='FLAT_RENT', blank=True),
        ),
        migrations.AlterField(
            model_name='societyflat',
            name='flat_size_per_sq_feet_builtup_area',
            field=models.IntegerField(null=True, db_column='FLAT_SIZE_PER_SQ_FEET_BUILTUP_AREA', blank=True),
        ),
        migrations.AlterField(
            model_name='societyflat',
            name='flat_size_per_sq_feet_carpet_area',
            field=models.IntegerField(null=True, db_column='FLAT_SIZE_PER_SQ_FEET_CARPET_AREA', blank=True),
        ),
        migrations.AlterField(
            model_name='societyflat',
            name='rent_per_sqft',
            field=models.IntegerField(null=True, db_column='RENT_PER_SQFT', blank=True),
        ),
    ]
