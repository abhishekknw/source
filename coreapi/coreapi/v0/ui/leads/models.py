from __future__ import division
from django.db import models
from v0.ui.base.models import BaseModel
from v0.ui.common.models import mongo_client
from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields
from v0.ui.proposal.models import ShortlistedSpaces
from v0.ui.supplier.models import SupplierTypeSociety
import copy


# class LeadsFormContacts(BaseModel):
#     form = models.ForeignKey('LeadsForm', null=False, blank=False)
#     contact_name = models.CharField(max_length=70, null=True, blank=True)
#     contact_mobile = models.IntegerField(blank=False, null=True)
#
#     class Meta:
#         db_table = 'leads_form_contacts'

def get_extra_leads_dict(campaign_list=None, only_latest_count=False, user_start_datetime=None):
    match_constraints = []
    if campaign_list:
        if not isinstance(campaign_list, list):
            campaign_list = [campaign_list]
        match_constraints.append({"campaign_id": {"$in": campaign_list}})
    if user_start_datetime:
        match_constraints.append({"created_at": {"$gte": user_start_datetime}})
    if len(match_constraints) == 0:
        match_dict = {}
    else:
        match_dict = {"$and": match_constraints}
    all_leads_count = get_leads_summary(campaign_list=campaign_list, user_start_datetime=None, user_end_datetime=None,
                                        with_extra=False)
    suppliers_with_data = [data_point["supplier_id"] for data_point in all_leads_count if data_point["total_leads_count"] > 0]
    all_extra_leads = list(mongo_client.leads_extras.find(match_dict).sort("created_at",-1))
    all_extra_leads_dict = {}
    for extra_leads in all_extra_leads:
        if extra_leads['supplier_id'] in suppliers_with_data:
            continue
        if extra_leads['campaign_id'] not in all_extra_leads_dict:
            all_extra_leads_dict[extra_leads['campaign_id']] = {}
        if extra_leads['supplier_id'] not in all_extra_leads_dict[extra_leads['campaign_id']]:
            all_extra_leads_dict[extra_leads['campaign_id']][extra_leads['supplier_id']] = []
        if only_latest_count:
            if len(all_extra_leads_dict[extra_leads['campaign_id']][extra_leads['supplier_id']]) > 0:
                continue
        all_extra_leads_dict[extra_leads['campaign_id']][extra_leads['supplier_id']].append({
            "supplier_id":extra_leads["supplier_id"],
            "extra_hot_leads": extra_leads["extra_hot_leads"],
            "extra_leads": extra_leads["extra_leads"],
            "created_at": extra_leads["created_at"],
            "leads_form_id": extra_leads["leads_form_id"],
        })
    return all_extra_leads_dict


def add_extra_leads(leads_summary, campaign_list=None, user_start_datetime=None):
    leads_extras_all_dict = get_extra_leads_dict(None, False, user_start_datetime)
    leads_extras_dict = {}
    leads_summary_dict = {}
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
    for campaign_id in leads_extras_all_dict:
        print(campaign_id, campaign_list)
        if campaign_id in campaign_list:
            for supplier_id in leads_extras_all_dict[campaign_id]:
                    if (campaign_id not in leads_summary_dict) or (supplier_id not in leads_summary_dict[campaign_id]):
                        total_leads_count = leads_extras_all_dict[campaign_id][supplier_id][0]["extra_leads"]
                        hot_leads_count = leads_extras_all_dict[campaign_id][supplier_id][0]["extra_hot_leads"]
                        leads_summary.append({'campaign_id': campaign_id,
                                              'supplier_id': supplier_id,
                                              'total_leads_count': total_leads_count,
                                              'hot_leads_count': hot_leads_count,
                                              'hot_leads_percentage': float(total_leads_count) / float(
                                                  hot_leads_count) * 100 if hot_leads_count > 0 else 0,
                                              })
    return leads_summary


def get_leads_summary(campaign_list=None, user_start_datetime=None,user_end_datetime=None, with_extra=True):
    if campaign_list:
        if not isinstance(campaign_list, list):
            campaign_list = [campaign_list]
        match_constraint = [{"campaign_id": {"$in": campaign_list}}]
        if user_start_datetime:
            match_constraint.append({"created_at": {"$gte": user_start_datetime}})
        if user_end_datetime:
            match_constraint.append({"created_at": {"$lte": user_end_datetime}})
        match_dict = {"$and": match_constraint}
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
                            "created_at": {"$first": '$created_at'},
                            "total_leads_count": {"$sum": 1},
                            "hot_leads_count": {"$sum": {"$cond": ["$is_hot", 1, 0]}},
                        }
                },
                {
                    "$project": {
                        "campaign_id": 1,
                        "supplier_id": 1,
                        "created_at": 1,
                        "total_leads_count": 1,
                        "hot_leads_count": 1,
                        "hot_leads_percentage": {
                            "$multiply": [{"$divide": [100, "$total_leads_count"]}, "$hot_leads_count"]},
                    }
                }
            ]
        )
    leads_summary = list(leads_summary)

    if with_extra:
        leads_summary = add_extra_leads(leads_summary, campaign_list, user_start_datetime)
    return leads_summary


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
def get_leads_summary_by_campaign_and_hotness_level(leads, lead_form):
    result = {}

    for lead in leads:
        result.setdefault(lead['supplier_id'],{})
        result[lead['supplier_id']].setdefault('lead_data', {})
        get_hot_lead_data(lead_form, lead, result[lead['supplier_id']]['lead_data'])

    return result

def get_hot_lead_data(lead_form, lead, result):
    for hot_level, values in lead_form['global_hot_lead_criteria'].items():
        result.setdefault(hot_level, 0)
        if 'or' in values:
            for item in values['or']:
                itemValues = values['or'][item]
                if lead['data'][int(item)]['value']:
                    if 'AnyValue' in itemValues or lead['data'][int(item)]['value'] in itemValues:
                        result[hot_level] = result[hot_level] + 1
                        break

class LeadsPermissions(MongoModel):
    profile_id = fields.IntegerField()
    organisation_id = fields.CharField()
    leads_permissions = fields.ListField()  # CREATE, UPDATE, READ, DELETE, FILL
    allowed_campaigns = fields.ListField()  #  All if empty
    created_by = fields.CharField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'


class ExcelDownloadHash(MongoModel):
    leads_form_id = fields.IntegerField()
    supplier_id = fields.CharField()
    one_time_hash = fields.ListField()  # CREATE, UPDATE, READ, DELETE, FILL
    created_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'


class CampaignExcelDownloadHash(MongoModel):
    campaign_id = fields.CharField()
    one_time_hash = fields.CharField()
    created_at = fields.DateTimeField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'mongo_app'
