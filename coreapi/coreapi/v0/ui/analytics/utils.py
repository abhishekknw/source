import numpy as np
from v0.ui.supplier.models import SupplierPhase
from datetime import datetime
import pytz, copy


def get_metrics_from_code(code, raw_metrics, derived_metrics):
    if type(code) is str:
        if code[0] == 'm':
            code_index = code[1:]
            metric = derived_metrics[int(code_index) - 1]
        else:
            metric = raw_metrics[int(code) - 1]
    else:
        metric=code
    return metric


weekday_names = {'0': 'Monday', '1': 'Tuesday', '2': 'Wednesday', '3': 'Thursday',
                 '4': 'Friday', '5': 'Saturday', '6': 'Sunday'}
weekday_codes = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
                 'Friday': 4, 'Saturday': 5, 'Sunday': 6}


level_name_by_model_id = {
    "supplier_id": "supplier", "object_id": "supplier", "campaign_id": "campaign", "proposal_id": "campaign",
    "flat_count": "flat","total_negotiated_price":"cost", "created_at": "date", "phase_no": "phase"
}


count_details_kids_map = {
    'campaign': {'supplier', 'checklist'},
    'supplier': {'flat'}
}


count_details_parent_map = {
    'supplier':{'parent': 'campaign', 'model_name': 'ShortlistedSpaces', 'database_type': 'mysql',
                'self_name_model': 'object_id', 'parent_name_model': 'proposal_id', 'storage_type': 'name'},
    'checklist': {'parent': 'campaign', 'model_name': 'checklists', 'database_type': 'mongodb',
                  'self_name_model': 'checklist_id', 'parent_name_model': 'campaign_id', 'storage_type': 'unique'},
    'flat': {'parent': 'supplier', 'model_name': 'SupplierTypeSociety', 'database_type': 'mysql',
             'self_name_model': 'flat_count', 'parent_name_model': 'supplier_id', 'storage_type': 'sum'},
    'lead': {'parent': 'campaign', 'model_name': 'leads', 'database_type': 'mongodb',
             'self_name_model': 'entry_id', 'parent_name_model': 'campaign_id', 'storage_type': 'count'},
    'hot_lead': {'parent': 'campaign', 'model_name': 'leads', 'database_type': 'mongodb',
                 'self_name_model': 'is_hot', 'parent_name_model': 'campaign_id',
                 'storage_type': 'condition'},
    'cost': {'parent': 'campaign', 'model_name':'ShortlistedSpaces', 'database_type': 'mysql',
             'self_name_model': 'total_negotiated_price', 'parent_name_model': 'proposal_id',
             'storage_type': 'sum'},
    'phase': {'parent': 'campaign', 'model_name': 'SupplierPhase', 'database_type': 'mysql',
              'self_model_name': 'phase_no', 'parent_name_model':'campaign_id', 'storage_type': 'unique'},
    'hot_lead^': {'parent': 'campaign', 'model_name': 'leads', 'database_type': 'mongodb',
                  'self_name_model': 'hotness_level', 'parent_name_model': 'campaign_id',
                  'storage_type': 'condition'}
}

count_details_parent_map_multiple = {
    'lead': {'parent': 'supplier,campaign', 'model_name': 'leads', 'database_type': 'mongodb',
             'self_name_model': 'entry_id', 'parent_name_model': 'supplier_id,campaign_id', 'storage_type': 'count'},
    'hot_lead': {'parent': 'supplier,campaign', 'model_name': 'leads', 'database_type': 'mongodb',
                 'self_name_model': 'is_hot', 'parent_name_model': 'supplier_id,campaign_id',
                 'storage_type': 'condition'},
    'cost': {'parent': 'supplier,campaign', 'model_name': 'ShortlistedSpaces', 'database_type': 'mysql',
             'self_name_model': 'total_negotiated_price', 'parent_name_model': 'object_id,proposal_id',
             'storage_type': 'sum'},
    'date': {'parent': 'campaign,phase', 'model_name': 'SupplierPhase', 'database_type': 'mysql',
             'self_model_name': 'start_date+end_date', 'parent_name_model': 'campaign_id, phase_no',
             'storage_type': 'range'}
}

