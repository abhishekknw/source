from __future__ import division
from django.db import models
from v0.ui.base.models import BaseModel
from v0.ui.common.models import mongo_client
from pymodm.connection import connect
from pymongo.write_concern import WriteConcern
from pymodm import MongoModel, fields
from v0.ui.proposal.models import ShortlistedSpaces
from v0.ui.supplier.models import SupplierTypeSociety
import copy

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


def get_leads_summary(campaign_list=None, user_start_datetime=None,user_end_datetime=None):
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
    updated_leads_summary = add_extra_leads(leads_summary, campaign_list)
    return updated_leads_summary


level_name_by_model_id = {
    "supplier_id": "supplier", "object_id": "supplier", "campaign_id": "campaign", "proposal_id": "campaign",
    "flat_count": "flat"
}

def find_key_alias_dict_array(dict_array, key_name):
    first_element = dict_array[0]
    dict_keys = first_element.keys()
    for key in dict_keys:
        if key in level_name_by_model_id and level_name_by_model_id[key]==key_name:
            return key
    return key_name


def convert_dict_arrays_keys_to_standard_names(dict_arrays):
    final_array = []
    for curr_array in dict_arrays:
        keys = curr_array[0].keys()
        new_array = []
        for curr_dict in curr_array:
            for curr_key in keys:
                new_key = level_name_by_model_id[curr_key] if curr_key in level_name_by_model_id else curr_key
                curr_dict[new_key] = curr_dict.pop(curr_key)
            new_array.append(curr_dict)
        final_array.append(new_array)
    return final_array


def merge_dict_array_dict_single(metric_dict,key_name):
    key_values = []
    final_array = []
    metric_list = metric_dict.keys()
    first_array = metric_dict[metric_list[0]]
    local_key_names = {}
    for curr_metric in metric_dict:
        curr_array = metric_dict[curr_metric]
        local_key_name = find_key_alias_dict_array(curr_array, key_name)
        local_key_names[curr_metric] = local_key_name
        if curr_array==first_array:
            key_values = [x[local_key_name] for x in curr_array]
    for curr_value in key_values:
        curr_final_dict = {}
        missing_value = False
        for curr_metric in metric_list:
            local_key_name = local_key_names[curr_metric]
            curr_dict = [x for x in metric_dict[curr_metric] if x[local_key_name]==curr_value]
            if not curr_dict == []:
                curr_final_dict.update(curr_dict[0])
            else:
                missing_value = True
                continue
        if missing_value == False:
            final_array.append(curr_final_dict)
    return final_array


def merge_dict_array_array_single(array, key_name):
    final_array=[]
    first_array = array[0]
    first_array_keys = first_array[0].keys()
    desired_key_values = [x[key_name] for x in first_array]
    for curr_value in desired_key_values:
        curr_final_dict = {}
        missing_value = False
        for curr_array in array:
            curr_dict = [x for x in curr_array if x[key_name]==curr_value]
            if not curr_dict == []:
                curr_final_dict.update(curr_dict[0])
            else:
                missing_value = True
                continue
        if missing_value == False:
            final_array.append(curr_final_dict)
    return final_array


# function to check whether a dict array key structure matches a desired key array
def get_similar_structure_keys(main_dict, required_keys):
    keys = main_dict.keys()

    similar_array = []
    for key_name in keys:
        curr_array = main_dict[key_name]
        curr_keys = curr_array[0].keys()
        curr_keys = [level_name_by_model_id[x] if x in level_name_by_model_id else x for x in
                         curr_keys]
        if not isinstance(required_keys, list):
            required_keys = [required_keys]
        matching_keys = required_keys + [key_name]
        if curr_keys == matching_keys:
            similar_array.append(key_name)
    return similar_array


