from django.db import models
from django.conf import settings
from v0.models import BaseModel, managers, fields
from django.contrib.contenttypes.models import ContentType
from v0.constants import supplier_id_max_length


def getPriceDict():
    price_dict = {
        'Standee': {
            'duration': '1',
            'types': {
                'Small': '3',
                'Medium': '4',
                # 'Large'  : '5'
            }
        },

        'Flier': {
            'duration': '5',
            'types': {
                'Door-to-Door': '12',
                'Mailbox': '13',
            }
        },

        'Stall': {
            'duration': '5',
            'types': {
                'Canopy': '6',
                'Small': '7',
                'Large': '8',
                # 'Customize' : '9'
            }
        }
    }

    return price_dict

class DurationType(BaseModel):
    id = models.AutoField(db_column='ID', primary_key=True)
    duration_name = models.CharField(db_column='DURATION_NAME', max_length=20)
    days_count = models.CharField(db_column='DAYS_COUNT', max_length=10)

    class Meta:
        db_table = 'duration_type'

class DoorToDoorInfo(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    supplier = models.ForeignKey('SupplierTypeSociety', related_name='door_to_doors', db_column='SUPPLIER_ID', blank=True, null=True, on_delete=models.CASCADE)
    adinventory_id = models.CharField(db_column='ADINVENTORY_ID', max_length=22, blank=True, null=True)
    flier_distribution_frequency_door = models.CharField(db_column='FLIER_DISTRIBUTION_FREQUENCY_DOOR', max_length=20, blank=True, null=True)
    door_to_door_inventory_status = models.CharField(db_column='DOOR_TO_DOOR_INVENTORY_STATUS', max_length=15, blank=True, null=True)
    door_to_door_price_society = models.FloatField(db_column='DOOR_TO_DOOR_PRICE_SOCIETY', default=0.0, blank=True, null=True)
    door_to_door_price_business = models.FloatField(db_column='DOOR_TO_DOOR_PRICE_BUSINESS', default=0.0, blank=True, null=True)
    master_door_to_door_flyer_price_society = models.FloatField(db_column='MASTER_DOOR_TO_DOOR_FLYER_PRICE_SOCIETY', default=0.0, blank=True, null=True)
    master_door_to_door_flyer_price_business = models.FloatField(db_column='MASTER_DOOR_TO_DOOR_FLYER_PRICE_BUSINESS', default=0.0, blank=True, null=True)
    leaflet_handover = models.CharField(db_column='LEAFLET_HANDOVER', max_length=50, blank=True, null=True)
    activities = models.CharField(db_column='ACTIVITIES', max_length=255, blank=True, null=True)
    banner_spaces_count = models.IntegerField(db_column='BANNER_SPACES_COUNT', blank=True, null=True)

    class Meta:

        db_table = 'door_to_door_info'

class PriceMapping(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    supplier = models.ForeignKey('SupplierTypeSociety', db_column='SUPPLIER_ID', related_name='inv_prices', blank=True, null=True, on_delete=models.CASCADE)
    adinventory_id = models.ForeignKey('AdInventoryLocationMapping', db_column='ADINVENTORY_LOCATION_MAPPING_ID', related_name='prices', blank=True, null=True, on_delete=models.CASCADE)
    adinventory_type = models.ForeignKey('AdInventoryType', db_column='ADINVENTORY_TYPE_ID', blank=True, null=True, on_delete=models.CASCADE)
    society_price = models.IntegerField(db_column='SUGGESTED_SOCIETY_PRICE')
    business_price = models.IntegerField(db_column='ACTUAL_SOCIETY_PRICE')
    duration_type = models.ForeignKey('DurationType', db_column='DURATION_ID', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'price_mapping'

class PriceMappingDefault(BaseModel):
    id = models.AutoField(db_column='ID', primary_key=True)
    supplier = models.ForeignKey('SupplierTypeSociety', db_column='SUPPLIER_ID', related_name='default_prices', blank=True, null=True, on_delete=models.CASCADE)
    adinventory_type = models.ForeignKey('AdInventoryType', db_column='ADINVENTORY_TYPE_ID', blank=True, null=True, on_delete=models.CASCADE)
    suggested_supplier_price = models.IntegerField(db_column='SUGGESTED_SOCIETY_PRICE', null=True, blank=True)
    actual_supplier_price = models.IntegerField(db_column='ACTUAL_SOCIETY_PRICE', null=True, blank=True)
    duration_type = models.ForeignKey('DurationType', db_column='DURATION_ID', blank=True, null=True, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.CharField(db_index=True, max_length=supplier_id_max_length, null=True)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    objects = managers.GeneralManager()

    class Meta:
        db_table = 'price_mapping_default'

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

class AbstractGeneralCost(BaseModel):
    """
    This class is an abstract class for all types of cost's. Any type of cost example, PrintingCost, LogisticCost,
    SpaceBookingCost etc are inherited from this basic cost table. A proposal version can only have one PrintingCost,
    one LogisticCost, one SpaceBookingCost etc, hence this table is linked to proposal version by ONE to ONE relation.
    also one mastercost sheet will only have one "cost", doesn't matter what type ( ofcourse different types of costs, but all are actualy
    a cost ! ).
    """
    proposal_master_cost = models.ForeignKey('ProposalMasterCost', null=True, blank=True)
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

class AuditDate(BaseModel):
    """
    A particular inventory can have multiple audit dates
    """
    shortlisted_inventory = models.ForeignKey(ShortlistedInventoryPricingDetails, null=True, blank=True)
    audit_date = models.DateTimeField(null=True, blank=True)
    audited_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)

    class Meta:
        db_table = 'audit_date'

class AuditorSocietyMapping(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    user_id = models.IntegerField(db_column='USER_ID', null=True) #change to user id FK
    society = models.ForeignKey('SupplierTypeSociety', related_name='auditors', db_column='SUPPLIER_ID', null=True, on_delete=models.CASCADE)

    class Meta:

        db_table = 'auditor_society_mapping'

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