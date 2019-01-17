from __future__ import print_function
from __future__ import absolute_import
from .utils import (level_name_by_model_id, merge_dict_array_array_single, merge_dict_array_dict_single,
                    convert_dict_arrays_keys_to_standard_names, get_similar_structure_keys, geographical_parent_details,
                    count_details_parent_map, find_level_sequence, binary_operation, count_details_direct_match_multiple,
                    sum_array_by_key, z_calculator_array_multiple, get_metrics_from_code, reverse_direct_match,
                    count_details_parent_map_time, date_to_other_groups, merge_dict_array_array_multiple_keys,
                    merge_dict_array_dict_multiple_keys, count_details_parent_map_multiple, sum_array_by_keys,
                    sum_array_by_single_key, append_array_by_keys, frequency_mode_calculator)
from v0.ui.campaign.views import calculate_mode
from v0.ui.common.models import mongo_client
from v0.ui.proposal.models import ShortlistedSpaces
from v0.ui.supplier.models import SupplierTypeSociety
import copy
from rest_framework.views import APIView
from v0.ui.utils import handle_response, get_user_organisation_id
from datetime import datetime
# from unittest import TestCase
# from unittest.mock import patch
# import unittest

statistics_map = {"z_score": z_calculator_array_multiple, "frequency_distribution": frequency_mode_calculator}

unilevel_categories = ['time']