# this function is used to get the number of desired raw data or metrics for the given
# data point within the chosen scope
def get_leads_summary_all_old(data_scope = None, data_point = None, raw_data = ['total_leads','hot_leads'],
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
    test_lower_level_elements = get_details_by_higher_level('supplier,campaign', 'lead', ['TESYOG06F2', 'BYJMACC9CA'])
    leads_summary = list(leads_summary)
    return (test_lower_level_elements)


# currently working with the following constraints:
# exactly one scope restrictor with exact match, one type of data point, one raw data element, metrics ignored
def get_leads_summary_all(data_scope = None, data_point = None, raw_data = ['lead'],
                          metrics = ['2/1']):

    data_scope_first = data_scope['1']
    highest_level = data_scope_first['value_type']
    grouping_level = data_point['level']
    # if highest_level == grouping_level:
    #     return "lowest level should be lower than highest level"
    individual_metric_output = {}
    highest_level_values = data_scope_first['values']['exact']
    default_value_type = data_scope_first['value_type']
    for curr_metric in raw_data:
        lowest_level = curr_metric
        curr_output = get_details_by_higher_level(highest_level, lowest_level, highest_level_values,
                                                  default_value_type, grouping_level)
        individual_metric_output[lowest_level] = curr_output

    matching_format_metrics = get_similar_structure_keys(individual_metric_output, grouping_level)
    #raw_metrics = individual_metric_output.keys()
    combined_array = []


    first_metric_array = individual_metric_output[matching_format_metrics[0]] if len(matching_format_metrics)>0 else []
    for ele_id in range(0,len(first_metric_array)):
        curr_dict = first_metric_array[ele_id]
        new_dict = curr_dict.copy()
        for metric in matching_format_metrics[1:len(matching_format_metrics)]:
            new_dict[metric]=individual_metric_output[metric][ele_id][metric]
        combined_array.append(new_dict)

    single_array = merge_dict_array_dict_single(individual_metric_output, grouping_level[0])
    single_array_keys = single_array[0].keys()
    reverse_map = {}
    for key in single_array_keys:
        reverse_key = level_name_by_model_id[key] if key in level_name_by_model_id else None
        if reverse_key in raw_data:
            reverse_map[reverse_key] = key


    derived_array = copy.deepcopy(single_array)
    metric_names = []
    for curr_metric in metrics:
        op = '/'
        split_metric = curr_metric.split(op)

        if not split_metric[0][0] == 'm':
            nr_source = raw_data
            nr_index = int(split_metric[0])-1
            nr = nr_source[nr_index]
        else:
            nr_source = metric_names
            nr_index = int(split_metric[0][1:])-1
            nr = nr_source[nr_index]

        if not split_metric[1][0] == 'm':
            dr_source = raw_data
            dr_index = int(split_metric[1])-1
            dr = raw_data[dr_index]
        else:
            dr_source = metric_names
            dr_index = int(split_metric[1][1:])-1
            dr = metric_names[dr_index]


        if nr in nr_source and dr in dr_source:
            metric_name = nr + op + dr
            metric_names.append(metric_name)
        #derived_array = []
        for curr_dict in derived_array:
            nr_value = curr_dict[nr] if nr in curr_dict else curr_dict[reverse_map[nr]]
            dr_value = curr_dict[dr] if dr in curr_dict else curr_dict[reverse_map[dr]]
            result_value = eval(str(nr_value)+op+str(dr_value))
            curr_dict[metric_name]=result_value

    return [individual_metric_output, single_array, derived_array]


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
                 'self_name_model': 'flat_count', 'parent_name_model': 'supplier_id', 'storage_type': 'sum'},
    'lead': {'parent': 'supplier,campaign', 'model_name': 'leads', 'database_type': 'mongodb',
                 'self_name_model': 'entry_id', 'parent_name_model': 'supplier_id,campaign_id', 'storage_type': 'count'},
    'hot_lead': {'parent': 'supplier,campaign', 'model_name': 'leads', 'database_type': 'mongodb',
                 'self_name_model': 'is_hot', 'parent_name_model': 'supplier_id,campaign_id',
                 'storage_type': 'condition'},
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


