from __future__ import print_function
from __future__ import absolute_import
from .utils import (level_name_by_model_id, convert_date_to_days, merge_dict_array_dict_single,
                    convert_dict_arrays_keys_to_standard_names, get_similar_structure_keys, geographical_parent_details,
                    count_details_parent_map, find_level_sequence, binary_operation, count_details_direct_match_multiple,
                    sum_array_by_key, z_calculator_array_multiple, get_metrics_from_code, reverse_direct_match,
                    count_details_parent_map_time, date_to_other_groups, merge_dict_array_array_multiple_keys,
                    merge_dict_array_dict_multiple_keys, count_details_parent_map_multiple, sum_array_by_keys,
                    sum_array_by_single_key, append_array_by_keys, frequency_mode_calculator, var_stdev_calculator,
                    mean_calculator, count_details_parent_map_custom, flatten, flatten_dict_array,
                    round_sig_min, time_parent_names, raw_data_unrestricted, averaging_metrics_list,
                    key_replace_group_multiple, key_replace_group, truncate_by_value_ranges, linear_extrapolator,
                    get_constrained_values, add_related_field, related_fields_dict, reverse_supplier_levels,
                    add_binary_field_status, binary_parameters_list, get_list_elements_frequency_mongo,
                    cumulative_distribution, get_list_elements_single_array, cumulative_distribution_from_array,
                    cumulative_distribution_from_array_day)
from v0.ui.common.models import mongo_client
from v0.ui.proposal.models import ShortlistedSpaces, ProposalInfo, ProposalCenterMapping
from v0.ui.supplier.models import SupplierTypeSociety
import copy
from rest_framework.views import APIView
from v0.ui.utils import handle_response, get_user_organisation_id
from datetime import datetime
from bson.objectid import ObjectId
# from unittest import TestCase
# from unittest.mock import patch
# import unittest
import numpy as np
from v0.ui.campaign.models import CampaignAssignment

statistics_map = {"z_score": z_calculator_array_multiple, "frequency_distribution": frequency_mode_calculator,
                  "variance_stdev": var_stdev_calculator, "mean": mean_calculator,
                  "straight_line_forecasting": linear_extrapolator}

unilevel_categories = ['time']

custom_keys = ['total_orders_punched_cum_pct','date_old',"lead_date"]


def get_reverse_dict(original_dict):
    keys = original_dict.keys()
    reverse_dict = {}
    for curr_key in keys:
        curr_values = original_dict[curr_key]
        if isinstance(curr_values, list) == False:
            curr_values = [curr_values]
        for value in curr_values:
            reverse_dict[value] = curr_key
    return reverse_dict


# first_part_query = model_name + '.objects.filter('
# full_query = first_part_query + parent_model_name + '__in=match_list)'
# add_query = '.filter(' + add_variable_name + '__in=add_match_list)'
# add_match_list = add_match_list["exact"]
def get_campaigns_from_vendors(vendor_list):
    model_name = 'ProposalInfo'
    parent_name_model = 'principal_vendor_id'
    self_name_model = 'proposal_id'
    match_list = vendor_list
    full_query = model_name + '.objects.filter(' + parent_name_model + '__in=match_list)'
    #ProposalInfo.objects.filter(principal_vendor_id__in=['1', 'v2'])
    final_query = eval(full_query)
    if not final_query:
        return [{},[]]
    final_dict = dict(final_query.values_list(self_name_model, parent_name_model))
    next_level_array = list(final_dict.keys())
    final_result = [final_dict, next_level_array]
    return final_result