# currently working with the following constraints:
# exactly one scope restrictor with exact match, one type of data point
def get_data_analytics(data_scope, data_point, raw_data, metrics, statistical_information,
                       higher_level_statistical_information):
    unilevel_constraints = {}
    data_scope_first = {}
    if not data_scope == {}:
        data_scope_keys = list(data_scope.keys()) if not data_scope == {} else []
        for curr_key in data_scope_keys:
            if data_scope[curr_key]["category"] in unilevel_categories:
                unilevel_constraints[curr_key] = data_scope[curr_key]
                data_scope.pop(curr_key)
        data_scope_first = data_scope[data_scope_keys[0]] if data_scope_keys is not [] else {}
    highest_level = data_scope_first['value_type'] if 'value_type' in data_scope_first else None
    if 'category' not in data_point or 'level' not in data_point:
        return []
    grouping_level = data_point['level'] if 'level' in data_point else None
    grouping_level_first = grouping_level[0] if grouping_level is not None else None
    grouping_category = data_point["category"] if 'category' in data_point else None
    # if highest_level == grouping_level:
    #     return "lowest level should be lower than highest level"
    individual_metric_output = {}
    highest_level_values = data_scope_first['values']['exact'] if 'values' in data_scope_first \
        and 'exact' in data_scope_first['values'] else []
    default_value_type = data_scope_first['value_type'] if not data_scope_first == {} else None
    data_point_category = data_point['category']
    data_scope_category = data_scope_first['category'] if not data_scope_first == {} else data_point_category
    for curr_metric in raw_data:
        lowest_level = curr_metric
        if data_scope_category == 'geographical':
            lowest_geographical_level = geographical_parent_details['base']
            if data_point_category == 'geographical':
                results_by_lowest_level = False if grouping_level_first == lowest_geographical_level else True
                result_dict = get_details_by_higher_level_geographical(
                    highest_level, highest_level_values, grouping_level_first, results_by_lowest_level)
                curr_dict = result_dict['final_dict']
                curr_highest_level_values = result_dict['single_list']
            else:
                lowest_geographical_level = geographical_parent_details['base']
                result_dict = get_details_by_higher_level_geographical(
                    highest_level, highest_level_values, lowest_geographical_level, 0)
                curr_dict = result_dict['final_dict']
                curr_highest_level_values = result_dict['single_list']
            lgl = lowest_geographical_level
            curr_output = get_details_by_higher_level(lgl, lowest_level, curr_highest_level_values, lgl, lgl, curr_dict,
                                                      [],unilevel_constraints, grouping_category)
        else:
            curr_output = get_details_by_higher_level(highest_level, lowest_level, highest_level_values,
                        default_value_type, grouping_level.copy(), [],unilevel_constraints, grouping_category)
            curr_output_keys = curr_output[0].keys()
            allowed_keys = set([highest_level] + grouping_level + [curr_metric])
            #curr_output = key_replace_group(curr_output,'supplier','flattype')
            if not curr_output_keys<=allowed_keys:
                curr_output = sum_array_by_keys(curr_output, [highest_level]+grouping_level,[curr_metric])
        individual_metric_output[lowest_level] = curr_output

    matching_format_metrics = get_similar_structure_keys(individual_metric_output, grouping_level)
    combined_array = []

    first_metric_array = individual_metric_output[matching_format_metrics[0]] if len(
        matching_format_metrics) > 0 else []
    for ele_id in range(0, len(first_metric_array)):
        curr_dict = first_metric_array[ele_id]
        new_dict = curr_dict.copy()
        for metric in matching_format_metrics[1:len(matching_format_metrics)]:
            new_dict[metric] = individual_metric_output[metric][ele_id][metric]
        combined_array.append(new_dict)

    single_array = merge_dict_array_dict_multiple_keys(individual_metric_output, grouping_level)
    single_array_keys = single_array[0].keys() if len(single_array) > 0 else []
    reverse_map = {}
    for key in single_array_keys:
        reverse_key = level_name_by_model_id[key] if key in level_name_by_model_id else None
        if reverse_key in raw_data:
            reverse_map[reverse_key] = key
    if "sublevel" in data_point:
        single_array = date_to_other_groups(single_array,grouping_level, data_point["sublevel"],
                                            raw_data, highest_level_values)
    derived_array = copy.deepcopy(single_array)
    metric_names = []
    metric_processed = []

    for curr_metric in metrics:
        a_code = curr_metric[0]
        b_code = curr_metric[1]
        op = curr_metric[2]
        a = get_metrics_from_code(a_code,raw_data, metric_names)
        if type(a_code) is str:
            if a_code[0] == 'm':
                a_code = a_code[1:]
                a = metric_names[int(a_code) - 1]
                a_source = metric_names
            else:
                a = raw_data[int(a_code) - 1]
        else:
            a = a_code
        if type(b_code) is str:
            if b_code[0] == 'm':
                b_code = b_code[1:]
                b = metric_names[int(b_code) - 1]
                b_source = metric_names
            else:
                b = raw_data[int(b_code) - 1]
        else:
            b = b_code

        metric_name_a = curr_metric[3]['nr'] if len(curr_metric) > 3 and 'nr' in curr_metric[3] else a
        metric_name_b = curr_metric[3]['dr'] if len(curr_metric) > 3 and 'dr' in curr_metric[3] else b
        metric_name_op = curr_metric[3]['op'] if len(curr_metric) > 3 and 'op' in curr_metric[3] else op
        metric_name = str(metric_name_a) + metric_name_op + str(metric_name_b)
        metric_names.append(metric_name)
        metric_processed.append({
            "a": a,
            "b": b,
            "op": op,
            "name": metric_name
        })

    for curr_dict in derived_array:
        for curr_metric in metric_processed:
            a = curr_metric["a"]
            b = curr_metric["b"]
            nr_value = a
            dr_value = b
            if type(nr_value) is str:
                nr_value = curr_dict[a] if a in curr_dict else curr_dict[reverse_map[a]]
            if type(dr_value) is str:
                dr_value = curr_dict[b] if b in curr_dict else curr_dict[reverse_map[b]]
            result_value = binary_operation(float(nr_value), float(dr_value), curr_metric['op']) if \
                not dr_value == 0 and nr_value is not None and dr_value is not None else None
            curr_dict[curr_metric['name']] = result_value

    stats = []
    statistics_array = []
    if statistical_information is not {}:
        stats = statistical_information['stats']
        stat_metrics_indices = statistical_information['metrics']
        stat_metrics = []
        for curr_index in stat_metrics_indices:
            stat_metrics.append(get_metrics_from_code(curr_index,raw_data,metric_names))
        metrics_array_dict = sum_array_by_single_key(derived_array, stat_metrics)

    for curr_stat in stats:
        statistics_array = statistics_map[curr_stat](derived_array, metrics_array_dict)
        derived_array = statistics_array

    if higher_level_statistical_information is not {}:
        stats = higher_level_statistical_information['stats']
        stat_metrics_indices = higher_level_statistical_information['metrics']
        grouping_level = higher_level_statistical_information['level']
        stat_metrics = []
        for curr_index in stat_metrics_indices:
            stat_metrics.append(get_metrics_from_code(curr_index,raw_data,metric_names))
        higher_level_list = append_array_by_keys(derived_array,grouping_level,stat_metrics)

    for curr_stat in stats:
        higher_level_list = statistics_map[curr_stat](higher_level_list,stat_metrics)


    return {"individual metrics":individual_metric_output, "lower_group_data": derived_array,
            "higher_group_data":higher_level_list}


