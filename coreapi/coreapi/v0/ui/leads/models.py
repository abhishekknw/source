from django.db import models
from v0.ui.base.models import BaseModel


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
    ('TEXTAREA', 'TEXTAREA'),
    ('FLOAT', 'FLOAT'),
    ('DATE', 'DATE')
)

LEAD_ITEM_STATUS = (
    ('ACTIVE', 'ACTIVE'),
    ('INACTIVE', 'INACTIVE')
)


class LeadsForm(BaseModel):
    campaign_id = models.CharField(max_length=70, null=True, blank=True) # to be changed to foreign key
    leads_form_name = models.CharField(max_length=100, null=True, blank=True)
    last_entry_id = models.IntegerField(blank=False, null=True)
    fields_count = models.IntegerField(blank=False, null=True, default = 0)
    last_contact_id = models.IntegerField(blank=False, null=True)
    status = models.CharField(max_length=70, null=True, choices=LEAD_ITEM_STATUS)

    class Meta:
        db_table = 'leads_form'


class LeadsFormItems(BaseModel):
    leads_form = models.ForeignKey('LeadsForm', null=False, blank=False)
    campaign_id = models.CharField(max_length=70, null=True, blank=True)
    supplier_id = models.CharField(max_length=70, null=True, blank=True)
    key_name = models.CharField(max_length=70, null=True, blank=True)
    key_options = models.CharField(max_length=200, null=True, blank=True)  # delimiter separated
    key_type = models.CharField(max_length=70, null=True, choices=LEAD_KEY_TYPES)
    order_id = models.IntegerField(blank=False, null=True)
    item_id = models.IntegerField(blank=False, null=True)
    status = models.CharField(max_length=70, null=True, choices=LEAD_ITEM_STATUS)
    is_required = models.BooleanField(default=False)
    hot_lead_criteria = models.CharField(max_length=70, null=True, blank=True)

    class Meta:
        db_table = 'leads_form_items'


class LeadsFormData(BaseModel):
    leads_form = models.ForeignKey('LeadsForm', null=False, blank=False)
    supplier_id = models.CharField(max_length=70, null=True, blank=True)
    campaign_id = models.CharField(max_length=70, null=True, blank=True)
    item_value = models.CharField(max_length=200, null=True, blank=True)
    entry_id = models.IntegerField(blank=False, null=True)
    item_id = models.IntegerField(blank=False, null=True)
    status = models.CharField(max_length=70, null=True, choices=LEAD_ITEM_STATUS)

    class Meta:
        db_table = 'leads_form_data'


class LeadsFormContacts(BaseModel):
    form = models.ForeignKey('LeadsForm', null=False, blank=False)
    contact_name = models.CharField(max_length=70, null=True, blank=True)
    contact_mobile = models.IntegerField(blank=False, null=True)

    class Meta:
        db_table = 'leads_form_contacts'


class LeadsFormSummary(BaseModel):
    leads_form = models.ForeignKey('LeadsForm', null=False, blank=False)
    supplier_id = models.CharField(max_length=70, null=True, blank=True)
    campaign_id = models.CharField(max_length=70, null=True, blank=True)
    total_leads_count = models.IntegerField(blank=False, null=True)
    hot_leads_count = models.IntegerField(blank=False, null=True)
    hot_leads_percentage = models.FloatField(blank=False, null=True)

    class Meta:
        db_table = 'leads_form_summary'