count_details_parent_map_time = {
    'lead': {'parent': 'date,campaign', 'model_name': 'leads', 'database_type': 'mongodb',
             'self_name_model': 'entry_id', 'parent_name_model': 'created_at,campaign_id', 'storage_type': 'count'},
    'hot_lead': {'parent': 'date,campaign', 'model_name': 'leads', 'database_type': 'mongodb',
                 'self_name_model': 'is_hot', 'parent_name_model': 'created_at,campaign_id', 'storage_type': 'condition'},
    'hot_lead^': {'parent': 'date, campaign', 'model_name': 'leads', 'database_type': 'mongodb',
                  'self_name_model': 'hotness_level', 'parent_name_model': 'created_at,campaign_id',
                  'storage_type': 'condition'}
    }

geographical_parent_details = {
    'base': 'supplier', 'model_name': 'SupplierTypeSociety', 'database_type': 'mysql',
    'base_model_name':'supplier_id', 'storage_type': 'name',
    'member_names': {'locality': 'society_locality', 'city': 'society_city', 'state': 'society_state',
                     'supplier': 'supplier_id'}
}

date_to_others = {
    'phase': {'model_name': 'SupplierPhase', 'variables':{'date':['start_date','end_date'],'campaign':['campaign_id'],},
              'self_name_model': 'phase_no'}
}


time_parent_names = {
    "default": "created_at"
}


def z_calculator_array_multiple(data_array, metrics_array_dict):
    result_array = []
    global_data = {}
    for curr_metric in metrics_array_dict:
        global_data[curr_metric] = {}
        global_data[curr_metric]['global_mean'] = np.mean(metrics_array_dict[curr_metric])
        global_data[curr_metric]['stdev'] = np.std(metrics_array_dict[curr_metric])
    for curr_data in data_array:
        for curr_metric in metrics_array_dict:
            global_mean = global_data[curr_metric]['global_mean']
            stdev = global_data[curr_metric]['stdev']
            curr_mean = curr_data[curr_metric]
            if curr_mean is None:
                continue
            z_value = (curr_mean - global_mean) / stdev if not stdev == 0 else 0
            z_score_name = curr_metric+' z_score'
            z_color_name = curr_metric+' z_category'
            curr_data[z_score_name] = z_value
            if z_value > 1:
                color = 'Green'
            elif z_value < -1:
                color = 'Red'
            else:
                color = 'Yellow'
            curr_data[z_color_name] = color

    return data_array


# redundant
def sum_array_by_key(array, keys):
    count_dict = {}
    # valid_array =[]
    # for curr_dict in array:
    #     append = True
    #     for curr_key in keys:
    #         if curr_dict[curr_key] is None:
    #             append = False
    #     if append:
    #         valid_array.append(curr_dict)
    for curr_key in keys:
        values = [x[curr_key] for x in array if x[curr_key] is not None]
        count_dict[curr_key]=values
    return count_dict


def binary_operation(a, b, op):
    operator_map = {"/": round(float(a)/b,5), "*":a*b, "+":a+b, "-": a-b}
    return operator_map[op]


def merge_dict_array_dict_multiple_keys(metric_dict, key_names):
    return merge_dict_array_array_multiple_keys(list(metric_dict.values()),key_names)


def merge_dict_array_dict_single(metric_dict, key_name):
    key_values = []
    final_array = []
    metric_list = list(metric_dict.keys())
    first_key = metric_list[0]
    first_array = metric_dict[first_key]
    local_key_names = {}
    for curr_metric in metric_dict:
        curr_array = metric_dict[curr_metric]
        if curr_array == []:
            continue
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


def find_key_alias_dict_array(dict_array, key_name):
    first_element = dict_array[0]
    dict_keys = first_element.keys()
    for key in dict_keys:
        if key in level_name_by_model_id and level_name_by_model_id[key]==key_name:
            return key
    return key_name


