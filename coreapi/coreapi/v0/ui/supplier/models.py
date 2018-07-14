from django.db import models
from django.conf import settings
from v0.models import BaseModel, managers, fields
from v0.ui.account.models import ContactDetailsGeneric

RETAIL_SHOP_TYPE = (
    ('GROCERY_STORE', 'GROCERY_STORE'),
    ('ELECTRONIC_STORE', 'ELECTRONIC_STORE'),
    ('SANITARY_STORE', 'SANITARY_STORE'),
    ('STATIONARY_STORE', 'STATIONARY_STORE')
)

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

class SupplierTypeCode(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    supplier_type_name = models.CharField(db_column='SUPPLIER_TYPE_NAME', max_length=20, null=True)
    supplier_type_code = models.CharField(db_column='SUPPLIER_TYPE_CODE', max_length=5, null=True)

    class Meta:

        db_table = 'supplier_type_code'

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

class SupplierTypeBusShelter(BasicSupplierDetails):
    """
    model inherits basic supplier fields from abstract model BasicSupplierDetails
    """
    lit_status = models.CharField(max_length=255, null=True, blank=True)
    halt_buses_count = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'supplier_bus_shelter'

class SupplierAmenitiesMap(BaseModel):
    """
    This table represents the idea that each supplier can have multiple amenities
    """

    content_type = models.ForeignKey('ContentType')
    object_id = models.CharField(max_length=1000)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    amenity = models.ForeignKey('Amenity', null=True, blank=True)

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