def get_data_analytics(data_scope, data_point, raw_data, metrics, statistical_information,
                       higher_level_statistical_information, bivariate_statistical_information,
                       custom_functions = []):
    unilevel_constraints = {}
    supplier_constraints = {}
    data_scope_first = {}
    if not data_scope == {}:
        data_scope_keys = list(data_scope.keys()) if not data_scope == {} else []
        for curr_key in data_scope_keys:
            if data_scope[curr_key]["category"] in unilevel_categories:
                if "range" in data_scope[curr_key]["values"]:
                    data_range = data_scope[curr_key]["values"]["range"]
                    if not (len(data_range)) == 2:
                        return "data scope range not defined properly"
                unilevel_constraints[curr_key] = data_scope[curr_key]
                data_scope.pop(curr_key)
                continue
            if data_scope[curr_key]["category"] == 'supplier':
                supplier_constraints = data_scope[curr_key]["values"]
                data_scope.pop(curr_key)
        data_scope_first = data_scope[data_scope_keys[0]] if data_scope_keys is not [] else {}
    highest_level = data_scope_first['value_type'] if 'value_type' in data_scope_first else data_scope_first['level']

    data_summary = 0
    if 'category' not in data_point or 'level' not in data_point:
        return []
    elif 'summary' in data_point:
        data_summary = data_point['summary']
    grouping_level = data_point['level'] if 'level' in data_point else None
    grouping_level_first = grouping_level[0] if grouping_level is not None else None
    grouping_category = data_point["category"] if 'category' in data_point else None

    individual_metric_output = {}
    highest_level_values = data_scope_first['values']['exact'] if 'values' in data_scope_first \
        and 'exact' in data_scope_first['values'] else []
    default_value_type = data_scope_first['value_type'] if not data_scope_first == {} else None
    data_point_category = data_point['category']
    value_ranges = data_point['value_ranges'] if 'value_ranges' in data_point else {}
    range_type = data_point.get('range_type',0)
    data_scope_category = data_scope_first['category'] if not data_scope_first == {} else data_point_category
    highest_level_original = highest_level
    if highest_level == 'vendor':
        highest_level_original = 'vendor'
        values = data_scope_first['values']['exact'] if 'values' in data_scope_first \
                                                        and 'exact' in data_scope_first['values'] else []
        [vendor_values_dict, vendor_level_values_list] = get_campaigns_from_vendors(values)
        if vendor_values_dict == {}:
            return "vendors do not exist"
        highest_level_values = vendor_level_values_list
        highest_level = 'campaign'
        default_value_type = 'campaign'
    supplier_list = []

    raw_data_original = raw_data.copy()
    raw_data_lf = raw_data.copy() # raw data with lead first
    if 'lead' in raw_data_lf and not raw_data_lf[0]=='lead':
        raw_data_lf.remove('lead')
        raw_data_lf.insert(0,'lead')
    common_supplier_list = []
    for curr_metric in raw_data_lf:
        zero_filter = False
        # if curr_metric in zero_filtered_raw_data:
        #     zero_filter = True
        if '_nz' in curr_metric:
            zero_filter = True
            curr_index = raw_data_lf.index(curr_metric)
            original_index = raw_data.index(curr_metric)
            curr_metric = curr_metric[:-3]
            raw_data_lf[curr_index] = curr_metric
            raw_data[original_index] = curr_metric
        lowest_level = curr_metric
        curr_index = raw_data_lf.index(curr_metric)
        print("current_level: ",lowest_level)
        if data_scope_category == 'geographical':
            lowest_geographical_level = geographical_parent_details['base']
            if data_point_category == 'geographical':
                results_by_lowest_level = False if grouping_level_first == lowest_geographical_level else True
                result_dict = get_details_by_higher_level_geographical(
                    highest_level, highest_level_values, grouping_level_first, results_by_lowest_level)
                curr_dict = result_dict['final_dict']
                curr_highest_level_values = result_dict['single_list']
            else:
                value_type = 'supplier'
                lowest_geographical_level = geographical_parent_details['base']
                result_dict = get_details_by_higher_level_geographical(
                    highest_level, highest_level_values, lowest_geographical_level, 0)
                curr_dict = result_dict['final_dict']
                curr_highest_level_values = result_dict['single_list']
            lgl = lowest_geographical_level
            hl = lgl
            #lgl = ["supplier","campaign"]
            grouping_level_original = None
            if lgl not in grouping_level:
                grouping_level_original = grouping_level.copy()
                grouping_level = [lgl] + grouping_level
            if len(grouping_level) > 1:
                hl = grouping_level[-1]

            curr_output_all = get_details_by_higher_level(hl, lowest_level, curr_highest_level_values, lgl, grouping_level,
                                                      curr_dict, unilevel_constraints, grouping_category, value_ranges,
                                                          zero_filter= zero_filter)
            curr_output = curr_output_all[0]
            supplier_list = curr_output_all[1]
            # add missing key, if needed
            if len(individual_metric_output.keys())>0:
                prev_raw_data = list(individual_metric_output.keys())
                ref_data_all = individual_metric_output[prev_raw_data[0]]
                ref_data = ref_data_all[0]
                missing_keys = (set(ref_data.keys())-set(curr_output[0].keys())) - set(raw_data)
                common_key = set.intersection(set(ref_data.keys()),set(curr_output[0].keys()))
                if len(missing_keys)>0:
                    missing_key = list(missing_keys)[0]
                    new_array = []
                    for curr_dict in curr_output:
                        query_list = [curr_dict[x] for x in common_key]
                        for prev_dict in ref_data_all:
                            match_list = [prev_dict[x] for x in common_key]
                            value = prev_dict[missing_key]
                            if query_list == match_list:
                                curr_dict[missing_key] = value
                                new_array.append(curr_dict)
                    curr_output = new_array

            if grouping_level_original is not None:
                curr_output = sum_array_by_keys(curr_output, [highest_level]+grouping_level_original,[curr_metric])
                grouping_level = grouping_level_original
        else:
            curr_output_all = get_details_by_higher_level(highest_level, lowest_level, highest_level_values,
                          default_value_type, grouping_level.copy(), [],unilevel_constraints, grouping_category,
                          value_ranges, supplier_constraints, supplier_list = supplier_list, zero_filter = zero_filter,
                                                          custom_functions = custom_functions)
            curr_output = curr_output_all[0]
            supplier_list = curr_output_all[1]

            if curr_output == []:
                continue
            if highest_level_original == 'vendor':
                curr_output_new = []
                for curr_dict in curr_output:
                    curr_key = curr_dict[default_value_type]
                    curr_value = vendor_values_dict[curr_key]
                    curr_dict[highest_level_original] = curr_value
                    curr_output_new.append(curr_dict)
                curr_output = curr_output_new

            curr_output_keys = curr_output[0].keys()
            allowed_keys = set([highest_level_original] + grouping_level + [curr_metric])
            if 'order_cumulative' in custom_functions:
                allowed_keys = allowed_keys.union(set(custom_keys))
            # if not curr_output_keys<=allowed_keys:
            #     curr_output = sum_array_by_keys(curr_output, list(allowed_keys-set([curr_metric])),[curr_metric])
        if data_summary == 1:
            print("summarizing data")
            final_value = sum([x[curr_metric] for x in curr_output])
            curr_output = final_value
        individual_metric_output[lowest_level] = curr_output

    for curr_metric in raw_data_original:
        if '_nz' in curr_metric:
            zero_filter = True
            curr_metric = curr_metric[:-3]
        if curr_metric not in individual_metric_output:
            continue
        curr_output = individual_metric_output[curr_metric]
        if curr_metric == 'total_orders_punched' and 'order_cumulative' in custom_functions:
            curr_grouping_levels = [highest_level_original]+ list(set(reverse_supplier_levels(grouping_level))
                                                                  - set({"date"}))
            if 'supplier' not in curr_grouping_levels:
                curr_grouping_levels = curr_grouping_levels + ["supplier"]
            curr_output = convert_date_to_days(curr_output, curr_grouping_levels,
                                                             ['total_orders_punched'], 'date')
        if 'supplier' in curr_output[0]:
            curr_output = [x for x in curr_output if x['supplier'] in supplier_list]
            superlevels_base_set = ['supplier']
            superlevels = [x for x in grouping_level if x in reverse_direct_match]
            curr_metric_sp_case = 'hotness_level_' if 'hotness_level' in curr_metric else curr_metric
            storage_type = count_details_parent_map[curr_metric_sp_case]['storage_type']
            if len(superlevels)>0:
                curr_output = key_replace_group_multiple(curr_output, superlevels_base_set[0], superlevels, curr_metric,
                                                         value_ranges, None, storage_type)
        curr_output_keys = set(curr_output[0].keys())
        allowed_keys = set([highest_level_original] + grouping_level + [curr_metric])
        if 'order_cumulative' in custom_functions:
            curr_output = cumulative_distribution_from_array_day(curr_output, grouping_level,
                                                             ['total_orders_punched'], 'date')
            allowed_keys = allowed_keys.union(set(custom_keys))
        curr_sum_key = [curr_metric]
        if not curr_output_keys <= allowed_keys:
            curr_output = sum_array_by_keys(curr_output, list(allowed_keys - set([curr_metric])), [curr_metric])
        individual_metric_output[curr_metric] = curr_output

    reverse_map = {}
    custom_binary_field_labels = data_point["custom_binary_field_labels"] if "custom_binary_field_labels" in data_point\
        else {}
    if data_summary == 0:
        if grouping_level[0] in reverse_direct_match.keys() or data_scope_category == 'geographical' \
                or data_point["level"] == ["date"]:
            single_array = merge_dict_array_dict_multiple_keys(individual_metric_output, [highest_level]+grouping_level)
        else:
            single_array = merge_dict_array_dict_multiple_keys(individual_metric_output, grouping_level)
        # adding binary fields status, such as 'fliertype', 'postertype', etc.
        single_array = add_binary_field_status(single_array,binary_parameters_list,
                                               custom_binary_field_labels = custom_binary_field_labels)
        single_array_keys = single_array[0].keys() if len(single_array) > 0 else []
        for key in single_array_keys:
            reverse_key = level_name_by_model_id[key] if key in level_name_by_model_id else None
            if reverse_key in raw_data:
                reverse_map[reverse_key] = key
        if "sublevel" in data_point:
            single_array = date_to_other_groups(single_array,[grouping_level[0]], data_point["sublevel"],
                                                raw_data, highest_level_values)
        single_array_subleveled = copy.deepcopy(single_array)
        single_array_truncated = truncate_by_value_ranges(single_array_subleveled,value_ranges, range_type)

        if single_array_truncated == []:
            print("no data within the given range")
            return {"individual metrics": individual_metric_output, "lower_group_data": [],
                    "higher_group_data": []}
        derived_array_original = single_array_truncated
    else:
        derived_array_original = [individual_metric_output.copy()]
        single_array_keys = list(individual_metric_output.keys())
        for key in single_array_keys:
            reverse_key = level_name_by_model_id[key] if key in level_name_by_model_id else None
            if reverse_key in raw_data:
                reverse_map[reverse_key] = key
    derived_array = derived_array_original
    additional_fields_list = list(related_fields_dict.keys())
    for curr_field in additional_fields_list:
        derived_array = add_related_field(derived_array, *(related_fields_dict[curr_field]))

    metric_parents = {}
    remaining_metrics = individual_metric_output.keys()
    metric_names = []
    metric_processed = []
    for curr_metric in metrics:
        curr_metric_parents = []
        a_code = curr_metric[0]
        b_code = curr_metric[1]
        op = curr_metric[2]
        a = get_metrics_from_code(a_code,raw_data, metric_names)
        if type(a_code) is str:
            if a_code[0] == 'm':
                a_code = a_code[1:]
                a = metric_names[int(a_code) - 1]
                curr_metric_parents.append(metric_parents[a])
                a_source = metric_names
            else:
                a = raw_data[int(a_code) - 1]
                curr_metric_parents.append(a)
        else:
            a = a_code
        if type(b_code) is str:
            if b_code[0] == 'm':
                b_code = b_code[1:]
                b = metric_names[int(b_code) - 1]
                curr_metric_parents.append(metric_parents[b])
                b_source = metric_names
            else:
                b = raw_data[int(b_code) - 1]
                curr_metric_parents.append(b)
        else:
            b = b_code

        # giving custom names to metrics
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

        metric_parents[metric_name] = curr_metric_parents

    for curr_dict in derived_array:
        for curr_metric in metric_processed:
            a = curr_metric["a"]
            b = curr_metric["b"]
            if (a in raw_data and a not in remaining_metrics) or (b in raw_data and b not in remaining_metrics):
                return {"individual metrics": individual_metric_output,
                        "lower_group_data": "missing data for some metrics",
                        "higher_group_data": "missing data for some metrics"}

            nr_value = a
            dr_value = b
            if type(nr_value) is str:
                nr_value = curr_dict[a] if a in curr_dict else curr_dict[reverse_map[a]]
            if type(dr_value) is str:
                dr_value = curr_dict[b] if b in curr_dict else curr_dict[reverse_map[b]]
            result_value = binary_operation(float(nr_value), float(dr_value), curr_metric['op']) if \
                not dr_value == 0 and nr_value is not None and dr_value is not None else None
            curr_dict[curr_metric['name']] = round_sig_min(result_value) if result_value is not None else result_value

    stats = []
    statistics_array = []
    higher_level_list = []
    if not statistical_information == {}:
        stats = statistical_information['stats']
        stat_metrics_indices = statistical_information['metrics']
        stat_metrics = []
        for curr_index in stat_metrics_indices:
            stat_metrics.append(get_metrics_from_code(curr_index,raw_data,metric_names))
        metrics_array_dict = sum_array_by_single_key(derived_array, stat_metrics)

        for curr_stat in stats:
            statistics_array = statistics_map[curr_stat](derived_array, metrics_array_dict)
            derived_array = statistics_array
    bsi = []
    if not bivariate_statistical_information == {}:
        stats = list(bivariate_statistical_information.keys())
        for curr_stat in stats:
            stat_array = bivariate_statistical_information[curr_stat]
            y_stat = get_metrics_from_code(stat_array[0], raw_data,metric_names) # dependent metrics
            x_stat = get_metrics_from_code(stat_array[1], raw_data,metric_names) # independent metrics
            n_pts = stat_array[2] if len(stat_array)>2 else 100 # no. of points to extrapolate
            diff = stat_array[3] if len(stat_array)>3 else 0.01 # fraction of range per point
            curr_dict = statistics_map[curr_stat](derived_array, y_stat, x_stat, n_pts, diff)
            if curr_dict is not None:
                bsi.append(curr_dict)

    if not higher_level_statistical_information == {}:
        stats = higher_level_statistical_information['stats']
        stat_metrics_indices = higher_level_statistical_information['metrics']
        grouping_level = higher_level_statistical_information['level']
        stat_metrics = []
        for curr_index in stat_metrics_indices:
            stat_metrics.append(get_metrics_from_code(curr_index,raw_data,metric_names))
        raw_data_list = []
        for prev_data in raw_data:
            curr_data = prev_data
            raw_data_list.append(curr_data)
            new_metric_names = []
        for curr_dict in derived_array:
            for curr_metric in metric_processed:
                a = curr_metric["a"]
                b = curr_metric["b"]
                nr = a
                dr = b
                if isinstance(nr, str):
                    nr_value = curr_dict[nr] if nr in curr_dict else curr_dict[reverse_map[nr]]
                else:
                    nr_value = nr
                if isinstance(dr, str):
                    dr_value = curr_dict[dr] if dr in curr_dict else curr_dict[reverse_map[dr]]
                else:
                    dr_value = dr
                result_value = binary_operation(float(nr_value), float(dr_value), curr_metric['op']) if \
                    not dr_value == 0 and nr_value is not None and dr_value is not None else None
                new_name = curr_metric['name']
                new_metric_names.append(new_name)
                curr_dict[new_name] = round_sig_min(result_value, 7) if result_value is not None else result_value
        higher_level_list_old = append_array_by_keys(derived_array,grouping_level,stat_metrics+raw_data)
        for curr_field in additional_fields_list:
            higher_level_list_test = add_related_field(higher_level_list_old, *(related_fields_dict[curr_field]))

        higher_level_list = []
        higher_level_raw_data = []
        for curr_dict in higher_level_list_old:
            for curr_metric in raw_data:
                curr_name = curr_metric
                curr_list = curr_dict[curr_metric]
                if not type(curr_list)==list:
                    curr_list = [curr_list]
                curr_list = [int(y) for y in curr_list if y is not None]
                if curr_metric in averaging_metrics_list:
                    curr_value = np.mean(curr_list)
                else:
                    curr_value = sum(curr_list)
                curr_dict[curr_name] = curr_value
                if len(higher_level_raw_data) < len(raw_data):
                    higher_level_raw_data.append(curr_name)
            higher_level_list.append(curr_dict)

        new_stat_metrics = []
        for curr_stat in stat_metrics:
            new_name = curr_stat
            new_stat_metrics.append(new_name)
        for curr_stat in stats:
            weighted = 0
            pfix = 'weighted_'
            if curr_stat[:len(pfix)] == pfix:
                curr_stat = curr_stat[len(pfix):]
                weighted = 1
            print(statistics_map[curr_stat])
            higher_level_list = statistics_map[curr_stat](higher_level_list,stat_metrics, weighted=weighted)

    custom_function_output = {}
    if not custom_functions == []:
        for curr_function in custom_functions:
            if curr_function == "order_cumulative":
                campaign_list = data_scope_first["values"]["exact"]
                model_name = "leads"
                outer_key = "data"
                inner_key = "key_name"
                inner_value = 'Order Punched Date'
                nonnull_key = "value"
                frequency_results = {}
                sum_results = {}
                for curr_campaign in campaign_list:
                    match_dict = {"campaign_id": curr_campaign}
                    curr_res = get_list_elements_frequency_mongo(model_name, match_dict, outer_key, inner_key,
                                                                 inner_value, nonnull_key)
                    frequency_results[curr_campaign] = curr_res[0]
                    sum_results[curr_campaign] = curr_res[1]
                cumulative_frequency_results = cumulative_distribution(campaign_list, frequency_results, sum_results,
                                                                       'date', 'total orders punched pct')
                custom_function_output["order_cumulative"] = cumulative_frequency_results


    return {"individual metrics":individual_metric_output, "lower_group_data": derived_array,
            "higher_group_data":higher_level_list, "bivariate_statistical_information": bsi,
            "custom function output": custom_function_output}


