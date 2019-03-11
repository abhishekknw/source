import numpy as np
from v0.ui.supplier.models import SupplierPhase, SupplierTypeSociety
from v0.ui.proposal.models import ProposalInfo
from datetime import datetime
import pytz, copy
from v0.ui.campaign.views import calculate_mode
from collections import Iterable
import math
from v0.ui.organisation.models import Organisation
from scipy import interpolate
from scipy import stats


def flatten(items):
    """Yield items from any nested iterable"""
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            for sub_x in flatten(x):
                yield sub_x
        else:
            yield x


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


alternate_name_keys = {"supplier": "supplier_name", "campaign":"campaign_name"}


weekday_names = {'0': 'Monday', '1': 'Tuesday', '2': 'Wednesday', '3': 'Thursday',
                 '4': 'Friday', '5': 'Saturday', '6': 'Sunday'}
weekday_codes = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
                 'Friday': 4, 'Saturday': 5, 'Sunday': 6}


# list of raw data points which cannot be restricted
raw_data_unrestricted = ['flat','cost','cost_flat']

level_name_by_model_id = {
    "supplier_id": "supplier", "object_id": "supplier", "campaign_id": "campaign", "proposal_id": "campaign",
    "flat_count": "flat","total_negotiated_price": "cost", "created_at": "date", "phase_no": "phase",
    "society_city": "city", "society_name":"supplier_name", "cost_per_flat":"cost_flat", "name":"campaign_name"
}


related_fields_dict = {"campaign": ['ProposalInfo', 'proposal_id', 'campaign', 'name', 'campaign_name'],
                       "supplier": ['SupplierTypeSociety', 'supplier_id', 'supplier', 'society_name', 'supplier_name'],
                       "vendor": ['Organisation', 'organisation_id', 'vendor', 'name', 'vendor_name']
                       }

# increment types: 0 - equal to, 1 - greater than, 2 - less than,
# 3 - greater than or equal to, 4 - less than or equal to
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
    'hotness_level_': {'parent': 'campaign', 'model_name': 'leads', 'database_type': 'mongodb',
                       'self_name_model': 'hotness_level', 'parent_name_model': 'campaign_id',
                       'storage_type': 'condition', 'increment_type':3},
    'supplier,flattype': {'parent': 'flattype', 'model_name': 'SupplierTypeSociety', 'database_type': 'mysql',
                          'self_name_model': 'supplier_id', 'parent_name_model': 'flat_count_type',
                          'storage_type': 'name'},
    'cost_flat': {'parent': 'campaign', 'model_name':'ShortlistedSpaces', 'database_type': 'mysql',
                  'self_name_model': 'cost_per_flat', 'parent_name_model': 'proposal_id',
                  'storage_type': 'sum', 'other_grouping_column':'object_id'}
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
             'storage_type': 'range'},
    'hotness_level_': {'parent': 'supplier,campaign', 'model_name': 'leads', 'database_type': 'mongodb',
                       'self_name_model': 'hotness_level', 'parent_name_model': 'supplier_id,campaign_id',
                       'storage_type': 'condition', 'increment_type': 3},
    'cost_flat': {'parent': 'supplier,campaign', 'model_name': 'ShortlistedSpaces', 'database_type': 'mysql',
                  'self_name_model': 'cost_per_flat', 'parent_name_model': 'object_id,proposal_id',
                  'storage_type': 'sum'}
}

reverse_direct_match = {'flattype':'supplier', 'qualitytype':'supplier','standeetype':'supplier',
                        'fliertype':'supplier','stalltype':'supplier','liftpostertype':'supplier',
                        'nbpostertype':'supplier','bannertype':'supplier', 'bachelortype':'supplier'}


count_details_parent_map_custom = {
    'lead': {'parent': 'date,supplier,campaign', 'model_name': 'leads', 'database_type': 'mongodb',
             'self_name_model': 'entry_id', 'parent_name_model': 'created_at,supplier_id,campaign_id',
             'storage_type': 'count'},
    'hot_lead': {'parent': 'date,supplier,campaign', 'model_name': 'leads', 'database_type': 'mongodb',
                 'self_name_model': 'is_hot', 'parent_name_model': 'created_at,supplier_id,campaign_id',
                 'storage_type': 'condition'},
}