def get_details_by_higher_level(highest_level, lowest_level, highest_level_list, default_value_type=None, grouping_level=None):
    grouping_level = grouping_level[0]
    second_lowest_parent = count_details_parent_map[lowest_level]['parent']
    second_lowest_parent_name_model = count_details_parent_map[lowest_level]['parent_name_model']
    if ',' in second_lowest_parent or ',' in second_lowest_parent_name_model:
        parents = second_lowest_parent.split(',')
        desc_sequence = [parents, lowest_level]
        parent_model_names = second_lowest_parent_name_model.split(',')
        parent_type = 'multiple'
    else:
        desc_sequence = find_level_sequence(highest_level, lowest_level)
        parent_type = 'single'
        parents = [second_lowest_parent]
    curr_level_id = 0
    last_level_id = len(desc_sequence) - 1

    all_results = []

    while curr_level_id < last_level_id:
        curr_level = desc_sequence[curr_level_id]
        next_level = desc_sequence[curr_level_id+1]
        entity_details = count_details_parent_map[next_level]
        (model_name, database_type, self_model_name, parent_model_name, storage_type) = (
            entity_details['model_name'], entity_details['database_type'], entity_details['self_name_model'],
            entity_details['parent_name_model'], entity_details['storage_type'])

        if parent_type == 'multiple':
            if default_value_type in parents:
                value_type_index = parents.index(default_value_type)
                parent_model_name = parent_model_names[value_type_index]
            #parent_model_name = default_value_type if default_value_type in parent_model_names else parent_model_names[-1]
        else:
            parent_model_names = [parent_model_name]

        if curr_level_id==0:
            match_list = highest_level_list
        else:
            match_list = next_level_match_list
        query = []

        # general queries common to all storage types
        if database_type == 'mongodb':
            match_constraint = [{parent_model_name: {"$in": match_list}}]
            match_dict = {"$and": match_constraint}
        elif database_type == 'mysql':
            first_part_query = model_name + '.objects.filter('
            full_query = first_part_query + parent_model_name + '__in=match_list)'
            query = list(eval(full_query).values(self_model_name, parent_model_name))
        else:
            return "database does not exist"

        if storage_type == 'unique' or storage_type == 'name':
            if database_type == 'mongodb':
                group_dict = {"_id":{self_model_name: '$' + self_model_name},
                              self_model_name: {"$first": '$' + self_model_name}}
                project_dict = {self_model_name: 1, "_id":0}
                for curr_parent_model_name in parent_model_names:
                    group_dict["_id"][curr_parent_model_name] = '$' + curr_parent_model_name
                    group_dict[curr_parent_model_name] = {"$first": '$' + curr_parent_model_name}
                    project_dict[curr_parent_model_name] = 1

                query = mongo_client[model_name].aggregate(
                    [
                        {"$match": match_dict},
                        {
                            "$group": group_dict
                        },
                        {
                            "$project": project_dict
                        }
                    ]
                )
                query = list(query)
                next_level_match_list = [x[self_model_name] for x in query]
                # count = mongo_client[model_name].find({}).distinct(self_model_name).length
            elif database_type == 'mysql':
                if grouping_level in parents:
                    print 'true'
                    all_results.append(query)
                next_level_match_list = list(set([x[self_model_name] for x in query]))
            else:
                print("database does not exist")

        elif storage_type == 'count' or storage_type == 'sum' or storage_type == 'condition':
            if database_type == 'mongodb':
                project_dict = {next_level:1, "_id":0}
                if storage_type == 'count':
                    group_dict = {'_id': {}, next_level: {"$sum": 1}}
                elif storage_type == 'sum':
                    group_dict = {'_id': {}, next_level: {"$sum": self_model_name}}
                else:
                    if 'incrementing_value' in entity_details:
                        incrementing_value = entity_details['incrementing_value']
                        group_dict = {'_id': {}, next_level: {"$sum":{
                            "$sum": {"$cond":[{"$eq": ["$"+self_model_name,incrementing_value]}, 1, 0]}}}}
                    else:
                        group_dict = {'_id': {}, next_level: {"$sum": {"$cond": ["$"+self_model_name, 1, 0]}}}
                for curr_parent_model_name in parent_model_names:
                    group_dict["_id"][curr_parent_model_name] = '$' + curr_parent_model_name
                    group_dict[curr_parent_model_name] = {"$first": '$' + curr_parent_model_name}
                    project_dict[curr_parent_model_name] = 1
                query = mongo_client[model_name].aggregate(
                    [
                        {"$match": match_dict},
                        {
                            "$group": group_dict
                        },
                        {
                            "$project": project_dict
                        }
                    ]
                )
                query = list(query)
                all_results.append(query)
            # this is not complete yet
            elif database_type == 'mysql':
                first_part_query = model_name + '.objects.filter('
                full_query = first_part_query + parent_model_name + '__in=match_list)'
                query = list(eval(full_query).values(self_model_name, parent_model_name))
                all_results.append(query)
                next_level_match_array = [x[self_model_name] for x in query if x[self_model_name] is not None]
                if storage_type == 'count':
                    next_level_match_list = len(next_level_match_array)
                else:
                    next_level_match_list = [sum(next_level_match_array)]
            else:
                print("database does not exist")
        else:
            print("pass")
        curr_level_id = curr_level_id+1
    new_results = convert_dict_arrays_keys_to_standard_names(all_results)
    single_array_results = merge_dict_array_array_single(new_results,grouping_level)
    return single_array_results


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