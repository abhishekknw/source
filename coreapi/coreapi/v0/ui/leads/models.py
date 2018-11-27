from django.db import models
from v0.ui.base.models import BaseModel
from v0.ui.common.models import mongo_client
from pymodm.connection import connect
from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields

connect("mongodb://localhost:27017/machadalo", alias="mongo_app")

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


def add_extra_leads(leads_summary,campaign_list=None):
    leads_extras_all = list(mongo_client.leads_extras.find())
    leads_extras_dict = {}
    leads_summary_dict = {}
    for single_leads_extras in leads_extras_all:
        if single_leads_extras['campaign_id'] not in leads_extras_dict:
            leads_extras_dict[single_leads_extras['campaign_id']] = {}
        if single_leads_extras['supplier_id'] not in leads_extras_dict[single_leads_extras['campaign_id']]:
            leads_extras_dict[single_leads_extras['campaign_id']][single_leads_extras['supplier_id']] = single_leads_extras
    for single_summary in leads_summary:
        if single_summary['campaign_id'] not in leads_summary_dict:
            leads_summary_dict[single_summary['campaign_id']] = {}
        if single_summary['supplier_id'] not in leads_summary_dict[single_summary['campaign_id']]:
            leads_summary_dict[single_summary['campaign_id']][single_summary['supplier_id']] = single_summary
    for single_summary in leads_summary:
        if single_summary['campaign_id'] in leads_extras_dict:
            if single_summary['supplier_id'] in leads_extras_dict[single_summary['campaign_id']]:
                if single_summary['total_leads_count'] == 0:
                    single_summary['total_leads_count'] = leads_extras_dict[single_summary['campaign_id']][single_summary['supplier_id']]["extra_leads"]
                    single_summary['hot_leads_count'] = leads_extras_dict[single_summary['campaign_id']][single_summary['supplier_id']]["extra_hot_leads"]
                    single_summary['hot_leads_percentage'] = (float(single_summary['hot_leads_count'])/float(single_summary['total_leads_count']) * 100)
    for extra_leads in leads_extras_all:
        if extra_leads['campaign_id'] in campaign_list:
            if (extra_leads['campaign_id'] not in leads_summary_dict) or (extra_leads['supplier_id'] not in leads_summary_dict[extra_leads['campaign_id']]):
                leads_summary.append({'campaign_id': extra_leads['campaign_id'],
                                      'supplier_id': extra_leads['supplier_id'],
                                      'total_leads_count': extra_leads['extra_leads'],
                                      'hot_leads_count': extra_leads['extra_hot_leads'],
                                      'hot_leads_percentage': float(extra_leads['extra_hot_leads'])/float(extra_leads['extra_leads']) * 100,
                                      })
    return leads_summary


def get_leads_summary(campaign_list=None):
    if campaign_list:
        if not isinstance(campaign_list, list):
            campaign_list = [campaign_list]
        match_dict = {"campaign_id": {"$in": campaign_list}}
    else:
        match_dict = {}
    leads_summary = mongo_client.leads.aggregate(
            [
                {
                    "$match": match_dict
                },
                {
                    "$group":
                        {
                            "_id": {"campaign_id": "$campaign_id", "supplier_id": "$supplier_id"},
                            "campaign_id": {"$first": '$campaign_id'},
                            "supplier_id": {"$first": '$supplier_id'},
                            "total_leads_count": {"$sum": 1},
                            "hot_leads_count": {"$sum": {"$cond": ["$is_hot", 1, 0]}},
                        }
                },
                {
                    "$project": {
                        "campaign_id": 1,
                        "supplier_id": 1,
                        "total_leads_count": 1,
                        "hot_leads_count": 1,
                        "hot_leads_percentage": {
                            "$multiply": [{"$divide": [100, "$total_leads_count"]}, "$hot_leads_count"]},
                    }
                }
            ]
        )
    leads_summary = list(leads_summary)
    updated_leads_summary = add_extra_leads(leads_summary, campaign_list)
    return updated_leads_summary


def get_leads_summary_by_campaign(campaign_list=None):
    if campaign_list:
        if not isinstance(campaign_list, list):
            campaign_list = [campaign_list]
        match_dict = {"campaign_id": {"$in": campaign_list}}
    else:
        match_dict = {}
    leads_summary = mongo_client.leads.aggregate(
            [
                {
                    "$match": match_dict
                },
                {
                    "$group":
                        {
                            "_id": {"campaign_id": "$campaign_id"},
                            "campaign_id": {"$first": '$campaign_id'},
                            "total_leads_count": {"$sum": 1},
                            "hot_leads_count": {"$sum": {"$cond": ["$is_hot", 1, 0]}},
                        }
                },
                {
                    "$project": {
                        "campaign_id": 1,
                        "supplier_id": 1,
                        "total_leads_count": 1,
                        "hot_leads_count": 1,
                        "hot_leads_percentage": {
                            "$multiply": [{"$divide": [100, "$total_leads_count"]}, "$hot_leads_count"]},
                    }
                }
            ]
        )
    return list(leads_summary)


class LeadsPermissions(MongoModel):
    user_id = fields.IntegerField()
    organisation_id = fields.CharField()
    leads_permissions = fields.ListField()  # CREATE, UPDATE, READ, DELETE, FILL
    allowed_campaigns = fields.ListField()  #  All if empty
    created_by = fields.CharField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'