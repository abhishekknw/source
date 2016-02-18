# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0018_suppliertypesociety_society_locality'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adinventorylocationmapping',
            name='adinventory_id',
            field=models.CharField(max_length=22, db_column='ADINVENTORY_ID'),
        ),
        migrations.AlterField(
            model_name='bannerinventory',
            name='adinventory_id',
            field=models.CharField(max_length=22, db_column='ADINVENTORY_ID', blank=True),
        ),
        migrations.AlterField(
            model_name='cardisplayinventory',
            name='adinventory_id',
            field=models.CharField(max_length=22, null=True, db_column='ADINVENTORY_ID', blank=True),
        ),
        migrations.AlterField(
            model_name='doortodoorinfo',
            name='adinventory_id',
            field=models.CharField(max_length=22, null=True, db_column='ADINVENTORY_ID', blank=True),
        ),
        migrations.AlterField(
            model_name='liftdetails',
            name='adinventory_id',
            field=models.CharField(max_length=22, null=True, db_column='ADINVENTORY_ID', blank=True),
        ),
        migrations.AlterField(
            model_name='mailboxinfo',
            name='adinventory_id',
            field=models.CharField(max_length=22, null=True, db_column='ADINVENTORY_ID', blank=True),
        ),
        migrations.AlterField(
            model_name='noticeboarddetails',
            name='adinventory_id',
            field=models.CharField(max_length=22, null=True, db_column='ADINVENTORY_ID', blank=True),
        ),
        migrations.AlterField(
            model_name='poleinventory',
            name='adinventory_id',
            field=models.CharField(max_length=22, null=True, db_column='ADINVENTORY_ID', blank=True),
        ),
        migrations.AlterField(
            model_name='posterinventory',
            name='adinventory_id',
            field=models.CharField(max_length=22, serialize=False, primary_key=True, db_column='ADINVENTORY_ID'),
        ),
        migrations.AlterField(
            model_name='posterinventorymapping',
            name='banner_adinventory_id',
            field=models.CharField(max_length=22, null=True, db_column='BANNER_ADINVENTORY_ID', blank=True),
        ),
        migrations.AlterField(
            model_name='posterinventorymapping',
            name='poster_adinventory_id',
            field=models.CharField(max_length=22, null=True, db_column='POSTER_ADINVENTORY_ID', blank=True),
        ),
        migrations.AlterField(
            model_name='posterinventorymapping',
            name='stall_adinventory_id',
            field=models.CharField(max_length=22, null=True, db_column='STALL_ADINVENTORY_ID', blank=True),
        ),
        migrations.AlterField(
            model_name='posterinventorymapping',
            name='standee_adinventory_id',
            field=models.CharField(max_length=22, null=True, db_column='STANDEE_ADINVENTORY_ID', blank=True),
        ),
        migrations.AlterField(
            model_name='stallinventory',
            name='adinventory_id',
            field=models.CharField(max_length=22, db_column='ADINVENTORY_ID'),
        ),
        migrations.AlterField(
            model_name='standeeinventory',
            name='adinventory_id',
            field=models.CharField(max_length=22, null=True, db_column='ADINVENTORY_ID', blank=True),
        ),
        migrations.AlterField(
            model_name='streetfurniture',
            name='adinventory_id',
            field=models.CharField(max_length=22, null=True, db_column='ADINVENTORY_ID', blank=True),
        ),
        migrations.AlterField(
            model_name='wallinventory',
            name='adinventory_id',
            field=models.CharField(max_length=22, db_column='ADINVENTORY_ID'),
        ),
    ]
