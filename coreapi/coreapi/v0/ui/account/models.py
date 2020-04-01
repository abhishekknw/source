from django.db import models
from django.conf import settings
from django.contrib.contenttypes import fields
from v0.ui.base.models import BaseModel
from v0 import managers
from django.contrib.contenttypes.models import ContentType
from v0.constants import supplier_id_max_length
from v0.ui.common.models import BaseUser


class Profile(BaseModel):
    """
    This model describes profile. a user can only have one profile.
    """
    name = models.CharField(max_length=255)
    organisation = models.ForeignKey('Organisation', on_delete=models.CASCADE)
    is_standard = models.BooleanField(default=False)

    class Meta:
        db_table = 'profile'

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

class BusinessAccountContact(BaseModel):
    id = models.AutoField(db_column='ID', primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=20)
    business_account_id = fields.GenericForeignKey('content_type','object_id')
    name = models.CharField(db_column='NAME', max_length=50, blank=True)
    designation = models.CharField(db_column='DESIGNATION', max_length=20, blank=True)
    department = models.CharField(db_column='DEPARTMENT', max_length=20, blank=True)
    phone = models.CharField(db_column='PHONE', max_length=10,  blank=True)
    email = models.CharField(db_column='EMAILID',  max_length=50, blank=True)
    spoc = models.BooleanField(db_column='SPOC', default=False)
    comments = models.TextField(db_column='COMMENTS',  max_length=100, blank=True)

    class Meta:
        db_table = 'business_account_contact'


class BusinessInfo(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID, on_delete=models.CASCADE)
    business_id = models.CharField(db_column='BUSINESS_ID',max_length=15, primary_key=True)
    name = models.CharField(db_column='NAME', max_length=50, blank=True) ## changed -> name
    type_name = models.ForeignKey('BusinessTypes',related_name='type_set',db_column='TYPE', blank=False,null=False, on_delete=models.CASCADE) ## changed -> CharField
    sub_type = models.ForeignKey('BusinessSubTypes',related_name='sub_type_set',db_column='SUB_TYPE', blank=False, null=False, on_delete=models.CASCADE) ## changed -> CharField
    phone = models.CharField(db_column='PHONE', max_length=10,  blank=True)
    email = models.CharField(db_column='EMAILID',  max_length=50, blank=True)
    address = models.CharField(db_column='ADDRESS',  max_length=100, blank=True)
    reference_name = models.CharField(db_column='REFERENCE_NAME', max_length=50, blank=True)
    reference_phone = models.CharField(db_column='REFERENCE_PHONE', max_length=10, blank=True)
    reference_email = models.CharField(db_column='REFERENCE_EMAIL', max_length=50, blank=True)
    comments = models.TextField(db_column='COMMENTS',  max_length=100, blank=True)
    contacts = fields.GenericRelation(BusinessAccountContact)
    objects = managers.GeneralManager()

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def get_contacts(self):
        try:
            return self.contacts.all()
        except:
            return None

    class Meta:
        db_table = 'business_info'


class AccountInfo(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID, on_delete=models.CASCADE)
    account_id = models.CharField(db_column='ACCOUNT_ID', max_length=15, primary_key=True)
    business  = models.ForeignKey(BusinessInfo, related_name='accounts', db_column='BUSINESS_ID', null=True, on_delete=models.CASCADE)
    organisation = models.ForeignKey('Organisation', null=True, blank=True, on_delete=models.CASCADE)
    name    = models.CharField(db_column='NAME', max_length=50, blank=True)
    phone       = models.CharField(db_column='PHONE', max_length=10,  blank=True)
    email       = models.CharField(db_column='EMAILID',  max_length=50, blank=True)
    address     = models.CharField(db_column='ADDRESS',  max_length=100, blank=True)
    reference_name  = models.CharField(db_column='REFERENCE_NAME', max_length=50, blank=True)
    reference_phone = models.CharField(db_column='REFERENCE_PHONE', max_length=10, blank=True)
    reference_email = models.CharField(db_column='REFERENCE_EMAIL', max_length=50, blank=True)
    comments    = models.TextField(db_column='COMMENTS',  max_length=100, blank=True)
    contacts = fields.GenericRelation(BusinessAccountContact)
    objects = managers.GeneralManager()

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def get_contacts(self):
        try:
            return self.contacts.all()
        except:
            return None

    def get_proposals(self):
        # ProposalInfo --> related_name='proposals'
        try:
            return self.proposals.all()
        except:
            return None

    class Meta:
        db_table = 'account_info'


