# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0011_auto_20160308_1247'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlatTypeCode',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('flat_type_name', models.CharField(max_length=20, null=True, db_column='FLAT_TYPE_NAME')),
                ('flat_type_code', models.CharField(max_length=5, null=True, db_column='FLAT_TYPE_CODE')),
            ],
            options={
                'db_table': 'flat_type_code',
            },
        ),
        migrations.RenameModel(
            old_name='SupplierType',
            new_name='SupplierTypeCode',
        ),
        migrations.AddField(
            model_name='citysubarea',
            name='city_code',
            field=models.ForeignKey(related_name='citycodes', db_column='CITY_CODE', to='v0.City', null=True),
        ),
        migrations.AlterField(
            model_name='city',
            name='state_code',
            field=models.ForeignKey(related_name='statecode', db_column='STATE_CODE', to='v0.State', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='citysubarea',
            unique_together=set([('area_code', 'city_code')]),
        ),
        migrations.AlterModelTable(
            name='suppliertypecode',
            table='supplier_type_code',
        ),
    ]
