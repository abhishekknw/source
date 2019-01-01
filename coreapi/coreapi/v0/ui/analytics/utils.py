import numpy as np


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


level_name_by_model_id = {
    "supplier_id": "supplier", "object_id": "supplier", "campaign_id": "campaign", "proposal_id": "campaign",
    "flat_count": "flat","total_negotiated_price":"cost", "created_at": "date"
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
    'lead': {'parent': 'supplier,campaign', 'model_name': 'leads', 'database_type': 'mongodb',
             'self_name_model': 'entry_id', 'parent_name_model': 'supplier_id,campaign_id', 'storage_type': 'count'},
    'hot_lead': {'parent': 'supplier,campaign', 'model_name': 'leads', 'database_type': 'mongodb',
                 'self_name_model': 'is_hot', 'parent_name_model': 'supplier_id,campaign_id',
                 'storage_type': 'condition'},
    'cost': {'parent': 'supplier,campaign', 'model_name':'ShortlistedSpaces', 'database_type': 'mysql',
             'self_name_model': 'total_negotiated_price', 'parent_name_model': 'object_id,proposal_id',
             'storage_type': 'sum'},
    'phase': {'parent': 'campaign', 'model_name': 'SupplierPhase', 'database_type': 'mysql',
              'self_model_name': 'phase_no', 'parent_model_name':'campaign_id', 'storage_type': 'unique'},
    'date': {'parent': 'campaign,phase', 'model_name': 'SupplierPhase', 'database_type': 'mysql',
             'self_model_name': 'start_date+end_date', 'parent_model_name': 'campaign_id, phase_no',
             'storage_type': 'range'}
}

count_details_parent_map_time = {
    'lead': {'parent': 'date', 'model_name': 'leads1', 'database_type': 'mongodb',
             'self_name_model': 'entry_id', 'parent_name_model': 'created_at', 'storage_type': 'count'},
    'hot_lead': {'parent': 'date', 'model_name': 'leads1', 'database_type': 'mongodb',
                 'self_name_model': 'is_hot', 'parent_name_model': 'created_at', 'storage_type': 'condition'},
}

geographical_parent_details = {
    'base': 'supplier', 'model_name': 'SupplierTypeSociety', 'database_type': 'mysql',
    'base_model_name':'supplier_id', 'storage_type': 'name',
    'member_names': {'locality': 'society_locality', 'city': 'society_city', 'state': 'society_state',
                     'supplier': 'supplier_id'}
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


# def merge_dict_array_dict_single(metric_dict, key_name):
#     key_values = []
#     final_array = []
#     metric_list = metric_dict.keys()
#     first_array = metric_dict[metric_list[0]]
#     local_key_names = {}
#     for curr_metric in metric_dict:
#         curr_array = metric_dict[curr_metric]
#         if curr_array == []:
#             continue
#         local_key_name = find_key_alias_dict_array(curr_array, key_name)
#         local_key_names[curr_metric] = local_key_name
#         if curr_array==first_array:
#             key_values = [x[local_key_name] for x in curr_array]
#     for curr_value in key_values:
#         curr_final_dict = {}
#         missing_value = False
#         for curr_metric in metric_list:
#             local_key_name = local_key_names[curr_metric]
#             curr_dict = [x for x in metric_dict[curr_metric] if x[local_key_name]==curr_value]
#             if not curr_dict == []:
#                 curr_final_dict.update(curr_dict[0])
#             else:
#                 missing_value = True
#                 continue
#         if missing_value == False:
#             final_array.append(curr_final_dict)
#     return final_array


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


def date_to_other_groups(dict_array, group_name, desired_metric):
    sequential_time_metrics = ['day','month','year']
    new_dict = {}
    new_array = []
    all_keys_sequential = []
    for curr_dict in dict_array:
        all_keys = list(curr_dict.keys())
        curr_date = curr_dict[group_name]
        if desired_metric == 'date':
            new_date = curr_date.strftime('%d/%m/%y')
            if new_date in new_dict:
                for curr_key in all_keys:
                    if curr_key == group_name:
                        new_dict[new_date][curr_key] = new_date
                    else:
                        new_dict[new_date][curr_key] = new_dict[new_date][curr_key]+curr_dict[curr_key]
            else:
                new_dict[new_date] = {}
                for curr_key in all_keys:
                    if curr_key == group_name:
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
            # if curr_key_sequential in all_keys_sequential:
            #     for curr_key in all_keys:
            #         if curr_key == group_name:
            #             new_dict[curr_key_sequential][curr_key] = curr_dict[curr_key]
            #         else:
            #             new_dict[curr_key_sequential][curr_key] = new_dict[curr_key_sequential][curr_key]\
            #                                                       + curr_dict[curr_key]
            # else:
            #     all_keys_sequential.append(curr_key_sequential)
            #     new_dict[curr_key_sequential] = {}
            #     for curr_key in all_keys:
            #         new_dict[curr_key_sequential][curr_key] = curr_dict[curr_key]
            curr_dict.update(curr_key_sequential)
            curr_dict.pop(group_name)
            new_array.append(curr_dict)
        else:
            return dict_array
    if new_array == []:
        new_array = list(new_dict.values())
    return new_array


