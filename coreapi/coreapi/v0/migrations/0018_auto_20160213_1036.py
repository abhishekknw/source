# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0017_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='societyinventorybooking',
            name='comments',
        ),
        migrations.AddField(
            model_name='campaignsocietymapping',
            name='adjusted_price',
            field=models.IntegerField(null=True, db_column='ADJUSTED_PRICE'),
        ),
        migrations.AddField(
            model_name='campaignsocietymapping',
            name='comments',
            field=models.TextField(max_length=100, db_column='COMMENTS', blank=True),
        ),
        migrations.AlterField(
            model_name='societyinventorybooking',
            name='adinventory_type',
            field=models.ForeignKey(db_column='ADINVENTORY_TYPE', to='v0.CampaignTypeMapping', null=True),
        ),
        migrations.AlterField(
            model_name='societyinventorybooking',
            name='end_date',
            field=models.DateTimeField(null=True, db_column='END_DATE'),
        ),
        migrations.AlterField(
            model_name='societyinventorybooking',
            name='start_date',
            field=models.DateTimeField(null=True, db_column='START_DATE'),
        ),
    ]
