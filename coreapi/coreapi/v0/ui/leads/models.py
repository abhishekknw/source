from django.db import models
from v0.ui.base.models import BaseModel
from v0.ui.common.models import mongo_client
from pymodm.connection import connect
from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields
from v0.ui.proposal.models import ShortlistedSpaces
from v0.ui.supplier.models import SupplierTypeSociety

connect("mongodb://localhost:27017/machadalo", alias="mongo_app")


# class LeadsFormContacts(BaseModel):
#     form = models.ForeignKey('LeadsForm', null=False, blank=False)
#     contact_name = models.CharField(max_length=70, null=True, blank=True)
#     contact_mobile = models.IntegerField(blank=False, null=True)
#
#     class Meta:
#         db_table = 'leads_form_contacts'

def get_extra_leads_dict(campaign_list=None):
    if campaign_list:
        if not isinstance(campaign_list, list):
            campaign_list = [campaign_list]
        match_dict = {"campaign_id": {"$in": campaign_list}}
    else:
        match_dict = {}
    all_leads_count = get_leads_summary(campaign_list=campaign_list, user_start_datetime=None, user_end_datetime=None,
                                        with_extra=False)
    suppliers_with_data = [data_point["supplier_id"] for data_point in all_leads_count if data_point["total_leads_count"] > 0]
    all_extra_leads = list(mongo_client.leads_extras.find(match_dict))
    all_extra_leads_dict = {}
    for extra_leads in all_extra_leads:
        if extra_leads['supplier_id'] in suppliers_with_data:
            continue
        if extra_leads['campaign_id'] not in all_extra_leads_dict:
            all_extra_leads_dict[extra_leads['campaign_id']] = {}
        if extra_leads['supplier_id'] not in all_extra_leads_dict[extra_leads['campaign_id']]:
            all_extra_leads_dict[extra_leads['campaign_id']][extra_leads['supplier_id']] = []
        all_extra_leads_dict[extra_leads['campaign_id']][extra_leads['supplier_id']].append({
            "supplier_id":extra_leads["supplier_id"],
            "extra_hot_leads": extra_leads["extra_hot_leads"],
            "extra_leads": extra_leads["extra_leads"],
            "created_at": extra_leads["created_at"],
            "leads_form_id": extra_leads["leads_form_id"],
        })
    return all_extra_leads_dict


def get_aggregated_extra_leads(campaign_list=None):
    if campaign_list:
        if not isinstance(campaign_list, list):
            campaign_list = [campaign_list]
        match_dict = {"campaign_id": {"$in": campaign_list}}
    else:
        match_dict = {}
    leads_summary = mongo_client.leads_extras.aggregate(
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
                            "extra_leads":{"$sum":"$extra_leads"},
                            "extra_hot_leads": {"$sum": "$extra_hot_leads"},
                        }
                },
                {
                    "$project": {
                        "campaign_id": 1,
                        "supplier_id": 1,
                        "extra_leads": 1,
                        "extra_hot_leads": 1,
                    }
                }
            ]
        )
    return list(leads_summary)


def add_extra_leads(leads_summary,campaign_list=None):
    leads_extras_all = get_aggregated_extra_leads()
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
    if with_extra:
        leads_summary = add_extra_leads(leads_summary, campaign_list)
    return leads_summary

# this function is used to get the number of desired raw data or metrics for the given
# data point within the chosen scope


def get_leads_summary_all(data_scope = None, data_point = None, raw_data = ['total_leads','hot_leads'],
                          metrics = ['2/1']):
    match_dict = {}
    scope_restrictor_count = len(data_scope.keys()) if data_scope is not None else 0 # get number of restrictors
    if scope_restrictor_count == 0: # case of full database
        match_dict = {}
        # else do something else
    group_dict = {
        "_id": {},
    }
    project_dict = {}
    data_point_category = data_point['category']
    data_point_levels = data_point['level']
    if data_point is None:
        return 'no data point criteria specified'
    if data_point_category == 'unordered':
        if 'campaign' in data_point_levels:
            group_dict["_id"]["campaign_id"] = "$campaign_id"
            group_dict["campaign_id"] = {"$first": "$campaign_id"}
            project_dict["campaign_id"] = 1
        if 'supplier' in data_point_levels:
            group_dict["_id"]["supplier_id"] = "$supplier_id"
            group_dict["supplier_id"] = {"$first": "$supplier_id"}
            project_dict["supplier_id"] = 1
    raw_data_available = ['total_leads','hot_leads']
    # for curr_data in raw_data:
    #     if curr_data in raw_data_available:
    #         group_dict[curr_data]
    if 'total_leads' in raw_data:
        group_dict["total_leads"] = {"$sum": 1}
        project_dict["total_leads"] = 1
    if 'hot_leads' in raw_data:
        group_dict["hot_leads"] = {"$sum": {"$cond": ["$is_hot", 1, 0]}}
        project_dict["hot_leads"] = 1
    operators = ['/'] # more operators will be added later
    for curr_metric in metrics:
        nr_index = int(curr_metric.split('/')[0])-1
        dr_index = int(curr_metric.split('/')[1])-1
        nr = raw_data[nr_index]
        dr = raw_data[dr_index]
        if nr in raw_data_available and dr in raw_data_available:
            metric_name = nr + '/' + dr
            project_dict[metric_name] = {"$divide": ['$'+nr, '$'+dr]}
    final_array = [
        {
            "$match": match_dict
        },
        {
            "$group": group_dict
        },
        {
            "$project": project_dict
        }
    ]
    leads_summary = mongo_client.leads.aggregate(final_array)
    test_lower_level_elements = get_details_by_higher_level('supplier', 'flat', ['BENBLDBHRSAPP', 'BENBLDBHRSAPR'])
    leads_summary = list(leads_summary)
    return (test_lower_level_elements)


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

