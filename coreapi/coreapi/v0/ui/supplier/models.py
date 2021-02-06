from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields
from v0.ui.base.models import BaseModel
from v0.ui.account.models import ContactDetailsGeneric, ContactDetails
from v0.ui.proposal.models import SupplierPhase
from v0 import managers

Q = models.Q

RETAIL_SHOP_TYPE = (
    # ('GROCERY_STORE', 'GROCERY_STORE'),
    # ('ELECTRONIC_STORE', 'ELECTRONIC_STORE'),
    # ('SANITARY_STORE', 'SANITARY_STORE'),
    # ('STATIONARY_STORE', 'STATIONARY_STORE'),
    ('Toy Store', 'Toy Store'),
    ('Sports Goods', 'Sports Goods'),
    ('Electronic Goods', 'Electronic Goods'),
    ('Sanitary Goods', 'Sanitary Goods'),
    ('Grocery Goods', 'Grocery Goods'),
    ('Stationery Goods', 'Stationery Goods'),
    ('Merchandise Goods', 'Merchandise Goods'),
    ('Mobile Store', 'Mobile Store'),
    ('Mixed Store', 'Mixed Store'),
    ('Hypermart', 'Hypermart'),
    ('Jewelry Store', 'Jewelry Store'),
    ('Auto Dealership Store', 'Auto Dealership Store'),
    ('Shoes Store', 'Shoes Store'),
    ('Mall', 'Mall'),
    ('Gaming Zone', 'Gaming Zone'),
    ('FND (Food & Dining)', 'FND (Food & Dining)'),
)

FLAT_COUNT_TYPE = (
    ('1-150', '1-150'),
    ('151-400', '151-400'),
    ('401+', '401+')
)

