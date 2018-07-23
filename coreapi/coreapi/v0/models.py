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

from v0.constants import supplier_id_max_length
from v0.ui.user.models import BaseUser
from v0.ui.base.models import BaseModel
from v0.ui.campaign.models import CampaignAssignment
from v0.ui.organisation.models import Organisation
from v0.ui.proposal.models import SpaceMapping, SpaceMappingVersion
from v0.ui.supplier.models import SupplierTypeCorporate

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



class ImageMapping(BaseModel):
    id = models.AutoField(db_column='ID', primary_key=True)
    location_id = models.CharField(db_column='LOCATION_ID', max_length=20, blank=True, null=True)
    location_type = models.CharField(db_column='LOCATION_TYPE', max_length=20, blank=True, null=True)
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

class DurationType(BaseModel):
    id = models.AutoField(db_column='ID', primary_key=True)
    duration_name = models.CharField(db_column='DURATION_NAME', max_length=20)
    days_count = models.CharField(db_column='DAYS_COUNT', max_length=10)

    class Meta:
        db_table = 'duration_type'


class UserInquiry(models.Model):
    inquiry_id = models.AutoField(db_column='INQUIRY_ID', primary_key=True)
    company_name = models.CharField(db_column='COMPANY_NAME', max_length=40)
    contact_person_name = models.CharField(db_column='CONTACT_PERSON_NAME', max_length=40, blank=True, null=True)
    email = models.CharField(db_column='EMAIL', max_length=40, blank=True, null=True)
    phone = models.IntegerField(db_column='PHONE', blank=True, null=True)
    inquiry_details = models.TextField(db_column='INQUIRY_DETAILS')

    class Meta:

        db_table = 'user_inquiry'

class SocietyMajorEvents(BaseModel):
    id = models.AutoField(db_column='ID', primary_key=True)
    supplier = models.ForeignKey('SupplierTypeSociety', related_name='society_events', db_column='SUPPLIER_ID', blank=True, null=True, on_delete=models.CASCADE)
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
    event_id = models.AutoField(db_column='EVENT_ID', primary_key=True)
    supplier = models.ForeignKey('SupplierTypeSociety', related_name='events', db_column='SUPPLIER_ID', blank=True, null=True, on_delete=models.CASCADE)
    event_name = models.CharField(db_column='EVENT_NAME', max_length=20, blank=True, null=True)
    event_location = models.CharField(db_column='EVENT_LOCATION', max_length=50, blank=True, null=True)
    past_gathering_per_event = models.IntegerField(db_column='PAST_GATHERING_PER_EVENT', blank=True, null=True)
    start_day = models.CharField(db_column='START_DAY', max_length=30, blank=True, null=True)
    end_day = models.CharField(db_column='END_DAY', max_length=30, blank=True, null=True)
    important_day = models.CharField(db_column='IMPORTANT_DAY', max_length=30, blank=True, null=True)
    activities = models.CharField(db_column='ACTIVITIES', max_length=50, blank=True, null=True)
    stall_spaces_count = models.IntegerField(db_column='STALL_SPACES_COUNT', blank=True, null=True)
    banner_spaces_count = models.IntegerField(db_column='BANNER_SPACES_COUNT', blank=True, null=True)
    poster_spaces_count = models.IntegerField(db_column='POSTER_SPACES_COUNT', blank=True, null=True)
    standee_spaces_count = models.IntegerField(db_column='STANDEE_SPACES_COUNT', blank=True, null=True)
    event_status = models.CharField(db_column='EVENT_STATUS', max_length=10, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.CharField(max_length=supplier_id_max_length, null=True)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    objects = managers.GeneralManager()

    class Meta:

        db_table = 'events'

# Check whether it is being used or not



class OperationsInfo(models.Model):
    operator_id = models.CharField(db_column='OPERATOR_ID', primary_key=True, max_length=10)
    operator_name = models.CharField(db_column='OPERATOR_NAME', max_length=100, blank=True, null=True)
    operator_email = models.CharField(db_column='OPERATOR_EMAIL', max_length=50, blank=True, null=True)
    operator_company = models.CharField(db_column='OPERATOR_COMPANY', max_length=100, blank=True, null=True)
    operator_phone_number = models.IntegerField(db_column='OPERATOR_PHONE_NUMBER', blank=True, null=True)
    comments_1 = models.CharField(db_column='COMMENTS_1', max_length=500, blank=True, null=True)
    comments_2 = models.CharField(db_column='COMMENTS_2', max_length=500, blank=True, null=True)
    company_id = models.CharField(db_column='COMPANY_ID', max_length=50, blank=True, null=True)
    company_address = models.CharField(db_column='COMPANY_ADDRESS', max_length=250, blank=True, null=True)

    class Meta:

        db_table = 'operations_info'

class Signup(models.Model):
    user_id = models.AutoField(db_column='USER_ID', primary_key=True)
    first_name = models.TextField(db_column='FIRST_NAME', blank=True, null=True)
    email = models.TextField(db_column='EMAIL', blank=True, null=True)
    password = models.TextField(db_column='PASSWORD', blank=True, null=True)
    login_type = models.TextField(db_column='LOGIN_TYPE', blank=True, null=True)
    system_generated_id = models.BigIntegerField(db_column='SYSTEM_GENERATED_ID')
    adminstrator_approved = models.CharField(db_column='ADMINSTRATOR_APPROVED', max_length=255, blank=True, null=True)
    company_name = models.CharField(db_column='COMPANY_NAME', max_length=255, blank=True, null=True)
    name = models.CharField(db_column='NAME', max_length=255, blank=True, null=True)
    mobile_no = models.CharField(db_column='MOBILE_NO', max_length=255, blank=True, null=True)
    signup_status = models.CharField(db_column='SIGNUP_STATUS', max_length=255, blank=True, null=True)

    class Meta:

        db_table = 'signup'

class CorporateParkCompanyList(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.CharField(db_column='COMPANY_NAME',max_length=50, blank=True, null=True)
    supplier_id = models.ForeignKey(SupplierTypeCorporate, db_column='CORPORATEPARK_ID', related_name='corporatecompany', blank=True, null=True, on_delete=models.CASCADE)

    def get_company_details(self):
        return self.companydetails.all()

    class Meta:
      db_table = 'corporateparkcompanylist'

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

class FlatTypeCode(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    flat_type_name = models.CharField(db_column='FLAT_TYPE_NAME', max_length=20, null=True)
    flat_type_code = models.CharField(db_column='FLAT_TYPE_CODE', max_length=5, null=True)

    class Meta:

        db_table = 'flat_type_code'

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
#     corporatepark_id = models.ForeignKey(SupplierTypeCorporate, db_column='CORPORATEPARK_NAME', related_name='corporatecompany', blank=True, null=True, on_delete=models.CASCADE)

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


# this is giving problems



class Filters(BaseModel):
    """
    Stores all kinds of filters and there respective codes. Filters are used when you filter all the suppliers
    on the basis of what inventories you would like to have in there, etc. because different suppliers can have
    different types of filters, we have content_type field for capturing that. These filters are predefined in constants
    and are populated from there.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID)
    center = models.ForeignKey('ProposalCenterMapping', null=True, blank=True)
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

class Amenity(BaseModel):
    """
    Stores individual amenities. There basic details.
    """
    name = models.CharField(max_length=1000)
    code = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        db_table = 'amenities'

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