def get_details_by_higher_level(highest_level, lowest_level, highest_level_list, default_value_type=None,
                                grouping_level=None, all_results = [], unilevel_constraints = {},
                                grouping_category = ""):
    # check for custom sequence
    incrementing_value = None
    if lowest_level == None:
        return []
    if grouping_level == None:
        grouping_level = highest_level
    if not type(grouping_level) == 'str':
        grouping_levels = grouping_level
        grouping_level = grouping_level[0]
    else:
        grouping_levels = [grouping_level]
    custom_level = lowest_level+'_'+grouping_level+'_'+highest_level
    if len(grouping_levels) > 1 or grouping_levels[0] in reverse_direct_match:
        default_map = count_details_parent_map_multiple
    else:
        default_map = count_details_parent_map
    if highest_level == None:
        highest_level = grouping_level
    if grouping_category == 'time':
        default_map = count_details_parent_map_time
    if custom_level in default_map:
        lowest_level_original = lowest_level
        lowest_level = custom_level
    if 'hotness_level' in lowest_level:
        incrementing_value = int(lowest_level[-1])
        lowest_level = lowest_level[:-1]
    if lowest_level not in default_map:
        default_map = count_details_parent_map
    second_lowest_parent = default_map[lowest_level]['parent']
    second_lowest_parent_name_model = default_map[lowest_level]['parent_name_model']
    parent_type = 'single'
    original_grouping_levels = None
    if ',' in second_lowest_parent or ',' in second_lowest_parent_name_model:
        parents = [x.strip() for x in second_lowest_parent.split(',')]
        original_grouping_levels = grouping_levels.copy()
        for i in range(0,len(grouping_levels)):
            if grouping_levels[i] in reverse_direct_match and reverse_direct_match[grouping_levels[i]] in parents:
                grouping_levels[i] = reverse_direct_match[grouping_levels[i]]
        desc_sequence = [parents, lowest_level]
        parent_model_names = second_lowest_parent_name_model.split(',')
        if not parents[0] == highest_level:
            parent_type = 'multiple'
        else:
            second_lowest_parent = parents[0]
    if parent_type == 'single':
        desc_sequence = find_level_sequence(highest_level, lowest_level, default_map)
        #parent_type = 'single'
        parents = [second_lowest_parent]
    curr_level_id = 0
    last_level_id = len(desc_sequence) - 1
    common_keys = []
    while curr_level_id < last_level_id:
        curr_level = desc_sequence[curr_level_id]
        next_level = desc_sequence[curr_level_id+1]
        if curr_level not in grouping_levels:
            common_keys.append(curr_level)
        entity_details = default_map[next_level]
        (model_name, database_type, self_model_name, parent_model_name, storage_type) = (
            entity_details['model_name'], entity_details['database_type'], entity_details['self_name_model'],
            entity_details['parent_name_model'], entity_details['storage_type'])

        if parent_type == 'multiple':
            if default_value_type in parents:
                value_type_index = parents.index(default_value_type)
                parent_model_name = parent_model_names[value_type_index]
        else:
            parent_model_names = [parent_model_name]

        if curr_level_id == 0:
            match_list = highest_level_list
        else:
            match_list = next_level_match_list
        query = []

        if next_level == lowest_level and not unilevel_constraints == {}:
            first_constraint_index = list(unilevel_constraints.keys())[0]
            first_constraint = unilevel_constraints[first_constraint_index]
            add_category = first_constraint['category']
            add_map_name = add_category + '_parent_names'
            add_variable_name = eval(add_map_name)['default']
            add_match_type = first_constraint["match_type"]
            add_match_list = first_constraint["values"]

        # general queries common to all storage types
        if database_type == 'mongodb':
            add_constraint = []
            project_dict = {}
            group_dict = {}
            if highest_level_list == [] or highest_level_list is None:
                match_dict ={}

            else:
                match_constraint = [{parent_model_name: {"$in": match_list}}]
                match_dict = {"$and": match_constraint}
            if next_level == lowest_level and not unilevel_constraints == {}:
                project_dict = {add_variable_name:1}
                if add_match_type == 0:
                    add_match_list = add_match_list["exact"]
                    add_constraint = [{add_variable_name:{"$in": match_list}}]
                else:
                    add_match_list = add_match_list["range"]
                    start_value = add_match_list[0]
                    end_value = add_match_list[1]
                    if add_category == 'time':
                        start_value = datetime.strptime(start_value, "%Y-%m-%d")
                        end_value = datetime.strptime(end_value, "%Y-%m-%d")
                    add_constraint = [{add_variable_name:{"$gte": start_value, "$lte": end_value}}]
                match_constraint = match_constraint + add_constraint
        elif database_type == 'mysql':
            add_query = ''
            if next_level == lowest_level and not unilevel_constraints == {}:
                if add_match_type == 0:
                    add_query = '.filter(' + add_variable_name + '__in=add_match_list)'
                    add_match_list = add_match_list["exact"]
                else:
                    add_query = '.filter(' + add_variable_name + '__range=add_match_list)'
                    add_match_list = add_match_list["range"]
            if highest_level_list == [] or highest_level_list is None:
                full_query = model_name + '.objects.all()'
            else:
                first_part_query = model_name + '.objects.filter('
                full_query = first_part_query + parent_model_name + '__in=match_list)'
            full_query = full_query + add_query
            query = list(eval(full_query).values(self_model_name, parent_model_name))
        else:
            return "database does not exist"

        if storage_type == 'unique' or storage_type == 'name':
            if database_type == 'mongodb':
                group_dict.update({"_id":{self_model_name: '$' + self_model_name},
                              self_model_name: {"$first": '$' + self_model_name}})
                project_dict.update({self_model_name: 1, "_id":0})
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
            elif database_type == 'mysql':
                all_results.append(query)
                next_level_match_list = list(set([x[self_model_name] for x in query]))
            else:
                print("database does not exist")

        elif storage_type == 'count' or storage_type == 'sum' or storage_type == 'condition':
            if database_type == 'mongodb':
                if 'hotness_level' in next_level:
                    next_level = next_level + str(incrementing_value)
                if next_level == custom_level:
                    project_dict.update({lowest_level_original:1, "_id":0})
                else:
                    project_dict.update({next_level:1, "_id":0})
                if storage_type == 'count':
                    if next_level == custom_level:
                        group_dict.update({'_id': {}, lowest_level_original: {"$sum": 1}})
                    else:
                        group_dict.update({'_id': {}, next_level: {"$sum": 1}})
                elif storage_type == 'sum':
                    group_dict.update({'_id': {}, next_level: {"$sum": self_model_name}})
                else:
                    if 'incrementing_value' in entity_details:
                        incrementing_value = entity_details['incrementing_value']
                    if incrementing_value is not None:
                        group_dict.update({'_id': {}, next_level: {"$sum":
                        {"$cond":[{"$eq": ["$"+self_model_name,incrementing_value]}, 1, 0]}}})
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
                if not query==[]:
                    all_results.append(query)
            elif database_type == 'mysql':
                all_values = parent_model_names.copy()
                all_values.append(self_model_name)
                query = list(eval(full_query).values(*all_values))
                query_grouped = sum_array_by_key(query,parent_model_names, self_model_name)
                query=query_grouped
                if not query==[]:
                    all_results.append(query)
                #query2 = merge_dict_array_array_multiple_keys(all_results,parent_model_names)
                next_level_match_array = [x[self_model_name] for x in query if x[self_model_name] is not None]
                if storage_type == 'count':
                    next_level_match_list = len(next_level_match_array)
                else:
                    next_level_match_array=[int(x) for x in next_level_match_array]
                    next_level_match_list = [sum(next_level_match_array)]
            else:
                print("database does not exist")
        else:
            print("pass")
        curr_level_id = curr_level_id+1
        if not len(all_results) == 0 and isinstance(all_results[0], dict):
            all_results = [all_results]
    if not len(all_results)==[]:
        new_results = convert_dict_arrays_keys_to_standard_names(all_results)
        try:
            single_array_results = merge_dict_array_array_multiple_keys(new_results, grouping_levels)
        except:
            single_array_results = merge_dict_array_array_multiple_keys(new_results, ['supplier'])
        if original_grouping_levels is not None:
            single_array_results = key_replace_group(single_array_results, grouping_levels[0],
                                                     original_grouping_levels[0], lowest_level)
    else:
        single_array_results = []
    return single_array_results


