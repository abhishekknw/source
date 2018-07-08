# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.

# codes for supplier Types  Society -> RS   Corporate -> CP  Gym -> GY   salon -> SA

from __future__ import unicode_literals

import managers
from django.conf import settings
# from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.contenttypes import fields
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone

from v0.constants import supplier_id_max_length
from v0.ui.user.models import BaseUser
from v0.ui.base.models import BaseModel
from v0.ui.campaign.models import Campaign, CampaignTypeMapping
from v0.ui.organisation.models import Organisation
from v0.ui.account.models import ContactDetailsGeneric


AD_INVENTORY_CHOICES = (
    ('POSTER', 'Poster'),
    ('STANDEE', 'Standee'),
    ('STALL', 'Stall'),
    ('CAR DISPLAY', 'Car Display'),
    ('FLIER', 'Flier'),
    ('BANNER', 'Banner'),
    ('POSTER LIFT', 'Poster Lift'),
    ('GLASS_FACADE', 'GLASS_FACADE'),
    ('HOARDING', 'HOARDING'),
    ('DROPDOWN', 'DROPDOWN'),
    ('STANDEE', 'STANDEE'),
    ('PROMOTION_DESK', 'PROMOTION_DESK'),
    ('PILLAR', 'PILLAR'),
    ('TROLLEY', 'TROLLEY'),
    ('WALL_INVENTORY', 'WALL_INVENTORY'),
    ('FLOOR_INVENTORY', 'FLOOR_INVENTORY'),
    ('GATEWAY ARCH', 'GATEWAY ARCH')
)

RETAIL_SHOP_TYPE = (
    ('GROCERY_STORE', 'GROCERY_STORE'),
    ('ELECTRONIC_STORE', 'ELECTRONIC_STORE'),
    ('SANITARY_STORE', 'SANITARY_STORE'),
    ('STATIONARY_STORE', 'STATIONARY_STORE')
)

INVENTORY_ACTIVITY_TYPES = (
    ('RELEASE', 'RELEASE'),
    ('CLOSURE', 'CLOSURE'),
    ('AUDIT', 'AUDIT')
)


# class BaseInventory(BaseModel):
#     """
#     A BaseInventory model for all inventories. The fields here are common for all inventories.
#     """
#     status = models.CharField(max_length=10, default=v0_constants.inventory_status)
#
#     class Meta:
#         abstract = True


class CustomPermissions(BaseModel):
    """
    This is a model which stores extra permissions granted for a particular user
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID)
    extra_permission_code = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, null=True)

    class Meta:
        db_table = 'custom_permissions'


class BasicSupplierDetails(BaseModel):
    """
    This is an abstract base class for all the suppliers. As we know more common fields, add
    them here in order of relevance and run python manage.py makemigrations. all the models who
    inherit from this class will have those fields automatically.

    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID)
    supplier_id = models.CharField(max_length=20, primary_key=True)
    supplier_code = models.CharField(max_length=3, null=True)
    name = models.CharField(max_length=70, null=True, blank=True)
    address1 = models.CharField(max_length=250, null=True, blank=True)
    address2 = models.CharField(max_length=250, null=True, blank=True)
    area = models.CharField(max_length=255, null=True, blank=True)
    subarea = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=250, null=True, blank=True)
    state = models.CharField(max_length=250, null=True, blank=True)
    zipcode = models.IntegerField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True, default=0.0)
    longitude = models.FloatField(null=True, blank=True, default=0.0)
    locality_rating = models.CharField(max_length=50, null=True, blank=True)
    quality_rating = models.CharField(max_length=50, null=True, blank=True)
    machadalo_index = models.CharField(max_length=30, null=True, blank=True)
    bank_account_name = models.CharField(max_length=250, blank=True, null=True)
    bank_name = models.CharField(max_length=250, blank=True, null=True)
    ifsc_code = models.CharField(max_length=30, blank=True, null=True)
    account_number = models.CharField(max_length=250, blank=True, null=True)
    food_tasting_allowed = models.BooleanField(default=False)
    sales_allowed = models.BooleanField(default=False)
    objects = managers.GeneralManager()

    class Meta:
        abstract = True