class ContactDetails(BaseModel):
    """
    holds contacts of all kinds.
    """
    contact_type = models.CharField(max_length=30, blank=True, null=True)
    specify_others = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    salutation = models.CharField(max_length=50, blank=True, null=True)
    landline = models.CharField(blank=True, null=True, max_length=30)
    std_code = models.CharField(max_length=6, blank=True, null=True)
    mobile = models.BigIntegerField(blank=True, null=True)
    country_code = models.CharField(max_length=10, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    spoc = models.CharField(max_length=5, blank=True, null=True)
    contact_authority = models.CharField(max_length=5, blank=True, null=True)
    designation = models.CharField(max_length=155, null=True, blank=True)
    department = models.CharField(max_length=155, null=True, blank=True)
    comments = models.TextField(max_length=255, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, null=True, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=supplier_id_max_length, null=True)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    other_contact_type = models.CharField(max_length=255, null=True, blank=True)
    objects = managers.GeneralManager()

    class Meta:

        db_table = 'contact_details'

class OwnershipDetails(models.Model):
    """
    holds Ownership of all kinds.
    """
    
    object_id = models.CharField(max_length=supplier_id_max_length, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    gst_number = models.CharField(max_length=255, blank=True, null=True)
    pan_number = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    subarea = models.CharField(max_length=100, blank=True, null=True)
    address1 = models.CharField(max_length=100, blank=True, null=True)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateTimeField(max_length=50, blank=True, null=True)
    end_date = models.DateTimeField(max_length=50, blank=True, null=True)
    payment_terms_condition = models.TextField(max_length=255, blank=True, null=True)
    food_tasting = models.CharField(choices=(( 'YES', 'YES' ),  ('NO', 'NO')), max_length=10, blank=True, null=True)
    
    class Meta:
        db_table = 'ownership_details'


class ContactDetailsGeneric(models.Model):
    id = models.AutoField(db_column='CONTACT_ID', primary_key=True)  # Field name made lowercase.
    content_type = models.ForeignKey(ContentType, related_name='contacts', on_delete=models.CASCADE)
    object_id = models.CharField(max_length=12)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    contact_type = models.CharField(db_column='CONTACT_TYPE',  max_length=30, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='CONTACT_NAME',  max_length=50, blank=True, null=True)  # Field name made lowercase.
    salutation = models.CharField(db_column='SALUTATION',  max_length=50, blank=True, null=True)  # Field name made lowercase.
    landline = models.BigIntegerField(db_column='CONTACT_LANDLINE', blank=True, null=True)  # Field name made lowercase.
    stdcode = models.CharField(db_column='STD_CODE',max_length=6, blank=True, null=True)  # Field name made lowercase.
    mobile = models.BigIntegerField(db_column='CONTACT_MOBILE', blank=True, null=True)  # Field name made lowercase.
    countrycode = models.CharField(db_column='COUNTRY_CODE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='CONTACT_EMAILID',  max_length=50, blank=True, null=True)  # Field name made lowercase.


    class Meta:

        db_table = 'contact_details_generic'

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


class ActivityLog(BaseModel):
    user = models.ForeignKey('BaseUser', null=False, blank=False, on_delete=models.CASCADE)
    organisation = models.ForeignKey('Organisation', on_delete=models.CASCADE)
    class Meta:
        db_table = 'activity_log'