def get_details_by_higher_level_geographical(highest_level, highest_level_list, lowest_level='supplier',
                                             results_by_lowest_level=0):
    # highest_level = request.data['highest_level']
    # lowest_level = request.data['lowest_level'] if 'lowest_level' in request.data else 'supplier'
    # highest_level_list = request.data['highest_level_list']
    model_name = geographical_parent_details['model_name']
    parent_name_model = geographical_parent_details['member_names'][highest_level]
    self_name_model = geographical_parent_details['member_names'][lowest_level]
    match_list = highest_level_list
    query = eval(model_name + '.objects.filter(' + parent_name_model + '__in=match_list)')
    lowest_level = geographical_parent_details['base']
    lowest_level_model_name = geographical_parent_details['base_model_name']
    if results_by_lowest_level == 1:
        query_values = list(query.values(parent_name_model, self_name_model, lowest_level_model_name))
        list_values = list(query.values_list(lowest_level_model_name, flat=True))
    else:
        query_values = list(query.values(parent_name_model, self_name_model))
        list_values = list(query.values_list(self_name_model, flat=True))
    list_values_distinct = list(set([x for x in list_values if x is not None]))
    final_values_with_null = [dict(t) for t in {tuple(d.items()) for d in query_values}]
    final_dict = [d for d in final_values_with_null if all(d.values())]
    return {'final_dict':final_dict, 'single_list':list_values_distinct}