class ImageMapping(BaseModel):
    id = models.AutoField(db_column='ID', primary_key=True)
    location_id = models.CharField(db_column='LOCATION_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    location_type = models.CharField(db_column='LOCATION_TYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    supplier = models.ForeignKey('SupplierTypeSociety', db_column='SUPPLIER_ID', related_name='images', blank=True, null=True, on_delete=models.CASCADE)
    image_url = models.CharField(db_column='IMAGE_URL', max_length=100)
    comments = models.CharField(db_column='COMMENTS', max_length=100, blank=True, null=True)
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.CharField(max_length=supplier_id_max_length, null=True)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    objects = managers.GeneralManager()

    class Meta:
        db_table = 'image_mapping'

class InventoryLocation(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field n
    location_id = models.CharField(db_column='LOCATION_ID', max_length=20)  # Field name made lowercase.
    location_type = models.CharField(db_column='LOCATION_TYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'inventory_location'

class AdInventoryLocationMapping(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', max_length=22)  # Field name made lowercase.
    adinventory_name = models.CharField(db_column='ADINVENTORY_NAME', max_length=10,
                                        choices=AD_INVENTORY_CHOICES, default='POSTER')  # Field name made lowercase.
    location = models.ForeignKey('InventoryLocation', db_column='INVENTORY_LOCATION_ID', related_name='inventory_locations', blank=True, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(AdInventoryLocationMapping, self).save()
        if self.adinventory_name == 'POSTER':
            ad_type = AdInventoryType.objects.filter(adinventory_name=self.adinventory_name)
        else:
            ad_type = AdInventoryType.objects.filter(adinventory_name=self.adinventory_name, adinventory_type=args[0]) #add type = stall/standee.type
        default_prices = PriceMappingDefault.objects.filter(adinventory_type__in=ad_type, supplier=args[1])

        for key in default_prices:
            pm = PriceMapping(adinventory_id = self, adinventory_type=key.adinventory_type,
                              society_price = key.society_price, business_price=key.business_price,
                              duration_type = key.duration_type, supplier=key.supplier)
            pm.save()

    class Meta:
        db_table = 'ad_inventory_location_mapping'

class AdInventoryType(BaseModel):
    id = models.AutoField(db_column='ID', primary_key=True)
    adinventory_name = models.CharField(db_column='ADINVENTORY_NAME', max_length=20,
                                        choices=AD_INVENTORY_CHOICES, default='POSTER')
    adinventory_type = models.CharField(db_column='ADINVENTORY_TYPE', max_length=20)  # Field name made lowercase.

    def __str__(self):
        return self.adinventory_name

    class Meta:
        db_table = 'ad_inventory_type'


class DurationType(BaseModel):
    id = models.AutoField(db_column='ID', primary_key=True)
    duration_name = models.CharField(db_column='DURATION_NAME', max_length=20)  # Field name made lowercase.
    days_count = models.CharField(db_column='DAYS_COUNT', max_length=10)  # Field name made lowercase.

    class Meta:
        db_table = 'duration_type'


class BannerInventory(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    supplier = models.ForeignKey('SupplierTypeSociety', db_column='SUPPLIER_ID', related_name='banners', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', max_length=22, blank=True)  # Field name made lowercase.
    type = models.CharField(db_column='BANNER_TYPE', max_length=20, blank=True)  # Field name made lowercase.
    banner_location = models.CharField(db_column='BANNER_DISPLAY_LOCATION', max_length=50, blank=True)  # Field name made lowercase.
    banner_size = models.CharField(db_column='BANNER_SIZE', max_length=10, blank=True)  # Field name made lowercase.
    inventory_status = models.CharField(db_column='INVENTORY_STATUS', blank=True,  max_length=15)  # Field name made lowercase.

    class Meta:

        db_table = 'banner_inventory'

class CommunityHallInfo(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    supplier = models.ForeignKey('SupplierTypeSociety', related_name='community_halls', db_column='SUPPLIER_ID', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    size_length = models.FloatField(db_column='SIZE_LENGTH', default=0.0, blank=True, null=True)  # Field name made lowercase.
    size_breadth = models.FloatField(db_column='SIZE_BREADTH', default=0.0, blank=True, null=True)  # Field name made lowercase.
    ceiling_height = models.FloatField(db_column='CEILING_HEIGHT', default=0.0, blank=True, null=True)  # Field name made lowercase.
    timings_open = models.TimeField(db_column='TIMINGS_OPEN', blank=True, null=True)  # Field name made lowercase.
    timings_close = models.TimeField(db_column='TIMINGS_CLOSE', blank=True, null=True)  # Field name made lowercase.
    rentals_current = models.FloatField(db_column='RENTALS_CURRENT', default=0.0, blank=True, null=True)  # Field name made lowercase.
    daily_price_society = models.FloatField(db_column='DAILY_PRICE_SOCIETY', default=0.0, blank=True, null=True)  # Field name made lowercase.
    daily_price_business = models.FloatField(db_column='DAILY_PRICE_BUSINESS', default=0.0, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='LOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    furniture_available = models.CharField(db_column='FURNITURE_AVAILABLE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    chair_count = models.IntegerField(db_column='CHAIR_COUNT', blank=True, null=True)  # Field name made lowercase.
    tables_count = models.IntegerField(db_column='TABLES_COUNT', blank=True, null=True)  # Field name made lowercase.
    air_conditioned = models.CharField(db_column='AIR_CONDITIONED', max_length=5, blank=True, null=True)  # Field name made lowercase.
    projector_available = models.CharField(db_column='PROJECTOR_AVAILABLE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    inventory_status = models.CharField(db_column='INVENTORY_STATUS', max_length=15, blank=True, null=True)  # Field name made lowercase.
    sitting = models.IntegerField(db_column='SITTING', blank=True, null=True)  # Field name made lowercase.
    audio_video_display_available = models.CharField(db_column='AUDIO_VIDEO_DISPLAY_AVAILABLE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    electricity_charges_perhour = models.FloatField(db_column='ELECTRICITY_CHARGES_PERHOUR',default=0.0, blank=True, null=True)  # Field name made lowercase.
    notice_board_count_per_community_hall = models.IntegerField(db_column='NOTICE_BOARD_COUNT_PER_COMMUNITY_HALL', blank=True, null=True)  # Field name made lowercase.
    standee_location_count_per_community_hall = models.IntegerField(db_column='STANDEE_LOCATION_COUNT_PER_COMMUNITY_HALL', blank=True, null=True)  # Field name made lowercase.
    stall_count_per_community_hall = models.IntegerField(db_column='STALL_COUNT_PER_COMMUNITY_HALL', blank=True, null=True)  # Field name made lowercase.
    banner_count_per_community_hall = models.IntegerField(db_column='BANNER_COUNT_PER_COMMUNITY_HALL', blank=True, null=True)  # Field name made lowercase.

    class Meta:

        db_table = 'community_hall_info'

class DoorToDoorInfo(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    supplier = models.ForeignKey('SupplierTypeSociety', related_name='door_to_doors', db_column='SUPPLIER_ID', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', max_length=22, blank=True, null=True)  # Field name made lowercase.
    flier_distribution_frequency_door = models.CharField(db_column='FLIER_DISTRIBUTION_FREQUENCY_DOOR', max_length=20, blank=True, null=True)  # Field name made lowercase.
    door_to_door_inventory_status = models.CharField(db_column='DOOR_TO_DOOR_INVENTORY_STATUS', max_length=15, blank=True, null=True)  # Field name made lowercase.
    door_to_door_price_society = models.FloatField(db_column='DOOR_TO_DOOR_PRICE_SOCIETY', default=0.0, blank=True, null=True)  # Field name made lowercase.
    door_to_door_price_business = models.FloatField(db_column='DOOR_TO_DOOR_PRICE_BUSINESS', default=0.0, blank=True, null=True)  # Field name made lowercase.
    master_door_to_door_flyer_price_society = models.FloatField(db_column='MASTER_DOOR_TO_DOOR_FLYER_PRICE_SOCIETY', default=0.0, blank=True, null=True)  # Field name made lowercase.
    master_door_to_door_flyer_price_business = models.FloatField(db_column='MASTER_DOOR_TO_DOOR_FLYER_PRICE_BUSINESS', default=0.0, blank=True, null=True)  # Field name made lowercase.
    leaflet_handover = models.CharField(db_column='LEAFLET_HANDOVER', max_length=50, blank=True, null=True)  # Field name made lowercase.
    activities = models.CharField(db_column='ACTIVITIES', max_length=255, blank=True, null=True)  # Field name made lowercase.
    banner_spaces_count = models.IntegerField(db_column='BANNER_SPACES_COUNT', blank=True, null=True)  # Field name made lowercase.

    class Meta:

        db_table = 'door_to_door_info'


class FlierThroughLobbyInfo(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    supplier = models.ForeignKey('SupplierTypeSociety', related_name='flier_lobby', db_column='SUPPLIER_ID', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', max_length=22, blank=True, null=True)  # Field name made lowercase.
    flier_distribution_frequency_lobby = models.CharField(db_column='FLIER_DISTRIBUTION_FREQUENCY_LOBBY', max_length=20, blank=True, null=True)  # Field name made lowercase.
    flier_lobby_inventory_status = models.CharField(db_column='FLIER_LOBBY_INVENTORY_STATUS', max_length=15, blank=True, null=True)  # Field name made lowercase.
    flier_lobby_price_society = models.FloatField(db_column='FLIER_LOBBY_PRICE_SOCIETY', default=0.0, blank=True, null=True)  # Field name made lowercase.
    flier_lobby_price_business = models.FloatField(db_column='FLIER_LOBBY_PRICE_BUSINESS', default=0.0, blank=True, null=True)  # Field name made lowercase.
    master_flier_lobby_price_society = models.FloatField(db_column='MASTER_FLIER_LOBBY_PRICE_SOCIETY', default=0.0, blank=True, null=True)  # Field name made lowercase.
    master_flier_lobby_price_business = models.FloatField(db_column='MASTER_FLIER_LOBBY_PRICE_BUSINESS', default=0.0, blank=True, null=True)  # Field name made lowercase.

    class Meta:

        db_table = 'flier_through_lobby_info'


class LiftDetails(models.Model):

    lift_tag = models.CharField(db_column='LIFT_TAG', max_length=20, blank=True, null=True)  # Field name made lowercase.
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', max_length=22, blank=True, null=True)  # Field name made lowercase.
    acrylic_board_available = models.CharField(db_column='ACRYLIC_BOARD_AVAILABLE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    lift_location = models.CharField(db_column='LIFT_LOCATION', max_length=100, blank=True, null=True)  # Field name made lowercase.
    total_poster_per_lift = models.IntegerField(db_column='TOTAL_POSTER_PER_LIFT', blank=True, null=True)  # Field name made lowercase.
    lift_lit = models.CharField(db_column='LIFT_LIT', max_length=5, blank=True, null=True)  # Field name made lowercase.
    lift_bubble_wrapping_allowed = models.CharField(db_column='LIFT_BUBBLE_WRAPPING_ALLOWED', max_length=5, blank=True, null=True)  # Field name made lowercase.
    lift_advt_walls_count = models.IntegerField(db_column='LIFT_ADVT_WALLS_COUNT', blank=True, null=True)  # Field name made lowercase.
    photograph_1 = models.CharField(db_column='PHOTOGRAPH_1', max_length=45, blank=True, null=True)  # Field name made lowercase.
    photograph_2 = models.CharField(db_column='PHOTOGRAPH_2', max_length=45, blank=True, null=True)  # Field name made lowercase.
    tower = models.ForeignKey('SocietyTower', related_name='lifts', db_column='TOWER_ID', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    inventory_status_lift = models.CharField(db_column='INVENTORY_STATUS_LIFT', max_length=20, blank=True, null=True)  # Field name made lowercase.
    inventory_size = models.CharField(db_column='INVENTORY_SIZE', max_length=30, blank=True, null=True)  # Field name made lowercase.

    def get_tower_name(self):
        try:
            return self.tower.tower_name
        except:
            return None

    class Meta:
        db_table = 'lift_details'


class NoticeBoardDetails(BaseModel):

    notice_board_tag = models.CharField(db_column='NOTICE_BOARD_TAG',max_length=20, blank=True, null=True )  # Field name made lowercase.
    notice_board_type = models.CharField(db_column='NOTICE_BOARD_TYPE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    notice_board_type_other = models.CharField(db_column='NOTICE_BOARD_TYPE_OTHER', max_length=30, blank=True, null=True)  # Field name made lowercase.
    notice_board_location = models.CharField(db_column='NOTICE_BOARD_LOCATION', max_length=100, blank=True, null=True)  # Field name made lowercase.
    total_poster_per_notice_board = models.IntegerField(db_column='TOTAL_POSTER_PER_NOTICE_BOARD', blank=True, null=True)  # Field name made lowercase.
    poster_location_notice_board = models.CharField(db_column='POSTER_LOCATION_NOTICE_BOARD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    notice_board_lit = models.CharField(db_column='NOTICE_BOARD_LIT', max_length=5, blank=True, null=True)  # Field name made lowercase.
    tower = models.ForeignKey('SocietyTower', related_name='notice_boards', db_column='TOWER_ID', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    notice_board_size_length = models.FloatField(db_column='NOTICE_BOARD_SIZE_LENGTH', default=0.0, blank=True, null=True)  # Field name made lowercase.
    notice_board_size_breadth = models.FloatField(db_column='NOTICE_BOARD_SIZE_BREADTH', default=0.0, blank=True, null=True)  # Field name made lowercase.
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', max_length=22, blank=True, null=True)  # Field name made lowercase.

    def get_tower_name(self):
        try:
            return self.tower.tower_name
        except:
            return None

    class Meta:
        db_table = 'notice_board_details'


class PosterInventory(BaseModel):

    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', primary_key=True, max_length=25)  # Field name made lowercase.
    tower_name = models.CharField(db_column='TOWER_NAME', max_length=20, blank=True, null=True)  # Field name made lowercase.
    poster_location = models.CharField(db_column='POSTER_LOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    poster_area = models.CharField(db_column='POSTER_AREA', max_length=10, blank=True, null=True)  # Field name made lowercase.
    inventory_status = models.CharField(db_column='INVENTORY_STATUS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    poster_count_per_notice_board = models.IntegerField(db_column='POSTER_COUNT_PER_NOTICE_BOARD', blank=True, null=True)  # Field name made lowercase.
    inventory_type_id = models.CharField(db_column='INVENTORY_TYPE_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    supplier = models.ForeignKey('SupplierTypeSociety', db_column='SUPPLIER_ID', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.CharField(max_length=supplier_id_max_length, null=True)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    objects = managers.GeneralManager()
    tower = models.ForeignKey('SocietyTower', null=True, blank=True)

    class Meta:
        db_table = 'poster_inventory'


class SocietyFlat(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    flat_tag = models.CharField(db_column='FLAT_TAG',max_length=20, blank=True, null=True)  # Field name made lowercase.
    tower = models.ForeignKey('SocietyTower', related_name='flats', db_column='TOWER_ID', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    flat_type = models.CharField(db_column='FLAT_TYPE', max_length=20)  # Field name made lowercase.
    flat_count = models.IntegerField(db_column='FLAT_COUNT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'society_flat'
        unique_together = (('tower', 'flat_type'),)


class FlatType(BaseModel):

    id = models.AutoField(db_column='ID', primary_key=True)
    society = models.ForeignKey('SupplierTypeSociety', related_name='flatTypes', db_column='SUPPLIER_ID', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    flat_type = models.CharField(db_column='FLAT_TYPE', max_length=20)  # Field name made lowercase.
    flat_count = models.IntegerField(db_column='FLAT_COUNT', blank=True, null=True)  # Field name made lowercase.
    flat_type_count = models.IntegerField(db_column='FLAT_TYPE_COUNT', blank=True, null=True)  # Field name made lowercase.
    size_carpet_area = models.FloatField(db_column='SIZE_CARPET_AREA', blank=True, null=True)  # Field name made lowercase.
    size_builtup_area = models.FloatField(db_column='SIZE_BUILTUP_AREA', blank=True, null=True)  # Field name made lowercase.
    flat_rent = models.IntegerField(db_column='FLAT_RENT', blank=True, null=True)  # Field name made lowercase.
    average_rent_per_sqft = models.FloatField(db_column='AVERAGE_RENT_PER_SQFT', blank=True, null=True)  # Field name made lowercase.
    content_type = models.ForeignKey(ContentType,default=None, null=True)
    object_id = models.CharField(max_length=supplier_id_max_length, null=True)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    objects = managers.GeneralManager()

    class Meta:
        db_table = 'flat_type'


class StandeeInventory(BaseModel):

    id = models.AutoField(db_column='ID', primary_key=True)
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', max_length=22, blank=True, null=True)  # Field name made lowercase.
    inventory_type_id = models.CharField(db_column='INVENTORY_TYPE_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    inventory_status = models.CharField(db_column='INVENTORY_STATUS', max_length=15, blank=True, null=True)  # Field name made lowercase.
    standee_location = models.CharField(db_column='STANDEE_LOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='STANDEE_TYPE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    standee_size = models.CharField(db_column='STANDEE_SIZE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    standee_sides = models.CharField(db_column='STANDEE_SIDES', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tower = models.ForeignKey('SocietyTower', db_column='TOWER_ID', related_name='standees', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.CharField(max_length=supplier_id_max_length, null=True)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    objects = managers.GeneralManager()

    def get_tower_name1(self):
        try:
            return self.tower.tower_name
        except:
            return None

    class Meta:
        db_table = 'standee_inventory'


class SwimmingPoolInfo(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    supplier = models.ForeignKey('SupplierTypeSociety', related_name='swimming_pools', db_column='SUPPLIER_ID', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    size_breadth = models.FloatField(db_column='SIZE_BREADTH', default=0.0, blank=True, null=True)  # Field name made lowercase.
    size_length = models.FloatField(db_column='SIZE_LENGTH', default=0.0, blank=True, null=True)  # Field name made lowercase.
    side_area = models.FloatField(db_column='SIDE_AREA', default=0.0, blank=True, null=True)  # Field name made lowercase.
    side_rentals = models.CharField(db_column='SIDE_RENTALS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    timings_open = models.TimeField(db_column='TIMINGS_OPEN', blank=True, null=True)  # Field name made lowercase.
    timings_close = models.TimeField(db_column='TIMINGS_CLOSE', blank=True, null=True)  # Field name made lowercase.
    daily_price_society = models.FloatField(db_column='DAILY_PRICE_SOCIETY', default=0.0, blank=True, null=True)  # Field name made lowercase.
    daily_price_business = models.FloatField(db_column='DAILY_PRICE_BUSINESS', default=0.0, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='LOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    notice_board_count_per_swimming_pool = models.IntegerField(db_column='NOTICE_BOARD_COUNT_PER_SWIMMING_POOL', blank=True, null=True)  # Field name made lowercase.
    standee_location_count_per_swimming_pool = models.IntegerField(db_column='STANDEE_LOCATION_COUNT_PER_SWIMMING_POOL', blank=True, null=True)  # Field name made lowercase.
    stall_count_per_swimming_pool = models.IntegerField(db_column='STALL_COUNT_PER_SWIMMING_POOL', blank=True, null=True)  # Field name made lowercase.
    banner_count_per_swimming_pool = models.IntegerField(db_column='BANNER_COUNT_PER_SWIMMING_POOL', blank=True, null=True)  # Field name made lowercase.
    sitting = models.IntegerField(db_column='SITTING', blank=True, null=True)  # Field name made lowercase.
    inventory_status = models.CharField(db_column='INVENTORY_STATUS', max_length=15, blank=True, null=True)  # Field name made lowercase.
    audio_video_display_available = models.CharField(db_column='AUDIO_VIDEO_DISPLAY_AVAILABLE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    electricity_charges_perhour = models.IntegerField(db_column='ELECTRICITY_CHARGES_PERHOUR', blank=True, null=True)  # Field name made lowercase.
    changing_room_available = models.CharField(db_column='CHANGING_ROOM_AVAILABLE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    lit_unlit = models.CharField(db_column='LIT_UNLIT', max_length=5, blank=True, null=True)  # Field name made lowercase.
    photograph_1 = models.CharField(db_column='PHOTOGRAPH_1', max_length=45, blank=True, null=True)  # Field name made lowercase.
    photograph_2 = models.CharField(db_column='PHOTOGRAPH_2', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:

        db_table = 'swimming_pool_info'

class WallInventory(BaseModel):
    inventory_type_id = models.CharField(db_column='INVENTORY_TYPE_ID', max_length=20, blank=True)  # Field name made lowercase.
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', max_length=22)  # Field name made lowercase.
    wall_size = models.CharField(db_column='WALL_SIZE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    wall_frame_size = models.CharField(db_column='WALL_FRAME_SIZE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    wall_area = models.CharField(db_column='WALL_AREA', max_length=10, blank=True, null=True)  # Field name made lowercase.
    wall_type = models.CharField(db_column='WALL_TYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    wall_internal_external = models.CharField(db_column='WALL_INTERNAL_EXTERNAL', max_length=10, blank=True, null=True)  # Field name made lowercase.
    wall_sides = models.CharField(db_column='WALL_SIDES', max_length=10, blank=True, null=True)  # Field name made lowercase.
    wall_monthly_price_society = models.FloatField(db_column='WALL_MONTHLY_PRICE_SOCIETY', default=0.0, blank=True, null=True)  # Field name made lowercase.
    wall_quarterly_price_society = models.FloatField(db_column='WALL_QUARTERLY_PRICE_SOCIETY', default=0.0, blank=True, null=True)  # Field name made lowercase.
    wall_monthly_price_business = models.FloatField(db_column='WALL_MONTHLY_PRICE_BUSINESS', default=0.0, blank=True, null=True)  # Field name made lowercase.
    wall_quarterly_price_business = models.FloatField(db_column='WALL_QUARTERLY_PRICE_BUSINESS', default=0.0, blank=True, null=True)  # Field name made lowercase.
    wall_location = models.CharField(db_column='WALL_LOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    wall_paint_allowed = models.CharField(db_column='WALL_PAINT_ALLOWED', max_length=5, blank=True, null=True)  # Field name made lowercase.
    wall_frame_status = models.CharField(db_column='WALL_FRAME_STATUS', max_length=5, blank=True, null=True)  # Field name made lowercase.
    wall_inventory_status = models.CharField(db_column='WALL_INVENTORY_STATUS', max_length=15, blank=True, null=True)  # Field name made lowercase.
    supplier = models.ForeignKey('SupplierTypeSociety', related_name='walls', db_column='SUPPLIER_ID', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.CharField(max_length=supplier_id_max_length, null=True)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    objects = managers.GeneralManager()

    class Meta:

        db_table = 'wall_inventory'

class UserInquiry(models.Model):
    inquiry_id = models.AutoField(db_column='INQUIRY_ID', primary_key=True)  # Field name made lowercase.
    company_name = models.CharField(db_column='COMPANY_NAME', max_length=40)  # Field name made lowercase.
    contact_person_name = models.CharField(db_column='CONTACT_PERSON_NAME', max_length=40, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=40, blank=True, null=True)  # Field name made lowercase.
    phone = models.IntegerField(db_column='PHONE', blank=True, null=True)  # Field name made lowercase.
    inquiry_details = models.TextField(db_column='INQUIRY_DETAILS')  # Field name made lowercase.

    class Meta:

        db_table = 'user_inquiry'

class CommonAreaDetails(models.Model):
    common_area_id = models.CharField(db_column='COMMON_AREA_ID', primary_key=True, max_length=20)  # Field name made lowercase.
    pole_count = models.IntegerField(db_column='POLE_COUNT', blank=True, null=True)  # Field name made lowercase.
    street_furniture_count = models.IntegerField(db_column='STREET_FURNITURE_COUNT', blank=True, null=True)  # Field name made lowercase.
    banner_count = models.IntegerField(db_column='BANNER_COUNT', blank=True, null=True)  # Field name made lowercase.
    common_area_stalls_count = models.IntegerField(db_column='COMMON_AREA_STALLS_COUNT', blank=True, null=True)  # Field name made lowercase.
    car_display = models.IntegerField(db_column='CAR_DISPLAY', blank=True, null=True)  # Field name made lowercase.
    wall_count = models.IntegerField(db_column='WALL_COUNT', blank=True, null=True)  # Field name made lowercase.
    major_event_count = models.IntegerField(db_column='MAJOR_EVENT_COUNT', blank=True, null=True)  # Field name made lowercase.
    supplier = models.ForeignKey('SupplierTypeSociety', related_name='ca', db_column='SUPPLIER_ID', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.

    class Meta:

        db_table = 'common_area_details'


class SocietyMajorEvents(BaseModel):
    id = models.AutoField(db_column='ID', primary_key=True)
    supplier = models.ForeignKey('SupplierTypeSociety', related_name='society_events', db_column='SUPPLIER_ID', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    Ganpati = models.BooleanField(db_column='Ganpati', default=False)
    Diwali = models.BooleanField(db_column='Diwali', default=False)
    Lohri = models.BooleanField(db_column='Lohri', default=False)
    Navratri = models.BooleanField(db_column='Navratri', default=False)
    Holi = models.BooleanField(db_column='Holi', default=False)
    Janmashtami = models.BooleanField(db_column='Janmashtami', default=False)
    IndependenceDay = models.BooleanField(db_column='IndependenceDay', default=False)
    RepublicDay = models.BooleanField(db_column='RepublicDay', default=False)
    SportsDay = models.BooleanField(db_column='SportsDay', default=False)
    AnnualDay = models.BooleanField(db_column='AnnualDay', default=False)
    Christmas = models.BooleanField(db_column='Christmas', default=False)
    NewYear = models.BooleanField(db_column='NewYear', default=False)
    past_major_events = models.IntegerField(db_column='PAST_MAJOR_EVENTS', blank=True, null=True)


class Events(models.Model):
    event_id = models.AutoField(db_column='EVENT_ID', primary_key=True)  # Field name made lowercase.
    supplier = models.ForeignKey('SupplierTypeSociety', related_name='events', db_column='SUPPLIER_ID', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    event_name = models.CharField(db_column='EVENT_NAME', max_length=20, blank=True, null=True)  # Field name made lowercase.
    event_location = models.CharField(db_column='EVENT_LOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    past_gathering_per_event = models.IntegerField(db_column='PAST_GATHERING_PER_EVENT', blank=True, null=True)  # Field name made lowercase.
    start_day = models.CharField(db_column='START_DAY', max_length=30, blank=True, null=True)  # Field name made lowercase.
    end_day = models.CharField(db_column='END_DAY', max_length=30, blank=True, null=True)
    important_day = models.CharField(db_column='IMPORTANT_DAY', max_length=30, blank=True, null=True)
    activities = models.CharField(db_column='ACTIVITIES', max_length=50, blank=True, null=True)  # Field name made lowercase.
    stall_spaces_count = models.IntegerField(db_column='STALL_SPACES_COUNT', blank=True, null=True)  # Field name made lowercase.
    banner_spaces_count = models.IntegerField(db_column='BANNER_SPACES_COUNT', blank=True, null=True)  # Field name made lowercase.
    poster_spaces_count = models.IntegerField(db_column='POSTER_SPACES_COUNT', blank=True, null=True)  # Field name made lowercase.
    standee_spaces_count = models.IntegerField(db_column='STANDEE_SPACES_COUNT', blank=True, null=True)  # Field name made lowercase.
    event_status = models.CharField(db_column='EVENT_STATUS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.CharField(max_length=supplier_id_max_length, null=True)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    objects = managers.GeneralManager()

    class Meta:

        db_table = 'events'

# Check whether it is being used or not
class InventoryInfo(models.Model):
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

        db_table = 'inventory_info'

class MailboxInfo(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    tower_id = models.CharField(db_column='TOWER_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    supplier = models.ForeignKey('SupplierTypeSociety', related_name='mail_boxes', db_column='SUPPLIER_ID', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', max_length=22, blank=True, null=True)  # Field name made lowercase.
    flier_distribution_frequency = models.CharField(db_column='FLIER_DISTRIBUTION_FREQUENCY', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mail_box_inventory_status = models.CharField(db_column='MAIL_BOX_INVENTORY_STATUS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mailbox_count_per_tower = models.IntegerField(db_column='MAILBOX_COUNT_PER_TOWER', blank=True, null=True)  # Field name made lowercase.
    mailbox_flyer_price_society = models.FloatField(db_column='MAILBOX_FLYER_PRICE_SOCIETY', default=0.0, blank=True, null=True)  # Field name made lowercase.
    mailbox_flyer_price_business = models.FloatField(db_column='MAILBOX_FLYER_PRICE_BUSINESS', default=0.0, blank=True, null=True)  # Field name made lowercase.
    photograph_1 = models.CharField(db_column='PHOTOGRAPH_1', max_length=45, blank=True, null=True)  # Field name made lowercase.
    photograph_2 = models.CharField(db_column='PHOTOGRAPH_2', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:

        db_table = 'mailbox_info'

class OperationsInfo(models.Model):
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

        db_table = 'operations_info'

class PoleInventory(BaseModel):
    inventory_type_id = models.CharField(db_column='INVENTORY_TYPE_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', max_length=22, blank=True, null=True)  # Field name made lowercase.
    supplier = models.ForeignKey('SupplierTypeSociety', related_name='poles', db_column='SUPPLIER_ID', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    pole_hoarding_size = models.CharField(db_column='POLE_HOARDING_SIZE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    pole_area = models.CharField(db_column='POLE_AREA', max_length=10, blank=True, null=True)  # Field name made lowercase.
    pole_hoarding_type = models.CharField(db_column='POLE_HOARDING_TYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    pole_lit_status = models.CharField(db_column='POLE_LIT_STATUS',  max_length=5, blank=True)  # Field name made lowercase. This field type is a guess.
    pole_sides = models.CharField(db_column='POLE_SIDES', max_length=10, blank=True, null=True)  # Field name made lowercase.
    pole_monthly_price_society = models.FloatField(db_column='POLE_MONTHLY_PRICE_SOCIETY', null=True)  # Field name made lowercase.
    pole_quarterly_price_society = models.FloatField(db_column='POLE_QUARTERLY_PRICE_SOCIETY', null=True)  # Field name made lowercase.
    pole_monthly_price_business = models.FloatField(db_column='POLE_MONTHLY_PRICE_BUSINESS', null=True)  # Field name made lowercase.
    pole_quarterly_price_business = models.FloatField(db_column='POLE_QUARTERLY_PRICE_BUSINESS', null=True)  # Field name made lowercase.
    pole_location = models.CharField(db_column='POLE_LOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    pole_inventory_status = models.CharField(db_column='POLE_INVENTORY_STATUS', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:

        db_table = 'pole_inventory'

class PosterInventoryMapping(models.Model):
    inventory_mapping_id = models.AutoField(db_column='INVENTORY_MAPPING_ID', primary_key=True)  # Field name made lowercase.
    inventory_type_id = models.CharField(db_column='INVENTORY_TYPE_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    poster_adinventory_id = models.CharField(db_column='POSTER_ADINVENTORY_ID', max_length=22, blank=True, null=True)  # Field name made lowercase.
    standee_adinventory_id = models.CharField(db_column='STANDEE_ADINVENTORY_ID', max_length=22, blank=True, null=True)  # Field name made lowercase.
    banner_adinventory_id = models.CharField(db_column='BANNER_ADINVENTORY_ID', max_length=22, blank=True, null=True)  # Field name made lowercase.
    stall_adinventory_id = models.CharField(db_column='STALL_ADINVENTORY_ID', max_length=22, blank=True, null=True)  # Field name made lowercase.

    class Meta:


        db_table = 'poster_inventory_mapping'


class RatioDetails(models.Model):
    supplier_id = models.CharField(db_column='SUPPLIER_ID', max_length=20)  # Field name made lowercase.
    machadalo_index = models.CharField(db_column='MACHADALO_INDEX', max_length=30)  # Field name made lowercase.
    age_proportions = models.CharField(db_column='AGE_PROPORTIONS', max_length=15, blank=True, null=True)  # Field name made lowercase.
    flat_avg_rental_persqft = models.CharField(db_column='FLAT_AVG_RENTAL_PERSQFT', max_length=10, blank=True, null=True)  # Field name made lowercase.
    flat_avg_size = models.CharField(db_column='FLAT_AVG_SIZE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    flat_sale_cost_persqft = models.CharField(db_column='FLAT_SALE_COST_PERSQFT', max_length=5, blank=True, null=True)  # Field name made lowercase.
    wall_count = models.IntegerField(db_column='WALL_COUNT', blank=True, null=True)  # Field name made lowercase.
    major_event_count = models.IntegerField(db_column='MAJOR_EVENT_COUNT', blank=True, null=True)  # Field name made lowercase.

    class Meta:

        db_table = 'ratio_details'
        unique_together = (('supplier_id', 'machadalo_index'),)


class Signup(models.Model):
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

        db_table = 'signup'


class StallInventory(BaseModel):
    id = models.AutoField(db_column='ID', primary_key=True)
    supplier = models.ForeignKey('SupplierTypeSociety', db_column='SUPPLIER_ID', related_name='stalls', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', max_length=22)  # Field name made lowercase.
    stall_small = models.BooleanField(db_column='STALL_SMALL', default=False)
    stall_canopy = models.BooleanField(db_column='STALL_CANOPY', default=False)
    stall_medium = models.BooleanField(db_column='STALL_MEDIUM', default=False)
    car_standard = models.BooleanField(db_column='CAR_STANDARD', default=False)
    car_premium = models.BooleanField(db_column='CAR_PREMIUM', default=False)
    stall_morning = models.BooleanField(db_column='STALL_MORNING', default=False)
    stall_evening = models.BooleanField(db_column='STALL_EVENING', default=False)
    stall_time_both = models.BooleanField(db_column='STALL_TIME_BOTH', default=False)
    stall_weekdays = models.BooleanField(db_column='STALL_WEEKDAYS', default=False)
    stall_location = models.CharField(db_column='STALL_LOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    electricity_available = models.BooleanField(db_column='ELECTRICITY_AVAILABLE_STALLS', default=False)  # Field name made lowercase.
    electricity_charges_daily = models.FloatField(db_column='ELECTRICITY_CHARGES_DAILY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sound_system_allowed = models.BooleanField(db_column='SOUND_SYSTEM_ALLOWED', default=False)  # Field name made lowercase.
    furniture_available = models.BooleanField(db_column='STALL_FURNITURE_AVAILABLE', default=False)  # Field name made lowercase.
    furniture_details = models.CharField(db_column='STALL_FURNITURE_DETAILS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    stall_size = models.CharField(db_column='STALL_SIZE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    stall_timing = models.CharField(db_column='STALL_TIMINGS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.CharField(max_length=supplier_id_max_length, null=True)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    objects = managers.GeneralManager()

    class Meta:

        db_table = 'stall_inventory'


class FlyerInventory(BaseModel):
    id = models.AutoField(db_column='ID', primary_key=True)
    supplier = models.ForeignKey('SupplierTypeSociety', db_column='SUPPLIER_ID', related_name='flyers', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', max_length=22,unique=True)  # Field name made lowercase.
    flat_count = models.IntegerField(db_column='FLAT_COUNT', blank=True, null=True)
    mailbox_allowed = models.BooleanField(db_column='MAILBOX_ALLOWED', default=False)
    d2d_allowed = models.BooleanField(db_column='D2D_ALLOWED', default=False)
    lobbytolobby_allowed = models.BooleanField(db_column='LOBBYTOLOBBY_ALLOWED', default=False)
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.CharField(max_length=supplier_id_max_length, null=True)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    objects = managers.GeneralManager()

    class Meta:

        db_table = 'flyer_inventory'

class StreetFurniture(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', max_length=22, blank=True, null=True)  # Field name made lowercase.
    supplier = models.ForeignKey('SupplierTypeSociety', related_name='street_furniture', db_column='SUPPLIER_ID', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    no_of_furniture = models.IntegerField(db_column='NO_OF_FURNITURE', blank=True, null=True)  # Field name made lowercase.
    type_of_furniture = models.CharField(db_column='TYPE_OF_FURNITURE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    photograph_1 = models.CharField(db_column='PHOTOGRAPH_1', max_length=45, blank=True, null=True)  # Field name made lowercase.
    photograph_2 = models.CharField(db_column='PHOTOGRAPH_2', max_length=45, blank=True, null=True)  # Field name made lowercase.
    comment_1 = models.TextField(db_column='COMMENT_1', blank=True, null=True)  # Field name made lowercase.
    comment_2 = models.TextField(db_column='COMMENT_2', blank=True, null=True)  # Field name made lowercase.
    furniture_status = models.CharField(db_column='FURNITURE_STATUS', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:

        db_table = 'street_furniture'

#Check whether this model is being used or not
class SupplierInfo(models.Model):
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

        db_table = 'supplier_info'


class SportsInfra(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sports_infrastructure_id = models.CharField(db_column='SPORTS_INFRASTRUCTURE_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    supplier = models.ForeignKey('SupplierTypeSociety', related_name='sports', db_column='SUPPLIER_ID', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    stall_spaces_count = models.IntegerField(db_column='STALL_SPACES_COUNT', blank=True, null=True)  # Field name made lowercase.
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


class SupplierTypeCorporate(BasicSupplierDetails):

    corporate_type = models.CharField(max_length=25,blank=True, null= True)
    industry_segment = models.CharField(max_length=30, blank=True, null=True)
    possession_year = models.CharField(max_length=5, blank=True, null=True)
    building_count = models.IntegerField(blank=True, null=True)
    floorperbuilding_count = models.IntegerField(blank=True, null=True)
    totalcompanies_count = models.IntegerField(blank=True, null=True)
    totalemployees_count = models.IntegerField(blank=True, null=True)
    isrealestateallowed = models.BooleanField(default=False)
    total_area = models.FloatField(blank=True, null=True, default=0.0)
    quantity_rating = models.CharField(max_length=50, blank=True, null=True)
    luxurycars_count = models.IntegerField(blank=True, null=True)
    standardcars_count = models.IntegerField(blank=True, null=True)
    totallift_count = models.IntegerField(blank=True, null=True)
    parkingspaces_count = models.IntegerField(blank=True, null=True)
    entryexit_count = models.IntegerField(blank=True, null=True)
    openspaces_count = models.IntegerField(blank=True, null=True)
    constructionspaces_count = models.IntegerField(blank=True, null=True)
    constructedspace = models.FloatField(blank=True, null=True, default=0.0)
    parkingspace = models.FloatField(blank=True, null=True, default=0.0)
    openspace = models.FloatField(blank=True, null=True, default=0.0)
    averagerent = models.FloatField(blank=True, null=True, default=0.0)
    fields.GenericRelation(ContactDetailsGeneric)
    is_common_cafeteria_available = models.BooleanField(default=False)

    def get_buildings(self):
        return self.corporatebuilding.all()

    def get_corporate_companies(self):
        return self.corporatecompany.all()

    class Meta:
        db_table = 'supplier_corporate'

class CorporateParkCompanyList(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.CharField(db_column='COMPANY_NAME',max_length=50, blank=True, null=True)
    supplier_id = models.ForeignKey('SupplierTypeCorporate', db_column='CORPORATEPARK_ID', related_name='corporatecompany', blank=True, null=True, on_delete=models.CASCADE)

    def get_company_details(self):
        return self.companydetails.all()

    class Meta:
      db_table = 'corporateparkcompanylist'


class SupplierTypeSalon(BasicSupplierDetails):

    salon_type = models.CharField(db_column='SALON_TYPE', max_length=30, blank=True, null=True)
    category = models.CharField(db_column='CATEGORY', max_length=30, blank=True, null=True)
    salon_type_chain = models.CharField(db_column='SALON_TYPE_CHAIN', max_length=30, blank=True, null=True)
    footfall_day = models.IntegerField(db_column='FOOTFALL_DAY', blank=True, null=True)
    footfall_week = models.IntegerField(db_column='FOOTFALL_WEEK', blank=True, null=True)
    footfall_weekend = models.IntegerField(db_column='FOOTFALL_WEEKEND', blank=True, null=True)
    isspaavailable = models.BooleanField(db_column='ISSPAAVAILABLE', default=False)
    advertising_media = models.CharField(db_column='AD_MEDIA', max_length=30, blank=True, null=True)
    shop_size = models.CharField(db_column='SHOP_SIZE', max_length=30, blank=True, null=True)
    floor_size = models.CharField(db_column='FLOOR_SIZE', max_length=30, blank=True, null=True)
    standee_price_week = models.IntegerField(db_column='ST_PRICE_WEEK', blank=True, null=True)
    standee_price_weekend = models.IntegerField(db_column='ST_PRICE_WEEKEND', blank=True, null=True)
    standee_places = models.IntegerField(db_column='ST_PLACES', blank=True, null=True)
    standee_location = models.IntegerField(db_column='ST_LOCATION', blank=True, null=True)
    banner_price_week = models.IntegerField(db_column='BA_PRICE_WEEK', blank=True, null=True)
    banner_price_weekend = models.IntegerField(db_column='BA_PRICE_WEEKEND', blank=True, null=True)
    banner_places = models.IntegerField(db_column='BA_PLACES', blank=True, null=True)
    banner_location = models.IntegerField(db_column='BA_LOCATION', blank=True, null=True)
    flyer_price_week = models.IntegerField(db_column='FL_PRICE_WEEK', blank=True, null=True)
    flyer_distribution = models.IntegerField(db_column='FL_DISTRIBUTION', blank=True, null=True)
    poster_price_week = models.IntegerField(db_column='PO_PRICE_WEEK', blank=True, null=True)
    poster_price_weekend = models.IntegerField(db_column='PO_PRICE_WEEKEND', blank=True, null=True)
    poster_places = models.IntegerField(db_column='PO_PLACES', blank=True, null=True)
    mirrorstrip_price_week = models.IntegerField(db_column='MS_PRICE_WEEK', blank=True, null=True)
    mirrorstrip_price_month = models.IntegerField(db_column='MS_PRICE_MONTH', blank=True, null=True)
    fields.GenericRelation(ContactDetailsGeneric)

    class Meta:
        db_table = 'supplier_salon'


class SupplierTypeGym(BasicSupplierDetails):

    gym_type = models.CharField(max_length=30, blank=True, null=True)
    category = models.CharField(max_length=30, blank=True, null=True)
    gym_type_chain = models.CharField(max_length=30, blank=True, null=True)
    chain_origin = models.CharField(max_length=30, blank=True, null=True)
    totalmembership_perannum = models.IntegerField(blank=True, null=True)
    footfall_day = models.IntegerField(blank=True, null=True)
    footfall_weekend = models.IntegerField(blank=True, null=True)
    advertising_media = models.CharField(max_length=30, blank=True, null=True)
    dietchart_price = models.IntegerField(blank=True, null=True)
    stall_price_day = models.IntegerField(blank=True, null=True)
    stall_price_two_day = models.IntegerField(blank=True, null=True)
    standee_price_week = models.IntegerField(blank=True, null=True)
    standee_price_two_week = models.IntegerField(blank=True, null=True)
    standee_price_month = models.IntegerField(blank=True, null=True)
    standee_places = models.IntegerField(blank=True, null=True)
    standee_location = models.CharField(max_length=30, blank=True, null=True)
    banner_price_week = models.IntegerField(blank=True, null=True)
    banner_price_month = models.IntegerField(blank=True, null=True)
    banner_places = models.IntegerField(blank=True, null=True)
    banner_location = models.CharField(max_length=30, blank=True, null=True)
    flyer_price_month = models.IntegerField(blank=True, null=True)
    flyer_distribution = models.CharField(max_length=30, blank=True, null=True)
    poster_price_week = models.IntegerField(blank=True, null=True)
    poster_price_month = models.IntegerField(blank=True, null=True)
    poster_places = models.IntegerField(blank=True, null=True)
    mirrorstrip_count = models.IntegerField(blank=True, null=True)
    mirrorstrip_price_week = models.IntegerField(blank=True, null=True)
    mirrorstrip_price_month = models.IntegerField(blank=True, null=True)
    locker_count = models.IntegerField(blank=True, null=True)
    locker_price_week = models.IntegerField(blank=True, null=True)
    locker_price_month = models.IntegerField(blank=True, null=True)
    wall_price_month = models.IntegerField(blank=True, null=True)
    wall_price_three_month = models.IntegerField(blank=True, null=True)
    fields.GenericRelation(ContactDetailsGeneric)

    class Meta:
        db_table = 'supplier_gym'


class SocietyTower(models.Model):
    tower_id = models.AutoField(db_column='TOWER_ID', primary_key=True)  # Field name made lowercase.
    tower_tag = models.CharField(db_column='TOWER_TAG', max_length=20, blank=True, null=True)  # Field name made lowercase.
    supplier = models.ForeignKey('SupplierTypeSociety', related_name='towers', db_column='SUPPLIER_ID', blank=True, null=True, on_delete=models.CASCADE)  # Field name made lowercase.
    tower_name = models.CharField(db_column='TOWER_NAME', max_length=20, blank=True, null=True)  # Field name made lowercase.
    flat_count_per_tower = models.IntegerField(db_column='FLAT_COUNT_PER_TOWER', blank=True, null=True)  # Field name made lowercase.
    floor_count_per_tower = models.IntegerField(db_column='FLOOR_COUNT_PER_TOWER', blank=True, null=True)  # Field name made lowercase.
    notice_board_count_per_tower = models.IntegerField(db_column='NOTICE_BOARD_COUNT_PER_TOWER', default=0)  # Field name made lowercase.
    standee_location_count_per_tower = models.IntegerField(db_column='STANDEE_LOCATION_COUNT_PER_TOWER', blank=True, null=True)  # Field name made lowercase.
    mailbox_count_per_tower = models.IntegerField(db_column='MAILBOX_COUNT_PER_TOWER', blank=True, null=True)  # Field name made lowercase.
    stall_count_per_tower = models.IntegerField(db_column='STALL_COUNT_PER_TOWER', blank=True, null=True)  # Field name made lowercase.
    tower_location = models.CharField(db_column='TOWER_LOCATION', max_length=100, blank=True, null=True)  # Field name made lowercase.
    tower_resident_count = models.IntegerField(db_column='TOWER_RESIDENT_COUNT', blank=True, null=True)  # Field name made lowercase.
    lift_count = models.IntegerField(db_column='LIFT_COUNT', default=0)  # Field name made lowercase.
    flat_type_count = models.IntegerField(db_column='FLAT_TYPE_COUNT', default=0)  # Field name made lowercase.
    standee_count = models.IntegerField(db_column='STANDEE_COUNT', default=0)  # Field name made lowercase.
    average_rent_per_sqft = models.IntegerField(db_column='AVERAGE_RENT_PER_SQFT', blank=True, null=True)  # Field name made lowercase.
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


class BusinessTypes(BaseModel):
    id              = models.AutoField(db_column='ID', primary_key=True)
    business_type   = models.CharField(db_column='BUSINESS_TYPE', max_length=100, blank=True)
    business_type_code = models.CharField(db_column='TYPE_CODE',unique=True, max_length=4, blank=True, null=True)

    def __str__(self):
        return self.business_type

    def __unicode__(self):
        return self.business_type

    class Meta:
        #db_table = 'BUSINESS_TYPES'
        db_table = 'business_types'


class BusinessSubTypes(BaseModel):
    id = models.AutoField(db_column='ID', primary_key=True)
    business_type = models.ForeignKey(BusinessTypes, related_name='business_subtypes', db_column='BUSINESS_TYPE',
                                      null=True, on_delete=models.CASCADE)  ## changed -> business
    business_sub_type = models.CharField(db_column='SUBTYPE', max_length=100, blank=True)
    business_sub_type_code = models.CharField(db_column='SUBTYPE_CODE', max_length=3, blank=True, null=True)

    def __str__(self):
        return self.business_sub_type

    def __unicode__(self):
        return self.business_sub_type

    class Meta:
        db_table = 'business_subtypes'



# class ProposalInfo(models.Model):
#     proposal_id         = models.CharField(db_column = 'PROPOSAL ID',max_length=15,primary_key=True)
#     account             = models.ForeignKey(AccountInfo,related_name='proposals', db_column ='ACCOUNT',on_delete=models.CASCADE)
#     name                = models.CharField(db_column='NAME', max_length=50,blank=True)
#     payment_status      = models.BooleanField(default=False, db_column='PAYMENT STATUS')
#     updated_on          = models.DateTimeField(auto_now=True, auto_now_add=False)
#     updated_by          = models.CharField(max_length=50,default='Admin')
#     created_on          = models.DateTimeField(auto_now_add=True,auto_now=False)
#     created_by          = models.CharField(max_length=50, default='Admin')
#     tentative_cost      = models.IntegerField(default=5000)
#     tentative_start_date = models.DateTimeField(null=True)
#     tentative_end_date  = models.DateTimeField(null=True)
#
#     def get_centers(self):
#         # ProposalCenterMapping --> related_name='centers'
#         try:
#             return self.centers.all()
#         except:
#             return None
#
#     def get_proposal_versions(self):
#         return self.proposal_versions.all().order_by('-timestamp')
#
#     class Meta:
#
#         #db_table = 'PROPOSAL_INFO'
#         db_table = 'proposal_info'



# class AccountContact(models.Model):
#     id = models.AutoField(db_column='ID', primary_key=True)
#     name = models.CharField(db_column='NAME', max_length=50, blank=True)
#     designation = models.CharField(db_column='DESIGNATION', max_length=20, blank=True)
#     department = models.CharField(db_column='DEPARTMENT', max_length=20, blank=True)
#     phone = models.CharField(db_column='PHONE', max_length=10,  blank=True)
#     email = models.CharField(db_column='EMAILID',  max_length=50, blank=True)
#     account = models.ForeignKey(AccountInfo, related_name='contacts', db_column='ACCOUNT_ID', null=True, on_delete=models.CASCADE)
#     spoc = models.BooleanField(db_column='SPOC', default=False)
#     comments = models.TextField(db_column='COMMENTS',  max_length=100, blank=True)


#     class Meta:
#
#         #db_table = 'PROPOSAL_INFO'
#         db_table = 'proposal_info'

#         db_table = 'account_contact'

class ProposalCenterMapping(BaseModel):
    """
    for a given proposal, stores lat, long, radius, city, pincode etc.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID)
    proposal    = models.ForeignKey('ProposalInfo', db_index=True, related_name='centers', on_delete=models.CASCADE)
    center_name = models.CharField(max_length=50)
    address     = models.CharField(max_length=150,null=True, blank=True)
    latitude    = models.FloatField(default=0.0)
    longitude   = models.FloatField(default=0.0)
    radius      = models.FloatField(default=0.0)
    subarea     = models.CharField(max_length=35)
    area        = models.CharField(max_length=35)
    city        = models.CharField(max_length=35)
    pincode     = models.IntegerField()
    objects = managers.GeneralManager()

    def get_space_mappings(self):
        return SpaceMapping.objects.get(center=self)

    class Meta:
        db_table = 'proposal_center_mapping'
        unique_together = (('proposal','center_name'),)


class SpaceMapping(models.Model):
    """
    This model talks about what spaces or suppliers are allowed or not at a center for a given proposal.
    """
    center              = models.OneToOneField(ProposalCenterMapping,db_index=True, related_name='space_mappings', on_delete=models.CASCADE)
    proposal            = models.ForeignKey('ProposalInfo', related_name='space_mapping', on_delete=models.CASCADE)
    society_allowed     = models.BooleanField(default=False)
    society_count       = models.IntegerField(default=0)
    society_buffer_count = models.IntegerField(default=0)
    corporate_allowed   = models.BooleanField(default=False)
    corporate_count     = models.IntegerField(default=0)
    corporate_buffer_count = models.IntegerField(default=0)
    gym_allowed         = models.BooleanField(default=False)
    gym_count           = models.IntegerField(default=0)
    gym_buffer_count    = models.IntegerField(default=0)
    salon_allowed      = models.BooleanField(default=False)
    salon_count        = models.IntegerField(default=0)
    salon_buffer_count = models.IntegerField(default=0)

    def get_all_inventories(self):
        return self.inventory_types.all()

    def get_society_inventories(self):
        return self.inventory_types.get(supplier_code='RS')

    def get_corporate_inventories(self):
        return self.inventory_types.get(supplier_code='CP')

    def get_gym_inventories(self):
        return self.inventory_types.get(supplier_code='GY')

    def get_salon_inventories(self):
        return self.inventory_types.get(supplier_code='SA')

    def get_all_spaces(self):
        return self.spaces.all()

    def get_societies(self):
        return self.spaces.filter(supplier_code='RS')

    def get_corporates(self):
        return self.spaces.filter(supplier_code='CP')

    def get_gyms(self):
        return self.spaces.filter(supplier_code='GY')

    def get_salons(self):
        return self.spaces.filter(supplier_code='SA')

    class Meta:
        #db_table = 'SPACE_MAPPING'
        db_table = 'space_mapping'

class InventoryType(models.Model):
    supplier_code   = models.CharField(db_index=True, max_length=4)
    space_mapping   = models.ForeignKey(SpaceMapping, db_index=True, related_name='inventory_types', on_delete=models.CASCADE)
    poster_allowed  = models.BooleanField(default=False)
    poster_type     = models.CharField(max_length=10, blank=True, null=True)
    standee_allowed = models.BooleanField(default=False)
    standee_type    = models.CharField(max_length=10, blank=True, null=True)
    flier_allowed   = models.BooleanField(default=False)
    flier_type      = models.CharField(max_length=20, blank=True, null=True)
    stall_allowed   = models.BooleanField(default=False)
    stall_type      = models.CharField(max_length=10, blank=True, null=True)
    banner_allowed  = models.BooleanField(default=False)
    banner_type     = models.CharField(max_length=10, blank=True, null=True)

    class Meta:

        #db_table = 'INVENTORY_TYPE'
        db_table = 'inventory_type'
#
# class ShortlistedSpaces(models.Model):
#     space_mapping   = models.ForeignKey(SpaceMapping,db_index=True, related_name='spaces',on_delete=models.CASCADE)
#     supplier_code   = models.CharField(max_length=4)
#     content_type    = models.ForeignKey(ContentType, related_name='spaces')
#     object_id       = models.CharField(max_length=12)
#     content_object  = fields.GenericForeignKey('content_type', 'object_id')
#     buffer_status   = models.BooleanField(default=False)
#
#     class Meta:
#         #db_table = 'SHORTLISTED_SPACES'
#         db_table = 'shortlisted_spaces'

class ProposalInfoVersion(models.Model):
    # proposal_id         = models.CharField(db_column = 'PROPOSAL ID',max_length=15,primary_key=True)
    # account             = models.ForeignKey(AccountInfo,related_name='proposals', db_column ='ACCOUNT',on_delete=models.CASCADE)
    proposal            = models.ForeignKey('ProposalInfo', related_name='proposal_versions', db_column='PROPOSAL', on_delete=models.CASCADE)
    name                = models.CharField(db_column='NAME', max_length=50,blank=True)
    payment_status      = models.BooleanField(default=False, db_column='PAYMENT STATUS')
    # updated_on          = models.DateTimeField(auto_now=True, auto_now_add=False)
    # updated_by          = models.CharField(max_length=50,default='Admin')
    created_on          = models.DateTimeField()
    created_by          = models.CharField(max_length=50, default='Admin')
    tentative_cost      = models.IntegerField(default=5000)
    tentative_start_date = models.DateTimeField(null=True)
    tentative_end_date  = models.DateTimeField(null=True)
    timestamp           = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        #db_table = 'PROPOSAL_INFO_VERSION'
        db_table = 'proposal_info_version'

class ProposalCenterMappingVersion(models.Model):
    proposal_version    = models.ForeignKey(ProposalInfoVersion, db_index=True, related_name='centers_version', on_delete=models.CASCADE)
    center_name = models.CharField(max_length=50)
    address     = models.CharField(max_length=150, null=True, blank=True)
    latitude    = models.FloatField()
    longitude   = models.FloatField()
    radius      = models.FloatField()
    subarea     = models.CharField(max_length=35, default='')
    area        = models.CharField(max_length=35, default='')
    city        = models.CharField(max_length=35, default='')
    pincode     = models.IntegerField(default=0)

    def get_space_mappings_versions(self):
        return SpaceMappingVersion.objects.get(center_version=self)

    class Meta:
        db_table = 'proposal_center_mapping_version'
        unique_together = (('proposal_version','center_name'),)


class SpaceMappingVersion(models.Model):
    center_version      = models.OneToOneField(ProposalCenterMappingVersion,db_index=True, related_name='space_mappings_version', on_delete=models.CASCADE)
    proposal_version    = models.ForeignKey(ProposalInfoVersion, related_name='space_mapping_version', on_delete=models.CASCADE)
    society_allowed     = models.BooleanField(default=False)
    society_count       = models.IntegerField(default=0)
    society_buffer_count = models.IntegerField(default=0)
    corporate_allowed   = models.BooleanField(default=False)
    corporate_count     = models.IntegerField(default=0)
    corporate_buffer_count = models.IntegerField(default=0)
    gym_allowed         = models.BooleanField(default=False)
    gym_count           = models.IntegerField(default=0)
    gym_buffer_count    = models.IntegerField(default=0)
    salon_allowed      = models.BooleanField(default=False)
    salon_count        = models.IntegerField(default=0)
    salon_buffer_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'space_mapping_version'

class InventoryTypeVersion(models.Model):
    supplier_code   = models.CharField(db_index=True, max_length=4)
    space_mapping_version   = models.ForeignKey(SpaceMappingVersion, db_index=True, related_name='inventory_types_version', on_delete=models.CASCADE)
    poster_allowed  = models.BooleanField(default=False)
    poster_type     = models.CharField(max_length=10, blank=True, null=True)
    standee_allowed = models.BooleanField(default=False)
    standee_type    = models.CharField(max_length=10, blank=True, null=True)
    flier_allowed   = models.BooleanField(default=False)
    flier_type      = models.CharField(max_length=20, blank=True, null=True)
    stall_allowed   = models.BooleanField(default=False)
    stall_type      = models.CharField(max_length=10, blank=True, null=True)
    banner_allowed  = models.BooleanField(default=False)
    banner_type     = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'inventory_type_version'

class ShortlistedSpacesVersion(models.Model):
    space_mapping_version   = models.ForeignKey(SpaceMappingVersion,db_index=True, related_name='spaces_version',on_delete=models.CASCADE)
    supplier_code   = models.CharField(max_length=4)
    content_type    = models.ForeignKey(ContentType, related_name='spaces_version')
    object_id       = models.CharField(max_length=12)
    content_object  = fields.GenericForeignKey('content_type', 'object_id')
    buffer_status   = models.BooleanField(default=False)

    class Meta:
        #db_table = 'SHORTLISTED_SPACES_VERSION'
        db_table = 'shortlisted_spaces_version'


class AssignedAudits(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    ad_inventory_id = models.CharField(db_column='AD_INVENTORY_ID', max_length=50, blank=True)
    ad_inventory_type = models.CharField(db_column='AD_INVENTORY_TYPE', null=True, max_length=50, blank=True)
    supplier_name = models.CharField(db_column='SUPPLIER_NAME', max_length=50, blank=True)
    ad_location = models.CharField(db_column='AD_LOCATION', max_length=50, blank=True) #ops to enter the location during finalization
    address = models.CharField(db_column='ADDRESS', max_length=100, blank=True)
    date = models.DateField(db_column='DATE', null=True)
    business_name = models.CharField(db_column='BUSINESS_NAME', max_length=50, blank=True)
    audit_type = models.CharField(db_column='AUDIT_TYPE', max_length=20, blank=True) #change to enum
    image_url = models.CharField(db_column='IMAGE_URL', max_length=100, null=True)
    db_table = 'assigned_audits'


class Audits(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    society_booking = models.ForeignKey('SocietyInventoryBooking', related_name='audits', db_column='SOCIETY_BOOKING_ID', null=True, on_delete=models.CASCADE)
    latitude = models.FloatField(db_column='LATITUDE', null=True)
    longitude = models.FloatField(db_column='LONGITUDE', null=True)
    timestamp = models.DateTimeField(db_column='TIMESTAMP', null=True)
    barcode = models.FloatField(db_column='BARCODE', null=True) #split to 2 barcode fields
    audited_by = models.IntegerField(db_column='USER_ID', null=True) #change to user id FK
    audit_type = models.CharField(db_column='AUDIT_TYPE', max_length=20, blank=True) #change to enum
    image_url = models.CharField(db_column='IMAGE_URL', max_length=100, null=True)

    class Meta:

        db_table = 'audits'


class AuditorSocietyMapping(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    user_id = models.IntegerField(db_column='USER_ID', null=True) #change to user id FK
    society = models.ForeignKey('SupplierTypeSociety', related_name='auditors', db_column='SUPPLIER_ID', null=True, on_delete=models.CASCADE)

    class Meta:

        db_table = 'auditor_society_mapping'


class SupplierTypeCode(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    supplier_type_name = models.CharField(db_column='SUPPLIER_TYPE_NAME', max_length=20, null=True)
    supplier_type_code = models.CharField(db_column='SUPPLIER_TYPE_CODE', max_length=5, null=True)

    class Meta:

        db_table = 'supplier_type_code'


class FlatTypeCode(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    flat_type_name = models.CharField(db_column='FLAT_TYPE_NAME', max_length=20, null=True)
    flat_type_code = models.CharField(db_column='FLAT_TYPE_CODE', max_length=5, null=True)

    class Meta:

        db_table = 'flat_type_code'


class InventorySummary(BaseModel):
    id = models.AutoField(db_column='ID', primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID)
    supplier = models.ForeignKey('SupplierTypeSociety', related_name='inventoy_summary', db_column='SUPPLIER_ID', blank=True, null=True, on_delete=models.CASCADE, unique=True)
    poster_allowed_nb = models.BooleanField(db_column='POSTER_ALLOWED_NB', default=False)
    poster_allowed_lift = models.BooleanField(db_column='POSTER_ALLOWED_LIFT', default=False)
    standee_allowed = models.BooleanField(db_column='STANDEE_ALLOWED', default=False)
    stall_allowed = models.BooleanField(db_column='STALL_ALLOWED', default=False)
    car_display_allowed = models.BooleanField(db_column='CAR_DISPLAY_ALLOWED', default=False)
    flier_allowed = models.BooleanField(db_column='FLIER_ALLOWED', default=False)
    nb_A4_allowed = models.BooleanField(db_column='NB_A4_ALLOWED', default=False)
    nb_A3_allowed = models.BooleanField(db_column='NB_A3_ALLOWED', default=False)
    poster_price_week_lift = models.IntegerField(db_column='POSTER_PRICE_WEEK_LIFT', null=True)
    poster_price_week_nb = models.IntegerField(db_column='POSTER_PRICE_WEEK_NB', null=True)
    standee_price_week = models.IntegerField(db_column='STANDEE_PRICE_WEEK', null=True)
    stall_price_day_small = models.IntegerField(db_column='STALL_PRICE_DAY_SMALL', null=True)
    stall_price_day_large = models.IntegerField(db_column='STALL_PRICE_DAY_LARGE', null=True)
    cd_price_day_standard = models.IntegerField(db_column='CD_PRICE_DAY_STANDARD', null=True)
    cd_price_day_premium = models.IntegerField(db_column='CD_PRICE_DAY_PREMIUM', null=True)
    flier_price_day = models.IntegerField(db_column='FLIER_PRICE_DAY', null=True)
    nb_count = models.IntegerField(db_column='NB_COUNT', null=True)
    total_poster_nb = models.IntegerField(db_column='TOTAL_POSTERS_NB',null=True)
    lift_count = models.IntegerField(db_column='LIFT_COUNT', null=True)
    total_poster_count = models.IntegerField(db_column='TOTAL_POSTER_COUNT', null=True)
    total_poster_campaigns = models.IntegerField(db_column='TOTAL_POSTER_CAMPAIGNS', null=True)
    standee_small = models.BooleanField(db_column='STANDEE_SMALL', default=False)
    standee_medium = models.BooleanField(db_column='STANDEE_MEDIUM', default=False)
    total_standee_count = models.IntegerField(db_column='TOTAL_STANDEE_COUNT', null=True)
    total_standee_campaigns = models.IntegerField(db_column='TOTAL_STANDEE_CAMPAIGNS', null=True)
    stall_canopy = models.BooleanField(db_column='STALL_CANOPY', default=False)
    stall_small = models.BooleanField(db_column='STALL_SMALL', default=False)
    stall_large = models.BooleanField(db_column='STALL_LARGE', default=False)
    cd_standard = models.BooleanField(db_column='CD_STANDARD', default=False)
    cd_premium = models.BooleanField(db_column='CD_PREMIUM', default=False)
    total_stall_count = models.IntegerField(db_column='TOTAL_STALL_COUNT', null=True)
    timing = models.CharField(db_column='STALL_TIMING', max_length=20, blank = True, null=True)
    furniture_available = models.BooleanField(db_column='FURNITURE_AVAILABLE', default=False)
    electricity_available = models.BooleanField(db_column='ELECTRICITY_SEPARATE', default=False)
    mailbox_allowed = models.BooleanField(db_column='MAILBOX_ALLOWED', default=False)
    d2d_allowed = models.BooleanField(db_column='D2D_ALLOWED', default=False)
    flier_frequency = models.IntegerField(db_column='FLIER_FREQUENCY', null=True)
    flier_lobby_allowed = models.BooleanField(db_column='FLIER_LOBBY_ALLOWED', default=False)
    poster_campaign = models.IntegerField(db_column='POSTER_CAMPAIGN', blank=True, null=True)  # Field name made lowercase.
    standee_campaign = models.IntegerField(db_column='STANDEE_CAMPAIGN', blank=True, null=True)  # Field name made lowercase.
    stall_or_cd_campaign = models.IntegerField(db_column='STALL_OR_CD_CAMPAIGN', blank=True, null=True)  # Field name made lowercase.
    flier_campaign = models.IntegerField(db_column='FLIER_CAMPAIGN', blank=True, null=True)  # Field name made lowercase.
    standee_per_campaign = models.IntegerField(db_column='STANDEE_PER_CAMPAIGN', null=True)
    poster_per_campaign = models.IntegerField(db_column='POSTER_PER_CAMPAIGN', null=True)
    campaign_count = models.IntegerField(db_column='CAMPAIGN_COUNT', null=True)
    nb_price_confidence = models.CharField(db_column='NB_PRICE_CONFIDENCE', max_length=20, blank = True, null=True)
    lift_price_confidence = models.CharField(db_column='LIFT_PRICE_CONFIDENCE', max_length=20, blank = True, null=True)
    standee_price_confidence = models.CharField(db_column='STANDEE_PRICE_CONFIDENCE', max_length=20, blank = True, null=True)
    smallStall_price_confidence = models.CharField(db_column='SMALLSTALL_PRICE_CONFIDENCE', max_length=20, blank = True, null=True)
    largeStall_price_confidence = models.CharField(db_column='LARGESTALL_PRICE_CONFIDENCE', max_length=20, blank = True, null=True)
    standard_price_confidence = models.CharField(db_column='STANDARD_PRICE_CONFIDENCE', max_length=20, blank = True, null=True)
    premium_price_confidence = models.CharField(db_column='PREMIUM_PRICE_CONFIDENCE', max_length=20, blank = True, null=True)
    flier_price_confidence = models.CharField(db_column='FLIER_PRICE_CONFIDENCE', max_length=20, blank = True, null=True)
    poster_count_per_tower = models.IntegerField(db_column='POSTER_COUNT_PER_TOWER', null=True)
    poster_count_per_nb = models.IntegerField(db_column='POSTER_COUNT_PER_NB', null=True)
    standee_count_per_tower = models.IntegerField(db_column='STANDEE_COUNT_PER_TOWER', null=True)
    content_type = models.ForeignKey(ContentType,default=None, null=True)
    object_id = models.CharField(max_length=supplier_id_max_length, null=True)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    objects = managers.GeneralManager()
    gateway_arch_allowed = models.BooleanField(default=False)
    lit = models.BooleanField(default=False)
    non_lit = models.BooleanField(default=False)
    gateway_arch_length = models.FloatField(default=0.0, null=True)
    gateway_arch_breadth = models.FloatField(default=0.0, null=True)

    class Meta:

        db_table = 'inventory_summary'


class CorporateBuilding(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    building_name = models.CharField(db_column='BUILDING_NAME', max_length=50, null=True, blank=True)
    number_of_wings = models.IntegerField(db_column='NUMBER_OF_WINGS', null=True, blank=True)
    corporatepark_id = models.ForeignKey('SupplierTypeCorporate',db_index=True, db_column='CORPORATE_ID',related_name='corporatebuilding', blank=True, null=True, on_delete=models.CASCADE)

    def get_wings(self):
        return self.buildingwing.all()

    class Meta:
        db_table='corporate_building'


class CorporateBuildingWing(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    wing_name = models.CharField(db_column='WING_NAME', max_length=50, null=True, blank=True)
    number_of_floors = models.IntegerField(db_column='NUMBER_OF_FLOORS', null=True, blank=True)
    building_id = models.ForeignKey('CorporateBuilding',db_index=True, db_column='BUILDING_ID',related_name='buildingwing', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table='corporate_building_wing'

# class CorporateCompany(models.Model):
#     id = models.AutoField(db_column='ID', primary_key=True)
#     company_name = models.CharField(db_column='COMPANY_NAME',max_length=50,blank=True,null=True)
#     corporatepark_id = models.ForeignKey('SupplierTypeCorporate', db_column='CORPORATEPARK_NAME', related_name='corporatecompany', blank=True, null=True, on_delete=models.CASCADE)

#     class Meta:
#         db_table='corporate_company'


class CorporateCompanyDetails(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    company_id = models.ForeignKey('CorporateParkCompanyList', db_column='COMPANY_ID', related_name='companydetails', blank=True, null=True, on_delete=models.CASCADE)
    building_name = models.CharField(db_column='BUILDING_NAME', max_length=20, blank=True, null=True)
    wing_name = models.CharField(db_column='WING_NAME', max_length=20, blank=True, null=True)

    def get_floors(self):
        return self.wingfloor.all()

    class Meta:
        db_table='corporate_company_details'


class CompanyFloor(models.Model):
    company_details_id = models.ForeignKey('CorporateCompanyDetails',db_column='COMPANY_DETAILS_ID',related_name='wingfloor', blank=True, null=True, on_delete=models.CASCADE)
    floor_number = models.IntegerField(db_column='FLOOR_NUMBER', blank=True, null=True)

    class Meta:
        db_table='corporate_building_floors'


class SocietyLeads(models.Model):
    id = models.CharField(max_length=100,null=False,primary_key=True)
    society = models.ForeignKey('SupplierTypeSociety', null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, null=True, blank=True,default='0')
    email = models.EmailField()

    class Meta:
        db_table = 'society_leads'


class ShortlistedInventoryPricingDetails(BaseModel):
    """
    Model for storing calculated price and count of an inventory for a given supplier.
    A particular inventory type is identified by it's content_type_id.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID)
    inventory_content_type = models.ForeignKey(ContentType, null=True, blank=True)
    inventory_id = models.CharField(max_length=255, null=True, blank=True)
    inventory_price = models.FloatField(default=0.0, null=True)
    inventory_count = models.IntegerField(default=0, null=True)
    factor = models.IntegerField(default=0.0, null=True)
    ad_inventory_type = models.ForeignKey('AdInventoryType', null=True)
    ad_inventory_duration = models.ForeignKey('DurationType', null=True)
    release_date = models.DateTimeField(null=True, blank=True)
    closure_date = models.DateTimeField(null=True, blank=True)
    shortlisted_spaces = models.ForeignKey('ShortlistedSpaces', null=True, blank=True)
    objects = managers.GeneralManager()
    inventory_object = fields.GenericForeignKey('inventory_content_type', 'inventory_id')
    comment = models.CharField(max_length=1000, null=True, blank=True)


    class Meta:
        db_table = 'shortlisted_inventory_pricing_details'


class SupplierTypeBusShelter(BasicSupplierDetails):
    """
    model inherits basic supplier fields from abstract model BasicSupplierDetails
    """
    lit_status = models.CharField(max_length=255, null=True, blank=True)
    halt_buses_count = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'supplier_bus_shelter'


class ProposalMasterCost(BaseModel):
    """
    A table to store revenue related costs. currently it's content will be populated by a sheet. only fixed fields
    and relations are covered up.
    Only one instance of MasterCost exists for one proposal version, proposal
    proposal_version alone does not make any sense. it's always tied to a proposal instance.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID)
    proposal = models.OneToOneField('ProposalInfo', null=True, blank=True)
    agency_cost = models.FloatField(null=True, blank=True)
    basic_cost = models.FloatField(null=True, blank=True)
    discount = models.FloatField(null=True, blank=True)
    total_cost = models.FloatField(null=True, blank=True)
    tax = models.FloatField(null=True, blank=True)
    total_impressions = models.FloatField(null=True, blank=True)
    average_cost_per_impression = models.FloatField(null=True, blank=True)
    objects = managers.GeneralManager()

    class Meta:
        db_table = 'proposal_master_cost_details'


class AbstractGeneralCost(BaseModel):
    """
    This class is an abstract class for all types of cost's. Any type of cost example, PrintingCost, LogisticCost,
    SpaceBookingCost etc are inherited from this basic cost table. A proposal version can only have one PrintingCost,
    one LogisticCost, one SpaceBookingCost etc, hence this table is linked to proposal version by ONE to ONE relation.
    also one mastercost sheet will only have one "cost", doesn't matter what type ( ofcourse different types of costs, but all are actualy
    a cost ! ).
    """
    proposal_master_cost = models.ForeignKey(ProposalMasterCost, null=True, blank=True)
    total_cost = models.FloatField(null=True, blank=True)
    comment = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        abstract = True


class PrintingCost(AbstractGeneralCost):
    """
    Printing cost is broken down into various costs. Hence a model is made to store it's pieces.
    """
    class Meta:
        db_table = 'printing_cost'


class LogisticOperationsCost(AbstractGeneralCost):
    """
    LogisticOperationsCost  is broken down into various costs. Hence a model is made to store it's pieces.
    """

    class Meta:
        db_table = 'logistic_operations_cost'


class IdeationDesignCost(AbstractGeneralCost):
    """
    IdeationDesignCost  is broken down into various costs. Hence a model is made to store it's pieces.
    """

    class Meta:
        db_table = 'ideation_design_cost'


class SpaceBookingCost(AbstractGeneralCost):
    """
    SpaceBookingCost  is broken down into various costs. Hence a model is made to store it's pieces.
    """
    supplier_type = models.ForeignKey(ContentType, null=True, blank=True)

    class Meta:
        db_table = 'space_booking_cost'


class EventStaffingCost(AbstractGeneralCost):
    """
    EventStaffingCost  is broken down into various costs. Hence a model is made to store it's pieces.
    """

    class Meta:
        db_table = 'event_staffing_cost'


class DataSciencesCost(AbstractGeneralCost):
    """
    DataSciencesCost is broken down into various costs. Hence a model is made to store it's pieces.
    """

    class Meta:
        db_table = 'data_sciences_cost'


class ProposalMetrics(BaseModel):
    """
    Different types of  spaces/suppliers will have different metrics. a metrics is list of predefined headers.
    one supplier can have many metrices. hence this model is used to store data for a given supplier that
    exists as a list of values.
    for proposal x, metric m1 has value of v1 for supplier S.
    for proposal x, metric m2 has value of v2 for supplier S.
    """
    proposal_master_cost = models.ForeignKey(ProposalMasterCost, null=True, blank=True)
    metric_name = models.CharField(max_length=255, null=True, blank=True)
    supplier_type = models.ForeignKey(ContentType, null=True, blank=True)
    value = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'proposal_metrics'


class ProposalInfo(BaseModel):
    """
    Two extra fields called parent and is_campaign is added. parent is a self referencing field. it refers to itself.
    parent stores the information that from what proposal_id, the current proposal_id was created.
    is_campaign determines weather this proposal is a campaign or not.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID)
    proposal_id = models.CharField(max_length=255, primary_key=True)
    account = models.ForeignKey('AccountInfo', related_name='proposals',on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    payment_status = models.BooleanField(default=False,)
    updated_on = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated_by = models.CharField(max_length=50, default='Admin')
    created_on = models.DateTimeField(auto_now_add=True, auto_now=False)
    created_by = models.CharField(max_length=50, default='Admin')
    tentative_cost = models.IntegerField(default=5000)
    tentative_start_date = models.DateTimeField(null=True)
    tentative_end_date = models.DateTimeField(null=True)
    campaign_state = models.CharField(max_length=10, null=True, blank=True)
    parent = models.ForeignKey('ProposalInfo', null=True, blank=True, default=None)
    objects = managers.GeneralManager()
    invoice_number = models.CharField(max_length=1000, null=True, blank=True)

    def get_centers(self):
        try:
            return self.centers.all()
        except:
            return None
    def get_proposal_versions(self):
        return self.proposal_versions.all().order_by('-timestamp')

    class Meta:

        db_table = 'proposal_info'


class Filters(BaseModel):
    """
    Stores all kinds of filters and there respective codes. Filters are used when you filter all the suppliers
    on the basis of what inventories you would like to have in there, etc. because different suppliers can have
    different types of filters, we have content_type field for capturing that. These filters are predefined in constants
    and are populated from there.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID)
    center = models.ForeignKey(ProposalCenterMapping, null=True, blank=True)
    proposal = models.ForeignKey('ProposalInfo', null=True, blank=True)
    supplier_type = models.ForeignKey(ContentType, null=True, blank=True)
    filter_name = models.CharField(max_length=255, null=True, blank=True)
    filter_code = models.CharField(max_length=255, null=True, blank=True)
    is_checked = models.BooleanField(default=False)
    supplier_type_code = models.CharField(max_length=255, null=True, blank=True)
    objects = managers.GeneralManager()

    class Meta:
        db_table = 'filters'


class ShortlistedSpaces(BaseModel):
    """
    This model stores all the shortlisted spaces. One Supplier or space can be under different campaigns.
    in one campaign it's status can be removed while in the other it's buffered. Hence this model is made
    for mapping such relations.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID)
    space_mapping = models.ForeignKey(SpaceMapping, db_index=True, related_name='spaces', on_delete=models.CASCADE, null=True, blank=True)
    center = models.ForeignKey('ProposalCenterMapping', null=True, blank=True)
    proposal = models.ForeignKey('ProposalInfo', null=True, blank=True)
    supplier_code = models.CharField(max_length=4, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, related_name='spaces')
    object_id = models.CharField(max_length=supplier_id_max_length)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    buffer_status = models.BooleanField(default=False)
    status = models.CharField(max_length=10, null=True, blank=True)
    objects = managers.GeneralManager()
    campaign_status = models.CharField(max_length=10, default='', null=True, blank=True)
    phase = models.CharField(max_length=10, default='',  null=True, blank=True)
    payment_status = models.CharField(max_length=255, null=True, blank=True)
    payment_method = models.CharField(max_length=255, null=True, blank=True)
    total_negotiated_price = models.CharField(max_length=255, null=True, blank=True)
    booking_status = models.CharField(max_length=10, null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        db_table = 'shortlisted_spaces'


class ProposalCenterSuppliers(BaseModel):
    """
    which suppliers are allowed in a given center under a proposal ?
    used when CreateInitialProposal is called. each center can have different suppliers allowed.
    each supplier is identified by a content_type and a unique code predefined for it.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID)
    proposal = models.ForeignKey('ProposalInfo', null=True, blank=True)
    center = models.ForeignKey('ProposalCenterMapping', null=True, blank=True)
    supplier_content_type = models.ForeignKey(ContentType, null=True, blank=True)
    supplier_type_code = models.CharField(max_length=255, null=True, blank=True)
    objects = managers.GeneralManager()

    class Meta:
        db_table = 'proposal_center_suppliers'


class Lead(BaseModel):
    """
    A model to store the leads data. This user is different django from auth_user. it's a 'lead'.
    """
    email = models.EmailField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)
    age = models.FloatField(null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    lead_type = models.CharField(max_length=255, null=True, blank=True)
    lead_status = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'lead'


class CampaignLeads(BaseModel):
    """
    a campaign can have multiple leads. a lead can go in multiple campaigns.
    campaign stores the campaign id.
    lead stores the lead id
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID)
    campaign_id = models.IntegerField(default=0)
    lead_email = models.EmailField(default='')
    comments = models.CharField(max_length=255, null=True)
    objects = managers.GeneralManager()

    class Meta:
        db_table = 'campaign_leads'
        unique_together = (('campaign_id', 'lead_email'),)


class GenericExportFileName(BaseModel):
    """
    This model stores file name generated by GenericExport API.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID)
    business = models.ForeignKey('BusinessInfo', null=True, blank=True)
    organisation = models.ForeignKey(Organisation, null=True, blank=True)
    account = models.ForeignKey('AccountInfo', null=True, blank=True)
    proposal = models.ForeignKey('ProposalInfo', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=1000, null=True, blank=True)
    is_exported = models.BooleanField(default=True)
    objects = managers.GeneralManager()

    @property
    def calculate_assignment_detail(self):
        """
        This method is a property which just calculates to whom this proposal was being assigned while converting it to a
        campaign. This can be used as a field in a serializer class.
        """
        try:
            instance = CampaignAssignment.objects.get(campaign=self.proposal)
            # can use caching here to avoid BaseUser calls.
            return {
                'assigned_by': BaseUser.objects.get(pk=instance.assigned_by.pk).username,
                'assigned_to': BaseUser.objects.get(pk=instance.assigned_to.pk).username
            }
        except ObjectDoesNotExist:
            return {
                'assigned_by': 'Nobody',
                'assigned_to': 'Nobody'
            }

    class Meta:
        db_table = 'generic_export_file_name'


class CampaignAssignment(BaseModel):
    """
    The model to store a particular campaign being assigned to a user
    """
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='assigned_by')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='assigned_to')
    campaign = models.OneToOneField(ProposalInfo, unique=True)
    # possible primary key should be campaign_id

    class Meta:
        db_table = 'campaign_assignment'

# class ShortlistedInventoryDetails(BaseModel):
#     """
#     This table stores information about Release Date, Audit Date, and Campaign Dates associated with each inventory_id
#     under each campaign. All inventories within this table are booked.Campaign is nothing but Proposal_id with is_campaign = True
#     """
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID)
#     inventory_content_type = models.ForeignKey(ContentType, null=True, blank=True)
#     inventory_id = models.CharField(max_length=255, null=True, blank=True)
#     campaign_id = models.ForeignKey(ProposalInfo, null=True, blank=True)
#     release_date = models.DateTimeField(default=timezone.now())
#     closure_date = models.DateTimeField(default=timezone.now())
#     factor = models.IntegerField(default=0.0, null=True)
#     center = models.ForeignKey('ProposalCenterMapping')
#     ad_inventory_type = models.ForeignKey('AdInventoryType', null=True)
#     ad_inventory_duration = models.ForeignKey('DurationType', null=True)
#     inventory_price = models.FloatField(default=0.0, null=True)
#     shortlisted_spaces = models.ForeignKey(ShortlistedSpaces, null=True, blank=True)
#     objects = managers.GeneralManager()
#


class AuditDate(BaseModel):
    """
    A particular inventory can have multiple audit dates
    """
    shortlisted_inventory = models.ForeignKey(ShortlistedInventoryPricingDetails, null=True, blank=True)
    audit_date = models.DateTimeField(null=True, blank=True)
    audited_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)

    class Meta:
        db_table = 'audit_date'


class Amenity(BaseModel):
    """
    Stores individual amenities. There basic details.
    """
    name = models.CharField(max_length=1000)
    code = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        db_table = 'amenities'


class SupplierAmenitiesMap(BaseModel):
    """
    This table represents the idea that each supplier can have multiple amenities
    """

    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=1000)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    amenity = models.ForeignKey(Amenity, null=True, blank=True)

    class Meta:
        db_table = 'supplier_amenities_map'


class InventoryActivity(BaseModel):
    """
    Stores activities like Release, Closure, Audits against each inventory
    """
    shortlisted_inventory_details = models.ForeignKey('ShortlistedInventoryPricingDetails')
    activity_type = models.CharField(max_length=255, null=True,  choices=INVENTORY_ACTIVITY_TYPES)

    class Meta:
        db_table = 'inventory_activity'


class InventoryActivityAssignment(BaseModel):
    """
    Assignment of ( inv_global_id, act_date, act_t  ype ) to a user here in this table.
    """

    inventory_activity = models.ForeignKey('InventoryActivity', null=True, blank=True)
    activity_date = models.DateTimeField(max_length=255, null=True, blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='activity_assigned_to', null=True, blank=True)
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='activity_assigned_by', null=True, blank=True)
    reassigned_activity_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'inventory_activity_assignment'


class InventoryActivityImage(BaseModel):
    """
    stores image path against each inventory_activity_assignment id
    """
    inventory_activity_assignment = models.ForeignKey('InventoryActivityAssignment', null=True, blank=True)
    image_path = models.CharField(max_length=1000, null=True, blank=True)
    comment = models.CharField(max_length=1000, null=True, blank=True)
    actual_activity_date = models.DateTimeField(null=True, blank=True)
    activity_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'inventory_activity_image'


class SupplierTypeRetailShop(BasicSupplierDetails):
    """
    stores details of RETAIL TYPE SUPPLIER.
    """
    retail_shop_type = models.CharField(choices=RETAIL_SHOP_TYPE, max_length=255, null=True, blank=True)
    size = models.FloatField(null=True, blank=True)
    is_modern_trade = models.BooleanField(default=False)
    is_traditional = models.BooleanField(default=False)
    category_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:

        db_table = 'supplier_type_retail_shop'


class SupplierTypeBusDepot(BasicSupplierDetails):
    """
    stores info about a bus depot
    """
    bus_count = models.IntegerField(null=True, blank=True)
    route_count_originate = models.IntegerField(null=True, blank=True)
    route_count_terminate = models.IntegerField(null=True, blank=True)
    bus_types = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'supplier_type_bus_depot'


class Profile(BaseModel):
    """
    This model describes profile. a user can only have one profile.
    """
    name = models.CharField(max_length=255)
    organisation = models.ForeignKey('Organisation')
    is_standard = models.BooleanField(default=False)

    class Meta:
        db_table = 'profile'


class ObjectLevelPermission(models.Model):
    """
    This class grants access  Read, Update, View, ViewAll, and UpdateAll on each object it's tied to.
    """
    name = models.CharField(max_length=255)
    codename = models.CharField(max_length=50)
    content_type = models.ForeignKey(ContentType)
    view = models.BooleanField(default=False)
    update = models.BooleanField(default=False)
    create = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)
    view_all = models.BooleanField(default=False)
    update_all = models.BooleanField(default=False)
    description = models.CharField(max_length=1000, null=True, blank=True)
    profile = models.ForeignKey(Profile)

    class Meta:
        db_table = 'object_level_permission'


class GeneralUserPermission(BaseModel):
    """
    This class defines all the possible functions in website and tells weather that is allowed/not allowed for a profile
    """
    name = models.CharField(max_length=255)
    codename = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, null=True, blank=True)
    is_allowed = models.BooleanField(default=False)
    profile = models.ForeignKey(Profile)

    class Meta:
        db_table = 'general_user_permission'

class Role(models.Model):
    """
    This model defines roles
    """
    name = models.CharField(max_length=255)
    codename = models.CharField(max_length=255)
    organisation = models.ForeignKey('Organisation')

    class Meta:
        db_table = 'role'

class RoleHierarchy(models.Model):
    """
    This model defines role hierarchy between roles
    """
    parent = models.ForeignKey('Role', related_name='parent')
    child = models.ForeignKey(Role)
    depth = models.IntegerField(default=0, null=False, blank=False)

    class Meta:
        db_table = 'role_hierarchy'

class Leads(BaseModel):
    """
    This model defines Leads
    """
    campaign = models.ForeignKey('ProposalInfo', null=False, blank=False)
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.CharField(max_length=supplier_id_max_length)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    objects = managers.GeneralManager()
    firstname1 = models.CharField(max_length=20, blank=True, null=True)
    lastname1 = models.CharField(max_length=20, blank=True, null=True)
    firstname2 = models.CharField(max_length=20, blank=True, null=True)
    lastname2 = models.CharField(max_length=20, blank=True, null=True)
    mobile1 = models.BigIntegerField(blank=True, null=True)
    mobile2 = models.BigIntegerField(blank=True, null=True)
    phone = models.BigIntegerField(blank=True, null=True)
    email1 = models.EmailField(max_length=50, blank=True, null=True)
    email2 = models.EmailField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    alphanumeric1 = models.CharField(max_length=50, null=True, blank=True)
    alphanumeric2 = models.CharField(max_length=50, null=True, blank=True)
    alphanumeric3 = models.CharField(max_length=50, null=True, blank=True)
    alphanumeric4 = models.CharField(max_length=50, null=True, blank=True)
    boolean1 = models.BooleanField(default=False)
    boolean2 = models.BooleanField(default=False)
    boolean3 = models.BooleanField(default=False)
    boolean4 = models.BooleanField(default=False)
    float1 = models.FloatField(null=True, blank=True)
    float2 = models.FloatField(null=True, blank=True)
    number1 = models.IntegerField(null=True, blank=True)
    number2 = models.IntegerField(null=True, blank=True)
    date1 = models.DateField(null=True, blank=True)
    date2 = models.DateField(null=True, blank=True)
    is_from_sheet = models.BooleanField(default=False)
    is_interested = models.BooleanField(default=False)
    class Meta:
        db_table = 'leads'

class LeadAlias(BaseModel):
    """
    This model defines aliases of leads model fields
    """
    campaign = models.ForeignKey('ProposalInfo', null=False, blank=False)
    original_name = models.CharField(max_length=255, null=False, blank=False)
    alias = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        db_table = 'lead_alias'

class GatewayArchInventory(BaseModel):
    """
    This model defines the inventory of GateWayArch Inventory
    """
    id = models.AutoField(db_column='ID', primary_key=True)
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', max_length=22,unique=True)
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.CharField(max_length=supplier_id_max_length, null=True)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    objects = managers.GeneralManager()

    class Meta:
        db_table = 'gateway_arch_inventory'