# format: a_b
# list: (a) flat,(b)quality, (c) standee, (d) flier, (e) stall
# (f) poster in lift, (g) poster on notice board, (h) banner, (i)
count_details_direct_match_multiple = {
    'supplier_flattype': {'parent': 'flattype', 'model_name': 'SupplierTypeSociety', 'database_type': 'mysql',
                          'self_name_model': 'supplier_id', 'parent_name_model': 'flat_count_type',
                          'storage_type': 'name'},
    'supplier_qualitytype': {'parent': 'qualitytype', 'model_name': 'SupplierTypeSociety', 'database_type': 'mysql',
                             'self_name_model': 'supplier_id', 'parent_name_model': 'society_type_quality',
                             'storage_type': 'name'},
    'supplier_standeetype': {'parent': 'standeetype', 'model_name': 'SupplierTypeSociety', 'database_type': 'mysql',
                             'self_name_model': 'supplier_id', 'parent_name_model': 'standee_allowed',
                             'storage_type': 'name'},
    'supplier_fliertype': {'parent': 'fliertype', 'model_name': 'SupplierTypeSociety', 'database_type': 'mysql',
                           'self_name_model': 'supplier_id', 'parent_name_model': 'flier_allowed',
                           'storage_type': 'name'},
    'supplier_stalltype': {'parent': 'stalltype', 'model_name': 'SupplierTypeSociety', 'database_type': 'mysql',
                           'self_name_model': 'supplier_id', 'parent_name_model': 'stall_allowed',
                           'storage_type': 'name'},
    'supplier_liftpostertype': {'parent': 'liftpostertype', 'model_name': 'SupplierTypeSociety', 'database_type': 'mysql',
                                'self_name_model': 'supplier_id', 'parent_name_model': 'poster_allowed_lift',
                                'storage_type': 'name'},
    'supplier_nbpostertype': {'parent': 'nbpostertype', 'model_name': 'SupplierTypeSociety', 'database_type': 'mysql',
                              'self_name_model': 'supplier_id', 'parent_name_model': 'poster_allowed_nb',
                              'storage_type': 'name'},
    'supplier_bannertype': {'parent': 'bannertype', 'model_name': 'SupplierTypeSociety', 'database_type': 'mysql',
                            'self_name_model': 'supplier_id', 'parent_name_model': 'banner_allowed',
                            'storage_type': 'name'},
    'supplier_bachelortype': {'parent': 'bachelortype', 'model_name': 'SupplierTypeSociety', 'database_type': 'mysql',
                              'self_name_model': 'supplier_id', 'parent_name_model': 'bachelor_tenants_allowed',
                              'storage_type': 'name'}
}