# Input: dict array: [{"supplier_id":"S1","campaign_id":"C1"},{"supplier_id":"S2","campaign_id":"C2"}]
# Output: [{"supplier":"S1","campaign":"C1"},{"supplier":"S2","campaign":"C2"}]
def convert_dict_arrays_keys_to_standard_names(dict_arrays):
    final_array = []
    for curr_array in dict_arrays:
        new_array = []
        for curr_dict in curr_array:
            keys = list(curr_dict.keys())
            for curr_key in keys:
                new_key = level_name_by_model_id[curr_key] if curr_key in level_name_by_model_id else curr_key
                if not curr_key == new_key:
                    curr_dict[new_key] = curr_dict.pop(curr_key)
            new_array.append(curr_dict)
        final_array.append(new_array)
    return final_array


def ranged_data_to_other_groups(base_array, range_array, start_field, end_field,
                                base_value_field, assigned_value_field, other_fields):
    if len(other_fields)>1:
        return "this part is not developed yet"
    else:
        other_field = other_fields[0]
    if assigned_value_field in level_name_by_model_id:
        assigned_value_field_standard = level_name_by_model_id[assigned_value_field]
    else:
        assigned_value_field_standard = assigned_value_field
    new_array = []
    # first_dict = base_array[0]
    # if other_field not in first_dict:
    #     other_field = level_name_by_model_id[other_field]
    for curr_dict in base_array:
        curr_value = curr_dict[base_value_field]
        other_value = curr_dict[other_field] if other_field in curr_dict else \
            curr_dict[level_name_by_model_id[other_field]]
        if isinstance(curr_value, datetime):
            curr_value = pytz.utc.localize(curr_value)
        assigned_value_array = [x[assigned_value_field] for x in range_array if x[other_field] == other_value and
                          x[end_field] > curr_value > x[start_field]]
        if assigned_value_array == []:
            assigned_value_array = [0]
        if len(assigned_value_array) > 1:
            continue
        curr_dict[assigned_value_field_standard] = assigned_value_array[0]
        curr_dict.pop(base_value_field)
        new_array.append(curr_dict)
    return new_array


def merge_dict_array_array_single(array, key_name):
    final_array=[]
    if array==[]:
        return array
    first_array = array[0]
    first_array_element = first_array[0]
    if key_name not in first_array_element:
        key_name = level_name_by_model_id[key_name]
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


def merge_dict_array_array_multiple_keys(arrays, key_names):
    final_array = []
    if arrays==[]:
        return arrays
    first_array = arrays[0]
    second_array = []
    for i in range(1,len(arrays)):
        curr_array = arrays[i]
        for first_dict in first_array:
            for curr_dict in curr_array:
                match = True
                for key in key_names:
                    if not curr_dict[key]==first_dict[key]:
                        match = False
                if match:
                    new_dict = curr_dict.copy()
                    new_dict.update(first_dict)
                    second_array.append(new_dict)
        first_array = second_array
        second_array = []
    return first_array


def sum_array_by_key(array, grouping_keys, sum_key):
    new_array = []
    required_keys = [sum_key] + grouping_keys
    for curr_dict in array:
        first_match = False
        curr_dict_sum = int(curr_dict[sum_key]) if curr_dict[sum_key] is not None else 0
        for curr_dict_new in new_array:
            match = True
            curr_dict_new_sum = int(curr_dict_new[sum_key]) if curr_dict_new[sum_key] is not None else 0
            for key in grouping_keys:
                curr_value = curr_dict[key]
                curr_value_new = curr_dict_new[key]
                if not curr_value_new == curr_value:
                    match = False
            if match:
                curr_dict_new[sum_key] = curr_dict_sum + curr_dict_new_sum
                first_match = True
        if not first_match:
            new_dict = {}
            for required_key in required_keys:
                new_dict[required_key] = curr_dict[required_key]
            new_array.append(new_dict)
    return new_array