def get_details_by_higher_level(highest_level, lowest_level, highest_level_list, default_value_type=None,
                                grouping_level=None, all_results = [], unilevel_constraints = {},
                                grouping_category = "", value_ranges = {}, supplier_constraints = {},
                                supplier_list = [], zero_filter = False, custom_functions = []):
    incrementing_value = None
    if lowest_level == None:
        return []
    if 'hotness_level' in lowest_level:
        incrementing_value = int(lowest_level[-1])
        lowest_level = lowest_level[:-1]
    if highest_level == 'city':
        highest_level_original = 'city'
        highest_level = 'campaign'
    else:
        highest_level_original = highest_level
    # check for custom sequence
    if grouping_level == None:
        grouping_level = highest_level
    if not isinstance(grouping_level,str):
        grouping_levels = grouping_level
        grouping_level = grouping_level[0]
    else:
        grouping_levels = [grouping_level]
    try:
        custom_level = lowest_level+'_'+grouping_level+'_'+highest_level
    except:
        custom_level = ''
    if (len(grouping_levels) > 1 or grouping_levels[0] in reverse_direct_match) and \
            lowest_level in count_details_parent_map_multiple:
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

    if lowest_level not in default_map:
        default_map = count_details_parent_map
        if lowest_level not in count_details_parent_map:
            print("incorrect raw data: ", lowest_level)
            return []
    if len(grouping_levels)>=3:
        trial_map = count_details_parent_map_custom
        if lowest_level in trial_map:
            default_map = trial_map
    second_lowest_parent = default_map[lowest_level]['parent']
    second_lowest_parent_name_model = default_map[lowest_level]['parent_name_model']
    parent_type = 'single'
    original_grouping_levels = None
    superlevels = [x for x in grouping_levels if x in reverse_direct_match]
    superlevels_base = []
    if len(superlevels)>0:
        original_grouping_levels = grouping_levels.copy()
        for i in range(0,len(grouping_levels)):
            if grouping_levels[i] in reverse_direct_match and \
                    (reverse_direct_match[grouping_levels[i]] in second_lowest_parent or
                     reverse_direct_match[grouping_levels[i]] == lowest_level):
                grouping_levels[i] = reverse_direct_match[grouping_levels[i]]
                superlevels_base.append(grouping_levels[i])
    if ',' in second_lowest_parent or ',' in second_lowest_parent_name_model:
        parents = [x.strip() for x in second_lowest_parent.split(',')]
        original_grouping_levels = grouping_levels.copy() if original_grouping_levels is None \
            else original_grouping_levels

        if (highest_level_original == 'city' or highest_level_original in reverse_direct_match) \
                and len(grouping_levels)>1 and grouping_levels[1] in reverse_direct_match:
            original_grouping_levels = [grouping_levels[1]]
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
    if not default_value_type == desc_sequence[0] and not default_value_type in desc_sequence[0]:
        desc_sequence_original = desc_sequence.copy()
        desc_sequence = desc_sequence[1:]
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

        # so far, only for restricting date in data scope
        if next_level == lowest_level and not unilevel_constraints == {} and not lowest_level in raw_data_unrestricted:
            first_constraint_index = list(unilevel_constraints.keys())[0]
            first_constraint = unilevel_constraints[first_constraint_index]
            add_category = first_constraint['category']
            add_map_name = add_category + '_parent_names'
            add_variable_name = eval(add_map_name)['default']
            if lowest_level in ['lead','hot_lead','total_booking_confirmed','total_orders_punched']:
                add_variable_name = "lead_date"
            add_match_type = first_constraint["match_type"]
            add_match_list = first_constraint["values"]

        # now restricting by supplier
        if (curr_level=='supplier' or 'supplier' in curr_level) and not supplier_constraints == {}:
            supplier_category = "supplier"
            supplier_match_type = 0
            supplier_model_name = SupplierTypeSociety
            supplier_match_list = get_constrained_values('SupplierTypeSociety','supplier_id',supplier_constraints)

        # general queries common to all storage types
        match_dict = {}
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
                if not (next_level == 'total_orders_punched' and 'order_cumulative' in custom_functions):
                    match_constraint = match_constraint + add_constraint
                    match_dict = {"$and": match_constraint}
        elif database_type == 'mysql':
            add_query = ''
            if next_level == lowest_level and not unilevel_constraints == {} and \
                    lowest_level not in raw_data_unrestricted:
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

        elif storage_type == 'count' or storage_type == 'sum' or storage_type == 'condition' or \
                storage_type == 'append' or storage_type == 'mean':
            self_model_name_mongo = '$' + self_model_name
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
                    group_dict.update({'_id': {}, next_level: {"$sum": self_model_name_mongo}})
                elif storage_type == 'mean':
                    group_dict.update({'_id': {}, next_level: {"$avg": self_model_name}})
                else:
                    if 'incrementing_value' in entity_details:
                        incrementing_value = entity_details['incrementing_value']
                    if incrementing_value is not None:
                        if 'increment_type' in entity_details and entity_details['increment_type'] == 3:
                            group_dict.update({'_id': {}, next_level: {"$sum":
                            {"$cond": [{"$gte": ["$" + self_model_name,incrementing_value]}, 1, 0]}}})
                        else:
                            group_dict.update({'_id': {}, next_level: {"$sum":
                            {"$cond":[{"$eq": ["$"+self_model_name,incrementing_value]}, 1, 0]}}})
                    else:
                        group_dict = {'_id': {}, next_level: {"$sum": {"$cond": ["$"+self_model_name, 1, 0]}}}
                for curr_parent_model_name in parent_model_names:
                    group_dict["_id"][curr_parent_model_name] = '$' + curr_parent_model_name
                    group_dict[curr_parent_model_name] = {"$first": '$' + curr_parent_model_name}
                    project_dict[curr_parent_model_name] = 1
                new_results = None
                if next_level == 'total_orders_punched' and 'order_cumulative' in custom_functions:
                    new_model_name = 'leads'
                    outer_key = 'data'
                    inner_key = 'key_name'
                    inner_value = 'Order Punched Date'
                    nonnull_key = 'value'
                    other_keys = parent_model_names
                    new_results = get_list_elements_single_array(new_model_name, match_dict.copy(), outer_key,
                                                                inner_key, inner_value, nonnull_key, other_keys)
                query = mongo_client[model_name].aggregate(
                    [
                        {"$match": match_dict},
                        {"$group": group_dict},
                        {"$project": project_dict}
                    ]
                )
                query = list(query)
                if new_results:
                    query = new_results
                if not query==[]:
                    if not all_results == [] and isinstance(all_results[0], dict) == True:
                        all_results = [all_results]
                    all_results.append(query)
            elif database_type == 'mysql':
                all_values = parent_model_names.copy()
                all_values.append(self_model_name)
                if 'other_grouping_column' in entity_details:
                    other_column = entity_details['other_grouping_column']
                    all_values.append(other_column)
                query = list(eval(full_query).values(*all_values))

                if 'other_grouping_column' in entity_details:
                    other_column_list = [x[other_column] for x in query]
                if self_model_name == 'cost_per_flat' and grouping_levels == ['campaign']:
                    model_name = 'SupplierTypeSociety'
                    col_name = 'supplier_id'
                    joining_data_query = model_name + '.objects.filter('+ col_name + '__in=other_column_list)'
                    joining_data = dict(eval(joining_data_query).values_list(col_name, 'flat_count'))
                    query_new = []
                    for curr_dict in query:
                        self_value = curr_dict[self_model_name]
                        if curr_dict[other_column] not in joining_data:
                            continue
                        joining_value = joining_data[curr_dict[other_column]]
                        if self_value is not None and joining_value is not None:
                            new_dict = {}
                            final_value = self_value*joining_value
                            new_dict[parent_model_names[0]] = curr_dict[parent_model_names[0]]
                            new_dict[self_model_name] = final_value
                            query_new.append(new_dict)
                    query = query_new
                query_grouped = sum_array_by_key(query,parent_model_names, self_model_name)

                query=query_grouped
                if not query==[]:
                    if not all_results == [] and isinstance(all_results[0], dict) == True:
                        all_results = [all_results]
                    all_results.append(query)

                #query2 = merge_dict_array_array_multiple_keys(all_results,parent_model_names)
                next_level_match_array = [x[self_model_name] for x in query if x[self_model_name] is not None]
                if storage_type == 'count':
                    next_level_match_list = len(next_level_match_array)
                elif storage_type == 'mean':
                    next_level_match_array = [int(x) for x in next_level_match_array]
                    next_level_match_list = [np.mean(next_level_match_array)]
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
    if not len(all_results)==0:
        new_results = convert_dict_arrays_keys_to_standard_names(all_results)
        try:
            single_array_results = merge_dict_array_array_multiple_keys(new_results, grouping_levels)
        except:
            single_array_results = merge_dict_array_array_multiple_keys(new_results, ['supplier'])

        if zero_filter:
            filtered_results = [x for x in single_array_results if x[lowest_level]>0]
            single_array_results = filtered_results
        if len(single_array_results)>0:
            result_keys = single_array_results[0].keys()
        else:
            result_keys = []
        if "supplier" in result_keys:
            if supplier_list == []:
                supplier_list = [x['supplier'] for x in single_array_results]
            else:
                # if len(single_array_results) > len(supplier_list) and not supplier_list == []:
                #     new_array_results = []
                #     for curr_array in single_array_results:
                #         if curr_array['supplier'] in supplier_list:
                #             new_array_results.append(curr_array)
                new_supplier_list = [x['supplier'] for x in single_array_results]
                net_supplier_list = list(set(supplier_list).intersection(set(new_supplier_list)))
                new_array_results = [x for x in single_array_results if x['supplier'] in net_supplier_list]
                single_array_results = new_array_results
                supplier_list = net_supplier_list

        # if original_grouping_levels is not None:
        #     superlevels = [x for x in original_grouping_levels if x in reverse_direct_match]
        #     superlevels_base_set = list(set(superlevels_base))
        #     if len(superlevels_base_set)>1:
        #         print("this is not developed yet")
        #     elif len(superlevels_base_set) == 1:
        #         base = len([x for x in original_grouping_levels if x == superlevels_base_set[0]])
        #         if len(superlevels)>1 or base==1:
        #             single_array_results = key_replace_group_multiple(single_array_results, superlevels_base_set[0],
        #                             superlevels, lowest_level, value_ranges, incrementing_value, storage_type, base)
        #         elif len(superlevels)==1:
        #             single_array_results = key_replace_group_multiple(single_array_results, superlevels_base_set[0],
        #                         superlevels, lowest_level, value_ranges, incrementing_value, storage_type)
        # if next_level == 'total_orders_punched' and 'order_cumulative' in custom_functions:
        #     curr_grouping_levels = list(set(original_grouping_levels) - set({"date"}))
        #     print(curr_grouping_levels)
        #     print(single_array_results)
        #     single_array_results = cumulative_distribution_from_array(single_array_results, curr_grouping_levels,
        #                                        ['total_orders_punched'],'date')
    else:
        single_array_results = []
    return [single_array_results, supplier_list, match_dict, original_grouping_levels]


