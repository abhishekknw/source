from v0 import managers
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from v0.ui.base.models import BaseModel
from v0.constants import supplier_id_max_length
from django.contrib.contenttypes import fields
from v0.ui.leads.models import LEAD_KEY_TYPES, LEAD_ITEM_STATUS

CHECKLIST_TYPE = (
    ('CAMPAIGN', 'CAMPAIGN'),
    ('SUPPLIER', 'SUPPLIER')
)


class Checklist(BaseModel):
    # checklist may be applicable to one or all suppliers
    campaign_id = models.CharField(max_length=70, null=True, blank=True)
    supplier_id = models.CharField(max_length=70, null=True, blank=True)
    checklist_name = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=70, null=True, choices=LEAD_ITEM_STATUS)
    checklist_type = models.CharField(max_length=70, null=True, choices=CHECKLIST_TYPE)
    rows = models.IntegerField(blank=False, null=True)
    is_template = models.BooleanField(blank=False, null=False)

    class Meta:
        db_table = 'checklist'


# rows currently support only two levels
class ChecklistRows(BaseModel):
    checklist = models.ForeignKey('Checklist', null=False, blank=False)
    list_item = models.CharField(max_length=70, null=True, blank=True)
    item_id = models.CharField(max_length=70, null=True, blank=True)
    order_id = models.IntegerField(blank=False, null=True)
    parent_id = models.IntegerField(blank=False, null=False)
    level = models.IntegerField(blank=False, null=True)
    status = models.CharField(max_length=70, null=True, choices=LEAD_ITEM_STATUS)

    class Meta:
        db_table = 'checklist_rows'


class ChecklistColumns(BaseModel):
    checklist = models.ForeignKey('Checklist', null=False, blank=False)
    column_name = models.CharField(max_length=70, null=True, blank=True)
    column_options = models.CharField(max_length=200, null=True, blank=True)  # delimiter separated
    column_type = models.CharField(max_length=70, null=True, choices=LEAD_KEY_TYPES)
    order_id = models.IntegerField(blank=False, null=True)
    column_id = models.IntegerField(blank=False, null=True)
    status = models.CharField(max_length=70, null=True, choices=LEAD_ITEM_STATUS)

    class Meta:
        db_table = 'checklist_columns'

class ChecklistData(BaseModel):
    checklist = models.ForeignKey('Checklist', null=False, blank=False)
    supplier_id = models.CharField(max_length=70, null=True, blank=True)
    cell_value = models.CharField(max_length=200, null=True, blank=True)
    row_id = models.IntegerField(blank=False, null=True)
    column_id = models.IntegerField(blank=False, null=True)
    status = models.CharField(max_length=70, null=True, choices=LEAD_ITEM_STATUS)
    class Meta:
        db_table = 'checklist_data'