from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields
from v0 import managers
from v0.ui.base.models import BaseModel

class CustomPermissions(BaseModel):
    """
    This is a model which stores extra permissions granted for a particular user
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=settings.DEFAULT_USER_ID)
    extra_permission_code = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, null=True)

    class Meta:
        db_table = 'custom_permissions'

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
    profile = models.ForeignKey('Profile')

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
    profile = models.ForeignKey('Profile')

    class Meta:
        db_table = 'general_user_permission'

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

class UserInquiry(models.Model):
    inquiry_id = models.AutoField(db_column='INQUIRY_ID', primary_key=True)
    company_name = models.CharField(db_column='COMPANY_NAME', max_length=40)
    contact_person_name = models.CharField(db_column='CONTACT_PERSON_NAME', max_length=40, blank=True, null=True)
    email = models.CharField(db_column='EMAIL', max_length=40, blank=True, null=True)
    phone = models.IntegerField(db_column='PHONE', blank=True, null=True)
    inquiry_details = models.TextField(db_column='INQUIRY_DETAILS')

    class Meta:

        db_table = 'user_inquiry'