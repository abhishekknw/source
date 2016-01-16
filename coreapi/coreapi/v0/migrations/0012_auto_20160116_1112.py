# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('v0', '0011_auto_20160116_0720'),
    ]

    operations = [
        migrations.DeleteModel(
            name='InventoryInfo',
        ),
        migrations.RemoveField(
            model_name='bannerinventory',
            name='banner_monthly_price_business',
        ),
        migrations.RemoveField(
            model_name='bannerinventory',
            name='banner_monthly_price_society',
        ),
        migrations.RemoveField(
            model_name='bannerinventory',
            name='banner_weekly_price_business',
        ),
        migrations.RemoveField(
            model_name='bannerinventory',
            name='banner_weekly_price_society',
        ),
        migrations.RemoveField(
            model_name='bannerinventory',
            name='event_id',
        ),
        migrations.RemoveField(
            model_name='bannerinventory',
            name='event_linked',
        ),
        migrations.RemoveField(
            model_name='cardisplayinventory',
            name='event_id',
        ),
        migrations.RemoveField(
            model_name='cardisplayinventory',
            name='event_linked',
        ),
        migrations.RemoveField(
            model_name='communityhallinfo',
            name='event_id',
        ),
        migrations.RemoveField(
            model_name='communityhallinfo',
            name='event_linked',
        ),
        migrations.RemoveField(
            model_name='doortodoorinfo',
            name='event_id',
        ),
        migrations.RemoveField(
            model_name='doortodoorinfo',
            name='event_linked',
        ),
        migrations.RemoveField(
            model_name='doortodoorinfo',
            name='event_location',
        ),
        migrations.RemoveField(
            model_name='doortodoorinfo',
            name='event_name',
        ),
        migrations.RemoveField(
            model_name='doortodoorinfo',
            name='event_plan_map',
        ),
        migrations.RemoveField(
            model_name='doortodoorinfo',
            name='event_status',
        ),
        migrations.RemoveField(
            model_name='doortodoorinfo',
            name='no_of_days',
        ),
        migrations.RemoveField(
            model_name='doortodoorinfo',
            name='past_gathering_per_event',
        ),
        migrations.RemoveField(
            model_name='doortodoorinfo',
            name='past_major_events',
        ),
        migrations.RemoveField(
            model_name='doortodoorinfo',
            name='poster_spaces_count',
        ),
        migrations.RemoveField(
            model_name='doortodoorinfo',
            name='stall_spaces_count',
        ),
        migrations.RemoveField(
            model_name='doortodoorinfo',
            name='standee_spaces_count',
        ),
        migrations.RemoveField(
            model_name='noticeboarddetails',
            name='notice_board_size_area',
        ),
        migrations.RemoveField(
            model_name='posterinventory',
            name='event_id',
        ),
        migrations.RemoveField(
            model_name='posterinventory',
            name='poster_monthly_price_business',
        ),
        migrations.RemoveField(
            model_name='posterinventory',
            name='poster_monthly_price_society',
        ),
        migrations.RemoveField(
            model_name='posterinventory',
            name='poster_weekly_price_business',
        ),
        migrations.RemoveField(
            model_name='posterinventory',
            name='poster_weekly_price_society',
        ),
        migrations.RemoveField(
            model_name='posterinventory',
            name='stall_id',
        ),
        migrations.RemoveField(
            model_name='posterinventory',
            name='stall_linked',
        ),
        migrations.RemoveField(
            model_name='stallinventory',
            name='event_id',
        ),
        migrations.RemoveField(
            model_name='stallinventory',
            name='event_linked',
        ),
        migrations.RemoveField(
            model_name='stallinventory',
            name='stall_daily_price_stall_business',
        ),
        migrations.RemoveField(
            model_name='stallinventory',
            name='stall_daily_price_stall_society',
        ),
        migrations.RemoveField(
            model_name='standeeinventory',
            name='event_id',
        ),
        migrations.RemoveField(
            model_name='standeeinventory',
            name='event_linked',
        ),
        migrations.RemoveField(
            model_name='standeeinventory',
            name='stall_id',
        ),
        migrations.RemoveField(
            model_name='standeeinventory',
            name='stall_linked',
        ),
        migrations.RemoveField(
            model_name='standeeinventory',
            name='standee_monthly_price_business',
        ),
        migrations.RemoveField(
            model_name='standeeinventory',
            name='standee_monthly_price_society',
        ),
        migrations.RemoveField(
            model_name='standeeinventory',
            name='standee_weekly_price_business',
        ),
        migrations.RemoveField(
            model_name='standeeinventory',
            name='standee_weekly_price_society',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='banner_available',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='banner_count',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='bill_sponsorship_electricity',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='bill_sponsorship_maintenanace',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='car_display_available',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='children_playing_area_available',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='children_playing_area_count',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='door_to_door_allowed',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='events_count',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='flier_distribution_frequency_per_month',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='mail_box_available',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='notice_board_available',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='past_collections_banners',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='past_collections_car',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='past_collections_poster',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='past_collections_stalls',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='past_collections_standee',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='past_sponsorship_collection_events',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='past_total_sponsorship',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='poster_count',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='sports_facility_available',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='stall_available',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='standee_count',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='street_furniture_available',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='street_furniture_count',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='swimming_pool_avaialblity',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='swimming_pool_availabel',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='tower_count',
        ),
        migrations.RemoveField(
            model_name='suppliertypesociety',
            name='wall_count',
        ),
        migrations.AlterField(
            model_name='cardisplayinventory',
            name='car_daily_price_business',
            field=models.FloatField(default=0.0, null=True, db_column='CAR_DAILY_PRICE_BUSINESS', blank=True),
        ),
        migrations.AlterField(
            model_name='cardisplayinventory',
            name='car_daily_price_society',
            field=models.FloatField(default=0.0, null=True, db_column='CAR_DAILY_PRICE_SOCIETY', blank=True),
        ),
        migrations.AlterField(
            model_name='communityhallinfo',
            name='ceiling_height',
            field=models.FloatField(default=0.0, null=True, db_column='CEILING_HEIGHT', blank=True),
        ),
        migrations.AlterField(
            model_name='communityhallinfo',
            name='daily_price_business',
            field=models.FloatField(default=0.0, null=True, db_column='DAILY_PRICE_BUSINESS', blank=True),
        ),
        migrations.AlterField(
            model_name='communityhallinfo',
            name='daily_price_society',
            field=models.FloatField(default=0.0, null=True, db_column='DAILY_PRICE_SOCIETY', blank=True),
        ),
        migrations.AlterField(
            model_name='communityhallinfo',
            name='electricity_charges_perhour',
            field=models.FloatField(default=0.0, null=True, db_column='ELECTRICITY_CHARGES_PERHOUR', blank=True),
        ),
        migrations.AlterField(
            model_name='communityhallinfo',
            name='rentals_current',
            field=models.FloatField(default=0.0, null=True, db_column='RENTALS_CURRENT', blank=True),
        ),
        migrations.AlterField(
            model_name='communityhallinfo',
            name='size_breadth',
            field=models.FloatField(default=0.0, null=True, db_column='SIZE_BREADTH', blank=True),
        ),
        migrations.AlterField(
            model_name='communityhallinfo',
            name='size_length',
            field=models.FloatField(default=0.0, null=True, db_column='SIZE_LENGTH', blank=True),
        ),
        migrations.AlterField(
            model_name='doortodoorinfo',
            name='banner_spaces_count',
            field=models.IntegerField(null=True, db_column='BANNER_SPACES_COUNT', blank=True),
        ),
        migrations.AlterField(
            model_name='doortodoorinfo',
            name='door_to_door_price_business',
            field=models.FloatField(default=0.0, null=True, db_column='DOOR_TO_DOOR_PRICE_BUSINESS', blank=True),
        ),
        migrations.AlterField(
            model_name='doortodoorinfo',
            name='door_to_door_price_society',
            field=models.FloatField(default=0.0, null=True, db_column='DOOR_TO_DOOR_PRICE_SOCIETY', blank=True),
        ),
        migrations.AlterField(
            model_name='doortodoorinfo',
            name='master_door_to_door_flyer_price_business',
            field=models.FloatField(default=0.0, null=True, db_column='MASTER_DOOR_TO_DOOR_FLYER_PRICE_BUSINESS', blank=True),
        ),
        migrations.AlterField(
            model_name='doortodoorinfo',
            name='master_door_to_door_flyer_price_society',
            field=models.FloatField(default=0.0, null=True, db_column='MASTER_DOOR_TO_DOOR_FLYER_PRICE_SOCIETY', blank=True),
        ),
        migrations.AlterField(
            model_name='mailboxinfo',
            name='mailbox_flyer_price_business',
            field=models.FloatField(default=0.0, null=True, db_column='MAILBOX_FLYER_PRICE_BUSINESS', blank=True),
        ),
        migrations.AlterField(
            model_name='mailboxinfo',
            name='mailbox_flyer_price_society',
            field=models.FloatField(default=0.0, null=True, db_column='MAILBOX_FLYER_PRICE_SOCIETY', blank=True),
        ),
        migrations.AlterField(
            model_name='noticeboarddetails',
            name='notice_board_size_breadth',
            field=models.FloatField(default=0.0, null=True, db_column='NOTICE_BOARD_SIZE_BREADTH', blank=True),
        ),
        migrations.AlterField(
            model_name='noticeboarddetails',
            name='notice_board_size_length',
            field=models.FloatField(default=0.0, null=True, db_column='NOTICE_BOARD_SIZE_length', blank=True),
        ),
        migrations.AlterField(
            model_name='stallinventory',
            name='stall_size_area',
            field=models.FloatField(default=0.0, null=True, db_column='STALL_SIZE_AREA', blank=True),
        ),
        migrations.AlterField(
            model_name='stallinventory',
            name='stall_timings_evening',
            field=models.TimeField(null=True, db_column='STALL_TIMINGS_evening', blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='machadalo_index',
            field=models.FloatField(default=0.0, null=True, db_column='MACHADALO_INDEX', blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='society_latitude',
            field=models.FloatField(default=0.0, null=True, db_column='SOCIETY_LATITUDE', blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='society_longitude',
            field=models.FloatField(default=0.0, null=True, db_column='SOCIETY_LONGITUDE', blank=True),
        ),
        migrations.AlterField(
            model_name='suppliertypesociety',
            name='society_zip',
            field=models.IntegerField(null=True, db_column='SOCIETY_ZIP', blank=True),
        ),
        migrations.AlterField(
            model_name='swimmingpoolinfo',
            name='daily_price_business',
            field=models.FloatField(default=0.0, null=True, db_column='DAILY_PRICE_BUSINESS', blank=True),
        ),
        migrations.AlterField(
            model_name='swimmingpoolinfo',
            name='daily_price_society',
            field=models.FloatField(default=0.0, null=True, db_column='DAILY_PRICE_SOCIETY', blank=True),
        ),
        migrations.AlterField(
            model_name='swimmingpoolinfo',
            name='side_area',
            field=models.FloatField(default=0.0, null=True, db_column='SIDE_AREA', blank=True),
        ),
        migrations.AlterField(
            model_name='swimmingpoolinfo',
            name='size_breadth',
            field=models.FloatField(default=0.0, null=True, db_column='SIZE_BREADTH', blank=True),
        ),
        migrations.AlterField(
            model_name='swimmingpoolinfo',
            name='size_length',
            field=models.FloatField(default=0.0, null=True, db_column='SIZE_LENGTH', blank=True),
        ),
        migrations.AlterField(
            model_name='swimmingpoolinfo',
            name='timings_close',
            field=models.TimeField(null=True, db_column='TIMINGS_CLOSE', blank=True),
        ),
        migrations.AlterField(
            model_name='swimmingpoolinfo',
            name='timings_open',
            field=models.TimeField(null=True, db_column='TIMINGS_OPEN', blank=True),
        ),
        migrations.AlterField(
            model_name='wallinventory',
            name='wall_monthly_price_business',
            field=models.FloatField(default=0.0, null=True, db_column='WALL_MONTHLY_PRICE_BUSINESS', blank=True),
        ),
        migrations.AlterField(
            model_name='wallinventory',
            name='wall_monthly_price_society',
            field=models.FloatField(default=0.0, null=True, db_column='WALL_MONTHLY_PRICE_SOCIETY', blank=True),
        ),
        migrations.AlterField(
            model_name='wallinventory',
            name='wall_quarterly_price_business',
            field=models.FloatField(default=0.0, null=True, db_column='WALL_QUARTERLY_PRICE_BUSINESS', blank=True),
        ),
        migrations.AlterField(
            model_name='wallinventory',
            name='wall_quarterly_price_society',
            field=models.FloatField(default=0.0, null=True, db_column='WALL_QUARTERLY_PRICE_SOCIETY', blank=True),
        ),
    ]