count_details_parent_map = {
    'supplier':{'parent':'campaign', 'model_name': 'ShortlistedSpaces', 'database_type': 'mysql',
                'self_name_model': 'object_id', 'parent_name_model': 'proposal_id', 'storage_type': 'name'},
    'checklist': {'parent': 'campaign', 'model_name': 'checklists', 'database_type': 'mongodb',
                 'self_name_model': 'checklist_id', 'parent_name_model': 'campaign_id', 'storage_type': 'unique'},
    'flat': {'parent': 'supplier', 'model_name': 'SupplierTypeSociety', 'database_type': 'mysql',
                 'self_name_model': 'flat_count', 'parent_name_model': 'supplier_id', 'storage_type': 'count'}
}

count_details_kids_map = {
    'campaign': {'supplier', 'checklist'},
    'supplier': {'flat'}
}

def get_count_details(entity):
    entity_details = count_details_parent_map[entity]

def find_level_sequence(highest_level, lowest_level):
    sequence = []
    curr_level = lowest_level
    n_levels = 3
    n=0
    while n < n_levels:
        sequence.append(curr_level)
        if curr_level == highest_level:
            desc_sequence = sequence[::-1]
            return desc_sequence
        elif curr_level not in count_details_parent_map:
            error_message = "incorrect hierarchy"
        else:
            next_level = count_details_parent_map[curr_level]['parent']
            curr_level = next_level
            n = n + 1
    if n>=n_levels:
        error_message = "too many levels"
    return error_message

def get_details_by_higher_level(highest_level, lowest_level, highest_level_list):
    # kids = parent_order.keys()
    # parents = parent_order.values()
    # if higher_level not in parents:
    #     return('incorrect higher level')
    # elif lower_level not in kids:
    #     return('incorrect lower level')
    desc_sequence = find_level_sequence(highest_level, lowest_level)
    curr_level_id = 0
    last_level_id = len(desc_sequence)-1
    while curr_level_id < last_level_id:
        curr_level = desc_sequence[curr_level_id]
        next_level = desc_sequence[curr_level_id+1]
        entity_details = count_details_parent_map[next_level]
        (model_name, database_type, self_model_name, parent_model_name, storage_type) = (
            entity_details['model_name'], entity_details['database_type'], entity_details['self_name_model'],
            entity_details['parent_name_model'], entity_details['storage_type'])

        if curr_level_id==0:
            match_list = highest_level_list
        else:
            match_list = next_level_match_list
        query = []
        if storage_type == 'unique' or storage_type == 'name':
            if database_type == 'mongodb':
                match_constraint = [{parent_model_name: {"$in": match_list}}]
                match_dict = {"$and": match_constraint}
                query = mongo_client[model_name].aggregate(
                    [
                        {"$match": match_dict},
                        {
                            "$group":
                                {
                                    "_id": {self_model_name: '$'+self_model_name, parent_model_name: '$'+ parent_model_name},
                                    parent_model_name:{"$first": '$'+parent_model_name},
                                }
                        },
                        {
                            "$project":
                                {
                                    parent_model_name: 1,
                                    self_model_name: 1
                                }
                        }
                    ]
                )
                query = list(query)
                next_level_match_list = [x["_id"][self_model_name] for x in query]
                # count = mongo_client[model_name].find({}).distinct(self_model_name).length
            elif database_type == 'mysql':
                first_part_query = model_name+'.objects.filter('
                full_query = first_part_query+ parent_model_name+'__in=match_list)'
                #query = eval(model_name).objects.filter(proposal_id__in=match_list)
                query = list(eval(full_query).values(self_model_name, parent_model_name))
                next_level_match_list = list(set([x[self_model_name] for x in query]))
            else:
                print("database does not exist")
        elif storage_type == 'count':
            if database_type == 'mongodb':
                match_constraint = [{parent_model_name: {"$in": match_list}}]
                match_dict = {"$and": match_constraint}
                query = mongo_client[model_name].find(match_dict, {'_id': 0, parent_model_name: 1, self_model_name: 1})
                query = list(query)
            elif database_type == 'mysql':
                first_part_query = model_name + '.objects.filter('
                full_query = first_part_query + parent_model_name + '__in=match_list)'
                query = list(eval(full_query).values(self_model_name, parent_model_name))
                next_level_match_array = [x[self_model_name] for x in query]
                next_level_match_list = [sum(next_level_match_array)]
                print next_level_match_list
            else:
                print("database does not exist")
        else:
            print("pass")
        curr_level_id = curr_level_id+1
    return query


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