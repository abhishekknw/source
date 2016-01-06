# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class MasterBannerInventory(models.Model):
    supplier = models.ForeignKey('MasterSupplierTypeSociety', db_column='SUPPLIER_ID', blank=True, null=True)  # Field name made lowercase.
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', primary_key=True, max_length=20)  # Field name made lowercase.
    banner_type = models.CharField(db_column='BANNER_TYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    banner_display_location = models.CharField(db_column='BANNER_DISPLAY_LOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    banner_size = models.CharField(db_column='BANNER_SIZE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    banner_weekly_price_society = models.CharField(db_column='BANNER_WEEKLY_PRICE_SOCIETY', max_length=5, blank=True, null=True)  # Field name made lowercase.
    banner_monthly_price_society = models.CharField(db_column='BANNER_MONTHLY_PRICE_SOCIETY', max_length=5, blank=True, null=True)  # Field name made lowercase.
    banner_weekly_price_business = models.CharField(db_column='BANNER_WEEKLY_PRICE_BUSINESS', max_length=5, blank=True, null=True)  # Field name made lowercase.
    banner_monthly_price_business = models.CharField(db_column='BANNER_MONTHLY_PRICE_BUSINESS', max_length=5, blank=True, null=True)  # Field name made lowercase.
    inventory_status = models.CharField(db_column='INVENTORY_STATUS', max_length=15)  # Field name made lowercase.
    event_id = models.CharField(db_column='EVENT_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    event_linked = models.CharField(db_column='EVENT_LINKED', max_length=5, blank=True, null=True)  # Field name made lowercase.
    photograph_1 = models.CharField(db_column='PHOTOGRAPH_1', max_length=45, blank=True, null=True)  # Field name made lowercase.
    photograph_2 = models.CharField(db_column='PHOTOGRAPH_2', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MASTER_BANNER_INVENTORY'


class MasterCarDisplayInventory(models.Model):
    inventory_type_id = models.AutoField(db_column='INVENTORY_TYPE_ID', primary_key=True)  # Field name made lowercase.
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    car_display_location = models.CharField(db_column='CAR_DISPLAY_LOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    car_display_location_size = models.CharField(db_column='CAR_DISPLAY_LOCATION_SIZE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    car_daily_price_society = models.CharField(db_column='CAR_DAILY_PRICE_SOCIETY', max_length=20, blank=True, null=True)  # Field name made lowercase.
    car_daily_price_business = models.CharField(db_column='CAR_DAILY_PRICE_BUSINESS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    car_display_inventory_status = models.CharField(db_column='CAR_DISPLAY_INVENTORY_STATUS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    car_display_type = models.CharField(db_column='CAR_DISPLAY_TYPE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    event_id = models.CharField(db_column='EVENT_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    event_linked = models.CharField(db_column='EVENT_LINKED', max_length=5, blank=True, null=True)  # Field name made lowercase.
    photograph_1 = models.CharField(db_column='PHOTOGRAPH_1', max_length=45, blank=True, null=True)  # Field name made lowercase.
    photograph_2 = models.CharField(db_column='PHOTOGRAPH_2', max_length=45, blank=True, null=True)  # Field name made lowercase.
    supplier = models.ForeignKey('MasterSupplierTypeSociety', db_column='SUPPLIER_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MASTER_CAR_DISPLAY_INVENTORY'


class MasterCommunityHallInfo(models.Model):
    community_hall_id = models.AutoField(db_column='COMMUNITY_HALL_ID', primary_key=True)  # Field name made lowercase.
    supplier = models.ForeignKey('MasterSupplierTypeSociety', db_column='SUPPLIER_ID', blank=True, null=True)  # Field name made lowercase.
    community_hall_size_length = models.CharField(db_column='COMMUNITY_HALL_SIZE_LENGTH', max_length=10, blank=True, null=True)  # Field name made lowercase.
    community_hall_size_breadth = models.CharField(db_column='COMMUNITY_HALL_SIZE_BREADTH', max_length=10, blank=True, null=True)  # Field name made lowercase.
    community_hall_ceiling_height = models.CharField(db_column='COMMUNITY_HALL_CEILING_HEIGHT', max_length=10, blank=True, null=True)  # Field name made lowercase.
    community_hall_timings_open = models.TimeField(db_column='COMMUNITY_HALL_TIMINGS_OPEN', blank=True, null=True)  # Field name made lowercase.
    community_hall_timings_close = models.TimeField(db_column='COMMUNITY_HALL_TIMINGS_CLOSE', blank=True, null=True)  # Field name made lowercase.
    community_hall_rentals_current = models.CharField(db_column='COMMUNITY_HALL_RENTALS_CURRENT', max_length=10, blank=True, null=True)  # Field name made lowercase.
    community_hall_daily_price_society = models.CharField(db_column='COMMUNITY_HALL_DAILY_PRICE_SOCIETY', max_length=5, blank=True, null=True)  # Field name made lowercase.
    community_hall_daily_price_business = models.CharField(db_column='COMMUNITY_HALL_DAILY_PRICE_BUSINESS', max_length=5, blank=True, null=True)  # Field name made lowercase.
    community_hall_location = models.CharField(db_column='COMMUNITY_HALL_LOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    community_hall_furniture_available = models.CharField(db_column='COMMUNITY_HALL_FURNITURE_AVAILABLE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    community_hall_chair_count = models.IntegerField(db_column='COMMUNITY_HALL_CHAIR_COUNT', blank=True, null=True)  # Field name made lowercase.
    community_hall_tables_count = models.IntegerField(db_column='COMMUNITY_HALL_TABLES_COUNT', blank=True, null=True)  # Field name made lowercase.
    community_hall_air_conditioned = models.CharField(db_column='COMMUNITY_HALL_AIR_CONDITIONED', max_length=5, blank=True, null=True)  # Field name made lowercase.
    community_hall_projector_available = models.CharField(db_column='COMMUNITY_HALL_PROJECTOR_AVAILABLE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    community_hall_inventory_status = models.CharField(db_column='COMMUNITY_HALL_INVENTORY_STATUS', max_length=15, blank=True, null=True)  # Field name made lowercase.
    community_hall_sitting = models.IntegerField(db_column='COMMUNITY_HALL_SITTING', blank=True, null=True)  # Field name made lowercase.
    audio_video_display_available = models.CharField(db_column='AUDIO_VIDEO_DISPLAY_AVAILABLE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    electricity_charges_perhour = models.IntegerField(db_column='ELECTRICITY_CHARGES_PERHOUR', blank=True, null=True)  # Field name made lowercase.
    notice_board_count_per_community_hall = models.IntegerField(db_column='NOTICE_BOARD_COUNT_PER_COMMUNITY_HALL', blank=True, null=True)  # Field name made lowercase.
    standee_location_count_per_community_hall = models.IntegerField(db_column='STANDEE_LOCATION_COUNT_PER_COMMUNITY_HALL', blank=True, null=True)  # Field name made lowercase.
    stall_count_per_community_hall = models.IntegerField(db_column='STALL_COUNT_PER_COMMUNITY_HALL', blank=True, null=True)  # Field name made lowercase.
    banner_count_per_community_hall = models.IntegerField(db_column='BANNER_COUNT_PER_COMMUNITY_HALL', blank=True, null=True)  # Field name made lowercase.
    event_id = models.CharField(db_column='EVENT_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    event_linked = models.CharField(db_column='EVENT_LINKED', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MASTER_COMMUNITY_HALL_INFO'


class MasterDoorToDoorInfo(models.Model):
    door_to_door_info_id = models.AutoField(db_column='DOOR_TO_DOOR_INFO_ID', primary_key=True)  # Field name made lowercase.
    supplier = models.ForeignKey('MasterSupplierTypeSociety', db_column='SUPPLIER_ID', blank=True, null=True)  # Field name made lowercase.
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    flier_distribution_frequency_door = models.CharField(db_column='FLIER_DISTRIBUTION_FREQUENCY_DOOR', max_length=20, blank=True, null=True)  # Field name made lowercase.
    door_to_door_inventory_status = models.CharField(db_column='DOOR_TO_DOOR_INVENTORY_STATUS', max_length=15, blank=True, null=True)  # Field name made lowercase.
    door_to_door_price_society = models.CharField(db_column='DOOR_TO_DOOR_PRICE_SOCIETY', max_length=5, blank=True, null=True)  # Field name made lowercase.
    door_to_door_price_business = models.CharField(db_column='DOOR_TO_DOOR_PRICE_BUSINESS', max_length=5, blank=True, null=True)  # Field name made lowercase.
    master_door_to_door_flyer_price_society = models.CharField(db_column='MASTER_DOOR_TO_DOOR_FLYER_PRICE_SOCIETY', max_length=5, blank=True, null=True)  # Field name made lowercase.
    master_door_to_door_flyer_price_business = models.CharField(db_column='MASTER_DOOR_TO_DOOR_FLYER_PRICE_BUSINESS', max_length=5, blank=True, null=True)  # Field name made lowercase.
    leaflet_handover = models.CharField(db_column='LEAFLET_HANDOVER', max_length=5, blank=True, null=True)  # Field name made lowercase.
    activities = models.CharField(db_column='ACTIVITIES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    banner_spaces_count = models.CharField(db_column='BANNER_SPACES_COUNT', max_length=255, blank=True, null=True)  # Field name made lowercase.
    event_id = models.CharField(db_column='EVENT_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    event_linked = models.CharField(db_column='EVENT_LINKED', max_length=255, blank=True, null=True)  # Field name made lowercase.
    event_location = models.CharField(db_column='EVENT_LOCATION', max_length=255, blank=True, null=True)  # Field name made lowercase.
    event_name = models.CharField(db_column='EVENT_NAME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    event_plan_map = models.CharField(db_column='EVENT_PLAN_MAP', max_length=255, blank=True, null=True)  # Field name made lowercase.
    event_status = models.CharField(db_column='EVENT_STATUS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    no_of_days = models.CharField(db_column='NO_OF_DAYS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    past_gathering_per_event = models.CharField(db_column='PAST_GATHERING_PER_EVENT', max_length=255, blank=True, null=True)  # Field name made lowercase.
    past_major_events = models.CharField(db_column='PAST_MAJOR_EVENTS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    poster_spaces_count = models.CharField(db_column='POSTER_SPACES_COUNT', max_length=255, blank=True, null=True)  # Field name made lowercase.
    stall_spaces_count = models.CharField(db_column='STALL_SPACES_COUNT', max_length=255, blank=True, null=True)  # Field name made lowercase.
    standee_spaces_count = models.CharField(db_column='STANDEE_SPACES_COUNT', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MASTER_DOOR_TO_DOOR_INFO'


class MasterLiftDetails(models.Model):
    lift_id = models.CharField(db_column='LIFT_ID', primary_key=True, max_length=20)  # Field name made lowercase.
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    acrylic_board_available = models.CharField(db_column='ACRYLIC_BOARD_AVAILABLE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    lift_location = models.CharField(db_column='LIFT_LOCATION', max_length=100, blank=True, null=True)  # Field name made lowercase.
    total_poster_per_lift = models.IntegerField(db_column='TOTAL_POSTER_PER_LIFT', blank=True, null=True)  # Field name made lowercase.
    lift_lit = models.CharField(db_column='LIFT_LIT', max_length=5, blank=True, null=True)  # Field name made lowercase.
    lift_bubble_wrapping_allowed = models.CharField(db_column='LIFT_BUBBLE_WRAPPING_ALLOWED', max_length=5, blank=True, null=True)  # Field name made lowercase.
    lift_advt_walls_count = models.IntegerField(db_column='LIFT_ADVT_WALLS_COUNT', blank=True, null=True)  # Field name made lowercase.
    photograph_1 = models.CharField(db_column='PHOTOGRAPH_1', max_length=45, blank=True, null=True)  # Field name made lowercase.
    photograph_2 = models.CharField(db_column='PHOTOGRAPH_2', max_length=45, blank=True, null=True)  # Field name made lowercase.
    tower = models.ForeignKey('MasterSupplierTypeSocietyTower', db_column='TOWER_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MASTER_LIFT_DETAILS'


class MasterNoticeBoardDetails(models.Model):
    notice_board_id = models.AutoField(db_column='NOTICE_BOARD_ID', primary_key=True)  # Field name made lowercase.
    notice_board_type = models.CharField(db_column='NOTICE_BOARD_TYPE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    notice_board_type_other = models.CharField(db_column='NOTICE_BOARD_TYPE_OTHER', max_length=30, blank=True, null=True)  # Field name made lowercase.
    notice_board_location = models.CharField(db_column='NOTICE_BOARD_LOCATION', max_length=100, blank=True, null=True)  # Field name made lowercase.
    total_poster_per_notice_board = models.IntegerField(db_column='TOTAL_POSTER_PER_NOTICE_BOARD', blank=True, null=True)  # Field name made lowercase.
    poster_location_notice_board = models.CharField(db_column='POSTER_LOCATION_NOTICE_BOARD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    notice_board_lit = models.CharField(db_column='NOTICE_BOARD_LIT', max_length=1)  # Field name made lowercase.
    tower = models.ForeignKey('MasterSupplierTypeSocietyTower', db_column='TOWER_ID', blank=True, null=True)  # Field name made lowercase.
    notice_board_size_length = models.CharField(db_column='NOTICE_BOARD_SIZE_length', max_length=10, blank=True, null=True)  # Field name made lowercase.
    notice_board_size_breadth = models.CharField(db_column='NOTICE_BOARD_SIZE_BREADTH', max_length=10, blank=True, null=True)  # Field name made lowercase.
    notice_board_size_area = models.CharField(db_column='NOTICE_BOARD_SIZE_AREA', max_length=10, blank=True, null=True)  # Field name made lowercase.
    photograph_1 = models.CharField(db_column='PHOTOGRAPH_1', max_length=45, blank=True, null=True)  # Field name made lowercase.
    photograph_2 = models.CharField(db_column='PHOTOGRAPH_2', max_length=45, blank=True, null=True)  # Field name made lowercase.
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MASTER_NOTICE_BOARD_DETAILS'


class MasterPosterInventory(models.Model):
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', primary_key=True, max_length=20)  # Field name made lowercase.
    notice_board_id = models.CharField(db_column='NOTICE_BOARD_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    poster_location = models.CharField(db_column='POSTER_LOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    poster_area = models.CharField(db_column='POSTER_AREA', max_length=10, blank=True, null=True)  # Field name made lowercase.
    event_id = models.CharField(db_column='EVENT_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    poster_weekly_price_society = models.CharField(db_column='POSTER_WEEKLY_PRICE_SOCIETY', max_length=5, blank=True, null=True)  # Field name made lowercase.
    poster_monthly_price_society = models.CharField(db_column='POSTER_MONTHLY_PRICE_SOCIETY', max_length=5, blank=True, null=True)  # Field name made lowercase.
    poster_weekly_price_business = models.CharField(db_column='POSTER_WEEKLY_PRICE_BUSINESS', max_length=5, blank=True, null=True)  # Field name made lowercase.
    poster_monthly_price_business = models.CharField(db_column='POSTER_MONTHLY_PRICE_BUSINESS', max_length=5, blank=True, null=True)  # Field name made lowercase.
    stall_linked = models.CharField(db_column='STALL_LINKED', max_length=5, blank=True, null=True)  # Field name made lowercase.
    stall_id = models.CharField(db_column='STALL_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    inventory_status = models.CharField(db_column='INVENTORY_STATUS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    poster_count_per_notice_board = models.IntegerField(db_column='POSTER_COUNT_PER_NOTICE_BOARD', blank=True, null=True)  # Field name made lowercase.
    inventory_type_id = models.CharField(db_column='INVENTORY_TYPE_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    supplier = models.ForeignKey('MasterSupplierTypeSociety', db_column='SUPPLIER_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MASTER_POSTER_INVENTORY'


class MasterSocietyFlat(models.Model):
    tower = models.ForeignKey('MasterSupplierTypeSocietyTower', db_column='TOWER_ID')  # Field name made lowercase.
    flat_type = models.CharField(db_column='FLAT_TYPE', max_length=20)  # Field name made lowercase.
    flat_count = models.IntegerField(db_column='FLAT_COUNT', blank=True, null=True)  # Field name made lowercase.
    flat_type_count = models.IntegerField(db_column='FLAT_TYPE_COUNT', blank=True, null=True)  # Field name made lowercase.
    flat_size_per_sq_feet_carpet_area = models.CharField(db_column='FLAT_SIZE_PER_SQ_FEET_CARPET_AREA', max_length=10, blank=True, null=True)  # Field name made lowercase.
    flat_size_per_sq_feet_builtup_area = models.CharField(db_column='FLAT_SIZE_PER_SQ_FEET_BUILTUP_AREA', max_length=10, blank=True, null=True)  # Field name made lowercase.
    flat_rent = models.CharField(db_column='FLAT_RENT', max_length=10, blank=True, null=True)  # Field name made lowercase.
    rent_per_sqft = models.CharField(db_column='RENT_PER_SQFT', max_length=10, blank=True, null=True)  # Field name made lowercase.
    average_rent_pers_sqft_tower = models.CharField(db_column='AVERAGE_RENT_PERS_SQFT_TOWER', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MASTER_SOCIETY_FLAT'
        unique_together = (('tower', 'flat_type'),)


class MasterStandeeInventory(models.Model):
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', primary_key=True, max_length=20)  # Field name made lowercase.
    inventory_type_id = models.CharField(db_column='INVENTORY_TYPE_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    inventory_status = models.CharField(db_column='INVENTORY_STATUS', max_length=15, blank=True, null=True)  # Field name made lowercase.
    standee_location = models.CharField(db_column='STANDEE_LOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    standee_area = models.CharField(db_column='STANDEE_AREA', max_length=10, blank=True, null=True)  # Field name made lowercase.
    standee_size = models.CharField(db_column='STANDEE_SIZE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    standee_sides = models.CharField(db_column='STANDEE_SIDES', max_length=10, blank=True, null=True)  # Field name made lowercase.
    standee_weekly_price_society = models.CharField(db_column='STANDEE_WEEKLY_PRICE_SOCIETY', max_length=5, blank=True, null=True)  # Field name made lowercase.
    standee_monthly_price_society = models.CharField(db_column='STANDEE_MONTHLY_PRICE_SOCIETY', max_length=5, blank=True, null=True)  # Field name made lowercase.
    standee_weekly_price_business = models.CharField(db_column='STANDEE_WEEKLY_PRICE_BUSINESS', max_length=5, blank=True, null=True)  # Field name made lowercase.
    standee_monthly_price_business = models.CharField(db_column='STANDEE_MONTHLY_PRICE_BUSINESS', max_length=5, blank=True, null=True)  # Field name made lowercase.
    standee_location_in_tower = models.CharField(db_column='STANDEE_LOCATION_IN_TOWER', max_length=50, blank=True, null=True)  # Field name made lowercase.
    standee_inventory_status = models.TextField(db_column='STANDEE_INVENTORY_STATUS', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    event_id = models.CharField(db_column='EVENT_ID', max_length=45, blank=True, null=True)  # Field name made lowercase.
    event_linked = models.CharField(db_column='EVENT_LINKED', max_length=5, blank=True, null=True)  # Field name made lowercase.
    stall_linked = models.CharField(db_column='STALL_LINKED', max_length=5, blank=True, null=True)  # Field name made lowercase.
    stall_id = models.CharField(db_column='STALL_ID', max_length=45, blank=True, null=True)  # Field name made lowercase.
    sides = models.CharField(db_column='SIDES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    supplier = models.ForeignKey('MasterSupplierTypeSociety', db_column='SUPPLIER_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MASTER_STANDEE_INVENTORY'


class MasterSwimmingPoolInfo(models.Model):
    swimming_pool_id = models.AutoField(db_column='SWIMMING_POOL_ID', primary_key=True)  # Field name made lowercase.
    supplier = models.ForeignKey('MasterSupplierTypeSociety', db_column='SUPPLIER_ID', blank=True, null=True)  # Field name made lowercase.
    swimming_pool_size_breadth = models.CharField(db_column='SWIMMING_POOL_SIZE_BREADTH', max_length=10, blank=True, null=True)  # Field name made lowercase.
    swimming_pool_size_length = models.CharField(db_column='SWIMMING_POOL_SIZE_LENGTH', max_length=10, blank=True, null=True)  # Field name made lowercase.
    swimming_pool_side_area = models.CharField(db_column='SWIMMING_POOL_SIDE_AREA', max_length=10, blank=True, null=True)  # Field name made lowercase.
    swimming_pool_side_rentals = models.CharField(db_column='SWIMMING_POOL_SIDE_RENTALS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    swimming_pool_timings_open = models.CharField(db_column='SWIMMING_POOL_TIMINGS_OPEN', max_length=20, blank=True, null=True)  # Field name made lowercase.
    swimming_pool_timings_close = models.CharField(db_column='SWIMMING_POOL_TIMINGS_CLOSE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    swimming_pool_daily_price_society = models.CharField(db_column='SWIMMING_POOL_DAILY_PRICE_SOCIETY', max_length=5, blank=True, null=True)  # Field name made lowercase.
    swimming_pool_daily_price_business = models.CharField(db_column='SWIMMING_POOL_DAILY_PRICE_BUSINESS', max_length=5, blank=True, null=True)  # Field name made lowercase.
    swimming_pool_location = models.CharField(db_column='SWIMMING_POOL_LOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    notice_board_count_per_swimming_pool = models.IntegerField(db_column='NOTICE_BOARD_COUNT_PER_SWIMMING_POOL', blank=True, null=True)  # Field name made lowercase.
    standee_location_count_per_swimming_pool = models.IntegerField(db_column='STANDEE_LOCATION_COUNT_PER_SWIMMING_POOL', blank=True, null=True)  # Field name made lowercase.
    stall_count_per_swimming_pool = models.IntegerField(db_column='STALL_COUNT_PER_SWIMMING_POOL', blank=True, null=True)  # Field name made lowercase.
    banner_count_per_swimming_pool = models.IntegerField(db_column='BANNER_COUNT_PER_SWIMMING_POOL', blank=True, null=True)  # Field name made lowercase.
    swimming_pool_sitting = models.IntegerField(db_column='SWIMMING_POOL_SITTING', blank=True, null=True)  # Field name made lowercase.
    swimming_pool_inventory_status = models.CharField(db_column='SWIMMING_POOL_INVENTORY_STATUS', max_length=15, blank=True, null=True)  # Field name made lowercase.
    audio_video_display_available = models.CharField(db_column='AUDIO_VIDEO_DISPLAY_AVAILABLE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    electricity_charges_perhour = models.IntegerField(db_column='ELECTRICITY_CHARGES_PERHOUR', blank=True, null=True)  # Field name made lowercase.
    changing_room_available = models.CharField(db_column='CHANGING_ROOM_AVAILABLE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    lit_unlit = models.CharField(db_column='LIT_UNLIT', max_length=5, blank=True, null=True)  # Field name made lowercase.
    photograph_1 = models.CharField(db_column='PHOTOGRAPH_1', max_length=45, blank=True, null=True)  # Field name made lowercase.
    photograph_2 = models.CharField(db_column='PHOTOGRAPH_2', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MASTER_SWIMMING_POOL_INFO'


class MasterWallInventory(models.Model):
    inventory_type_id = models.CharField(db_column='INVENTORY_TYPE_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', primary_key=True, max_length=20)  # Field name made lowercase.
    wall_size = models.CharField(db_column='WALL_SIZE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    wall_frame_size = models.CharField(db_column='WALL_FRAME_SIZE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    wall_area = models.CharField(db_column='WALL_AREA', max_length=10, blank=True, null=True)  # Field name made lowercase.
    wall_type = models.CharField(db_column='WALL_TYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    wall_internal_external = models.CharField(db_column='WALL_INTERNAL_EXTERNAL', max_length=10, blank=True, null=True)  # Field name made lowercase.
    wall_sides = models.CharField(db_column='WALL_SIDES', max_length=10, blank=True, null=True)  # Field name made lowercase.
    wall_monthly_price_society = models.CharField(db_column='WALL_MONTHLY_PRICE_SOCIETY', max_length=5, blank=True, null=True)  # Field name made lowercase.
    wall_quarterly_price_society = models.CharField(db_column='WALL_QUARTERLY_PRICE_SOCIETY', max_length=5, blank=True, null=True)  # Field name made lowercase.
    wall_monthly_price_business = models.CharField(db_column='WALL_MONTHLY_PRICE_BUSINESS', max_length=5, blank=True, null=True)  # Field name made lowercase.
    wall_quarterly_price_business = models.CharField(db_column='WALL_QUARTERLY_PRICE_BUSINESS', max_length=5, blank=True, null=True)  # Field name made lowercase.
    wall_location = models.CharField(db_column='WALL_LOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    wall_paint_allowed = models.CharField(db_column='WALL_PAINT_ALLOWED', max_length=5, blank=True, null=True)  # Field name made lowercase.
    wall_frame_status = models.CharField(db_column='WALL_FRAME_STATUS', max_length=5, blank=True, null=True)  # Field name made lowercase.
    wall_inventory_status = models.CharField(db_column='WALL_INVENTORY_STATUS', max_length=15, blank=True, null=True)  # Field name made lowercase.
    supplier = models.ForeignKey('MasterSupplierTypeSociety', db_column='SUPPLIER_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MASTER_WALL_INVENTORY'


class UserInquiry(models.Model):
    inquiry_id = models.AutoField(db_column='INQUIRY_ID', primary_key=True)  # Field name made lowercase.
    company_name = models.CharField(db_column='COMPANY_NAME', max_length=40)  # Field name made lowercase.
    contact_person_name = models.CharField(db_column='CONTACT_PERSON_NAME', max_length=40, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=40, blank=True, null=True)  # Field name made lowercase.
    phone = models.IntegerField(db_column='PHONE', blank=True, null=True)  # Field name made lowercase.
    inquiry_details = models.TextField(db_column='INQUIRY_DETAILS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USER_INQUIRY'


class CommonAreaDetails(models.Model):
    common_area_id = models.CharField(db_column='COMMON_AREA_ID', primary_key=True, max_length=20)  # Field name made lowercase.
    pole_count = models.IntegerField(db_column='POLE_COUNT', blank=True, null=True)  # Field name made lowercase.
    street_furniture_count = models.IntegerField(db_column='STREET_FURNITURE_COUNT', blank=True, null=True)  # Field name made lowercase.
    banner_count = models.IntegerField(db_column='BANNER_COUNT', blank=True, null=True)  # Field name made lowercase.
    common_area_stalls_count = models.IntegerField(db_column='COMMON_AREA_STALLS_COUNT', blank=True, null=True)  # Field name made lowercase.
    car_display = models.IntegerField(db_column='CAR_DISPLAY', blank=True, null=True)  # Field name made lowercase.
    wall_count = models.IntegerField(db_column='WALL_COUNT', blank=True, null=True)  # Field name made lowercase.
    major_event_count = models.IntegerField(db_column='MAJOR_EVENT_COUNT', blank=True, null=True)  # Field name made lowercase.
    supplier_id = models.CharField(db_column='SUPPLIER_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'common_area_details'


class MasterContactDetails(models.Model):
    contact_id = models.AutoField(db_column='CONTACT_ID', primary_key=True)  # Field name made lowercase.
    supplier_id = models.TextField(db_column='SUPPLIER_ID', blank=True, null=True)  # Field name made lowercase.
    contact_type = models.TextField(db_column='CONTACT_TYPE', blank=True, null=True)  # Field name made lowercase.
    specify_others = models.TextField(db_column='SPECIFY_OTHERS', blank=True, null=True)  # Field name made lowercase.
    contact_name = models.TextField(db_column='CONTACT_NAME', blank=True, null=True)  # Field name made lowercase.
    contact_landline = models.TextField(db_column='CONTACT_LANDLINE', blank=True, null=True)  # Field name made lowercase.
    contact_mobile = models.TextField(db_column='CONTACT_MOBILE', blank=True, null=True)  # Field name made lowercase.
    contact_emailid = models.TextField(db_column='CONTACT_EMAILID', blank=True, null=True)  # Field name made lowercase.
    spoc = models.CharField(db_column='SPOC', max_length=5, blank=True, null=True)  # Field name made lowercase.
    contact_authority = models.CharField(db_column='CONTACT_AUTHORITY', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'master_contact_details'


class MasterEvents(models.Model):
    event_id = models.AutoField(db_column='EVENT_ID', primary_key=True)  # Field name made lowercase.
    supplier = models.ForeignKey('MasterSupplierTypeSociety', db_column='SUPPLIER_ID', blank=True, null=True)  # Field name made lowercase.
    event_name = models.CharField(db_column='EVENT_NAME', max_length=20, blank=True, null=True)  # Field name made lowercase.
    event_location = models.CharField(db_column='EVENT_LOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    past_major_events = models.CharField(db_column='PAST_MAJOR_EVENTS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    past_gathering_per_event = models.CharField(db_column='PAST_GATHERING_PER_EVENT', max_length=5, blank=True, null=True)  # Field name made lowercase.
    no_of_days = models.IntegerField(db_column='NO_OF_DAYS', blank=True, null=True)  # Field name made lowercase.
    activities = models.CharField(db_column='ACTIVITIES', max_length=50, blank=True, null=True)  # Field name made lowercase.
    stall_spaces_count = models.IntegerField(db_column='STALL_SPACES_COUNT', blank=True, null=True)  # Field name made lowercase.
    banner_spaces_count = models.IntegerField(db_column='BANNER_SPACES_COUNT', blank=True, null=True)  # Field name made lowercase.
    poster_spaces_count = models.IntegerField(db_column='POSTER_SPACES_COUNT', blank=True, null=True)  # Field name made lowercase.
    standee_spaces_count = models.IntegerField(db_column='STANDEE_SPACES_COUNT', blank=True, null=True)  # Field name made lowercase.
    event_linked = models.CharField(db_column='EVENT_LINKED', max_length=5, blank=True, null=True)  # Field name made lowercase.
    photograph_1 = models.CharField(db_column='PHOTOGRAPH_1', max_length=45, blank=True, null=True)  # Field name made lowercase.
    photograph_2 = models.CharField(db_column='PHOTOGRAPH_2', max_length=45, blank=True, null=True)  # Field name made lowercase.
    photograph_3 = models.CharField(db_column='PHOTOGRAPH_3', max_length=45, blank=True, null=True)  # Field name made lowercase.
    event_plan_map = models.CharField(db_column='EVENT_PLAN_MAP', max_length=45, blank=True, null=True)  # Field name made lowercase.
    event_status = models.CharField(db_column='EVENT_STATUS', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'master_events'


class MasterInventoryInfo(models.Model):
    inventory_type_id = models.CharField(db_column='INVENTORY_TYPE_ID', primary_key=True, max_length=20)  # Field name made lowercase.
    inventory_length = models.CharField(db_column='INVENTORY_LENGTH', max_length=10, blank=True, null=True)  # Field name made lowercase.
    inventory_breadth = models.CharField(db_column='INVENTORY_BREADTH', max_length=10, blank=True, null=True)  # Field name made lowercase.
    inventory_height = models.CharField(db_column='INVENTORY_HEIGHT', max_length=10, blank=True, null=True)  # Field name made lowercase.
    inventory_area = models.CharField(db_column='INVENTORY_AREA', max_length=10, blank=True, null=True)  # Field name made lowercase.
    inventory_size = models.CharField(db_column='INVENTORY_SIZE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    inventory_name = models.CharField(db_column='INVENTORY_NAME', max_length=70, blank=True, null=True)  # Field name made lowercase.
    comments1 = models.CharField(db_column='COMMENTS1', max_length=500, blank=True, null=True)  # Field name made lowercase.
    comments2 = models.CharField(db_column='COMMENTS2', max_length=500, blank=True, null=True)  # Field name made lowercase.
    material_type = models.CharField(db_column='MATERIAL_TYPE', max_length=70, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'master_inventory_info'


class MasterMailboxInfo(models.Model):
    mailbox_info_id = models.AutoField(db_column='MAILBOX_INFO_ID', primary_key=True)  # Field name made lowercase.
    tower_id = models.CharField(db_column='TOWER_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    supplier = models.ForeignKey('MasterSupplierTypeSociety', db_column='SUPPLIER_ID', blank=True, null=True)  # Field name made lowercase.
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    flier_distribution_frequency = models.CharField(db_column='FLIER_DISTRIBUTION_FREQUENCY', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mail_box_inventory_status = models.CharField(db_column='MAIL_BOX_INVENTORY_STATUS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mailbox_count_per_tower = models.IntegerField(db_column='MAILBOX_COUNT_PER_TOWER', blank=True, null=True)  # Field name made lowercase.
    mailbox_flyer_price_society = models.CharField(db_column='MAILBOX_FLYER_PRICE_SOCIETY', max_length=5, blank=True, null=True)  # Field name made lowercase.
    mailbox_flyer_price_business = models.CharField(db_column='MAILBOX_FLYER_PRICE_BUSINESS', max_length=5, blank=True, null=True)  # Field name made lowercase.
    photograph_1 = models.CharField(db_column='PHOTOGRAPH_1', max_length=45, blank=True, null=True)  # Field name made lowercase.
    photograph_2 = models.CharField(db_column='PHOTOGRAPH_2', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'master_mailbox_info'


class MasterOperationsInfo(models.Model):
    operator_id = models.CharField(db_column='OPERATOR_ID', primary_key=True, max_length=10)  # Field name made lowercase.
    operator_name = models.CharField(db_column='OPERATOR_NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    operator_email = models.CharField(db_column='OPERATOR_EMAIL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    operator_company = models.CharField(db_column='OPERATOR_COMPANY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    operator_phone_number = models.IntegerField(db_column='OPERATOR_PHONE_NUMBER', blank=True, null=True)  # Field name made lowercase.
    comments_1 = models.CharField(db_column='COMMENTS_1', max_length=500, blank=True, null=True)  # Field name made lowercase.
    comments_2 = models.CharField(db_column='COMMENTS_2', max_length=500, blank=True, null=True)  # Field name made lowercase.
    company_id = models.CharField(db_column='COMPANY_ID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    company_address = models.CharField(db_column='COMPANY_ADDRESS', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'master_operations_info'


class MasterPoleInventory(models.Model):
    inventory_type_id = models.AutoField(db_column='INVENTORY_TYPE_ID', primary_key=True)  # Field name made lowercase.
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    pole_hoarding_size = models.CharField(db_column='POLE_HOARDING_SIZE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    pole_area = models.CharField(db_column='POLE_AREA', max_length=10, blank=True, null=True)  # Field name made lowercase.
    pole_hoarding_type = models.CharField(db_column='POLE_HOARDING_TYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    pole_lit_status = models.TextField(db_column='POLE_LIT_STATUS', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    pole_sides = models.CharField(db_column='POLE_SIDES', max_length=10, blank=True, null=True)  # Field name made lowercase.
    pole_monthly_price_society = models.CharField(db_column='POLE_MONTHLY_PRICE_SOCIETY', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pole_quarterly_price_society = models.CharField(db_column='POLE_QUARTERLY_PRICE_SOCIETY', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pole_monthly_price_business = models.CharField(db_column='POLE_MONTHLY_PRICE_BUSINESS', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pole_quarterly_price_business = models.CharField(db_column='POLE_QUARTERLY_PRICE_BUSINESS', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pole_location = models.CharField(db_column='POLE_LOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    pole_inventory_status = models.CharField(db_column='POLE_INVENTORY_STATUS', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'master_pole_inventory'


class MasterPosterInventoryMapping(models.Model):
    inventory_mapping_id = models.AutoField(db_column='INVENTORY_MAPPING_ID', primary_key=True)  # Field name made lowercase.
    inventory_type_id = models.CharField(db_column='INVENTORY_TYPE_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    poster_adinventory_id = models.CharField(db_column='POSTER_ADINVENTORY_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    standee_adinventory_id = models.CharField(db_column='STANDEE_ADINVENTORY_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    banner_adinventory_id = models.CharField(db_column='BANNER_ADINVENTORY_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stall_adinventory_id = models.CharField(db_column='STALL_ADINVENTORY_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'master_poster_inventory_mapping'


class MasterRatioDetails(models.Model):
    supplier_id = models.CharField(db_column='SUPPLIER_ID', max_length=20)  # Field name made lowercase.
    machadalo_index = models.CharField(db_column='MACHADALO_INDEX', max_length=30)  # Field name made lowercase.
    age_proportions = models.CharField(db_column='AGE_PROPORTIONS', max_length=15, blank=True, null=True)  # Field name made lowercase.
    flat_avg_rental_persqft = models.CharField(db_column='FLAT_AVG_RENTAL_PERSQFT', max_length=10, blank=True, null=True)  # Field name made lowercase.
    flat_avg_size = models.CharField(db_column='FLAT_AVG_SIZE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    flat_sale_cost_persqft = models.CharField(db_column='FLAT_SALE_COST_PERSQFT', max_length=5, blank=True, null=True)  # Field name made lowercase.
    wall_count = models.IntegerField(db_column='WALL_COUNT', blank=True, null=True)  # Field name made lowercase.
    major_event_count = models.IntegerField(db_column='MAJOR_EVENT_COUNT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'master_ratio_details'
        unique_together = (('supplier_id', 'machadalo_index'),)


class MasterSignup(models.Model):
    user_id = models.AutoField(db_column='USER_ID', primary_key=True)  # Field name made lowercase.
    first_name = models.TextField(db_column='FIRST_NAME', blank=True, null=True)  # Field name made lowercase.
    email = models.TextField(db_column='EMAIL', blank=True, null=True)  # Field name made lowercase.
    password = models.TextField(db_column='PASSWORD', blank=True, null=True)  # Field name made lowercase.
    login_type = models.TextField(db_column='LOGIN_TYPE', blank=True, null=True)  # Field name made lowercase.
    system_generated_id = models.BigIntegerField(db_column='SYSTEM_GENERATED_ID')  # Field name made lowercase.
    adminstrator_approved = models.CharField(db_column='ADMINSTRATOR_APPROVED', max_length=255, blank=True, null=True)  # Field name made lowercase.
    company_name = models.CharField(db_column='COMPANY_NAME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mobile_no = models.CharField(db_column='MOBILE_NO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    signup_status = models.CharField(db_column='SIGNUP_STATUS', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'master_signup'


class MasterStallInventory(models.Model):
    supplier = models.ForeignKey('MasterSupplierTypeSociety', db_column='SUPPLIER_ID', blank=True, null=True)  # Field name made lowercase.
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', primary_key=True, max_length=20)  # Field name made lowercase.
    stall_types = models.CharField(db_column='STALL_TYPES', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stall_timings_morning = models.CharField(db_column='STALL_TIMINGS_morning', max_length=10, blank=True, null=True)  # Field name made lowercase.
    stall_size_area = models.CharField(db_column='STALL_SIZE_AREA', max_length=10, blank=True, null=True)  # Field name made lowercase.
    stall_daily_price_stall_society = models.CharField(db_column='STALL_DAILY_PRICE_STALL_SOCIETY', max_length=15, blank=True, null=True)  # Field name made lowercase.
    stall_daily_price_stall_business = models.CharField(db_column='STALL_DAILY_PRICE_STALL_BUSINESS', max_length=15, blank=True, null=True)  # Field name made lowercase.
    current_price_stall = models.CharField(db_column='Current_Price_Stall', max_length=5, blank=True, null=True)  # Field name made lowercase.
    stall_timings_evening = models.CharField(db_column='STALL_TIMINGS_evening', max_length=10, blank=True, null=True)  # Field name made lowercase.
    stall_location = models.CharField(db_column='STALL_LOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    electricity_available_stalls = models.CharField(db_column='ELECTRICITY_AVAILABLE_STALLS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    electricity_charges_daily = models.CharField(db_column='ELECTRICITY_CHARGES_DAILY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sound_system_allowed = models.CharField(db_column='SOUND_SYSTEM_ALLOWED', max_length=50, blank=True, null=True)  # Field name made lowercase.
    stall_furniture_available = models.CharField(db_column='STALL_FURNITURE_AVAILABLE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    stall_furniture_details = models.CharField(db_column='STALL_FURNITURE_DETAILS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    stall_inventory_status = models.CharField(db_column='STALL_INVENTORY_STATUS', max_length=15, blank=True, null=True)  # Field name made lowercase.
    photograph_1 = models.CharField(db_column='PHOTOGRAPH_1', max_length=45, blank=True, null=True)  # Field name made lowercase.
    photograph_2 = models.CharField(db_column='PHOTOGRAPH_2', max_length=45, blank=True, null=True)  # Field name made lowercase.
    event_id = models.CharField(db_column='EVENT_ID', max_length=45, blank=True, null=True)  # Field name made lowercase.
    event_linked = models.CharField(db_column='EVENT_LINKED', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'master_stall_inventory'


class MasterStreetFurniture(models.Model):
    street_furniture_id = models.AutoField(db_column='STREET_FURNITURE_ID', primary_key=True)  # Field name made lowercase.
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    supplier = models.ForeignKey('MasterSupplierTypeSociety', db_column='SUPPLIER_ID', blank=True, null=True)  # Field name made lowercase.
    no_of_furniture = models.IntegerField(db_column='NO_OF_FURNITURE', blank=True, null=True)  # Field name made lowercase.
    type_of_furniture = models.CharField(db_column='TYPE_OF_FURNITURE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    photograph_1 = models.CharField(db_column='PHOTOGRAPH_1', max_length=45, blank=True, null=True)  # Field name made lowercase.
    photograph_2 = models.CharField(db_column='PHOTOGRAPH_2', max_length=45, blank=True, null=True)  # Field name made lowercase.
    comment_1 = models.TextField(db_column='COMMENT_1', blank=True, null=True)  # Field name made lowercase.
    comment_2 = models.TextField(db_column='COMMENT_2', blank=True, null=True)  # Field name made lowercase.
    furniture_status = models.CharField(db_column='FURNITURE_STATUS', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'master_street_furniture'


class MasterSupplierInfo(models.Model):
    supplier_id = models.CharField(db_column='SUPPLIER_ID', primary_key=True, max_length=20)  # Field name made lowercase.
    supplier_name = models.CharField(db_column='SUPPLIER_NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    supplier_emailid = models.CharField(db_column='SUPPLIER_EMAILID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    supplier_phone_no = models.CharField(db_column='SUPPLIER_PHONE_NO', max_length=15, blank=True, null=True)  # Field name made lowercase.
    supplier_location = models.CharField(db_column='SUPPLIER_LOCATION', max_length=70, blank=True, null=True)  # Field name made lowercase.
    supplier_business_type = models.CharField(db_column='SUPPLIER_BUSINESS_TYPE', max_length=30, blank=True, null=True)  # Field name made lowercase.
    comments_1 = models.CharField(db_column='COMMENTS_1', max_length=500, blank=True, null=True)  # Field name made lowercase.
    comments_2 = models.CharField(db_column='COMMENTS_2', max_length=500, blank=True, null=True)  # Field name made lowercase.
    supplier_address = models.CharField(db_column='SUPPLIER_ADDRESS', max_length=250, blank=True, null=True)  # Field name made lowercase.
    total_inventory = models.CharField(db_column='TOTAL_INVENTORY', max_length=5, blank=True, null=True)  # Field name made lowercase.
    total_inventory_currently_released = models.CharField(db_column='TOTAL_INVENTORY_CURRENTLY_RELEASED', max_length=5, blank=True, null=True)  # Field name made lowercase.
    total_inventory_currently_released_audit = models.CharField(db_column='TOTAL_INVENTORY_CURRENTLY_RELEASED_AUDIT', max_length=5, blank=True, null=True)  # Field name made lowercase.
    pan_id = models.CharField(db_column='PAN_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tan_id = models.CharField(db_column='TAN_ID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    supplier_type = models.CharField(db_column='SUPPLIER_TYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mapping_date = models.DateField(db_column='MAPPING_DATE', blank=True, null=True)  # Field name made lowercase.
    agreement_term_start = models.DateField(db_column='AGREEMENT_TERM_START', blank=True, null=True)  # Field name made lowercase.
    agreement_term_end = models.DateField(db_column='AGREEMENT_TERM_END', blank=True, null=True)  # Field name made lowercase.
    current_status = models.DateField(db_column='CURRENT_STATUS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'master_supplier_info'


class MasterSupplierTypeSociety(models.Model):
    supplier_id = models.CharField(db_column='SUPPLIER_ID', primary_key=True, max_length=20)  # Field name made lowercase.
    society_name = models.CharField(db_column='SOCIETY_NAME', max_length=70, blank=True, null=True)  # Field name made lowercase.
    society_address1 = models.CharField(db_column='SOCIETY_ADDRESS1', max_length=250, blank=True, null=True)  # Field name made lowercase.
    society_address2 = models.CharField(db_column='SOCIETY_ADDRESS2', max_length=250, blank=True, null=True)  # Field name made lowercase.
    society_zip = models.CharField(db_column='SOCIETY_ZIP', max_length=250, blank=True, null=True)  # Field name made lowercase.
    society_city = models.CharField(db_column='SOCIETY_CITY', max_length=250, blank=True, null=True)  # Field name made lowercase.
    society_state = models.CharField(db_column='SOCIETY_STATE', max_length=250, blank=True, null=True)  # Field name made lowercase.
    society_longitude = models.CharField(db_column='SOCIETY_LONGITUDE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    society_latitude = models.CharField(db_column='SOCIETY_LATITUDE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    society_location_type = models.CharField(db_column='SOCIETY_LOCATION_TYPE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    society_type_quality = models.CharField(db_column='SOCIETY_TYPE_QUALITY', max_length=30, blank=True, null=True)  # Field name made lowercase.
    society_type_quantity = models.CharField(db_column='SOCIETY_TYPE_QUANTITY', max_length=30, blank=True, null=True)  # Field name made lowercase.
    flat_count = models.IntegerField(db_column='FLAT_COUNT', blank=True, null=True)  # Field name made lowercase.
    resident_count = models.IntegerField(db_column='RESIDENT_COUNT', blank=True, null=True)  # Field name made lowercase.
    cars_count = models.IntegerField(db_column='CARS_COUNT', blank=True, null=True)  # Field name made lowercase.
    luxury_cars_count = models.IntegerField(db_column='LUXURY_CARS_COUNT', blank=True, null=True)  # Field name made lowercase.
    lift_count = models.IntegerField(db_column='LIFT_COUNT', blank=True, null=True)  # Field name made lowercase.
    machadalo_index = models.CharField(db_column='MACHADALO_INDEX', max_length=30, blank=True, null=True)  # Field name made lowercase.
    average_rent = models.IntegerField(db_column='AVERAGE_RENT', blank=True, null=True)  # Field name made lowercase.
    notice_board_available = models.TextField(db_column='NOTICE_BOARD_AVAILABLE', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    stall_available = models.TextField(db_column='STALL_AVAILABLE', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    car_display_available = models.TextField(db_column='CAR_DISPLAY_AVAILABLE', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    banner_available = models.TextField(db_column='BANNER_AVAILABLE', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    food_tasting_allowed = models.CharField(db_column='FOOD_TASTING_ALLOWED', max_length=5, blank=True, null=True)  # Field name made lowercase.
    events_count = models.IntegerField(db_column='EVENTS_COUNT', blank=True, null=True)  # Field name made lowercase.
    swimming_pool_avaialblity = models.TextField(db_column='SWIMMING_POOL_AVAIALBLITY', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    mail_box_available = models.TextField(db_column='MAIL_BOX_AVAILABLE', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    door_to_door_allowed = models.TextField(db_column='DOOR_TO_DOOR_ALLOWED', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    events_occurance = models.CharField(db_column='EVENTS_OCCURANCE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    street_furniture_available = models.TextField(db_column='STREET_FURNITURE_AVAILABLE', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    sports_facility_available = models.CharField(db_column='SPORTS_FACILITY_AVAILABLE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    swimming_pool_availabel = models.TextField(db_column='SWIMMING_POOL_AVAILABEL', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    street_furniture_count = models.IntegerField(db_column='STREET_FURNITURE_COUNT', blank=True, null=True)  # Field name made lowercase.
    tower_count = models.IntegerField(db_column='TOWER_COUNT', blank=True, null=True)  # Field name made lowercase.
    standee_count = models.IntegerField(db_column='STANDEE_COUNT', blank=True, null=True)  # Field name made lowercase.
    past_year_collections_stalls = models.IntegerField(db_column='PAST_YEAR_COLLECTIONS_STALLS', blank=True, null=True)  # Field name made lowercase.
    past_year_collections_car = models.IntegerField(db_column='PAST_YEAR_COLLECTIONS_CAR', blank=True, null=True)  # Field name made lowercase.
    past_year_collections_poster = models.IntegerField(db_column='PAST_YEAR_COLLECTIONS_POSTER', blank=True, null=True)  # Field name made lowercase.
    past_year_collections_banners = models.IntegerField(db_column='PAST_YEAR_COLLECTIONS_BANNERS', blank=True, null=True)  # Field name made lowercase.
    past_year_collections_standee = models.IntegerField(db_column='PAST_YEAR_COLLECTIONS_STANDEE', blank=True, null=True)  # Field name made lowercase.
    past_year_sponsorship_collection_events = models.IntegerField(db_column='PAST_YEAR_SPONSORSHIP_COLLECTION_EVENTS', blank=True, null=True)  # Field name made lowercase.
    past_year_total_sponsorship = models.IntegerField(db_column='PAST_YEAR_TOTAL_SPONSORSHIP', blank=True, null=True)  # Field name made lowercase.
    societies_preferred_business_type = models.CharField(db_column='SOCIETIES_PREFERRED_BUSINESS_TYPE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    societies_preferred_business_id = models.CharField(db_column='SOCIETIES_PREFERRED_BUSINESS_ID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    business_type_not_allowed = models.CharField(db_column='BUSINESS_TYPE_NOT_ALLOWED', max_length=5, blank=True, null=True)  # Field name made lowercase.
    business_id_not_allowed = models.IntegerField(db_column='BUSINESS_ID_NOT_ALLOWED', blank=True, null=True)  # Field name made lowercase.
    referred_by = models.CharField(db_column='REFERRED_BY', max_length=5, blank=True, null=True)  # Field name made lowercase.
    contact_person_count = models.IntegerField(db_column='CONTACT_PERSON_COUNT', blank=True, null=True)  # Field name made lowercase.
    poster_count = models.IntegerField(db_column='POSTER_COUNT', blank=True, null=True)  # Field name made lowercase.
    banner_count = models.IntegerField(db_column='BANNER_COUNT', blank=True, null=True)  # Field name made lowercase.
    wall_count = models.IntegerField(db_column='WALL_COUNT', blank=True, null=True)  # Field name made lowercase.
    flier_distribution_frequency_per_month = models.IntegerField(db_column='FLIER_DISTRIBUTION_FREQUENCY_PER_MONTH', blank=True, null=True)  # Field name made lowercase.
    bill_sponsorship_electricity = models.CharField(db_column='BILL_SPONSORSHIP_ELECTRICITY', max_length=20, blank=True, null=True)  # Field name made lowercase.
    bill_sponsorship_maintenanace = models.CharField(db_column='BILL_SPONSORSHIP_MAINTENANACE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    children_playing_area_available = models.CharField(db_column='CHILDREN_PLAYING_AREA_AVAILABLE', max_length=45, blank=True, null=True)  # Field name made lowercase.
    children_playing_area_count = models.IntegerField(db_column='CHILDREN_PLAYING_AREA_count', blank=True, null=True)  # Field name made lowercase.
    walking_area_available = models.CharField(db_column='WALKING_AREA_AVAILABLE', max_length=45, blank=True, null=True)  # Field name made lowercase.
    walking_area_size = models.CharField(db_column='WALKING_AREA_SIZE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    count_0to6 = models.IntegerField(db_column='COUNT_0TO6', blank=True, null=True)  # Field name made lowercase.
    count_6_18 = models.IntegerField(db_column='COUNT_6-18', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    count_19_35 = models.IntegerField(db_column='COUNT_19-35', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    count_36_50 = models.IntegerField(db_column='COUNT_36-50', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    count_50to65 = models.IntegerField(db_column='COUNT_50to65', blank=True, null=True)  # Field name made lowercase.
    count_65above = models.IntegerField(db_column='COUNT_65above', blank=True, null=True)  # Field name made lowercase.
    flat_avg_size = models.IntegerField(db_column='FLAT_AVG_SIZE', blank=True, null=True)  # Field name made lowercase.
    flat_avg_rental_persqft = models.IntegerField(db_column='FLAT_AVG_RENTAL_PERSQFT', blank=True, null=True)  # Field name made lowercase.
    flat_sale_cost_persqft = models.IntegerField(db_column='FLAT_SALE_COST_PERSQFT', blank=True, null=True)  # Field name made lowercase.
    total_ad_spaces = models.IntegerField(db_column='TOTAL_AD_SPACES', blank=True, null=True)  # Field name made lowercase.

    def get_contact_list(self):
        return MasterContactDetails.objects.filter(supplier_id=self.supplier_id)

    def get_reference(self):
        return None

    def is_contact_available(self):
        contacts = self.get_contact_list()
        if contacts and len(contacts) > 0 :
            return True
        return False

    def is_reference_available(self):
        if self.get_reference():
            return True
        return False

    class Meta:
        managed = False
        db_table = 'master_supplier_type_society'


class MasterSupplierTypeSocietyTower(models.Model):
    tower_id = models.AutoField(db_column='TOWER_ID', primary_key=True)  # Field name made lowercase.
    tower_tag = models.CharField(db_column='TOWER_TAG', max_length=20, blank=True, null=True)  # Field name made lowercase.
    supplier = models.ForeignKey(MasterSupplierTypeSociety, db_column='SUPPLIER_ID', blank=True, null=True)  # Field name made lowercase.
    tower_name = models.CharField(db_column='TOWER_NAME', max_length=20, blank=True, null=True)  # Field name made lowercase.
    flat_count_per_tower = models.IntegerField(db_column='FLAT_COUNT_PER_TOWER', blank=True, null=True)  # Field name made lowercase.
    floor_count_per_tower = models.IntegerField(db_column='FLOOR_COUNT_PER_TOWER', blank=True, null=True)  # Field name made lowercase.
    notice_board_count_per_tower = models.IntegerField(db_column='NOTICE_BOARD_COUNT_PER_TOWER', blank=True, null=True)  # Field name made lowercase.
    standee_location_count_per_tower = models.IntegerField(db_column='STANDEE_LOCATION_COUNT_PER_TOWER', blank=True, null=True)  # Field name made lowercase.
    mailbox_count_per_tower = models.IntegerField(db_column='MAILBOX_COUNT_PER_TOWER', blank=True, null=True)  # Field name made lowercase.
    stall_count_per_tower = models.IntegerField(db_column='STALL_COUNT_PER_TOWER', blank=True, null=True)  # Field name made lowercase.
    tower_location = models.CharField(db_column='TOWER_LOCATION', max_length=100, blank=True, null=True)  # Field name made lowercase.
    tower_resident_count = models.IntegerField(db_column='TOWER_RESIDENT_COUNT', blank=True, null=True)  # Field name made lowercase.
    lift_count = models.IntegerField(db_column='LIFT_COUNT', blank=True, null=True)  # Field name made lowercase.
    average_rent_per_sqft = models.IntegerField(db_column='AVERAGE_RENT_PER_SQFT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'master_supplier_type_society_tower'
