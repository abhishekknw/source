import math
from types import *

from django.db.models import Q

from rest_framework.response import Response
from rest_framework import  status

from constants import price_per_flat, inventorylist
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