# function to check whether a dict array key structure matches a desired key array
def get_similar_structure_keys(main_dict, required_keys):
    keys = main_dict.keys()

    similar_array = []
    for key_name in keys:
        curr_array = main_dict[key_name]
        if curr_array == []:
            continue
        curr_keys = curr_array[0].keys()
        curr_keys = [level_name_by_model_id[x] if x in level_name_by_model_id else x for x in
                         curr_keys]
        if not isinstance(required_keys, list):
            required_keys = [required_keys]
        matching_keys = required_keys + [key_name]
        if curr_keys == matching_keys:
            similar_array.append(key_name)
    return similar_array


def find_level_sequence(highest_level, lowest_level, default_map = count_details_parent_map):

    sequence = []
    curr_level = lowest_level
    n_levels = 3
    n=0
    while n < n_levels:
        sequence.append(curr_level)
        if curr_level == highest_level:
            desc_sequence = sequence[::-1]
            return desc_sequence
        elif curr_level not in default_map:
            error_message = "incorrect hierarchy"
            return error_message
        else:
            next_level = default_map[curr_level]['parent']
            curr_level = next_level
            n = n + 1
    if n >= n_levels:
        error_message = "too many levels"
    return error_message


def date_to_other_groups(dict_array, group_name, desired_metric, lowest_level, highest_level_values):
    sequential_time_metrics = ['day','month','year']
    new_dict = {}
    new_array = []
    all_keys_sequential = []

    for curr_dict in dict_array:
        all_keys = list(curr_dict.keys())
        curr_date = curr_dict[group_name[0]]
        if desired_metric == 'date':
            new_date = curr_date.strftime('%d/%m/%y')
            if new_date in new_dict:
                for curr_key in all_keys:
                    if curr_key == group_name[0]:
                        new_dict[new_date][curr_key] = new_date
                    else:
                        new_dict[new_date][curr_key] = new_dict[new_date][curr_key]+curr_dict[curr_key]
            else:
                new_dict[new_date] = {}
                for curr_key in all_keys:
                    if curr_key == group_name[0]:
                        new_dict[new_date][curr_key] = new_date
                    else:
                        new_dict[new_date][curr_key] = curr_dict[curr_key]
        elif desired_metric in sequential_time_metrics:
            required_time_metrics = []
            curr_key_sequential = {}
            for curr_metric in sequential_time_metrics:
                if curr_metric == desired_metric or (not required_time_metrics == []):
                    required_time_metrics.append(curr_metric)
                    new_value_query = 'curr_date.'+curr_metric
                    new_value = eval(new_value_query)
                    curr_key_sequential[curr_metric] = new_value
            if curr_key_sequential not in all_keys_sequential:
                all_keys_sequential.append(curr_key_sequential)
            curr_dict.update(curr_key_sequential)
            curr_dict.pop(group_name[0])
            new_array.append(curr_dict)
        elif desired_metric == 'weekday':
            curr_weekday = curr_date.weekday()
            curr_dict['weekday'] = curr_weekday
            new_array.append(curr_dict)
        elif desired_metric == 'phase':
            model_details = date_to_others[desired_metric]
            model_name = model_details['model_name']
            variables = model_details['variables']
            variables_list = list(variables.keys())
            start_field = variables[variables_list[0]][0]
            end_field = variables[variables_list[0]][1]
            assigned_field = model_details['self_name_model']
            other_fields = variables[variables_list[1]]
            first_part_query = model_name + '.objects.filter('
            full_query = first_part_query + other_fields[0] + '__in=highest_level_values)'
            query_results = list(eval(full_query).values(start_field,end_field,other_fields[0], assigned_field))
            phase_adjusted_results = ranged_data_to_other_groups(copy.deepcopy(dict_array),query_results,start_field, end_field,
                                                                 group_name[0], assigned_field, other_fields)
            new_array = phase_adjusted_results
        else:
            return dict_array
    if desired_metric == 'weekday' or desired_metric == 'phase':
        if desired_metric in date_to_others:
            group_name = list(date_to_others[desired_metric]['variables'].keys())
        group_name.remove('date')
        group_name.append(desired_metric)
        new_array = sum_array_by_key(new_array,group_name, lowest_level)
    if new_array == []:
        new_array = list(new_dict.values())

    return new_array


