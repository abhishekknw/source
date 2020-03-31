# Generated by Django 2.1.4 on 2020-03-31 09:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0003_auto_20200330_2055'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliertypecode',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AddField(
            model_name='suppliertypecode',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='accountinfo',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='accountinfo',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='activitylog',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='activitylog',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='addressmaster',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='addressmaster',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='adinventorytype',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='adinventorytype',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='amenity',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='amenity',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='auditdate',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='auditdate',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='businessaccountcontact',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='businessaccountcontact',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='businessinfo',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='businessinfo',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='businesssubtypes',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='businesssubtypes',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='businesstypes',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='businesstypes',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='campaignassignment',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='campaignassignment',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='campaigncomments',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='campaigncomments',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='custompermissions',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='custompermissions',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='datasciencescost',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='datasciencescost',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='durationtype',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='durationtype',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='emailsettings',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='emailsettings',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='eventstaffingcost',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='eventstaffingcost',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='filters',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='filters',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='flattype',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='flattype',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='flyerinventory',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='flyerinventory',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='gatewayarchinventory',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='gatewayarchinventory',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='generaluserpermission',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='generaluserpermission',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='genericexportfilename',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='genericexportfilename',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='hashtagimages',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='hashtagimages',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='ideationdesigncost',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='ideationdesigncost',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='imagemapping',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='imagemapping',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='inventoryactivity',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='inventoryactivity',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='inventoryactivityassignment',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='inventoryactivityassignment',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='inventoryactivityimage',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='inventoryactivityimage',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='inventorysummary',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='inventorysummary',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='logisticoperationscost',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='logisticoperationscost',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='noticeboarddetails',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='noticeboarddetails',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='organisationmap',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='organisationmap',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='poleinventory',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='poleinventory',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='posterinventory',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='posterinventory',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='pricemappingdefault',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='pricemappingdefault',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='printingcost',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='printingcost',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='proposalcentermapping',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='proposalcentermapping',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='proposalcentersuppliers',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='proposalcentersuppliers',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='proposalinfo',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='proposalinfo',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='proposalmastercost',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='proposalmastercost',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='proposalmetrics',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='proposalmetrics',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='shortlistedinventorypricingdetails',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='shortlistedinventorypricingdetails',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='shortlistedspaces',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='shortlistedspaces',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='societymajorevents',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='societymajorevents',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='spacebookingcost',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='spacebookingcost',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='stallinventory',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='stallinventory',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='standeeinventory',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='standeeinventory',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='sunboardinventory',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='sunboardinventory',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='supplieramenitiesmap',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='supplieramenitiesmap',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='supplierassignment',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='supplierassignment',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='suppliereducationalinstitute',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='suppliereducationalinstitute',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='supplierhording',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='supplierhording',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='suppliermaster',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='suppliermaster',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='supplierphase',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='supplierphase',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='suppliertypebusdepot',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='suppliertypebusdepot',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='suppliertypebusshelter',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='suppliertypebusshelter',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='suppliertypecorporate',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='suppliertypegym',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='suppliertyperetailshop',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='suppliertyperetailshop',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='suppliertypesalon',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='wallinventory',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
        migrations.AlterField(
            model_name='wallinventory',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 31, 14, 55, 9, 130107), editable=False),
        ),
    ]
