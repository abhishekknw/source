from v0 import managers
from django.db import models
from django.conf import settings
from v0.ui.base.models import BaseModel
from v0.ui.account.models import ContactDetails, PriceMappingDefault
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields
from datetime import date
from v0.constants import supplier_id_max_length

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


class InventoryType(models.Model):
    supplier_code   = models.CharField(db_index=True, max_length=4)
    space_mapping   = models.ForeignKey('SpaceMapping', db_index=True, related_name='inventory_types', on_delete=models.CASCADE)
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

class InventoryTypeVersion(models.Model):
    supplier_code   = models.CharField(db_index=True, max_length=4)
    space_mapping_version   = models.ForeignKey('SpaceMappingVersion', db_index=True, related_name='inventory_types_version', on_delete=models.CASCADE)
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
    object_id = models.CharField(max_length= supplier_id_max_length, null=True)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    objects = managers.GeneralManager()
    tower = models.ForeignKey('SocietyTower', null=True, blank=True)

    class Meta:
        db_table = 'poster_inventory'

class InventoryLocation(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field n
    location_id = models.CharField(db_column='LOCATION_ID', max_length=20)  # Field name made lowercase.
    location_type = models.CharField(db_column='LOCATION_TYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'inventory_location'

class AdInventoryType(BaseModel):
    id = models.AutoField(db_column='ID', primary_key=True)
    adinventory_name = models.CharField(db_column='ADINVENTORY_NAME', max_length=20,
                                        choices=AD_INVENTORY_CHOICES, default='POSTER')
    adinventory_type = models.CharField(db_column='ADINVENTORY_TYPE', max_length=20)  # Field name made lowercase.

    def __str__(self):
        return self.adinventory_name

    class Meta:
        db_table = 'ad_inventory_type'

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

class SupplierTypeSociety(BaseModel):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID)
    objects = managers.GeneralManager()
    supplier_id = models.CharField(db_column='SUPPLIER_ID', primary_key=True, max_length=20)  # Field name made lowercase.
    supplier_code = models.CharField(db_column='SUPPLIER_CODE', max_length=3, null=True)
    society_name = models.CharField(db_column='SOCIETY_NAME', max_length=70, blank=True, null=True)  # Field name made lowercase.
    society_address1 = models.CharField(db_column='SOCIETY_ADDRESS1', max_length=250, blank=True, null=True)  # Field name made lowercase.
    society_address2 = models.CharField(db_column='SOCIETY_ADDRESS2', max_length=250, blank=True, null=True)  # Field name made lowercase.
    society_zip = models.IntegerField(db_column='SOCIETY_ZIP', blank=True, null=True)  # Field name made lowercase.
    society_city = models.CharField(db_column='SOCIETY_CITY', max_length=250, blank=True, null=True)  # Field name made lowercase.
    society_state = models.CharField(db_column='SOCIETY_STATE', max_length=250, blank=True, null=True)  # Field name made lowercase.
    society_longitude = models.FloatField(db_column='SOCIETY_LONGITUDE', blank=True, null=True, default=0.0)  # Field name made lowercase.
    society_locality = models.CharField(db_column='SOCIETY_LOCALITY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    society_subarea = models.CharField(db_column='SOCIETY_SUBAREA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    society_latitude = models.FloatField(db_column='SOCIETY_LATITUDE', blank=True, null=True, default=0.0)  # Field name made lowercase.
    society_location_type = models.CharField(db_column='SOCIETY_LOCATION_TYPE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    society_type_quality = models.CharField(db_column='SOCIETY_TYPE_QUALITY', max_length=30, blank=True, null=True)  # Field name made lowercase.
    society_type_quantity = models.CharField(db_column='SOCIETY_TYPE_QUANTITY', max_length=30, blank=True, null=True)  # Field name made lowercase.
    society_off = models.BooleanField(db_column='SOCIETY_OFF', default=False)
    society_weekly_off = models.CharField(db_column='SOCIETY_WEEKLY_OFF', max_length=30, blank=True, null=True)
    society_count = models.BooleanField(db_column='SOCIETY_COUNT', default=True)
    society_ratings = models.BooleanField(db_column='SOCIETY_RATINGS', default=True)
    flat_count = models.IntegerField(db_column='FLAT_COUNT', blank=True, null=True)
    resident_count = models.IntegerField(db_column='RESIDENT_COUNT', blank=True, null=True)
    vacant_flat_count = models.IntegerField(db_column='VACANT_FLAT_COUNT', null=True)
    avg_household_occupants = models.IntegerField(db_column='AVG_HOUSEHOLD_OCCUPANTS', null=True)
    service_household_count = models.IntegerField(db_column='SERVICE_HOUSEHOLD_COUNT', null=True)
    working_women_count = models.IntegerField(db_column='WORKING_WOMEN_COUNT', null=True)
    bachelor_tenants_allowed = models.CharField(db_column='BACHELOR_TENANTS_ALLOWED', max_length=5, null=True)
    pg_flat_count = models.IntegerField(db_column='PG_FLAT_COUNT', null=True)
    women_occupants = models.IntegerField(db_column='WOMEN_OCCUPANTS', null=True)
    avg_pg_occupancy = models.IntegerField(db_column='AVG_PG_OCCUPANCY', null=True)
    cars_count = models.IntegerField(db_column='CARS_COUNT', blank=True, null=True)  # Field name made lowercase.
    luxury_cars_count = models.IntegerField(db_column='LUXURY_CARS_COUNT', blank=True, null=True)  # Field name made lowercase.
    lift_count = models.IntegerField(db_column='LIFT_COUNT', blank=True, null=True)  # Field name made lowercase.
    machadalo_index = models.FloatField(db_column='MACHADALO_INDEX', blank=True, null=True, default=0.0)  # Field name made lowercase.
    average_rent = models.FloatField(db_column='AVERAGE_RENT', blank=True, null=True)  # Field name made lowercase.
    food_tasting_allowed = models.CharField(db_column='FOOD_TASTING_ALLOWED', max_length=5, blank=True, null=True)  # Field name made lowercase.
    events_occurance = models.CharField(db_column='EVENTS_OCCURANCE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    preferred_business_type = models.CharField(db_column='SOCIETIES_PREFERRED_BUSINESS_TYPE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    preferred_business_id = models.CharField(db_column='SOCIETIES_PREFERRED_BUSINESS_ID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    business_type_not_allowed = models.CharField(db_column='BUSINESS_TYPE_NOT_ALLOWED', max_length=50, blank=True, null=True)  # Field name made lowercase.
    business_id_not_allowed = models.CharField(db_column='BUSINESS_ID_NOT_ALLOWED', max_length=50, blank=True, null=True)  # Field name made lowercase.
    referred_by = models.CharField(db_column='REFERRED_BY', max_length=5, blank=True, null=True)  # Field name made lowercase.
    contact_person_count = models.IntegerField(db_column='CONTACT_PERSON_COUNT', blank=True, null=True)  # Field name made lowercase.
    walking_area_available = models.CharField(db_column='WALKING_AREA_AVAILABLE', max_length=45, blank=True, null=True)  # Field name made lowercase.
    walking_area_size = models.CharField(db_column='WALKING_AREA_SIZE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    count_0_5 = models.IntegerField(db_column='COUNT_0-5', blank=True, null=True)  # Field name made lowercase.
    count_5_15 = models.IntegerField(db_column='COUNT_5-15', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    count_15_25 = models.IntegerField(db_column='COUNT_15-25', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    count_25_60 = models.IntegerField(db_column='COUNT_25-60', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    count_60above = models.IntegerField(db_column='count_60above', blank=True, null=True)  # Field name made lowercase.
    age_group_0_6 = models.IntegerField(blank=True, default=0)
    age_group_7_18 = models.IntegerField(blank=True, default=0)
    flat_type_count = models.IntegerField(db_column='FLAT_TYPE_COUNT', blank=True, null=True)  # Field name made lowercase.
    flat_avg_size = models.IntegerField(db_column='FLAT_AVG_SIZE', blank=True, null=True)  # Field name made lowercase.
    flat_avg_rental_persqft = models.IntegerField(db_column='FLAT_AVG_RENTAL_PERSQFT', blank=True, null=True)  # Field name made lowercase.
    flat_sale_cost_persqft = models.IntegerField(db_column='FLAT_SALE_COST_PERSQFT', blank=True, null=True)
    past_campaign_occurred = models.CharField(db_column='PAST_CAMPAIGN_OCCURRED', max_length=5, null=True)
    past_collections_stalls = models.IntegerField(db_column='PAST_YEAR_COLLECTIONS_STALLS', null=True)  # Field name made lowercase.
    past_collections_car = models.IntegerField(db_column='PAST_YEAR_COLLECTIONS_CAR', null=True)  # Field name made lowercase.
    past_collections_poster = models.IntegerField(db_column='PAST_YEAR_COLLECTIONS_POSTER', null=True)  # Field name made lowercase.
    past_collections_banners = models.IntegerField(db_column='PAST_YEAR_COLLECTIONS_BANNERS', null=True)  # Field name made lowercase.
    past_collections_standee = models.IntegerField(db_column='PAST_YEAR_COLLECTIONS_STANDEE', null=True)  # Field name made lowercase.
    past_sponsorship_collection_events = models.IntegerField(db_column='PAST_YEAR_SPONSORSHIP_COLLECTION_EVENTS', null=True)  # Field name made lowercase.
    past_total_sponsorship = models.IntegerField(db_column='PAST_YEAR_TOTAL_SPONSORSHIP', null=True)  # Field name made lowercase.
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID, related_name='societies', db_column='CREATED_BY', blank=True, null=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(db_column='CREATED_ON', auto_now_add=True)
    total_ad_spaces = models.IntegerField(db_column='TOTAL_AD_SPACES', null=True)
    tower_count = models.IntegerField(db_column='TOWER_COUNT', blank=True, null=True)  # Field name made lowercase.
    standee_count = models.IntegerField(db_column='STANDEE_COUNT', blank=True, null=True)  # Field name made lowercase.
    stall_count = models.IntegerField(db_column='STALL_COUNT', blank=True, null=True)  # Field name made lowercase.
    banner_count = models.IntegerField(db_column='BANNER_COUNT', blank=True, null=True)  # Field name made lowercase.
    total_campaign = models.IntegerField(db_column='TOTAL_CAMPAIGN', blank=True, null=True)  # Field name made lowercase.
    payment_details_available = models.BooleanField(db_column='PAYMENT_DETAILS_AVAILABLE', default=False)
    age_of_society = models.FloatField(db_column='AGE_OF_SOCIETY', blank=True, null=True)  # Field name made lowercase.
    name_for_payment = models.CharField(db_column='NAME_FOR_PAYMENT', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ifsc_code = models.CharField(db_column='IFSC_CODE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bank_name = models.CharField(db_column='BANK_NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    account_no = models.BigIntegerField (db_column='ACCOUNT_NUMBER', blank=True, null=True)  # Field name made lowercase.
    street_furniture_available = models.BooleanField(db_column='STREET_FURNITURE_AVAILABLE', default=False)  # Field name made lowercase. This field type is a guess.
    stall_timing = models.CharField(db_column='STALL_TIMING',max_length=10,blank=True, null=True)
    electricity_available  = models.BooleanField(db_column='ELECTRICITY_AVAILABLE',  default=False)
    sound_available = models.BooleanField(db_column='SOUND_AVAILABLE',  default=False)
    daily_electricity_charges = models.IntegerField(db_column='DAILY_ELECTRICITY_CHARGES',blank=True, null=True, default=0)
    poster_allowed_nb = models.BooleanField(db_column = 'POSTER_ALLOWED_NB', default=False)
    poster_allowed_lift = models.BooleanField(db_column = 'POSTER_ALLOWED_LIFT', default=False)
    standee_allowed = models.BooleanField(db_column = 'STANDEE_ALLOWED', default=False)
    flier_allowed = models.BooleanField(db_column = 'FLIER_ALLOWED', default=False)
    stall_allowed = models.BooleanField(db_column = 'STALL_ALLOWED', default=False)
    car_display_allowed = models.BooleanField(db_column='CAR_DISPLAY_ALLOWED', default=False)
    banner_allowed = models.BooleanField(db_column='BANNER_ALLOWED',default=False)
    total_tenant_flat_count = models.IntegerField(null=True, blank=True)
    landmark = models.CharField(max_length=255, null=True, blank=True)
    feedback = models.CharField(max_length=255, null=True, blank=True)
    representative = models.ForeignKey('Organisation', null=True, blank=True)

    def get_society_image(self):
        try:
            #Start : Code changed to save tag of image by name field
            image_list = list(self.images.all().filter(name="Society")[:1])
            #End : Code changed to save tag of image by name field
        except:
            return None
        if image_list:
          return image_list[0]
        return None

    def get_contact_list(self):
        try:
            return ContactDetails.objects.filter(object_id = self.supplier_id, content_type = ContentType.objects.get_for_models(SupplierTypeSociety).values()[0].id)
        except:
            return None

    def get_reference(self):
        try:
            return self.contacts.all().get(contact_type="Reference")
        except:
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

    def is_past_details_available(self):
        if (self.past_collections_poster is not None or self.past_collections_stalls is not None or self.past_total_sponsorship is not None):
            return True
        return False

    def is_demographic_details_available(self):
        if (self.count_0_5 is not None or self.count_5_15 is not None or self.count_15_25 is not None or self.count_25_60 is not None or self.count_60above is not None):
            return True
        return False

    def is_business_preferences_available(self):
        if (self.preferred_business_type is not None or self.business_type_not_allowed is not None):
            return True
        return False

    class Meta:

        db_table = 'supplier_society'


# Need to remove- verify
class SocietyInventoryBooking(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    campaign = models.ForeignKey('Campaign', related_name='inventory_bookings', db_column='CAMPAIGN_ID', null=True, on_delete=models.CASCADE)
    society = models.ForeignKey(SupplierTypeSociety, related_name='inventory_bookings', db_column='SUPPLIER_ID', null=True, on_delete=models.CASCADE)
    adinventory_type = models.ForeignKey('CampaignTypeMapping', db_column='ADINVENTORY_TYPE', null=True, on_delete=models.CASCADE)
    ad_location = models.CharField(db_column='AD_LOCATION', max_length=50, blank=True) #ops to enter the location during finalization
    start_date = models.DateField(db_column='START_DATE', null=True)
    end_date = models.DateField(db_column='END_DATE', null=True)
    audit_date = models.DateField(db_column='AUDIT_DATE', null=True)
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.CharField(max_length=12, null=True)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    objects = managers.GeneralManager()

    def get_type(self):
        try:
            return self.adinventory_type
        except:
            return None

    def get_society(self):
        try:
            return self.society
        except:
            return None

    def get_audit_type(self):
        if (self.start_date == date.today()):
            return 'Release'
        elif (self.audit_date == date.today()):
            return 'Audit'
        else:
            return None

    def get_status(self):
        return 'Pending'

    def get_price(self):
        try:
            price = PriceMappingDefault.objects.filter(object_id=self.object_id, adinventory_type__adinventory_name=self.adinventory_type.type.upper()).first().supplier_price
            return price
        except:
            return None

    class Meta:

        db_table = 'society_inventory_booking'