def get_details_by_date(lowest_level, highest_level, highest_level_list):

    match_dict = {}

    match_constraint = [{parent_model_name: {"$in": match_list}}]
    final_result = mongo_client.leads.aggregate(
    [
        {
            "$match": {"campaign_id": ["BYJMACC9CA", "TESYOG06F2"]}
        },
        {
            "$group":
                {
                    "_id": {"year":{"$year": "$created_at"},
                            "month":{"$month": "$created_at"},
                            "day":{"$dayOfMonth": "$created_at"}},
                    "campaign_id": {"$first": '$campaign_id'},
                    "total_leads_count": {"$sum": 1},
                    "hot_leads_count": {"$sum": {"$cond": ["$is_hot", 1, 0]}},
                }
        }
    ])


def key_replace_group(dict_array, existing_key, required_key, sum_key):
    if existing_key == required_key:
        return dict_array
    key_details = count_details_direct_match_multiple[existing_key]
    model_name = key_details['model_name']
    database_type = key_details['database_type']
    self_name_model = key_details['self_name_model']
    parent_name_model = key_details['parent_name_model']
    match_list = [x[existing_key] for x in dict_array]
    new_array = []
    if database_type == 'mysql':
        first_part_query = model_name + '.objects.filter('
        full_query = first_part_query + self_name_model + '__in=match_list)'
        query = list(eval(full_query).values_list(self_name_model, parent_name_model))
        query_dict = dict(query)
        for curr_dict in dict_array:
            curr_dict[required_key] = query_dict[curr_dict[existing_key]]
            curr_dict.pop(existing_key)
            new_array.append(curr_dict)
        all_keys = list(curr_dict.keys())
        grouping_keys = all_keys
        grouping_keys.remove(sum_key)
        new_array = sum_array_by_key(new_array,grouping_keys, sum_key)
    else:
        new_array = dict_array
    return new_array