def get_details_by_higher_level_geographical(highest_level, highest_level_list, lowest_level='supplier',
                                             results_by_lowest_level=0):
    # highest_level = request.data['highest_level']
    # lowest_level = request.data['lowest_level'] if 'lowest_level' in request.data else 'supplier'
    if highest_level_list == [] or highest_level is None or highest_level == '':
        return {'final_dict':{}, 'single_list':[]}
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


class GetLeadsDataGeneric(APIView):
    @staticmethod
    def put(request):
        success = True
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
        bivariate_statistical_information = all_data.get('bivariate_statistical_information',{})
        custom_functions = all_data.get('custom_functions', [])
        mongo_query = get_data_analytics(data_scope, data_point, raw_data, metrics, statistical_information,
                                         higher_level_statistical_information, bivariate_statistical_information,
                                         custom_functions)
        if type(mongo_query) == str:
            success = False
        return handle_response('', data=mongo_query, success=success)


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

class RangeAPIView(APIView):
    @staticmethod
    def post(request):
        data = request.data
        range_data = []
        for range in data['range_data']:
            range_data.append({
                'range_starts_at': range['starts_at'],
                'range_ends_at': range['ends_at'],
            })
        final_data_dict = {
            "attribute_name": data['attribute_name'],
            "organisation_id": data['organisation_id'],
            "range_data": range_data

        }
        mongo_client.ranges.insert_one(final_data_dict)
        return handle_response('', data={}, success=True)

    @staticmethod
    def get(request):
        organisation_id = request.query_params.get('organisation_id',None)
        data = mongo_client.ranges.find({"organisation_id": organisation_id})
        final_data = []
        for item in data:
            temp_data = {
                "id": str(item['_id']),
                "attribute_name": item['attribute_name'],
                "organisation_id": item['organisation_id'],
                "range_data": []
            }
            for range in item['range_data']:
                temp_data['range_data'].append({
                    "starts_at": range['range_starts_at'],
                    "ends_at": range['range_ends_at']
                })
            final_data.append(temp_data)

        return handle_response('', data=final_data, success=True)

    @staticmethod
    def put(request):
        data = request.data
        id = request.query_params.get('id', None)
        range_data = []
        for range in data['range_data']:
            range_data.append({
                'range_starts_at': range['starts_at'],
                'range_ends_at': range['ends_at'],
            })

        mongo_client.ranges.update_one({"_id": ObjectId(id)},
                                            {"$set": {"attribute_name": data['attribute_name'],
                                                      "organisation_id": data['organisation_id'],
                                                      "range_data": range_data}})
        return handle_response('', data={}, success=True)


