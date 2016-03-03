# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('v0', '0002_load_intial_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditorSocietyMapping',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('user_id', models.IntegerField(null=True, db_column='USER_ID')),
            ],
            options={
                'db_table': 'auditor_society_mapping',
            },
        ),
        migrations.CreateModel(
            name='Audits',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('latitude', models.FloatField(null=True, db_column='LATITUDE')),
                ('longitude', models.FloatField(null=True, db_column='LONGITUDE')),
                ('timestamp', models.DateTimeField(null=True, db_column='TIMESTAMP')),
                ('barcode', models.FloatField(null=True, db_column='BARCODE')),
                ('audited_by', models.IntegerField(null=True, db_column='USER_ID')),
                ('audit_type', models.CharField(max_length=20, db_column='AUDIT_TYPE', blank=True)),
                ('image_url', models.CharField(max_length=100, null=True, db_column='IMAGE_URL')),
            ],
            options={
                'db_table': 'audits',
            },
        ),
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('name', models.CharField(max_length=50, db_column='NAME', blank=True)),
                ('business_type', models.CharField(max_length=20, db_column='TYPE', blank=True)),
                ('business_sub_type', models.CharField(max_length=20, db_column='SUB_TYPE', blank=True)),
                ('phone', models.CharField(max_length=10, db_column='PHONE', blank=True)),
                ('email', models.CharField(max_length=50, db_column='EMAILID', blank=True)),
                ('address', models.CharField(max_length=100, db_column='ADDRESS', blank=True)),
                ('reference', models.CharField(max_length=50, db_column='REFERENCE', blank=True)),
                ('comments', models.TextField(max_length=100, db_column='COMMENTS', blank=True)),
            ],
            options={
                'db_table': 'business',
            },
        ),
        migrations.CreateModel(
            name='BusinessContact',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('name', models.CharField(max_length=50, db_column='NAME', blank=True)),
                ('designation', models.CharField(max_length=20, db_column='DESIGNATION', blank=True)),
                ('phone', models.CharField(max_length=10, db_column='PHONE', blank=True)),
                ('email', models.CharField(max_length=50, db_column='EMAILID', blank=True)),
                ('spoc', models.BooleanField(default=False, db_column='SPOC')),
                ('comments', models.TextField(max_length=100, db_column='COMMENTS', blank=True)),
                ('business', models.ForeignKey(related_name='contacts', db_column='BUSINESS_ID', to='v0.Business', null=True)),
            ],
            options={
                'db_table': 'business_contact',
            },
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('start_date', models.DateTimeField(null=True, db_column='START_DATE')),
                ('end_date', models.DateTimeField(null=True, db_column='END_DATE')),
                ('tentative_cost', models.IntegerField(null=True, db_column='TENTATIVE_COST')),
                ('booking_status', models.CharField(max_length=20, db_column='BOOKING_STATUS', blank=True)),
                ('business', models.ForeignKey(related_name='campaigns', db_column='BUSINESS_ID', to='v0.Business', null=True)),
            ],
            options={
                'db_table': 'campaign',
            },
        ),
        migrations.CreateModel(
            name='CampaignBookingInfo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('booking_id', models.IntegerField(null=True, db_column='BOOKING_ID')),
                ('booking_amount', models.FloatField(null=True, db_column='BOKING_AMOUNT')),
                ('instrument_type', models.CharField(max_length=20, db_column='INSTRUMENT_TYPE', blank=True)),
                ('instrument_no', models.CharField(max_length=20, db_column='INSTRUMENT_NO', blank=True)),
                ('date_received', models.DateField(null=True, db_column='DATE_RECEIVED')),
                ('campaign', models.ForeignKey(related_name='bookings', db_column='CAMPAIGN_ID', to='v0.Campaign', null=True)),
            ],
            options={
                'db_table': 'campaign_booking_info',
            },
        ),
        migrations.CreateModel(
            name='CampaignSocietyMapping',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('booking_status', models.CharField(max_length=20, db_column='BOOKING_STATUS', blank=True)),
                ('adjusted_price', models.IntegerField(null=True, db_column='ADJUSTED_PRICE')),
                ('comments', models.TextField(max_length=100, db_column='COMMENTS', blank=True)),
                ('campaign', models.ForeignKey(related_name='societies', db_column='CAMPAIGN_ID', to='v0.Campaign', null=True)),
            ],
            options={
                'db_table': 'campaign_society_mapping',
            },
        ),
        migrations.CreateModel(
            name='CampaignTypeMapping',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('type', models.CharField(max_length=20, db_column='TYPE', blank=True)),
                ('sub_type', models.CharField(max_length=20, db_column='SUB_TYPE', blank=True)),
                ('campaign', models.ForeignKey(related_name='types', db_column='CAMPAIGN_ID', to='v0.Campaign', null=True)),
            ],
            options={
                'db_table': 'campaign_type_mapping',
            },
        ),
        migrations.CreateModel(
            name='CampaignTypes',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('type_name', models.CharField(max_length=20, db_column='TYPE_NAME', blank=True)),
            ],
            options={
                'db_table': 'campaign_types',
            },
        ),
        migrations.CreateModel(
            name='FlatType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('flat_type', models.CharField(max_length=20, db_column='FLAT_TYPE')),
                ('flat_count', models.IntegerField(null=True, db_column='FLAT_COUNT', blank=True)),
                ('flat_type_count', models.IntegerField(null=True, db_column='FLAT_TYPE_COUNT', blank=True)),
                ('size_carpet_area', models.FloatField(null=True, db_column='SIZE_CARPET_AREA', blank=True)),
                ('size_builtup_area', models.FloatField(null=True, db_column='SIZE_BUILTUP_AREA', blank=True)),
                ('flat_rent', models.IntegerField(null=True, db_column='FLAT_RENT', blank=True)),
                ('average_rent_per_sqft', models.FloatField(null=True, db_column='AVERAGE_RENT_PER_SQFT', blank=True)),
            ],
            options={
                'db_table': 'flat_type',
            },
        ),
        migrations.CreateModel(
            name='SocietyInventoryBooking',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='ID')),
                ('ad_location', models.CharField(max_length=50, db_column='AD_LOCATION', blank=True)),
                ('start_date', models.DateField(null=True, db_column='START_DATE')),
                ('end_date', models.DateField(null=True, db_column='END_DATE')),
                ('audit_date', models.DateField(null=True, db_column='AUDIT_DATE')),
                ('adinventory_type', models.ForeignKey(db_column='ADINVENTORY_TYPE', to='v0.CampaignTypeMapping', null=True)),
                ('campaign', models.ForeignKey(related_name='inventory_bookings', db_column='CAMPAIGN_ID', to='v0.Campaign', null=True)),
            ],
            options={
                'db_table': 'society_inventory_booking',
            },
        ),
        migrations.RenameField(
            model_name='contactdetails',
            old_name='contact_id',
            new_name='id',
        ),
        migrations.RemoveField(
            model_name='contactdetails',
            name='contact_emailid',
        ),
        migrations.RemoveField(
            model_name='contactdetails',
            name='contact_landline',
        ),
        migrations.RemoveField(
            model_name='contactdetails',
            name='contact_mobile',
        ),
        migrations.RemoveField(
            model_name='contactdetails',
            name='contact_name',
        ),
        migrations.RemoveField(
            model_name='societyflat',
            name='average_rent_pers_sqft_tower',
        ),
        migrations.RemoveField(
            model_name='societyflat',
            name='flat_rent',
        ),
        migrations.RemoveField(
            model_name='societyflat',
            name='flat_size_per_sq_feet_builtup_area',
        ),
        migrations.RemoveField(
            model_name='societyflat',
            name='flat_size_per_sq_feet_carpet_area',
        ),
        migrations.RemoveField(
            model_name='societyflat',
            name='flat_type_count',
        ),
        migrations.RemoveField(
            model_name='societyflat',
            name='rent_per_sqft',
        ),
        migrations.RemoveField(
            model_name='stallinventory',
            name='current_price_stall',
        ),
        migrations.RemoveField(
            model_name='stallinventory',
            name='photograph_1',
        ),
        migrations.RemoveField(
            model_name='stallinventory',
            name='photograph_2',
        ),
        migrations.RemoveField(
            model_name='stallinventory',
            name='stall_size_area',
        ),
        migrations.RemoveField(
            model_name='stallinventory',
            name='stall_timings_evening',
        ),
        migrations.RemoveField(
            model_name='stallinventory',
            name='stall_timings_morning',
        ),
        migrations.AddField(
            model_name='contactdetails',
            name='country_code',
            field=models.CharField(max_length=10, null=True, db_column='COUNTRY_CODE', blank=True),
        ),
        migrations.AddField(
            model_name='contactdetails',
            name='email',
            field=models.CharField(max_length=50, null=True, db_column='CONTACT_EMAILID', blank=True),
        ),
        migrations.AddField(
            model_name='contactdetails',
            name='landline',
            field=models.BigIntegerField(null=True, db_column='CONTACT_LANDLINE', blank=True),
        ),
        migrations.AddField(
            model_name='contactdetails',
            name='mobile',
            field=models.BigIntegerField(null=True, db_column='CONTACT_MOBILE', blank=True),
        ),
        migrations.AddField(
            model_name='contactdetails',
            name='name',
            field=models.CharField(max_length=50, null=True, db_column='CONTACT_NAME', blank=True),
        ),
        migrations.AddField(
            model_name='contactdetails',
            name='salutation',
            field=models.CharField(max_length=50, null=True, db_column='SALUTATION', blank=True),
        ),
        migrations.AddField(
            model_name='contactdetails',
            name='std_code',
            field=models.CharField(max_length=6, null=True, db_column='STD_CODE', blank=True),
        ),
        migrations.AddField(
            model_name='liftdetails',
            name='inventory_size',
            field=models.CharField(max_length=30, null=True, db_column='INVENTORY_SIZE', blank=True),
        ),
        migrations.AddField(
            model_name='liftdetails',
            name='inventory_status_lift',
            field=models.CharField(max_length=20, null=True, db_column='INVENTORY_STATUS_LIFT', blank=True),
        ),
        migrations.AddField(
            model_name='societytower',
            name='flat_type_count',
            field=models.IntegerField(null=True, db_column='FLAT_TYPE_COUNT', blank=True),
        ),
        migrations.AddField(
            model_name='stallinventory',
            name='stall_availability',
            field=models.CharField(max_length=10, null=True, db_column='STALL_AVAILABILITY', blank=True),
        ),
        migrations.AddField(
            model_name='stallinventory',
            name='stall_size',
            field=models.CharField(max_length=20, null=True, db_column='STALL_SIZE', blank=True),
        ),
        migrations.AddField(
            model_name='stallinventory',
            name='stall_timing',
            field=models.CharField(max_length=10, null=True, db_column='STALL_TIMINGS', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='banner_count',
            field=models.IntegerField(null=True, db_column='BANNER_COUNT', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='created_by',
            field=models.ForeignKey(related_name='societies', db_column='CREATED_BY', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 24, 9, 48, 32, 622110, tzinfo=utc), auto_now_add=True, db_column='CREATED_ON'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='flat_type_count',
            field=models.IntegerField(null=True, db_column='FLAT_TYPE_COUNT', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='society_locality',
            field=models.CharField(max_length=30, null=True, db_column='SOCIETY_LOCALITY', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='stall_count',
            field=models.IntegerField(null=True, db_column='STALL_COUNT', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='standee_count',
            field=models.IntegerField(null=True, db_column='STANDEE_COUNT', blank=True),
        ),
        migrations.AddField(
            model_name='suppliertypesociety',
            name='tower_count',
            field=models.IntegerField(null=True, db_column='TOWER_COUNT', blank=True),
        ),
        migrations.AlterField(
            model_name='adinventorylocationmapping',
            name='adinventory_id',
            field=models.CharField(max_length=22, db_column='ADINVENTORY_ID'),
        ),
        migrations.AlterField(
            model_name='adinventorylocationmapping',
            name='adinventory_name',
            field=models.CharField(default='POSTER', max_length=10, db_column='ADINVENTORY_NAME', choices=[('POSTER', 'Poster'), ('STANDEE', 'Standee'), ('STALL', 'Stall'), ('CAR DISPLAY', 'Car Display'), ('FLIER', 'Flier'), ('BANNER', 'Banner')]),
        ),
        migrations.AlterField(
            model_name='adinventorytype',
            name='adinventory_name',
            field=models.CharField(default='POSTER', max_length=20, db_column='ADINVENTORY_NAME', choices=[('POSTER', 'Poster'), ('STANDEE', 'Standee'), ('STALL', 'Stall'), ('CAR DISPLAY', 'Car Display'), ('FLIER', 'Flier'), ('BANNER', 'Banner')]),
        ),
        migrations.AlterField(
            model_name='bannerinventory',
            name='adinventory_id',
            field=models.CharField(max_length=22, db_column='ADINVENTORY_ID', blank=True),
        ),
        migrations.AlterField(
            model_name='bannerinventory',
            name='banner_location',
            field=models.CharField(max_length=50, db_column='BANNER_DISPLAY_LOCATION', blank=True),
        ),
        migrations.AlterField(
            model_name='bannerinventory',
            name='banner_size',
            field=models.CharField(max_length=10, db_column='BANNER_SIZE', blank=True),
        ),
        migrations.AlterField(
            model_name='bannerinventory',
            name='inventory_status',
            field=models.CharField(max_length=15, db_column='INVENTORY_STATUS', blank=True),
        ),
        migrations.AlterField(
            model_name='bannerinventory',
            name='photograph_1',
            field=models.CharField(max_length=45, db_column='PHOTOGRAPH_1', blank=True),
        ),
        migrations.AlterField(
            model_name='bannerinventory',
            name='photograph_2',
            field=models.CharField(max_length=45, db_column='PHOTOGRAPH_2', blank=True),
        ),
        migrations.AlterField(
            model_name='bannerinventory',
            name='type',
            field=models.CharField(max_length=20, db_column='BANNER_TYPE', blank=True),
        ),
        migrations.AlterField(
            model_name='cardisplayinventory',
            name='adinventory_id',
            field=models.CharField(max_length=22, null=True, db_column='ADINVENTORY_ID', blank=True),
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='contact_type',
            field=models.CharField(max_length=30, null=True, db_column='CONTACT_TYPE', blank=True),
        ),
        migrations.AlterField(
            model_name='contactdetails',
            name='specify_others',
            field=models.CharField(max_length=50, null=True, db_column='SPECIFY_OTHERS', blank=True),
        ),
        migrations.AlterField(
            model_name='doortodoorinfo',
            name='adinventory_id',
            field=models.CharField(max_length=22, null=True, db_column='ADINVENTORY_ID', blank=True),
        ),
        migrations.AlterField(
            model_name='durationtype',
            name='days_count',
            field=models.CharField(max_length=10, db_column='DAYS_COUNT'),
        ),
        migrations.AlterField(
            model_name='events',
            name='past_gathering_per_event',
            field=models.IntegerField(null=True, db_column='PAST_GATHERING_PER_EVENT', blank=True),
        ),
        migrations.AlterField(
            model_name='imagemapping',
            name='location_id',
            field=models.CharField(max_length=20, null=True, db_column='LOCATION_ID', blank=True),
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
            model_name='noticeboarddetails',
            name='notice_board_lit',
            field=models.CharField(max_length=5, null=True, db_column='NOTICE_BOARD_LIT', blank=True),
        ),
        migrations.AlterField(
            model_name='poleinventory',
            name='adinventory_id',
            field=models.CharField(max_length=22, null=True, db_column='ADINVENTORY_ID', blank=True),
        ),
        migrations.AlterField(
            model_name='poleinventory',
            name='pole_lit_status',
            field=models.CharField(max_length=5, db_column='POLE_LIT_STATUS', blank=True),
        ),
        migrations.AlterField(
            model_name='poleinventory',
            name='pole_monthly_price_business',
            field=models.FloatField(null=True, db_column='POLE_MONTHLY_PRICE_BUSINESS'),
        ),
        migrations.AlterField(
            model_name='poleinventory',
            name='pole_monthly_price_society',
            field=models.FloatField(null=True, db_column='POLE_MONTHLY_PRICE_SOCIETY'),
        ),
        migrations.AlterField(
            model_name='poleinventory',
            name='pole_quarterly_price_business',
            field=models.FloatField(null=True, db_column='POLE_QUARTERLY_PRICE_BUSINESS'),
        ),
        migrations.AlterField(
            model_name='poleinventory',
            name='pole_quarterly_price_society',
            field=models.FloatField(null=True, db_column='POLE_QUARTERLY_PRICE_SOCIETY'),
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
            model_name='pricemapping',
            name='business_price',
            field=models.IntegerField(db_column='ACTUAL_SOCIETY_PRICE'),
        ),
        migrations.AlterField(
            model_name='pricemapping',
            name='society_price',
            field=models.IntegerField(db_column='SUGGESTED_SOCIETY_PRICE'),
        ),
        migrations.AlterField(
            model_name='pricemappingdefault',
            name='business_price',
            field=models.IntegerField(db_column='ACTUAL_SOCIETY_PRICE'),
        ),
        migrations.AlterField(
            model_name='pricemappingdefault',
            name='society_price',
            field=models.IntegerField(db_column='SUGGESTED_SOCIETY_PRICE'),
        ),
        migrations.AlterField(
            model_name='societyflat',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True, db_column='ID'),
        ),
        migrations.AlterField(
            model_name='stallinventory',
            name='adinventory_id',
            field=models.CharField(max_length=22, db_column='ADINVENTORY_ID'),
        ),
        migrations.AlterField(
            model_name='stallinventory',
            name='electricity_charges_daily',
            field=models.FloatField(max_length=50, null=True, db_column='ELECTRICITY_CHARGES_DAILY', blank=True),
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
            model_name='suppliertypesociety',
            name='business_id_not_allowed',
            field=models.CharField(max_length=50, null=True, db_column='BUSINESS_ID_NOT_ALLOWED', blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='business_type_not_allowed',
            field=models.CharField(max_length=50, null=True, db_column='BUSINESS_TYPE_NOT_ALLOWED', blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='past_collections_banners',
            field=models.IntegerField(null=True, db_column='PAST_YEAR_COLLECTIONS_BANNERS'),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='past_collections_car',
            field=models.IntegerField(null=True, db_column='PAST_YEAR_COLLECTIONS_CAR'),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='past_collections_poster',
            field=models.IntegerField(null=True, db_column='PAST_YEAR_COLLECTIONS_POSTER'),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='past_collections_stalls',
            field=models.IntegerField(null=True, db_column='PAST_YEAR_COLLECTIONS_STALLS'),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='past_collections_standee',
            field=models.IntegerField(null=True, db_column='PAST_YEAR_COLLECTIONS_STANDEE'),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='past_sponsorship_collection_events',
            field=models.IntegerField(null=True, db_column='PAST_YEAR_SPONSORSHIP_COLLECTION_EVENTS'),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='past_total_sponsorship',
            field=models.IntegerField(null=True, db_column='PAST_YEAR_TOTAL_SPONSORSHIP'),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='total_ad_spaces',
            field=models.IntegerField(null=True, db_column='TOTAL_AD_SPACES'),
        ),
        migrations.AlterField(
            model_name='wallinventory',
            name='adinventory_id',
            field=models.CharField(max_length=22, db_column='ADINVENTORY_ID'),
        ),
        migrations.AlterField(
            model_name='wallinventory',
            name='inventory_type_id',
            field=models.CharField(max_length=20, db_column='INVENTORY_TYPE_ID', blank=True),
        ),
        migrations.AddField(
            model_name='societyinventorybooking',
            name='society',
            field=models.ForeignKey(related_name='inventory_bookings', db_column='SUPPLIER_ID', to='v0.SupplierTypeSociety', null=True),
        ),
        migrations.AddField(
            model_name='flattype',
            name='society',
            field=models.ForeignKey(related_name='flatTypes', db_column='SUPPLIER_ID', blank=True, to='v0.SupplierTypeSociety', null=True),
        ),
        migrations.AddField(
            model_name='campaignsocietymapping',
            name='society',
            field=models.ForeignKey(related_name='campaigns', db_column='SUPPLIER_ID', to='v0.SupplierTypeSociety', null=True),
        ),
        migrations.AddField(
            model_name='audits',
            name='society_booking',
            field=models.ForeignKey(related_name='audits', db_column='SOCIETY_BOOKING_ID', to='v0.SocietyInventoryBooking', null=True),
        ),
        migrations.AddField(
            model_name='auditorsocietymapping',
            name='society',
            field=models.ForeignKey(related_name='auditors', db_column='SUPPLIER_ID', to='v0.SupplierTypeSociety', null=True),
        ),
    ]
