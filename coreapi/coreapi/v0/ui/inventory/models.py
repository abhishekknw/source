from v0 import managers
from django.db import models
from django.conf import settings
from v0.ui.base.models import BaseModel
from v0.ui.account.models import ContactDetails, PriceMappingDefault
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields
from datetime import date


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
