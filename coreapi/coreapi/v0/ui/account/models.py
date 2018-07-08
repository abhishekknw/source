from django.db import models
from django.conf import settings
from django.contrib.contenttypes import fields
from v0.ui.base.models import BaseModel
from v0 import managers
from django.contrib.contenttypes.models import ContentType
from v0.constants import supplier_id_max_length


class BusinessAccountContact(BaseModel):
    id = models.AutoField(db_column='ID', primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID)
    content_type = models.ForeignKey(ContentType)
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID)
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID)
    account_id = models.CharField(db_column='ACCOUNT_ID', max_length=15, primary_key=True)
    business  = models.ForeignKey(BusinessInfo, related_name='accounts', db_column='BUSINESS_ID', null=True, on_delete=models.CASCADE)
    organisation = models.ForeignKey('Organisation', null=True, blank=True)
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
    landline = models.BigIntegerField(blank=True, null=True)
    std_code = models.CharField(max_length=6, blank=True, null=True)
    mobile = models.BigIntegerField(blank=True, null=True)
    country_code = models.CharField(max_length=10, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    spoc = models.CharField(max_length=5, blank=True, null=True)
    contact_authority = models.CharField(max_length=5, blank=True, null=True)
    designation = models.CharField(max_length=155, null=True, blank=True)
    department = models.CharField(max_length=155, null=True, blank=True)
    comments = models.TextField(max_length=255, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.CharField(max_length=supplier_id_max_length, null=True)
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    objects = managers.GeneralManager()

    class Meta:

        db_table = 'contact_details'


class ContactDetailsGeneric(models.Model):
    id = models.AutoField(db_column='CONTACT_ID', primary_key=True)  # Field name made lowercase.
    content_type = models.ForeignKey(ContentType, related_name='contacts')
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