class CorporateCompanyDetails(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    company_id = models.ForeignKey('CorporateParkCompanyList', db_column='COMPANY_ID', related_name='companydetails', blank=True, null=True, on_delete=models.CASCADE)
    building_name = models.CharField(db_column='BUILDING_NAME', max_length=20, blank=True, null=True)
    wing_name = models.CharField(db_column='WING_NAME', max_length=20, blank=True, null=True)

    def get_floors(self):
        return self.wingfloor.all()

    class Meta:
        db_table='corporate_company_details'

class CorporateParkCompanyList(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.CharField(db_column='COMPANY_NAME',max_length=50, blank=True, null=True)
    supplier_id = models.ForeignKey('SupplierTypeCorporate', db_column='CORPORATEPARK_ID', related_name='corporatecompany', blank=True, null=True, on_delete=models.CASCADE)
    employeeCount = models.IntegerField(db_column='EMPLOYEE_COUNT',null=True, blank=True)

    def get_company_details(self):
        return self.companydetails.all()

    class Meta:
      db_table = 'corporateparkcompanylist'

class FlatTypeCode(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    flat_type_name = models.CharField(db_column='FLAT_TYPE_NAME', max_length=20, null=True)
    flat_type_code = models.CharField(db_column='FLAT_TYPE_CODE', max_length=5, null=True)

    class Meta:

        db_table = 'flat_type_code'

class BasicSupplierDetails(BaseModel):
    """
    This is an abstract base class for all the suppliers. As we know more common fields, add
    them here in order of relevance and run python manage.py makemigrations. all the models who
    inherit from this class will have those fields automatically.

    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID, on_delete=models.CASCADE)
    supplier_id = models.CharField(db_index=True, max_length=20, primary_key=True)
    supplier_code = models.CharField(max_length=3, null=True)
    name = models.CharField(max_length=70, null=True, blank=True)
    locality_rating = models.CharField(max_length=50, null=True, blank=True)
    quality_rating = models.CharField(max_length=50, null=True, blank=True)
    machadalo_index = models.CharField(max_length=30, null=True, blank=True)
    sales_allowed = models.BooleanField(default=False)
    objects = managers.GeneralManager()


    class Meta:
        abstract = True


SUPPLIER_STATUS = (
    ('Tapped', 'Tapped'),
    ('LetterGiven', 'LetterGiven'),
    ('MeetingRequired', 'MeetingRequired'),
    ('Other', 'Other')
)


class SupplierTypeSociety(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID, on_delete=models.CASCADE)
    objects = managers.GeneralManager()
    supplier_id = models.CharField(db_index=True, db_column='SUPPLIER_ID', primary_key=True, max_length=20)  # Field name made lowercase.
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
    flat_count_type = models.CharField(blank=True, null=True, choices=FLAT_COUNT_TYPE, max_length=55)
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
    representative = models.ForeignKey('Organisation', null=True, blank=True, on_delete=models.CASCADE)
    supplier_status = models.CharField(max_length=80, null=True,  choices=SUPPLIER_STATUS)
    comments = models.CharField(max_length=255, null=True, blank=True)
    relationship_manager = models.CharField(max_length=50, null=True, blank=True)
    rating = models.CharField(max_length=255, null=True, blank=True)

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
            return ContactDetails.objects.filter(~Q(contact_type="Reference"), object_id = self.supplier_id)
        except:
            return None

    def get_reference(self):
        try:
            return ContactDetails.objects.filter(contact_type="Reference", object_id = self.supplier_id)
        except:
            return None

    def is_contact_available(self):
        contacts = self.get_contact_list()
        if contacts and len(contacts) > 0 :
            return True
        return False

    def is_reference_available(self):
        if self.get_reference() and len(self.get_reference()) > 0:
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


class SupplierTypeCode(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    supplier_type_name = models.CharField(db_column='SUPPLIER_TYPE_NAME', max_length=35, null=True)
    supplier_type_code = models.CharField(db_column='SUPPLIER_TYPE_CODE', max_length=5, null=True)
    unit_primary_count = models.CharField(max_length=30, null=True, blank=True)
    unit_secondary_count = models.CharField(max_length=30, null=True, blank=True)
    unit_tertiary_count = models.CharField(max_length=30, null=True, blank=True)
    comments = models.CharField(max_length=255, null=True, blank=True)
    lower = models.CharField(max_length=30, null=True, blank=True)  #range for suppliers unit count
    middle = models.CharField(max_length=30, null=True, blank=True)
    upper = models.CharField(max_length=30, null=True, blank=True)
    created_at = models.DateTimeField(editable=False, default=settings.DEFAULT_DATE)
    updated_at = models.DateTimeField(editable=False, default=settings.DEFAULT_DATE)

    class Meta:
        db_table = 'supplier_type_code'


class SupplierTypeSalon(BasicSupplierDetails):
    salon_type = models.CharField(db_column='SALON_TYPE', max_length=30, blank=True, null=True)
    category = models.CharField(db_column='CATEGORY', max_length=30, blank=True, null=True)
    salon_type_chain = models.CharField(db_column='SALON_TYPE_CHAIN', max_length=30, blank=True, null=True)
    footfall_day = models.IntegerField(db_column='FOOTFALL_DAY', blank=True, null=True)
    footfall_week = models.IntegerField(db_column='FOOTFALL_WEEL', blank=True, null=True)
    isspaavailable = models.BooleanField(db_column='ISSPAAVAILABLE', default=False)
    advertising_media = models.CharField(db_column='AD_MEDIA', max_length=30, blank=True, null=True)
    shop_size = models.IntegerField(db_column='SHOP_SIZE', blank=True, null=True)
    floor_size = models.IntegerField(db_column='FLOOR_SIZE', blank=True, null=True)
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
    representative = models.ForeignKey('Organisation', null=True, blank=True, on_delete=models.CASCADE)
    comments = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        db_table = 'supplier_salon'


class CorporateBuilding(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    building_name = models.CharField(db_column='BUILDING_NAME', max_length=50, null=True, blank=True)
    number_of_wings = models.IntegerField(db_column='NUMBER_OF_WINGS', null=True, blank=True)
    corporatepark_id = models.ForeignKey('SupplierTypeCorporate',db_index=True, db_column='CORPORATE_ID',related_name='corporatebuilding', blank=True, null=True, on_delete=models.CASCADE)

    def get_wings(self):
        return self.buildingwing.all()

    class Meta:
        db_table='corporate_building'


class SupplierTypeGym(BasicSupplierDetails):
    gym_type = models.CharField(max_length=30, blank=True, null=True)
    category = models.CharField(max_length=30, blank=True, null=True)
    gym_type_chain = models.CharField(max_length=30, blank=True, null=True)
    chain_origin = models.CharField(max_length=30, blank=True, null=True)
    totalmembership_perannum = models.IntegerField(blank=True, null=True)
    footfall_day = models.IntegerField(blank=True, null=True)
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
    representative = models.ForeignKey('Organisation', null=True, blank=True, on_delete=models.CASCADE)
    comments = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'supplier_gym'


class SupplierEducationalInstitute(BasicSupplierDetails):
    inst_type = models.CharField(max_length=200, null=True, blank=True)
    inst_sub_type = models.CharField(max_length=200, null=True, blank=True)
    educationBoard = models.CharField(max_length=200, null=True, blank=True)
    comments = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'supplier_educational_institute'


class SupplierHording(BasicSupplierDetails):
    owner_name = models.CharField(max_length=255, null=True, blank=True)
    external_Number = models.CharField(max_length=255, null=True, blank=True)
    length = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    length_of_gantry = models.IntegerField(blank=True, null=True)
    width_of_gantry = models.IntegerField(blank=True, null=True)
    height_of_gantry = models.IntegerField(blank=True, null=True)
    force_majeure_clause = models.CharField(choices=(( 'YES', 'YES' ),  ('NO', 'NO')), max_length=10, blank=True, null=True)
    terms_around_print_mount = models.IntegerField(blank=True, null=True)
    cost_per_sqft = models.IntegerField(blank=True, null=True)
    cost_of_branding_space = models.IntegerField(blank=True, null=True)
    printing_and_mounting_cost = models.IntegerField(blank=True, null=True)
    contact_number = models.CharField(max_length=255, null=True, blank=True)
    cluster_of_hording = models.CharField(choices=(( 'YES', 'YES' ),  ('NO', 'NO')), max_length=10, blank=True, null=True)
    traffic_junction = models.CharField(max_length=255, null=True, blank=True)
    comments = models.CharField(max_length=255, null=True, blank=True)
    average_peakHourTraffic = models.CharField(max_length=255, null=True, blank=True)
    average_nonPeakHourTraffic = models.CharField(max_length=255, null=True, blank=True)
    average_pedestrianDailyCount = models.CharField(max_length=255, null=True, blank=True)
    lit_status = models.CharField(choices=(( 'YES', 'YES' ),  ('NO', 'NO')), max_length=10, blank=True, null=True)
    buses_count = models.IntegerField(blank=True, null=True)
    sequence_number = models.IntegerField(blank=True, null=True)
    signal_waiting_time = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'supplier_hording'        

#Check whether this model is being used or not
class SupplierInfo(models.Model):
    supplier_id = models.CharField(db_index=True, db_column='SUPPLIER_ID', primary_key=True, max_length=20)  # Field name made lowercase.
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


class SupplierTypeCorporate(BasicSupplierDetails):
    corporate_type = models.CharField(max_length=25,blank=True, null= True)
    industry_segment = models.CharField(max_length=30, blank=True, null=True)
    possession_year = models.CharField(max_length=5, blank=True, null=True)
    building_count = models.IntegerField(blank=True, null=True)
    floorperbuilding_count = models.IntegerField(blank=True, null=True)
    totalcompanies_count = models.IntegerField(blank=True, null=True)
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
    representative = models.ForeignKey('Organisation', null=True, blank=True, on_delete=models.CASCADE)
    name_for_payment = models.CharField(db_column='NAME_FOR_PAYMENT', max_length=100, blank=True,
                                        null=True)
    tower_count = models.IntegerField(db_column='TOWER_COUNT', blank=True, null=True)
    poster_allowed_nb = models.BooleanField(db_column='POSTER_ALLOWED_NB', default=False)
    poster_allowed_lift = models.BooleanField(db_column='POSTER_ALLOWED_LIFT', default=False)
    standee_allowed = models.BooleanField(db_column='STANDEE_ALLOWED', default=False)
    stall_allowed = models.BooleanField(db_column='STALL_ALLOWED', default=False)
    banner_allowed = models.BooleanField(db_column='BANNER_ALLOWED', default=False)
    supplier_status = models.CharField(max_length=80, null=True, choices=SUPPLIER_STATUS)
    comments = models.CharField(max_length=255, null=True, blank=True)
    relationship_manager = models.CharField(max_length=50, null=True, blank=True)
    rating = models.CharField(max_length=255, null=True, blank=True)
    feedback = models.CharField(max_length=250, null=True, blank=True)

    def get_buildings(self):
        return self.corporatebuilding.all()

    def get_corporate_companies(self):
        return self.corporatecompany.all()

    class Meta:
        db_table = 'supplier_corporate'


class SupplierTypeBusShelter(BasicSupplierDetails):
    """
    model inherits basic supplier fields from abstract model BasicSupplierDetails
    """
    lit_status = models.CharField(max_length=250, null=True, blank=True)
    halt_buses_count = models.IntegerField(null=True, blank=True, max_length=500)
    representative = models.ForeignKey('Organisation', null=True, blank=True, on_delete=models.CASCADE)
    average_down_boarding_daily_count = models.IntegerField(null=True, max_length=500, blank=True)
    average_on_boarding_daily_count = models.IntegerField(null=True, max_length=500, blank=True)
    external_number = models.CharField(max_length=200, null=True, blank=True)
    bus_shelter_road_name = models.CharField(max_length=200, null=True, blank=True)
    direction = models.CharField(max_length=200, null=True, blank=True)
    bus_shelter_supplier = models.CharField(max_length=200, null=True, blank=True)
    total_size = models.IntegerField(null=True, blank=True, max_length=500)
    size_top = models.IntegerField(null=True, blank=True, max_length=500)
    size_middle = models.IntegerField(null=True, blank=True, max_length=500)
    size_bottom = models.IntegerField(null=True, blank=True, max_length=500)
    size_side_ext = models.FloatField(null=True, blank=True)
    size_side_int = models.FloatField(null=True, blank=True)
    force_majeure_clause = models.CharField(max_length=200, null=True, blank=True)
    terms_print_mount = models.IntegerField(null=True, blank=True)
    type_road_status = models.CharField(max_length=200, null=True, blank=True)
    ac_hault = models.CharField(max_length=200, null=True, blank=True)
    type_bus_stand = models.CharField(max_length=200, null=True, blank=True)
    population_type = models.CharField(max_length=200, null=True, blank=True)
    cost_sqft = models.IntegerField(null=True, blank=True, max_length=500)
    cost = models.IntegerField(null=True, blank=True, max_length=500)
    print_cost = models.IntegerField(null=True, blank=True, max_length=500)
    bus_shelters_cluster = models.BooleanField(default=False)
    comments = models.CharField(max_length=255, null=True, blank=True)
    average_peak_hour_traffic = models.IntegerField(null=True, blank=True, max_length=500)
    average_non_peak_hour_traffic = models.IntegerField(null=True, blank=True, max_length=500)
    footfall_daily_count = models.IntegerField(null=True, blank=True, max_length=500)

    class Meta:
        db_table = 'supplier_bus_shelter'


class SupplierAmenitiesMap(BaseModel):
    """
    This table represents the idea that each supplier can have multiple amenities
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=1000)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    amenity = models.ForeignKey('Amenity', null=True, blank=True, on_delete=models.CASCADE)
    comments = models.TextField(blank=True, null=True)
    

    class Meta:
        db_table = 'supplier_amenities_map'

class SupplierTypeRetailShop(BasicSupplierDetails):
    """
    stores details of RETAIL TYPE SUPPLIER.
    """
    retail_shop_type = models.CharField(choices=RETAIL_SHOP_TYPE, max_length=255, null=True, blank=True)
    size = models.FloatField(null=True, blank=True)
    is_modern_trade = models.BooleanField(default=False)
    is_traditional = models.BooleanField(default=False)
    category_name = models.CharField(max_length=255, null=True, blank=True)
    store_size = models.CharField(max_length=250, blank=True, null=True)
    std_code = models.CharField(max_length=250, blank=True, null=True)
    salutation = models.CharField(max_length=250, blank=True, null=True)
    contact_name = models.CharField(max_length=250, blank=True, null=True)
    contact_type = models.CharField(max_length=250, blank=True, null=True)
    country_code = models.CharField(max_length=250, blank=True, null=True)
    email = models.CharField(max_length=250, blank=True, null=True)
    feedback = models.CharField(max_length=250, blank=True, null=True)
    mobile = models.CharField(max_length=250, blank=True, null=True)
    phone = models.CharField(max_length=250, blank=True, null=True)
    landmark = models.CharField(max_length=250, blank=True, null=True)
    comments = models.CharField(max_length=255, null=True, blank=True)
    rating = models.CharField(max_length=255, null=True, blank=True)
    food_tasting_allowed = models.BooleanField(default=False)
    representative = models.ForeignKey('Organisation', null=True, blank=True, on_delete=models.CASCADE)

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
    representative = models.ForeignKey('Organisation', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'supplier_type_bus_depot'


class SupplierMaster(BaseModel):
    """
    Master table for storing supplier ids of all type of suppliers and other common basic fileds
    """
    supplier_id = models.CharField(db_index=True, primary_key=True, max_length=20)
    supplier_name = models.CharField(max_length=70, null=True, blank=True)
    supplier_type = models.CharField(max_length=20, null=True, blank=True)
    unit_primary_count = models.IntegerField(null=True, blank=True)
    unit_secondary_count = models.IntegerField(null=True, blank=True)
    unit_tertiary_count = models.IntegerField(null=True, blank=True)
    representative = models.ForeignKey('Organisation', null=True, blank=True, on_delete=models.CASCADE)
    area = models.CharField(max_length=50, null=True, blank=True)
    subarea = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    landmark = models.CharField(max_length=50, null=True, blank=True)
    zipcode = models.IntegerField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True, default=0.0)
    longitude = models.FloatField(null=True, blank=True, default=0.0)
    feedback = models.CharField(null=True, blank=True, max_length=250)
    locality_rating = models.CharField(max_length=50, null=True, blank=True)
    quality_rating = models.CharField(max_length=50, null=True, blank=True)
    quantity_rating = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'supplier_master'


class AddressMaster(BaseModel):
    """
    Address table for storing addresses of all suppliers
    """
    supplier = models.OneToOneField('SupplierMaster', db_index=True, max_length=20, on_delete=models.CASCADE, related_name="address_supplier")
    address1 = models.CharField(max_length=250, null=True, blank=True)
    address2 = models.CharField(max_length=250, null=True, blank=True)
    area = models.CharField(max_length=255, null=True, blank=True)
    subarea = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=250, null=True, blank=True)
    state = models.CharField(max_length=250, null=True, blank=True)
    zipcode = models.IntegerField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True, default=0.0)
    longitude = models.FloatField(null=True, blank=True, default=0.0)
    nearest_landmark = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        db_table = 'address_master'

class SupplierRelationship(BaseModel):
    """
    Stores info about Suppliers who has retail shops inside them
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    society = models.ForeignKey('SupplierTypeSociety', db_column='society_id', on_delete=models.CASCADE)
    supplier_id = models.CharField(max_length=50, null=False)
    supplier_type = models.CharField(max_length=3, null=False)
    type = models.CharField(max_length=10, null=False, default='PREFERRED')

    class Meta:
        db_table = 'supplier_relationship'
        unique_together = ('society', 'supplier_id','type')

class SupplierBus(BasicSupplierDetails):
    comments = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'supplier_bus'

class SupplierGantry(BasicSupplierDetails):
    comments = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'supplier_gantry'

class SupplierRadioChannel(BasicSupplierDetails):
    comments = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'supplier_radio_channel'

class SupplierTvChannel(BasicSupplierDetails):
    comments = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'supplier_tv_channel'

class SupplierCorporates(BasicSupplierDetails):
    comments = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'supplier_type_corporates'

class SupplierTypeHospital(BasicSupplierDetails):
    comments = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'supplier_hospital'