count_details_parent_map_time = {
    'lead': {'parent': 'date,campaign', 'model_name': 'leads', 'database_type': 'mongodb',
             'self_name_model': 'entry_id', 'parent_name_model': 'created_at,campaign_id', 'storage_type': 'count'},
    'hot_lead': {'parent': 'date,campaign', 'model_name': 'leads', 'database_type': 'mongodb',
                 'self_name_model': 'is_hot', 'parent_name_model': 'created_at,campaign_id', 'storage_type': 'condition'},
    'hotness_level_': {'parent': 'date, campaign', 'model_name': 'leads', 'database_type': 'mongodb',
                  'self_name_model': 'hotness_level', 'parent_name_model': 'created_at,campaign_id',
                  'storage_type': 'condition'},
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


# rounds to sig places with minimum sig significant digits
# if sig = 2. round_sig_min(1547.128) = 1547.12, round_sig_min(0.000313) = 0.00031
def round_sig_min(x,sig=2):
    if x>=1:
        return round(x,2)
    elif x==0:
        return x
    else:
        return round(x, sig-int(math.floor(math.log10(abs(x))))-1)


def z_calculator_array_multiple(data_array, metrics_array_dict, weighted=0):
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
            curr_data[z_score_name] = round_sig_min(z_value)
            if z_value > 1:
                color = 'Green'
            elif z_value < -1:
                color = 'Red'
            else:
                color = 'Yellow'
            curr_data[z_color_name] = color

    return data_array


def calculate_freqdist_mode_from_list_floating(num_list, window_size=5):
    if not type(num_list) == list:
        return {}
    if len(num_list) == 0:
        return {}
    if len(num_list) == 1:
        return [num_list, num_list[0]]
    num_list = sorted(num_list)
    min_max = [num_list[0],num_list[-1]]
    last_window_size = (min_max[1]-min_max[0])%window_size
    last_window_start = min_max[1]-last_window_size
    freq_dist = {}
    num_list_copy = num_list.copy()
    lower_limit = min_max[0] - 0.0001
    actual_length = len(num_list)
    counter = 0
    while lower_limit < min_max[1]:
        upper_limit = lower_limit + window_size
        if upper_limit>min_max[1]:
            upper_limit = min_max[1]
        new_list = [round(x,4) for x in num_list_copy if x> lower_limit and x<=upper_limit]
        if new_list == []:
            lower_limit = upper_limit
            continue
        freq = len(new_list)
        counter = counter+freq
        group_name = str(round(lower_limit,4)) + ' to ' + str(round(upper_limit,4))
        freq_dist[group_name] = {}
        freq_dist[group_name]['values'] = new_list
        freq_dist[group_name]['mode'] = freq
        lower_limit = upper_limit
    return freq_dist


def calculate_freqdist_mode_from_list(num_list, window_size=5):
    if not type(num_list) == list:
        return {}
    if len(num_list) == 0:
        return {}
    if len(num_list) == 1:
        return [num_list, num_list[0]]
    num_list = sorted(num_list)
    min_max = [num_list[0],num_list[-1]]
    max = min_max[1]
    last_window_start = max-max%window_size
    freq_dist = {}
    num_list_copy = num_list.copy()
    lower_limit = 0
    actual_length = len(num_list)
    counter = 0
    while lower_limit <= last_window_start:
        upper_limit = lower_limit + window_size
        new_list = [round(x,4) for x in num_list_copy if lower_limit <= x < upper_limit]
        freq = len(new_list)
        mean = np.mean(new_list) if len(new_list)>0 else None
        counter = counter+freq
        group_name = str(lower_limit) + ' to ' + str(upper_limit)
        freq_dist[group_name] = {}
        if new_list == []:
            lower_limit = upper_limit
            continue
        freq_dist[group_name]['values'] = new_list
        freq_dist[group_name]['mode'] = freq
        freq_dist[group_name]['mean'] = mean
        lower_limit = upper_limit
    return freq_dist


def var_stdev_calculator(dict_array, keys, weighted=0):
    new_array = []
    for curr_dict in dict_array:
        for key in keys:
            num_list = curr_dict[key]
            if num_list == [] or num_list == None or not isinstance(num_list,list):
                continue
            num_list = [x for x in num_list if x is not None]
            stdev_key = 'stdev_' + key
            var_key = 'variance_' + key
            curr_stdev = np.std(num_list)
            curr_var = curr_stdev**2
            curr_dict[stdev_key] = round_sig_min(curr_stdev)
            curr_dict[var_key] = round_sig_min(curr_var)
        new_array.append(curr_dict)
    return new_array


def mean_calculator(dict_array, keys, weighted=0):
    new_array = []
    if weighted == 1:
        for curr_dict in dict_array:
            new_keys = []
            for curr_key in keys:
                new_name = curr_key + '_total'
                new_keys.append(new_name)
                mean_key = 'mean_' + new_name
                curr_dict[mean_key] = curr_dict[new_name]
            new_array.append(curr_dict)
    else:
        for curr_dict in dict_array:
            for key in keys:
                num_list = curr_dict[key]
                if num_list == []:
                    continue
                mean_key = 'mean_' + key
                curr_mean = np.mean(num_list)
                curr_dict[mean_key] = curr_mean
            new_array.append(curr_dict)
    return new_array


def linear_extrapolator(dict_array, y_stat, x_stat, n_pts = 100, diff = 0.01):
    y = [z[y_stat] for z in dict_array]
    x = [z[x_stat] for z in dict_array]
    if len(x)<2 or len(y)<2:
        return None

    #f = interpolate.interp1d(x, y, fill_value='extrapolate',kind='linear')
    [slope, intercept, r_value, p_value, std_err] = stats.linregress(x, y)
    x_range = max(x)-min(x)
    dx = x_range*diff
    ep_min = max(x)+dx
    ep_max = max(x)+n_pts*dx
    xnew = np.arange(min(x), ep_max, dx)
    ynew = [(intercept+slope*x) for x in xnew]
    final_output = {}
    final_output[x_stat] = x
    final_output[y_stat] = y
    xnew_name = x_stat+'_new'
    ynew_name = y_stat+'_new'
    final_output[xnew_name] = [round(x,4) for x in xnew]
    final_output[ynew_name] = [round(y,4) for y in ynew]
    return final_output

# redundant
def sum_array_by_single_key(array, keys):
    count_dict = {}
    for curr_key in keys:
        values = [x[curr_key] for x in array if x[curr_key] is not None]
        count_dict[curr_key]=values
    return count_dict


def binary_operation(a, b, op):
    operator_map = {"/": round(float(a)/b,5) if not b==0 else None, "*":a*b, "+":a+b, "-": a-b}
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


def flatten_dict_array(dict_array):
    new_array = []
    for curr_dict in dict_array:
        if isinstance(curr_dict, list) and curr_dict == [curr_dict[0]]:
            new_array = new_array + curr_dict
        else:
            new_array.append(curr_dict)
    return new_array


# Input: dict array: [{"supplier_id":"S1","campaign_id":"C1"},{"supplier_id":"S2","campaign_id":"C2"}]
# Output: [{"supplier":"S1","campaign":"C1"},{"supplier":"S2","campaign":"C2"}]
def convert_dict_arrays_keys_to_standard_names(dict_arrays):
    final_array = []
    for curr_array in dict_arrays:
        new_array = []
        for curr_dict in curr_array:
            if curr_dict == []:
                continue
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
    elif len(other_fields)==1:
        other_field = other_fields[0]
    else:
        return []
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


# get names of keys common to one or more dict arrays in array of arrays
def get_common_keys(arrays):
    key_set_list = []
    for dict_array in arrays:
        first_dict = dict_array[0]
        first_dict_keyset = set(first_dict.keys())
        key_set_list.append(first_dict_keyset)
    all_keys = set.intersection(*key_set_list)
    return all_keys


def merge_dict_array_array_multiple_keys(arrays, key_names):
    #key_names = ['date','campaign']
    final_array = []
    if arrays==[]:
        return arrays
    # if len(key_names) == 1:
    #     return merge_dict_array_array_single(arrays, key_names[0])
    common_keys_set = get_common_keys(arrays)
    if len(set.intersection(set(key_names),common_keys_set)) == 0:
        key_names = list(common_keys_set)
    first_array = arrays[0]
    second_array = []
    for i in range(1,len(arrays)):
        curr_array = arrays[i]
        for first_dict in first_array:
            for curr_dict in curr_array:
                match = True
                for key in key_names:
                    if key in curr_dict:
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


def append_array_by_keys(array, grouping_keys, append_keys):
    new_array = []
    required_keys = list(set(append_keys + grouping_keys))
    for curr_dict in array:
        first_match = False
        curr_dict_lists = {}
        for curr_dict_new in new_array:
            match = True
            curr_dict_new_lists = {}
            for key in grouping_keys:
                curr_value = curr_dict[key]
                curr_value_new = curr_dict_new[key]
                if not curr_value_new == curr_value:
                    match = False
            if match:
                for append_key in append_keys:
                    prev_list = [curr_dict[append_key]] if curr_dict[append_key] is not None else []
                    new_list = curr_dict_new[append_key] if curr_dict_new[append_key] is not None else []
                    if not type(new_list) == list:
                        new_list = [new_list]
                    # curr_dict_lists[append_key] = [int(curr_dict[append_key])] if curr_dict[append_key] is not None else []
                    # curr_dict_new_lists[append_key] = curr_dict_new[append_key] if curr_dict_new[
                    #                                 append_key] is not None else []
                    curr_dict_new[append_key] = prev_list + new_list
                first_match = True
        if not first_match:
            new_dict = {}
            for required_key in required_keys:
                new_dict[required_key] = curr_dict[required_key]
            new_array.append(new_dict)
    return new_array


def sum_array_by_keys(array, grouping_keys, sum_keys):
    new_array = []
    required_keys = set(sum_keys + grouping_keys)
    ref_sum_key = sum_keys[0]
    array_keys = array[0].keys()
    missing_keys = required_keys-set(array_keys)
    if len(missing_keys)>0:
        print("keys missing, ignored")
        required_keys = list(required_keys - missing_keys)
        grouping_keys = list(set(grouping_keys)-missing_keys)
    for curr_dict in array:
        first_match = False
        curr_dict_sum = {}
        for curr_dict_new in new_array:
            match = True
            curr_dict_new_sum = {}
            # check if grouping keys are matching
            for key in grouping_keys:
                curr_value = curr_dict[key]
                curr_value_new = curr_dict_new[key]
                if not curr_value_new == curr_value:
                    match = False
            if match:
                for sum_key in sum_keys:
                    curr_dict_sum[sum_key] = int(curr_dict[sum_key]) if curr_dict[sum_key] is not None else 0
                    curr_dict_new_sum[sum_key] = int(curr_dict_new[sum_key]) if curr_dict_new[
                                                 sum_key] is not None else 0
                    curr_dict_new[sum_key] = curr_dict_sum[sum_key] + curr_dict_new_sum[sum_key]
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


def date_to_other_groups(dict_array, group_name, desired_metric, raw_data, highest_level_values):
    sequential_time_metrics = ['day','month','year']
    new_dict = {}
    new_array = []
    all_keys_sequential = []

    for curr_dict in dict_array:
        all_keys = list(curr_dict.keys())
        curr_date = curr_dict['date'] if 'date' in curr_dict else curr_dict[group_name[0]]
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
    if desired_metric == 'phase':
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
        phase_adjusted_results = ranged_data_to_other_groups(copy.deepcopy(dict_array),query_results,start_field,
                                                             end_field, group_name[0], assigned_field, other_fields)
        new_array = phase_adjusted_results

    if len(group_name)>2:
        return new_array
    if desired_metric == 'weekday' or desired_metric == 'phase':
        if desired_metric in date_to_others:
            new_group_name = list(date_to_others[desired_metric]['variables'].keys())
        new_group_name.remove('date')
        new_group_name.append(desired_metric)
        new_array = sum_array_by_keys(new_array,new_group_name, raw_data)
    if new_array == []:
        new_array = list(new_dict.values())

    return new_array


def add_missing_keys(main_dict, main_keys):
    if main_keys == []:
        return main_dict
    key_set_list = []
    for curr_main_key in main_keys:
        sub_dict = main_dict[curr_main_key]
        sub_keys = sub_dict.keys()
        key_set_list.append(set(sub_keys))
    if len(key_set_list)>0:
        all_keys = set.union(*key_set_list)
    for curr_main_key in main_keys:
        sub_dict = main_dict[curr_main_key]
        sub_keys = sub_dict.keys()
        missing_keys = all_keys - sub_keys
        for missing_key in missing_keys:
            main_dict[curr_main_key][missing_key] = {}
    return main_dict


def frequency_mode_calculator(dict_array, frequency_keys, weighted=0, window_size=5):
    new_array= []
    for curr_dict in dict_array:
        freq_keys = []
        for key in frequency_keys:
            curr_dist = calculate_freqdist_mode_from_list(curr_dict[key],window_size)
            if curr_dist == {}:
                continue
            new_key = 'freq_dist_'+ key
            freq_keys.append(new_key)
            curr_dict[new_key] = curr_dist
        new_array.append(curr_dict)
        x = add_missing_keys(curr_dict,freq_keys)
    return new_array


# this function is used to add fields linked by 1-1 relationship to related fields in the same model, such as names
def add_related_field(dict_array, model_name, self_name_model, self_name,
                      related_name_model,related_name = None, database_type='mysql'):
    if related_name == None:
        related_name = self_name + '_name'
    if not database_type == 'mysql':
        print("this function is currently not developed for non-mysql database")
        return dict_array
    if self_name not in dict_array[0]:
        return dict_array
    self_values = [x[self_name] for x in dict_array]
    model_data_query = model_name+'.objects.filter('+self_name_model+'__in=self_values)'
    model_data = eval(model_data_query).values_list(self_name_model,related_name_model)
    model_data_dict = dict(model_data)
    new_dict_array = []
    for curr_dict in dict_array:
        col_value = curr_dict[self_name]
        curr_dict[related_name] = model_data_dict[col_value]
        new_dict_array.append(curr_dict)
    return new_dict_array


def add_campaign_name(dict_array):
    if 'campaign' not in dict_array[0]:
        return dict_array
    campaign_ids = [x["campaign"] for x in dict_array]
    model_data = ProposalInfo.objects.filter(proposal_id__in = campaign_ids).\
        values_list('proposal_id','name')
    new_col_name = level_name_by_model_id['name']
    model_data_dict = dict(model_data)
    new_dict_array = []
    for curr_dict in dict_array:
        col_value = curr_dict['campaign']
        curr_dict[new_col_name] = model_data_dict[col_value]
        new_dict_array.append(curr_dict)
    return new_dict_array


def add_supplier_name(dict_array):
    if dict_array == [] or 'supplier' not in dict_array[0]:
        return dict_array
    supplier_ids = [x["supplier"] for x in dict_array]
    model_data = SupplierTypeSociety.objects.filter(supplier_id__in = supplier_ids).\
        values_list('supplier_id','society_name')
    new_col_name = level_name_by_model_id['society_name']
    model_data_dict = dict(model_data)
    new_dict_array = []
    for curr_dict in dict_array:
        col_value = curr_dict['supplier']
        curr_dict[new_col_name] = model_data_dict[col_value]
        new_dict_array.append(curr_dict)
    return new_dict_array


def add_vendor_name(dict_array):
    if 'vendor' not in dict_array[0]:
        return dict_array
    vendor_ids = [x["vendor"] for x in dict_array]
    model_data = Organisation.objects.filter(organisation_id__in = vendor_ids).\
        values_list('organisation_id','name')
    new_col_name = 'vendor_name'
    model_data_dict = dict(model_data)
    new_dict_array = []
    for curr_dict in dict_array:
        col_value = curr_dict['vendor']
        if col_value in model_data_dict:
            curr_dict[new_col_name] = model_data_dict[col_value]
        new_dict_array.append(curr_dict)
    return new_dict_array


# [[{'lead': 66, 'supplier': 'MUMTWVVRSLOP', 'campaign': 'BYJMAC472C', 'city': 'Mumbai'},
# {'lead': 68, 'supplier': 'MUMGELBRSPRT', 'campaign': 'BYJMAC9E18', 'city': 'Mumbai'}],
# [{'hot_lead': 64, 'supplier': 'MUMTWVVRSLOP', 'campaign': 'BYJMAC472C', 'city': 'Mumbai'},
# {'hot_lead': 54, 'supplier': 'MUMGELBRSPRT', 'campaign': 'BYJMAC9E18', 'city': 'Mumbai'}]
# [{'flat': 78, 'supplier': 'MUMTWVVRSLOP', 'city': 'Mumbai'}, {'flat': 150, 'supplier': 'MUMMUGWRSAEC', 'city': 'Mumbai'}]
# Result: [ ... [{'flat': 78, 'supplier': 'MUMAMENNRSSRR', 'city': 'Mumbai','campaign': 'BYJMAC472C'}]
def append_higher_key_dict_array(arrays,key):
    key_set_list = []
    for array in arrays:
        curr_keys = array[0].keys()
        key_set_list.append(set(curr_keys))
    all_keys = set.union(*key_set_list)
    ref_array = None
    missing_array = None
    new_array = []
    for array in arrays:
        curr_keys = array[0].keys()
        missing_keys = all_keys-curr_keys
        if len(missing_keys) == 0:
            ref_array = array
        else:
            missing_array = array
    new_array


def key_replace_group(dict_array, existing_key, required_key, sum_key, value_ranges = {}, incrementing_value=None):
    if existing_key == required_key:
        return dict_array
    if incrementing_value is not None:
        sum_key = sum_key + str(incrementing_value)
    allowed_values = value_ranges[required_key] if required_key in value_ranges else None
    search_key = str(existing_key)+'_'+str(required_key)
    key_details = count_details_direct_match_multiple[search_key]
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
            curr_value = query_dict[curr_dict[existing_key]]
            curr_dict[required_key] = curr_value
            curr_dict.pop(existing_key)
            if allowed_values is not None and str(curr_value) not in allowed_values:
                continue
            new_array.append(curr_dict)
        all_keys = list(curr_dict.keys())
        grouping_keys = all_keys
        grouping_keys.remove(sum_key)
        new_array = sum_array_by_key(new_array,grouping_keys, sum_key)
    else:
        new_array = dict_array
    return new_array


def key_replace_group_multiple(dict_array, existing_key, required_keys, sum_key, value_ranges = {},
                               incrementing_value = None):
    # if existing_key == required_key:
    #     return dict_array
    if incrementing_value is not None:
        sum_key = sum_key + str(incrementing_value)
    for required_key in required_keys:
        allowed_values = value_ranges[required_key] if required_key in value_ranges else None
        search_key = str(existing_key) + '_' + str(required_key)
        key_details = count_details_direct_match_multiple[search_key]
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
                curr_value = query_dict[curr_dict[existing_key]]
                curr_dict[required_key] = curr_value
                if allowed_values is not None and str(curr_value) not in allowed_values:
                    continue
                new_array.append(curr_dict)

        else:
            new_array = dict_array
        dict_array = new_array
    all_keys = list(curr_dict.keys())
    grouping_keys = all_keys
    grouping_keys.remove(sum_key)
    new_array = sum_array_by_key(new_array, grouping_keys, sum_key)
    return(new_array)


# used to truncate a regular dict array using range of values possible on specific keys
def truncate_by_value_ranges(dict_array, value_ranges, range_type=0):
    if value_ranges == None or value_ranges == {}:
        return dict_array
    new_array = []
    if range_type == 1:
        for curr_key in value_ranges:
            curr_range = value_ranges[curr_key]
            if not len(curr_range)==2:
                print('incorrect range format, treating as exact')
                continue
            start_value = curr_range[0]
            end_value = curr_range[1]
            if start_value.isdigit() and end_value.isdigit():
                start_value = int(start_value)
                end_value = int(end_value)
                if start_value>end_value or end_value>100:
                    print('mathematically inconsistent range, treating as exact')
                    continue
            else:
                print('no integers found, treating as exact')
                continue
            curr_range_array = []
            curr_array = list(range(int(start_value),int(end_value)+1))
            value_ranges[curr_key] = [str(x) for x in curr_array]
    for curr_dict in dict_array:
        match = 1
        for curr_key in value_ranges:
            curr_range = value_ranges[curr_key]
            curr_dict_value = curr_dict[curr_key]
            if str(curr_dict_value) not in curr_range:
                match=0
                break
        if match==1:
            new_array.append(curr_dict)
    return new_array


# this function is used to get selected value of a chosen field on the basis of match from another field
def get_constrained_values(model_name, grouping_field, constraining_dict):
    basic_query = model_name +'.objects'
    for curr_field in constraining_dict.keys():
        curr_value = constraining_dict[curr_field]
        curr_query = basic_query + '.filter('+ curr_field + '=curr_value)'
    field_list = list(constraining_dict.keys())
    final_dict = list(eval(curr_query).values_list(grouping_field,flat=True))
    return final_dict

