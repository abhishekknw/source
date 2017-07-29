# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0062_auto_20170727_0701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactdetails',
            name='object_id',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='events',
            name='object_id',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='flattype',
            name='object_id',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='flyerinventory',
            name='object_id',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='imagemapping',
            name='object_id',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='inventorysummary',
            name='object_id',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='posterinventory',
            name='object_id',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='pricemappingdefault',
            name='object_id',
            field=models.CharField(max_length=20, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='shortlistedspaces',
            name='object_id',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='societytower',
            name='object_id',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='stallinventory',
            name='object_id',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='standeeinventory',
            name='object_id',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='wallinventory',
            name='object_id',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
