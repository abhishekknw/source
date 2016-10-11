import math
from types import *

from django.db.models import Q
from django.apps import apps
from django.contrib.contenttypes.models import ContentType


from rest_framework.response import Response
from rest_framework import  status

import constants as website_constants
from constants import price_per_flat, inventorylist
import v0.models as models
from v0.models import PriceMappingDefault


def get_union_keys_inventory_code(key_type, unique_inventory_codes):
    """
    :param key_type: can take value 'HEADER' or 'DATA'
    :param unique inventory_code: can take value, 'SL', 'CD', 'ST', 'PO'
    :return: a list containing HEADERS/DATA union of all inventory types hidden in inventory_code.
    """

    assert key_type is not None, 'key type should not be None'
    assert unique_inventory_codes is not None, 'inventory code  should not be None'
    assert type(inventorylist) is DictType, 'Inventory list is not dict type'

    try:
        response = Response(data={'status': True, 'data': ''}, status=status.HTTP_200_OK)
        # for each code in individual_codes union the data and return
        response.data['data'] = [item for code in unique_inventory_codes for item in inventorylist.get(code)[key_type]]
        return response
    except Exception as e:
        return Response(data={'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)



def getList(data, society_keys):
    return [data.get(key, '') for key in society_keys]


def remove_duplicates_preserver_order(sequence):
    """
    Args:
        sequence: a list  containing duplicatees
    Returns: a list which does not contains duplicates whilst preserving order of elements in orginal lis
    """
    assert type(sequence) is ListType, 'Sequence must be list type'
    seen = set()
    seen_add = seen.add
    return [x for x in sequence if not (x in seen or seen_add(x))]


def get_unique_inventory_codes(inventory_array):
    """
    Args:
        inventory_array: array of inventory codes like PL, SL, PLSL.
    Returns: an array containing unique codes. Pl, PLSL would just give [ PL, SL]
    """
    try:
        # our codes are two letters long (individual)
        step = 2
        # generate individual codes from inventory_array
        individual_codes = [inventory_code[i:i + step] for inventory_code in inventory_array for i in range(0, len(inventory_code), step)]
        return Response({'status': True, 'data': list(set(individual_codes))}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


def get_union_inventory_price_per_flat(data, unique_inventory_codes, index):
    """
    This function adds an extra key to the dict data based on price and flat count keys
    :param data: it's a dict containing 1 society data
    :param unique_inventory_code: array of inventory codes like 'FL', 'CD', 'ST' etc
    :return: calculates inventory price per flat by dividing two keys of the the dict and stores the result  in the dict itself
    """

    # assert type(data) is DictType, 'Data variable should be a dict'
    # assert type(inventory_code) is StringType, 'inventory_code should be a String {0}.'.format(inventory_code)

    try:
        response = Response(data={'status': True, 'data': ''}, status=status.HTTP_200_OK)
        # check if directly you can get the data kept against the inventory_code

        # iterate over individual codes and calculate for each code and  return
        for code in unique_inventory_codes:
            if data.get('flat_count'):
                price = data[price_per_flat[code][1]] if data.get(price_per_flat[code][1]) else 0
                data[price_per_flat[code][0]] = (price) / (data['flat_count'])
        response.data['data'] = data
        return response

    except Exception as e:
        return Response({'status': False, 'error': '{0} at society index {1}'.format(e.message, index)},
                        status=status.HTTP_400_BAD_REQUEST)


def get_related_dict():
    ''' This dictionary is simply a mapping from get params to their actual values '''
    # quality_dict if for both society_quality and its location_quality and similarly for other spaces
    quality_dict = {
        'UH': 'Ultra High', 'HH': 'High',
        'MH': 'Medium High', 'ST': 'Standard'
    }

    inventory_dict = {
        'PO': 'poster_allowed_nb', 'ST': 'standee_allowed',
        'SL': 'stall_allowed', 'FL': 'flier_allowed',
        'BA': 'banner_allowed', 'CD': 'car_display_allowed',
    }

    quantity_dict = {
        'LA': 'Large', 'MD': 'Medium',
        'VL': 'Very Large', 'SM': 'Small',
    }

    return quality_dict, inventory_dict, quantity_dict


def make_filter_query(data):
    """
    This function constructs the filter that later on will be used to query InventorySummary table.

    """
    try:
        quality_dict, inventory_dict, supplier_quantity_dict = get_related_dict()
        supplier_type_code = data.get('supplier_type_code')

        if not data['max_latitude'] or not data['min_latitude'] or not data['max_longitude'] or not data[
            'min_longitude'] or not data['supplier_type_code']:
            return None

        elif data['supplier_type_code'] == 'RS':
            filter_query =  Q(society_latitude__lt=data['max_latitude']) & Q(society_latitude__gt=data['min_latitude']) & Q(
                society_longitude__lt=data['max_longitude']) & Q(society_longitude__gt=data['min_longitude'])
        else:
            filter_query =  Q(latitude__lt=data['max_latitude']) & Q(latitude__gt=data['min_latitude']) & Q(
                longitude__lt=data['max_longitude']) & Q(longitude__gt=data['min_longitude'])

        if data.get('location_params'):
            location_ratings = []
            location_params = data.get('location_params').split()
            for param in location_params:
                try:
                    location_ratings.append(quality_dict[param])
                except KeyError:
                    pass
            if location_ratings:
                if supplier_type_code == 'RS': #todo: change this when clarity
                    filter_query &= Q(society_location_type__in=location_ratings)
                else:
                    filter_query &= Q(location_type__in=location_ratings)


                # if required to include suppliers with null value of this parameter uncomment following line
                # will not work if there is default value is something then replace __isnull=True --> = defaultValue
                # q &= Q(supplier_location_type__isnull=True)

        if data.get('supplier_quality_params'):
            supplier_quality_ratings = []
            supplier_quality_params = data.get('supplier_quality_params').split()
            for param in supplier_quality_params:
                try:
                    supplier_quality_ratings.append(quality_dict[param])
                except KeyError:
                    pass

            if supplier_quality_ratings:
                if supplier_type_code == 'RS':
                    filter_query &= Q(society_type_quality__in=supplier_quality_ratings)
                else:
                    filter_query &= Q(quality_rating__in=supplier_quality_ratings)

                # if required to include suppliers with null value of this parameter uncomment following line
                # will not work if there is default value is something then replace __isnull=True --> = defaultValue
                # q &= Q(supplier_type_quality__isnull=True)

        if data.get('supplier_quantity_params'):
            supplier_quantity_ratings = []
            supplier_quantity_params = data.get('supplier_quantity_params').split()
            for param in supplier_quantity_params:
                try:
                    supplier_quantity_ratings.append(supplier_quantity_dict[param])
                except KeyError:
                    pass

            if supplier_quantity_ratings:
                if supplier_type_code == 'RS':
                    filter_query &= Q(society_type_quantity__in=supplier_quantity_ratings)
                else:
                    filter_query &= Q(quantity_rating__in=supplier_quantity_ratings)


                # if required to include suppliers with null value of this parameter uncomment following line
                # will not work if there is default value is something then replace __isnull=True --> = defaultValue
                # q &= Q(supplier_type_quantity__isnull=True)

        if data.get('flat_count'):
            flat_count = data.get('flat_count').split()
            if len(flat_count) == 2:
                flat_min = flat_count[0]
                flat_max = flat_count[1]

                filter_query &= Q(flat_count__gte=flat_min) & Q(flat_count__lte=flat_max)
                # if required to include suppliers with null value of this parameter uncomment following line
                # will not work if there is default value is something then replace __isnull=True --> = defaultValue
                # q &= Q(flat_count__isnull=True)
        p = None
        if data.get('inventory_params'):
            inventory_params = data.get('inventory_params').split()
            temp = None  # temporary variable
            temp = None  # temporary variable
            for param in inventory_params:
                try:

                    # | 'STFL' | 'CDFL' | 'PSLF' | 'STSLFL' | 'POCDFL' | 'STCDFL'
                    if (param == 'POFL') | (param == 'STFL') | (param == 'SLFL') | (param == 'CDFL') | (
                        param == 'POSLFL') | (param == 'STSLFL') | (param == 'POCDFL') | (param == 'STCDFL'):

                        if param == 'POFL':
                            temp_q = (Q(poster_allowed_nb=True) & Q(flier_allowed=True))

                        if param == 'SLFL':
                            temp_q = (Q(stall_allowed=True) & Q(flier_allowed=True))

                        if param == 'STFL':
                            temp_q = (Q(standee_allowed=True) & Q(flier_allowed=True))

                        if param == 'CDFL':
                            temp_q = (Q(car_display_allowed=True) & Q(flier_allowed=True))

                        if param == 'POSLFL':
                            temp_q = (Q(poster_allowed_nb=True) & Q(stall_allowed=True) & Q(flier_allowed=True))

                        if param == 'STSLFL':
                            temp_q = (Q(stall_allowed=True) & Q(standee_allowed=True) & Q(flier_allowed=True))

                        if param == 'POCDFL':
                            temp_q = (Q(poster_allowed_nb=True) & Q(car_display_allowed=True) & Q(flier_allowed=True))

                        if param == 'STCDFL':
                            temp_q = (Q(standee_allowed=True) & Q(car_display_allowed=True) & Q(flier_allowed=True))

                    else:
                        temp_q = Q(**{"%s" % inventory_dict[param]: 'True'})

                    if temp:

                        p = (p | temp_q)
                    else:
                        p = temp_q
                        temp = 1
                except KeyError:
                    pass

        # code changes & added for 'OR' filters of inventory and 'AND' filters with inventory and others
        # code start
        if p:
            filter_query &= p
        return Response({'status': True, 'data': filter_query}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


def return_price(adinventory_type_dict, duration_type_dict, inv_type, dur_type):
    price_mapping = PriceMappingDefault.objects.filter(adinventory_type=adinventory_type_dict[inv_type],
                                                       duration_type=duration_type_dict[dur_type])
    if price_mapping:
        return price_mapping[0].business_price
    return 0


def get_min_max_lat_long(delta_dict):
    """
    :param data:
    :return:
    """
    # calculating for latitude and longitude
    # this is done to ensure that the suppliers are sent according to the current radius and center in frontend
    # user can change center and radius and it will not be stored in the database until saved
    if not delta_dict.get('latitude') or not delta_dict.get('longitude') or not delta_dict.get('supplier_type_code'):
        return Response({'status': False, 'error': 'provide lat/long/supplier_type_code'},
                        status=status.HTTP_400_BAD_REQUEST)

    latitude = delta_dict.get('latitude')
    longitude = delta_dict.get('longitude')
    supplier_code = delta_dict.get('supplier_type_code')

    try:
        latitude = float(latitude)
        longitude = float(longitude)

        data = {}

        data['max_latitude'] = latitude + delta_dict['delta_latitude']
        data['min_latitude'] = latitude - delta_dict['delta_latitude']

        delta_longitude = delta_dict['delta_longitude']
        data['max_longitude'] = longitude + delta_dict['delta_longitude']
        data['min_longitude'] = longitude - delta_dict['delta_longitude']
        data['supplier_type_code'] = supplier_code
        return Response({'status': True, 'data': data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


def get_delta_latitude_longitude(radius, latitude):
    delta_longitude = radius/(111.320 * math.cos(math.radians(latitude)))
    delta_latitude = radius/ 110.574

    return {'delta_latitude' : delta_latitude,
            'delta_longitude' : delta_longitude}


def space_on_circle(latitude, longitude, radius, space_lat, space_lng):
    return (space_lat - latitude)**2 + (space_lng - longitude)**2 <= (radius/110.574)**2


def initialize_keys(center_object, row):
    """
    Args:
        center_object: a dict representing one center object
    goal is to make dict request.data type
    Returns: intializes this dict  with all valid keys and defaults as values

    """

    try:

        # set societies inventory key
        center_object['societies_inventory'] = {}

        # set societies key
        center_object['societies'] = []

        # set center key
        center_object['center'] = {}

        # set space mapping
        center_object['center']['space_mappings'] = {}

        # set societies count
        center_object['societies_count'] = 0

        # set for shortlisted_inventory_details
        center_object['shortlisted_inventory_details'] = []

        # # initialize the keys for total counts and  total price to zero to be filled later when we get prices and counts
        # for field in website_constants.inventory_fields:
        #     if field in row.keys(): # add it only if the column is actualy present in the sheet
        #         center_object['societies_inventory'][field] = 0

        return Response({'status': True, 'data': center_object}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


def make_societies_inventory(center_object, row):
    """
    Args:
        center_object: a center object
        row: 1 row of sheet
    Returns: adds data for 'societies_inventory'

    """
    try:
        center_object['societies_inventory']['supplier_code'] = 'RS'  # hardcoded for society
        center_object['societies_inventory']['id'] = row['inventory_type_id']
        center_object['societies_inventory']['space_mapping'] = row['space_mapping_id']

        return Response({'status': True, 'data': center_object}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


def make_shortlisted_inventory_list(row):
    """
    Args:
        row: a single row of sheet.  it's dict

    Returns: a list of shortlisted inventory types for this supplier

    """
    try:

        shortlisted_inventory_list = []
        # check for predefined keys in the row. if available, we have that inventory !
        for inventory in website_constants.is_inventory_available:
            if inventory in row.keys():
                # create an empty dict to store individual inventory details
                shortlisted_inventory_details = {}

                # get the content_type for this inventory. when the time comes remove this get call out of loop
                # to speed up the process.
                inventory_type = ContentType.objects.get(model=website_constants.inventory_models[inventory]['MODEL'])

                # get the base_name so that we can fetch other fields from row
                base_name = website_constants.inventory_models[inventory]['BASE_NAME']

                # set the supplier_id
                shortlisted_inventory_details['supplier_id'] = row['supplier_id']

                # set the inventory_type
                shortlisted_inventory_details['inventory_type'] = inventory_type

                # set inventory_business_price
                shortlisted_inventory_details['inventory_price'] = row[base_name + '_business_price']

                # set inventory_count
                shortlisted_inventory_details['inventory_count'] = row[base_name + '_count']

                # add it to the list
                shortlisted_inventory_list.append(shortlisted_inventory_details)

        return Response({'status': True, 'data': shortlisted_inventory_list}, status=status.HTTP_200_OK)
    except KeyError as e:
        return Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


def make_societies(center_object, row):
    """
    Args:
        center_object: a center_object
        row: 1 row of data in sheet

    Returns: adds the society that is present in this row to center_object and returns

    """
    try:
        # collect society data in a dict and append it to the list of societies of center_object
        society = {}
        society['supplier_id'] = row['supplier_id']
        society['society_name'] = row['supplier_name']
        society['society_subarea'] = row['supplier_sub_area']
        society['society_type_quality'] = row['supplier_type']
        society['tower_count'] = row['supplier_tower_count']
        society['flat_count'] = row['supplier_flat_count']

        # get the list of shortlisted inventory details
        shortlisted_inventory_list_response = make_shortlisted_inventory_list(row)
        if not shortlisted_inventory_list_response.data['status']:
            return shortlisted_inventory_list_response

        shortlisted_inventory_list = shortlisted_inventory_list_response.data['data']

        # add it to the list of center_object
        center_object['societies'].append(society)

        # add shortlisted_inventory_list to the list already initialized
        center_object['shortlisted_inventory_details'].extend(shortlisted_inventory_list)

        # return the result after we are done scanning
        return Response({'status': True, 'data': center_object}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


def populate_shortlisted_inventory_details(result):
    """
    Args:
        result: it's a list containing final data

    Returns: success if it's able to create objects in the list else failure

    """
    try:
        # using a loop instead bulk_create() because bulk_create() will insert duplicates if the api
        # is hit twice by mistake, will ignore the unique values etc. This problem can be only be
        # solved by writing a custom raw SQL query which i think is an overkill right now. when the code gets slow
        # write a RAW query.
        for center in result:
            for shortlisted_inventory_detail in center['shortlisted_inventory_details']:
                is_created, obj = models.ShortlistedInventoryDetails.objects.get_or_create(**shortlisted_inventory_detail)

            # we do not want to send this to other API, so we will rather delete it
            del center['shortlisted_inventory_details']

        return Response({'status': True, 'data': 'success'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


def get_center_id_list(ws, index_of_center_id):
    """
    Args:
        ws: instance of worksheet
        index_of_center_id: index of center_id column in the sheet
    Returns: a list containing unique center_id's

    """
    try:
        center_id_set = set()
        for index, row in enumerate(ws.iter_rows()):
            # skip the headers
            if index == 0:
                continue
            if row[index_of_center_id].value:
                center_id_set.add(int(row[index_of_center_id].value))
        return Response({'status': True, 'data': list(center_id_set)}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


def get_headers(ws):
    """
    Args:
        ws: worksheet
    Returns: a list of headers

    """
    try:
        headers = []
        for index, row in enumerate(ws.rows[0]):
            headers[index] = row[index]
        return Response({'status': True, 'data': headers}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


def get_mapped_row(ws, row):
    """
    This makes a dict having headings with keys and corresponding cell values as values.
    Args:
        ws: worksheet instance
        row_index: the row index  for which the modified row with underscore keys needs to be made

    Returns: a dict in which keys are keys which are mapped to headers and value is the corresponding value from the row

    """
    try:
        row_dict = {}
        for index, cell in enumerate(row):
            heading_with_spaces = ws.cell(row=1, column=index+1).value.lower()
            heading_with_underscore = '_'.join(heading_with_spaces.split(' '))
            row_dict[heading_with_underscore] = cell.value
        return Response({'status': True, 'data': row_dict}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


def make_center(center_object, row):
    """
    Args:
        center_object: center_object
        row: a dict containg data of one row

    Returns: populates the center_object with data for it's 'center' key

    """
    # get the fields which also needs to sent for the other api to work upon because they are required for serializing .
    city, area, pincode, sub_area, latitude, longitude, radius = models.ProposalCenterMapping.objects.values_list('city', 'area', 'pincode', 'subarea', 'latitude', 'longitude', 'radius').get(id=row['center_id'])
    try:
        center_object['center']['center_name'] = row.get('center_name')
        center_object['center']['proposal'] = row['center_proposal_id']
        center_object['center']['id'] = row['center_id']
        center_object['center']['city'] = city
        center_object['center']['area'] = area
        center_object['center']['subarea'] = sub_area
        center_object['center']['pincode'] = pincode
        center_object['center']['latitude'] = latitude
        center_object['center']['longitude'] = longitude
        center_object['center']['radius'] = radius
        space_mapping_response = make_space_mappings(row)
        if not space_mapping_response.data['status']:
            return space_mapping_response
        center_object['center']['space_mappings'] = space_mapping_response.data['data']
        return Response({'status': True, 'data': center_object}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


def make_space_mappings(row):
    """
    Args:
        row: data of one row

    Returns: a dict of space mappings

    """
    try:
        space_mapping = {}
        space_mapping['center'] = row['center_id']
        space_mapping['proposal'] = row['center_proposal_id']
        space_mapping['id'] = row['space_mapping_id']
        return Response({'status': True, 'data': space_mapping}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


def save_proposal_version(center_id):
    """
    Args:
        center_id: center_id for which proposal version object is to be saved
         used in FinalProposal post request

    Returns:

    """

    try:
        center_object = models.ProposalCenterMapping.objects.select_related('proposal').get(id=center_id)
        proposal_object = center_object.proposal

        # version save
        proposal_version_object = models.ProposalInfoVersion(proposal=proposal_object, name=proposal_object.name,
                                                      payment_status=proposal_object.payment_status, \
                                                      created_on=proposal_object.created_on,
                                                      created_by=proposal_object.created_by,
                                                      tentative_cost=proposal_object.tentative_cost, \
                                                      tentative_start_date=proposal_object.tentative_start_date,
                                                      tentative_end_date=proposal_object.tentative_end_date)
        proposal_version_object.save()
        return Response({'status': True, 'data': proposal_version_object}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)

