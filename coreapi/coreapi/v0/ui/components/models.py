from django.db import models
from django.conf import settings
from v0.ui.base.models import BaseModel
from django.contrib.contenttypes.models import ContentType
from v0.constants import supplier_id_max_length
from django.contrib.contenttypes import fields
from v0 import managers

class Amenity(BaseModel):
    """
    Stores individual amenities. There basic details.
    """
    name = models.CharField(max_length=1000)
    code = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        db_table = 'amenities'

class CorporateBuildingWing(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    wing_name = models.CharField(db_column='WING_NAME', max_length=50, null=True, blank=True)
    number_of_floors = models.IntegerField(db_column='NUMBER_OF_FLOORS', null=True, blank=True)
    building_id = models.ForeignKey('CorporateBuilding',db_index=True, db_column='BUILDING_ID',related_name='buildingwing', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table='corporate_building_wing'

class CompanyFloor(models.Model):
    company_details_id = models.ForeignKey('CorporateCompanyDetails',db_column='COMPANY_DETAILS_ID',related_name='wingfloor', blank=True, null=True, on_delete=models.CASCADE)
    floor_number = models.IntegerField(db_column='FLOOR_NUMBER', blank=True, null=True)

    class Meta:
        db_table='corporate_building_floors'

class CommunityHallInfo(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    supplier = models.ForeignKey('SupplierTypeSociety', related_name='community_halls', db_column='SUPPLIER_ID', blank=True, null=True, on_delete=models.CASCADE)
    size_length = models.FloatField(db_column='SIZE_LENGTH', default=0.0, blank=True, null=True)
    size_breadth = models.FloatField(db_column='SIZE_BREADTH', default=0.0, blank=True, null=True)
    ceiling_height = models.FloatField(db_column='CEILING_HEIGHT', default=0.0, blank=True, null=True)
    timings_open = models.TimeField(db_column='TIMINGS_OPEN', blank=True, null=True)
    timings_close = models.TimeField(db_column='TIMINGS_CLOSE', blank=True, null=True)
    rentals_current = models.FloatField(db_column='RENTALS_CURRENT', default=0.0, blank=True, null=True)
    daily_price_society = models.FloatField(db_column='DAILY_PRICE_SOCIETY', default=0.0, blank=True, null=True)
    daily_price_business = models.FloatField(db_column='DAILY_PRICE_BUSINESS', default=0.0, blank=True, null=True)
    location = models.CharField(db_column='LOCATION', max_length=50, blank=True, null=True)
    furniture_available = models.CharField(db_column='FURNITURE_AVAILABLE', max_length=5, blank=True, null=True)
    chair_count = models.IntegerField(db_column='CHAIR_COUNT', blank=True, null=True)
    tables_count = models.IntegerField(db_column='TABLES_COUNT', blank=True, null=True)
    air_conditioned = models.CharField(db_column='AIR_CONDITIONED', max_length=5, blank=True, null=True)
    projector_available = models.CharField(db_column='PROJECTOR_AVAILABLE', max_length=15, blank=True, null=True)
    inventory_status = models.CharField(db_column='INVENTORY_STATUS', max_length=15, blank=True, null=True)
    sitting = models.IntegerField(db_column='SITTING', blank=True, null=True)
    audio_video_display_available = models.CharField(db_column='AUDIO_VIDEO_DISPLAY_AVAILABLE', max_length=5, blank=True, null=True)
    electricity_charges_perhour = models.FloatField(db_column='ELECTRICITY_CHARGES_PERHOUR',default=0.0, blank=True, null=True)
    notice_board_count_per_community_hall = models.IntegerField(db_column='NOTICE_BOARD_COUNT_PER_COMMUNITY_HALL', blank=True, null=True)
    standee_location_count_per_community_hall = models.IntegerField(db_column='STANDEE_LOCATION_COUNT_PER_COMMUNITY_HALL', blank=True, null=True)
    stall_count_per_community_hall = models.IntegerField(db_column='STALL_COUNT_PER_COMMUNITY_HALL', blank=True, null=True)
    banner_count_per_community_hall = models.IntegerField(db_column='BANNER_COUNT_PER_COMMUNITY_HALL', blank=True, null=True)

    class Meta:
        db_table = 'community_hall_info'

class LiftDetails(models.Model):

    lift_tag = models.CharField(db_column='LIFT_TAG', max_length=20, blank=True, null=True)
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', max_length=22, blank=True, null=True)
    acrylic_board_available = models.CharField(db_column='ACRYLIC_BOARD_AVAILABLE', max_length=5, blank=True, null=True)
    lift_location = models.CharField(db_column='LIFT_LOCATION', max_length=100, blank=True, null=True)
    total_poster_per_lift = models.IntegerField(db_column='TOTAL_POSTER_PER_LIFT', blank=True, null=True)
    lift_lit = models.CharField(db_column='LIFT_LIT', max_length=5, blank=True, null=True)
    lift_bubble_wrapping_allowed = models.CharField(db_column='LIFT_BUBBLE_WRAPPING_ALLOWED', max_length=5, blank=True, null=True)
    lift_advt_walls_count = models.IntegerField(db_column='LIFT_ADVT_WALLS_COUNT', blank=True, null=True)
    photograph_1 = models.CharField(db_column='PHOTOGRAPH_1', max_length=45, blank=True, null=True)
    photograph_2 = models.CharField(db_column='PHOTOGRAPH_2', max_length=45, blank=True, null=True)
    tower = models.ForeignKey('SocietyTower', related_name='lifts', db_column='TOWER_ID', blank=True, null=True, on_delete=models.CASCADE)
    inventory_status_lift = models.CharField(db_column='INVENTORY_STATUS_LIFT', max_length=20, blank=True, null=True)
    inventory_size = models.CharField(db_column='INVENTORY_SIZE', max_length=30, blank=True, null=True)

    def get_tower_name(self):
        try:
            return self.tower.tower_name
        except:
            return None

    class Meta:
        db_table = 'lift_details'

class NoticeBoardDetails(BaseModel):

    notice_board_tag = models.CharField(db_column='NOTICE_BOARD_TAG',max_length=20, blank=True, null=True )
    notice_board_type = models.CharField(db_column='NOTICE_BOARD_TYPE', max_length=50, blank=True, null=True)
    notice_board_type_other = models.CharField(db_column='NOTICE_BOARD_TYPE_OTHER', max_length=30, blank=True, null=True)
    notice_board_location = models.CharField(db_column='NOTICE_BOARD_LOCATION', max_length=100, blank=True, null=True)
    total_poster_per_notice_board = models.IntegerField(db_column='TOTAL_POSTER_PER_NOTICE_BOARD', blank=True, null=True)
    poster_location_notice_board = models.CharField(db_column='POSTER_LOCATION_NOTICE_BOARD', max_length=5, blank=True, null=True)
    notice_board_lit = models.CharField(db_column='NOTICE_BOARD_LIT', max_length=5, blank=True, null=True)
    tower = models.ForeignKey('SocietyTower', related_name='notice_boards', db_column='TOWER_ID', blank=True, null=True, on_delete=models.CASCADE)
    notice_board_size_length = models.FloatField(db_column='NOTICE_BOARD_SIZE_LENGTH', default=0.0, blank=True, null=True)
    notice_board_size_breadth = models.FloatField(db_column='NOTICE_BOARD_SIZE_BREADTH', default=0.0, blank=True, null=True)
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', max_length=22, blank=True, null=True)

    def get_tower_name(self):
        try:
            return self.tower.tower_name
        except:
            return None

    class Meta:
        db_table = 'notice_board_details'

class SocietyFlat(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    flat_tag = models.CharField(db_column='FLAT_TAG',max_length=20, blank=True, null=True)
    tower = models.ForeignKey('SocietyTower', related_name='flats', db_column='TOWER_ID', blank=True, null=True, on_delete=models.CASCADE)
    flat_type = models.CharField(db_column='FLAT_TYPE', max_length=20)
    flat_count = models.IntegerField(db_column='FLAT_COUNT', blank=True, null=True)

    class Meta:
        db_table = 'society_flat'
        unique_together = (('tower', 'flat_type'),)

class FlatType(BaseModel):

    id = models.AutoField(db_column='ID', primary_key=True)
    society = models.ForeignKey('SupplierTypeSociety', related_name='flatTypes', db_column='SUPPLIER_ID', blank=True, null=True, on_delete=models.CASCADE)
    flat_type = models.CharField(db_column='FLAT_TYPE', max_length=20)
    flat_count = models.IntegerField(db_column='FLAT_COUNT', blank=True, null=True)
    flat_type_count = models.IntegerField(db_column='FLAT_TYPE_COUNT', blank=True, null=True)
    size_carpet_area = models.FloatField(db_column='SIZE_CARPET_AREA', blank=True, null=True)
    size_builtup_area = models.FloatField(db_column='SIZE_BUILTUP_AREA', blank=True, null=True)
    flat_rent = models.IntegerField(db_column='FLAT_RENT', blank=True, null=True)
    average_rent_per_sqft = models.FloatField(db_column='AVERAGE_RENT_PER_SQFT', blank=True, null=True)
    content_type = models.ForeignKey(ContentType,default=None, null=True)
    object_id = models.CharField(max_length=supplier_id_max_length, null=True)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    objects = managers.GeneralManager()

    class Meta:
        db_table = 'flat_type'


class SwimmingPoolInfo(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)
    supplier = models.ForeignKey('SupplierTypeSociety', related_name='swimming_pools', db_column='SUPPLIER_ID', blank=True, null=True, on_delete=models.CASCADE)
    size_breadth = models.FloatField(db_column='SIZE_BREADTH', default=0.0, blank=True, null=True)
    size_length = models.FloatField(db_column='SIZE_LENGTH', default=0.0, blank=True, null=True)
    side_area = models.FloatField(db_column='SIDE_AREA', default=0.0, blank=True, null=True)
    side_rentals = models.CharField(db_column='SIDE_RENTALS', max_length=10, blank=True, null=True)
    timings_open = models.TimeField(db_column='TIMINGS_OPEN', blank=True, null=True)
    timings_close = models.TimeField(db_column='TIMINGS_CLOSE', blank=True, null=True)
    daily_price_society = models.FloatField(db_column='DAILY_PRICE_SOCIETY', default=0.0, blank=True, null=True)
    daily_price_business = models.FloatField(db_column='DAILY_PRICE_BUSINESS', default=0.0, blank=True, null=True)
    location = models.CharField(db_column='LOCATION', max_length=50, blank=True, null=True)
    notice_board_count_per_swimming_pool = models.IntegerField(db_column='NOTICE_BOARD_COUNT_PER_SWIMMING_POOL', blank=True, null=True)
    standee_location_count_per_swimming_pool = models.IntegerField(db_column='STANDEE_LOCATION_COUNT_PER_SWIMMING_POOL', blank=True, null=True)
    stall_count_per_swimming_pool = models.IntegerField(db_column='STALL_COUNT_PER_SWIMMING_POOL', blank=True, null=True)
    banner_count_per_swimming_pool = models.IntegerField(db_column='BANNER_COUNT_PER_SWIMMING_POOL', blank=True, null=True)
    sitting = models.IntegerField(db_column='SITTING', blank=True, null=True)
    inventory_status = models.CharField(db_column='INVENTORY_STATUS', max_length=15, blank=True, null=True)
    audio_video_display_available = models.CharField(db_column='AUDIO_VIDEO_DISPLAY_AVAILABLE', max_length=5, blank=True, null=True)
    electricity_charges_perhour = models.IntegerField(db_column='ELECTRICITY_CHARGES_PERHOUR', blank=True, null=True)
    changing_room_available = models.CharField(db_column='CHANGING_ROOM_AVAILABLE', max_length=5, blank=True, null=True)
    lit_unlit = models.CharField(db_column='LIT_UNLIT', max_length=5, blank=True, null=True)
    photograph_1 = models.CharField(db_column='PHOTOGRAPH_1', max_length=45, blank=True, null=True)
    photograph_2 = models.CharField(db_column='PHOTOGRAPH_2', max_length=45, blank=True, null=True)

    class Meta:

        db_table = 'swimming_pool_info'

class MailboxInfo(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    tower_id = models.CharField(db_column='TOWER_ID', max_length=20, blank=True, null=True)
    supplier = models.ForeignKey('SupplierTypeSociety', related_name='mail_boxes', db_column='SUPPLIER_ID', blank=True, null=True, on_delete=models.CASCADE)
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', max_length=22, blank=True, null=True)
    flier_distribution_frequency = models.CharField(db_column='FLIER_DISTRIBUTION_FREQUENCY', max_length=20, blank=True, null=True)
    mail_box_inventory_status = models.CharField(db_column='MAIL_BOX_INVENTORY_STATUS', max_length=20, blank=True, null=True)
    mailbox_count_per_tower = models.IntegerField(db_column='MAILBOX_COUNT_PER_TOWER', blank=True, null=True)
    mailbox_flyer_price_society = models.FloatField(db_column='MAILBOX_FLYER_PRICE_SOCIETY', default=0.0, blank=True, null=True)
    mailbox_flyer_price_business = models.FloatField(db_column='MAILBOX_FLYER_PRICE_BUSINESS', default=0.0, blank=True, null=True)
    photograph_1 = models.CharField(db_column='PHOTOGRAPH_1', max_length=45, blank=True, null=True)
    photograph_2 = models.CharField(db_column='PHOTOGRAPH_2', max_length=45, blank=True, null=True)

    class Meta:

        db_table = 'mailbox_info'

class SportsInfra(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    sports_infrastructure_id = models.CharField(db_column='SPORTS_INFRASTRUCTURE_ID', max_length=20, blank=True, null=True)
    supplier = models.ForeignKey('SupplierTypeSociety', related_name='sports', db_column='SUPPLIER_ID', blank=True, null=True, on_delete=models.CASCADE)
    stall_spaces_count = models.IntegerField(db_column='STALL_SPACES_COUNT', blank=True, null=True)
    banner_spaces_count = models.IntegerField(db_column='BANNER_SPACES_COUNT', blank=True, null=True)
    poster_spaces_count = models.IntegerField(db_column='POSTER_SPACES_COUNT', blank=True, null=True)
    standee_spaces_count = models.IntegerField(db_column='STANDEE_SPACES_COUNT', blank=True, null=True)
    sponsorship_amount_society = models.IntegerField(db_column='SPONSORSHIP_AMOUNT_SOCIETY', blank=True, null=True)
    sponsorship_amount_business = models.IntegerField(db_column='SPONSORSHIP_AMOUNT_BUSINESS)', blank=True, null=True)
    start_date = models.DateField(db_column='START_DATE', blank=True, null=True)
    end_date = models.DateField(db_column='END_DATE', blank=True, null=True)
    outside_participants_allowed = models.CharField(db_column='OUTSIDE_PARTICIPANTS_ALLOWED', max_length=5, blank=True, null=True)
    lit_unlit = models.CharField(db_column='LIT_UNLIT', max_length=5, blank=True, null=True)
    daily_infra_charges_society = models.IntegerField(db_column='DAILY_INFRA_CHARGES_SOCIETY', blank=True, null=True)
    daily_infra_charges_business = models.IntegerField(db_column='DAILY_INFRA_CHARGES_BUSINESS', blank=True, null=True)
    play_areas_count = models.IntegerField(db_column='PLAY_AREAS_COUNT', blank=True, null=True)
    play_area_size = models.IntegerField(db_column='PLAY_AREA_SIZE', blank=True, null=True)
    sports_type = models.CharField(db_column='SPORTS_TYPE', max_length=20, blank=True, null=True)

    class Meta:

        db_table = 'sports_infra'

class SocietyTower(models.Model):
    tower_id = models.AutoField(db_column='TOWER_ID', primary_key=True)
    tower_tag = models.CharField(db_column='TOWER_TAG', max_length=20, blank=True, null=True)
    supplier = models.ForeignKey('SupplierTypeSociety', related_name='towers', db_column='SUPPLIER_ID', blank=True, null=True, on_delete=models.CASCADE)
    tower_name = models.CharField(db_column='TOWER_NAME', max_length=20, blank=True, null=True)
    flat_count_per_tower = models.IntegerField(db_column='FLAT_COUNT_PER_TOWER', blank=True, null=True)
    floor_count_per_tower = models.IntegerField(db_column='FLOOR_COUNT_PER_TOWER', blank=True, null=True)
    notice_board_count_per_tower = models.IntegerField(db_column='NOTICE_BOARD_COUNT_PER_TOWER', default=0)
    standee_location_count_per_tower = models.IntegerField(db_column='STANDEE_LOCATION_COUNT_PER_TOWER', blank=True, null=True)
    mailbox_count_per_tower = models.IntegerField(db_column='MAILBOX_COUNT_PER_TOWER', blank=True, null=True)
    stall_count_per_tower = models.IntegerField(db_column='STALL_COUNT_PER_TOWER', blank=True, null=True)
    tower_location = models.CharField(db_column='TOWER_LOCATION', max_length=100, blank=True, null=True)
    tower_resident_count = models.IntegerField(db_column='TOWER_RESIDENT_COUNT', blank=True, null=True)
    lift_count = models.IntegerField(db_column='LIFT_COUNT', default=0)
    flat_type_count = models.IntegerField(db_column='FLAT_TYPE_COUNT', default=0)
    standee_count = models.IntegerField(db_column='STANDEE_COUNT', default=0)
    average_rent_per_sqft = models.IntegerField(db_column='AVERAGE_RENT_PER_SQFT', blank=True, null=True)
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.CharField(max_length=supplier_id_max_length, null=True)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    objects = managers.GeneralManager()

    def get_notice_board_list(self):
        return self.notice_boards.all()

    def get_lift_list(self):
        return self.lifts.all()

    def get_flat_list(self):
        return self.flats.all()

    def is_notice_board_available(self):
        notice_board = self.get_notice_board_list()
        if notice_board and len(notice_board) > 0 :
            return True
        return False

    def is_lift_available(self):
        lift = self.get_lift_list()
        if lift and len(lift) > 0:
            return True
        return False

    def is_flat_available(self):
        flat = self.get_flat_list()
        if flat and len(flat) > 0:
            return True
        return False

    class Meta:

        db_table = 'society_tower'
        unique_together = (('tower_tag','supplier'),)

class CommonAreaDetails(models.Model):
    common_area_id = models.CharField(db_column='COMMON_AREA_ID', primary_key=True, max_length=20)
    pole_count = models.IntegerField(db_column='POLE_COUNT', blank=True, null=True)
    street_furniture_count = models.IntegerField(db_column='STREET_FURNITURE_COUNT', blank=True, null=True)
    banner_count = models.IntegerField(db_column='BANNER_COUNT', blank=True, null=True)
    common_area_stalls_count = models.IntegerField(db_column='COMMON_AREA_STALLS_COUNT', blank=True, null=True)
    car_display = models.IntegerField(db_column='CAR_DISPLAY', blank=True, null=True)
    wall_count = models.IntegerField(db_column='WALL_COUNT', blank=True, null=True)
    major_event_count = models.IntegerField(db_column='MAJOR_EVENT_COUNT', blank=True, null=True)
    supplier = models.ForeignKey('SupplierTypeSociety', related_name='ca', db_column='SUPPLIER_ID', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:

        db_table = 'common_area_details'