def get_all_assigned_campaigns_vendor_city(user_id, city_list = None, vendor_list = None):
    final_result = None
    city_assigned_campaigns = None
    if vendor_list is not None:
        user_campaigns = CampaignAssignment.objects.filter(assigned_to_id=user_id,
                                                             campaign__principal_vendor__in=vendor_list).values_list(
            'campaign_id', flat=True).distinct()
    else:
        user_campaigns = CampaignAssignment.objects.filter(assigned_to_id=user_id).values_list(
            'campaign_id', flat=True).distinct()
    if city_list is not None:
        city_suppliers_result = get_details_by_higher_level_geographical('city',city_list)
        city_suppliers_list = city_suppliers_result['single_list']
        city_campaigns = ShortlistedSpaces.objects.filter(object_id__in=city_suppliers_list).values_list\
            ('proposal_id', flat=True).distinct()
        city_assigned_campaigns = CampaignAssignment.objects.filter(
            assigned_to_id=user_id, campaign_id__in=city_campaigns).values_list('campaign_id', flat=True).distinct()
        final_list = city_assigned_campaigns
        # if vendor_list is not None:
    if city_assigned_campaigns:
        final_list = list(set(user_campaigns).intersection(set(city_assigned_campaigns)))
    else:
        final_list = list(set(user_campaigns))
    final_result = ProposalInfo.objects.filter(proposal_id__in=final_list).extra(select={
                    'campaign_id': 'proposal_id', 'campaign_name': 'name'}).values('campaign_id', 'campaign_name')
    return final_result


class CityVendorCampaigns(APIView):
    @staticmethod
    def put(request):
        user_id = request.user.id
        user_data = request.data
        city_list = user_data.get('cities', None)
        vendor_list = user_data.get('vendors', None)
        all_assigned_campaigns = get_all_assigned_campaigns_vendor_city(user_id, city_list, vendor_list)

        return handle_response({}, data=all_assigned_campaigns, success=True)

