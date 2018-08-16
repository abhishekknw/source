from v0 import managers
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from v0.ui.base.models import BaseModel
from v0.constants import supplier_id_max_length
from django.contrib.contenttypes import fields
from v0.ui.proposal.models import ProposalInfo


class Leads(BaseModel):
    """
    This model defines Leads
    """
    campaign = models.ForeignKey(ProposalInfo, null=False, blank=False)
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
    campaign = models.ForeignKey(ProposalInfo, null=False, blank=False)
    original_name = models.CharField(max_length=255, null=False, blank=False)
    alias = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        db_table = 'lead_alias'


class LeadsForm(BaseModel):
    campaign_id = models.CharField(max_length=70, null=True, blank=True) # to be changed to foreign key
    leads_form_name = models.CharField(max_length=100, null=True, blank=True)
    last_entry_id = models.IntegerField(blank=False, null=True)

    class Meta:
        db_table = 'leads_form'


LEAD_KEY_TYPES = (
    ('STRING', 'STRING'),
    ('BOOLEAN', 'BOOLEAN'),
    ('INT', 'INT'),
    ('EMAIL', 'EMAIL'),
    ('PASSWORD', 'PASSWORD'),
    ('PHONE', 'PHONE'),
    ('RADIO', 'RADIO'),
    ('DROPDOWN', 'DROPDOWN'),
    ('CHECKBOX', 'CHECKBOX'),
    ('TEXTAREA', 'TEXTAREA')
)

LEAD_ITEM_STATUS = (
    ('ACTIVE', 'ACTIVE'),
    ('INACTIVE', 'INACTIVE')
)


class LeadsFormItems(BaseModel):
    leads_form = models.ForeignKey('LeadsForm', null=False, blank=False)
    key_name = models.CharField(max_length=70, null=True, blank=True)
    key_options = models.CharField(max_length=200, null=True, blank=True)  # delimiter separated
    key_type = models.CharField(max_length=70, null=True, choices=LEAD_KEY_TYPES)
    order_id = models.IntegerField(blank=False, null=True)
    item_id = models.IntegerField(blank=False, null=True)
    status = models.CharField(max_length=70, null=True, choices=LEAD_ITEM_STATUS)

    class Meta:
        db_table = 'leads_form_items'


class LeadsFormData(BaseModel):
    leads_form = models.ForeignKey('LeadsForm', null=False, blank=False)
    supplier_id = models.CharField(max_length=70, null=True, blank=True)
    item_order_id = models.IntegerField(blank=False, null=True)
    item_value = models.CharField(max_length=200, null=True, blank=True)
    entry_id = models.IntegerField(blank=False, null=True)
    class Meta:
        db_table = 'leads_form_data'
