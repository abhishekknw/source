from v0 import managers
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from v0.ui.base.models import BaseModel
from v0.constants import supplier_id_max_length
from django.contrib.contenttypes import fields

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

class SocietyLeads(models.Model):
    id = models.CharField(max_length=100,null=False,primary_key=True)
    society = models.ForeignKey('SupplierTypeSociety', null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, null=True, blank=True,default='0')
    email = models.EmailField()

    class Meta:
        db_table = 'society_leads'