class GetLeadsDataGeneric(APIView):
    @staticmethod
    def put(request):
        all_data = request.data
        default_raw_data = ['total_leads', 'hot_leads']
        default_metrics = []
        data_scope = all_data['data_scope'] if 'data_scope' in all_data else {}
        data_point = all_data['data_point'] if 'data_point' in all_data else {}
        raw_data = all_data['raw_data'] if 'raw_data' in all_data else default_raw_data
        metrics = all_data['metrics'] if 'metrics' in all_data else default_metrics
        statistical_information = all_data['statistical_information'] if 'statistical_information' in all_data else {}
        higher_level_statistical_information = all_data['higher_level_statistical_information'] if \
            'higher_level_statistical_information' in all_data else {}
        mongo_query = get_data_analytics(data_scope, data_point, raw_data, metrics, statistical_information,
                                         higher_level_statistical_information)
        return handle_response('', data=mongo_query, success=True)


class AnalyticSavedOperators(APIView):
    @staticmethod
    def post(request):
        operator_value = request.data['operator_value']
        owner_type = request.data['owner_type']
        operator_name = request.data['operator_name']
        user = request.user
        user_id = user.id
        organisation_id = get_user_organisation_id(user)
        owner_id = user_id if owner_type == 'user' else organisation_id
        final_operator_data = {}
        last_operator_list = mongo_client.analytic_operators.find_one(sort=[("operator_id", -1)])
        operator_id = 1
        if last_operator_list is not None:
            operator_id = last_operator_list["operator_id"] + 1
        final_operator_data ={
            "operator_id": operator_id,
            "owner_type": owner_type,
            "owner_id": str(owner_id),
            "operator_value": operator_value,
            "operator_name": operator_name
        }
        mongo_client.analytic_operators.insert_one(final_operator_data)
        return handle_response('', data="success", success=True)
    
    @staticmethod
    def get(request):
        query_type = request.query_params.get('type')
        query_value = request.query_params.get('value')
        if query_type == 'operator_id':
            query_dict = mongo_client.analytic_operators.find_one({'operator_id':int(query_value)})
        elif query_type == 'operator_name':
            query_dict = mongo_client.analytic_operators.find_one({'operator_name': str(query_value)})
        operator_data = query_dict["operator_value"] if query_dict is not None else {}
        return handle_response('', data=operator_data, success=True)

    @staticmethod
    def put(request):
        query_type = request.data['type']
        query_value = request.data['value']
        if query_type == 'operator_id':
            query_dict = mongo_client.analytic_operators.find_one({'operator_id': int(query_value)})
        elif query_type == 'operator_name':
            query_dict = mongo_client.analytic_operators.find_one({'operator_name': str(query_value)})
        operator_data = query_dict["operator_value"] if query_dict is not None else {}
        if operator_data == {}:
            return handle_response('', data=operator_data, success=True)
        data_scope = request.data['data_scope'] if 'data_scope' in request.data else operator_data['data_scope']
        data_point = request.data['data_point'] if 'data_point' in request.data else operator_data['data_point']
        raw_data = request.data['raw_data'] if 'raw_data' in request.data else operator_data['raw_data']
        metrics = operator_data['metrics']
        mongo_query = get_data_analytics(data_scope, data_point, raw_data, metrics)
        return handle_response('', data=mongo_query, success=True)


# class Calculator:
#     def sum(self, a, b):
#         return a + b
#
#
# class TestCalculator(TestCase):
#     @patch('Calculator.sum', return_value = 9)
#     def test_sum(self, sum):
#         self.assertEqual(sum(2, 3), 9)