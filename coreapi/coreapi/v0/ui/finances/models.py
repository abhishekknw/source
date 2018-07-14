from django.db import models
from django.conf import settings
from v0.models import BaseModel, managers, fields

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
    supplier_type = models.ForeignKey('ContentType', null=True, blank=True)

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
    shortlisted_inventory = models.ForeignKey('ShortlistedInventoryPricingDetails', null=True, blank=True)
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
