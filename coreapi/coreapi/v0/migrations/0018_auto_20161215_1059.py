# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0017_auto_20161215_1014'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountinfo',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='accountinfo',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='businessaccountcontact',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='businessaccountcontact',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='businessinfo',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='businessinfo',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='businesssubtypes',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='businesssubtypes',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='businesstypes',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='businesstypes',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='campaignleads',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='campaignleads',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='custompermissions',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='custompermissions',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='datasciencescost',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='datasciencescost',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='eventstaffingcost',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='eventstaffingcost',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='filters',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='filters',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='ideationdesigncost',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='ideationdesigncost',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='inventorysummary',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='lead',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='lead',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='logisticoperationscost',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='logisticoperationscost',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='pricemappingdefault',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='pricemappingdefault',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='printingcost',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='printingcost',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='proposalcentermapping',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='proposalcentermapping',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='proposalcentersuppliers',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='proposalcentersuppliers',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='proposalmastercost',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='proposalmastercost',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='proposalmetrics',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='proposalmetrics',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='shortlistedinventorypricingdetails',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='shortlistedinventorypricingdetails',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='shortlistedspaces',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='shortlistedspaces',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='spacebookingcost',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='spacebookingcost',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='suppliertypebusshelter',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='suppliertypebusshelter',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='suppliertypecorporate',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='suppliertypecorporate',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='suppliertypegym',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='suppliertypegym',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='suppliertypesalon',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
        migrations.AddField(
            model_name='suppliertypesalon',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 1, 0, 0, tzinfo=utc), editable=False),
        ),
    ]
