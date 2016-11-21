import math
import re
import datetime
import StringIO
from types import *
import os
import uuid

from django.db import transaction
from django.db.models import Q, F
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework.response import Response
from rest_framework import status
from pygeocoder import Geocoder, GeocoderError
import openpyxl

import constants as website_constants
from constants import price_per_flat, inventorylist
import v0.models as models
from v0.models import PriceMappingDefault
import v0.ui.utils as ui_utils
import serializers


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


def insert_supplier_sheet(workbook, result):
    """
    Args:
        workbook: a worksheet object
        result
    Returns: a worksheet in which the right rows are inserted and returned.
    """
    function_name = insert_supplier_sheet.__name__
    try:

        for code, supplier_data in result.iteritems():

            # create a new sheet for each supplier type
            ws = workbook.create_sheet(index=0, title=supplier_data['sheet_name'])

            # set the heading
            ws.append(supplier_data['header_keys'])

            for supplier_object in supplier_data['objects']:
                ws.append([ supplier_object[key] for key in supplier_data['data_keys']])

        # we also need to add metric sheet as part of export
        response = add_metric_sheet(workbook)
        if not response.data['status']:
            return response
        workbook = response.data['data']

        # return a workbook object
        return ui_utils.handle_response(function_name, data=workbook, success=True)
    except Exception as e:
        return ui_utils.handle_response(function_name, exception_object=e)


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
    This function constructs the filter that later on will be used to query the supplier table.
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
    """
    Args:
        latitude: latitude of the center
        longitude: longitude of the center
        radius: radius of center
        space_lat: supplier latitude
        space_lng: supplier longitude

    Returns: weather the supplier coordinates actually lie within a circle drawn with  given radius  ? The center
    coordinates being latitude, longitude in the params. The function uses simple pythagoras theorem to test this.
    """
    return (space_lat - latitude)**2 + (space_lng - longitude)**2 <= (radius/110.574)**2


def initialize_keys(center_object, supplier_type_code):
    """
    Args:
        center_object: a dict representing one center object
    goal is to make dict request.data type
    Returns: intializes this dict  with all valid keys and defaults as values

    """
    try:

        # set societies inventory key
        # center_object['societies_inventory'] = {}

        # set suppliers dict
        center_object['suppliers'] = {supplier_type_code: []}

        # set center key
        center_object['center'] = {}

        # set inventory type selected
        # center_object['suppliers_meta'] = {supplier_type_code: {'inventory_type_selected': []}}

        # set space mapping
        # center_object['center']['space_mappings'] = {}

        # set societies count
        # center_object['societies_count'] = 0

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


def make_shortlisted_inventory_list(row, supplier_type_code):
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

                # set supplier_type_code
                shortlisted_inventory_details['supplier_type_code'] = supplier_type_code

                # add it to the list
                shortlisted_inventory_list.append(shortlisted_inventory_details)

        return Response({'status': True, 'data': shortlisted_inventory_list}, status=status.HTTP_200_OK)
    except KeyError as e:
        return Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


def make_suppliers(center_object, row, supplier_type_code):
    """
    Args:
        center_object: a center_object
        row: 1 row of data in sheet

    Returns: adds the society that is present in this row to center_object and returns

    """
    function = make_suppliers.__name__
    try:
        # collect society data in a dict and append it to the list of societies of center_object

        supplier_header_keys = ['_'.join(header.split(' ')) for header in website_constants.inventorylist[supplier_type_code]['HEADER']]
        supplier_header_keys = [header.lower() for header in supplier_header_keys]
        supplier_data_keys = website_constants.inventorylist[supplier_type_code]['DATA']
        supplier = {data_key: row[header] for header, data_key in zip(supplier_header_keys, supplier_data_keys)}

        # get the list of shortlisted inventory details
        shortlisted_inventory_list_response = make_shortlisted_inventory_list(row, supplier_type_code)
        if not shortlisted_inventory_list_response.data['status']:
            return shortlisted_inventory_list_response

        shortlisted_inventory_list = shortlisted_inventory_list_response.data['data']

        # add it to the list of center_object
        center_object['suppliers'][supplier_type_code].append(supplier)

        # add shortlisted_inventory_list to the list already initialized
        center_object['shortlisted_inventory_details'].extend(shortlisted_inventory_list)

        # return the result after we are done scanning
        return Response({'status': True, 'data': center_object}, status=status.HTTP_200_OK)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


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
    function = get_center_id_list.__name__
    try:
        center_id_set = set()
        for index, row in enumerate(ws.iter_rows()):
            # skip the headers
            if index == 0:
                continue
            if row[index_of_center_id].value:
                center_id_set.add(int(row[index_of_center_id].value))
        return ui_utils.handle_response(function, data=list(center_id_set), success=True)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


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
            heading_cell = ws.cell(row=1, column=index+1)
            if heading_cell.value:
                heading_with_spaces = heading_cell.value.lower()
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
    # city, area, pincode, sub_area, latitude, longitude, radius = models.ProposalCenterMapping.objects.values_list('city', 'area', 'pincode', 'subarea', 'latitude', 'longitude', 'radius').get(id=row['center_id'])
    try:
        center_object['center']['center_name'] = row.get('center_name')
        center_object['center']['proposal'] = row['proposal']
        center_object['center']['id'] = row['center_id']
        # center_object['center']['city'] = city
        # center_object['center']['area'] = area
        # center_object['center']['subarea'] = sub_area
        # center_object['center']['pincode'] = pincode
        # center_object['center']['latitude'] = latitude
        # center_object['center']['longitude'] = longitude
        # center_object['center']['radius'] = radius
        # space_mapping_response = make_space_mappings(row)
        # if not space_mapping_response.data['status']:
        #     return space_mapping_response
        # center_object['center']['space_mappings'] = space_mapping_response.data['data']
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


def get_model_name(model_name):
    """
    Args:
        model_name: a model name in lower case joined with underscores

    Returns: removes underscores and joins on Intials with a capital letter

    """
    return ' '.join(model_name.split('_')).title()


def initialize_master_data(master_data):
    """
    Args:
        master_data: empty dict for import proposal cost data api

    Returns: initialized according to needs

    """
    # only one object exist per file hence a dict
    master_data['ideation_design_cost'] = {}

    # only one object exist per file hence a dict
    master_data['logistic_operations_cost'] = {}

    #  one object exist per supplier or row  hence a list
    master_data['space_booking_cost'] = []

    # only one object exist per file hence a dict
    master_data['event_staffing_cost'] = {}

    # only one object exist per file hence a dict
    master_data['data_sciences_cost'] = {}

    # only one object exist per file hence a dict
    master_data['printing_cost'] = {}

    # only one object exist per file hence a dict
    master_data['proposal_master_cost'] = {}

    # one object exist per supplier or row hence a list because there are multiple suppliers
    master_data['proposal_metrics'] = []

    return master_data


def handle_offline_pricing_row(row, master_data):
    """
    Args:
        row: a row of offline pricing sheet

    Returns: saves the data in the right model after processing the row

    """
    try:
        # this string is the base string against we perform the matching and determine to which model the
        #  row data belongs. example  'Use of Data Sciences to Identify Targeted Spaces'
        target_string = row[0].value

        # for all models and their contents declared in constants
        for model, model_content in website_constants.offline_pricing_data.iteritems():
            # because model names are joined by _, join them without underscore with first letter as capital
            # this is required for apps.get_model() to work. model_content is a list. each item of this list
            # will map to a row in db

            # for all types of row in model_content
            for model_row in model_content:

                # find the pattern which is predefined for the this model_row
                pattern = model_row['match_term']

                # match it
                match = re.search(pattern, target_string, re.I)

                # no point in going further if there is no match
                if not match:
                    continue
                # get the column name
                column_name = model_row['col_name']

                # get the value for that column
                value = row[website_constants.value_index].value

                # set data to previously saved data dict if it's a dict because here it will be updated
                # else set to an empty dict because it will be appended in the list
                data = master_data[model] if type(master_data[model]) == DictType else {}

                # add the content type information to data if 'specific' is not none
                if model_row.get('specific'):
                    supplier_content_type_response = ui_utils.get_content_type(model_row.get('specific')['code'])
                    if not supplier_content_type_response.data['status']:
                        return supplier_content_type_response
                    supplier_content_type = supplier_content_type_response.data['data']
                    data['supplier_type'] = supplier_content_type.id

                # add comment information to data if comment is not none. index for comment col is defined in constants
                if row[website_constants.comment_index].value:
                    data['comment'] = row[website_constants.comment_index].value

                # add the specific column and value
                data[column_name] = value

                # add metric_name and value of the metric in case it's a metric model
                if model == website_constants.metric_model:
                    data['metric_name'] = model_row.get('match_term')
                    data['value'] = value
                # we will not save here. we will collect the data in master_data
                # dict and save later. This is because multiple rows represent one object in some cases and  many objects
                # in other cases so saving on row by row basis cannot be done.
                insert_master_data_response = insert_into_master_data(data, master_data, model)
                if not insert_master_data_response.data['status']:
                    return insert_master_data_response
                master_data = insert_master_data_response.data['data']

        return ui_utils.handle_response(handle_offline_pricing_row.__name__, data=master_data, success=True)
    except KeyError as e:
        return ui_utils.handle_response(handle_offline_pricing_row.__name__, data='Key error', exception_object=e)
    except Exception as e:
        return ui_utils.handle_response(handle_offline_pricing_row.__name__, exception_object=e)


def insert_into_master_data(data, master_data, model_name):
    """
    Args:
        data: data is dict containing data of one row
        master_data: master data into which data can be assigned or appended depending upon what model_name is
        This function is made because 'data' can either be assigned or appended in master_data depending upon
        for which model you are collecting.

    Returns: master_data with modified content

    """
    try:
        # append the data to list
        if type(master_data[model_name]) == ListType:
            master_data[model_name].append(data)
        else:
            # update the existing dict with new data
            master_data[model_name] = data
        return ui_utils.handle_response(insert_into_master_data.__name__, data=master_data, success=True)
    except Exception as e:
        return ui_utils.handle_response(handle_offline_pricing_row.__name__, exception_object=e)


def save_master_data(master_data):
    """

    Args:
        master_data: the data to be saved in the models looks like
        {
           'data_sciences_cost':{
              'total_cost':40
           },
           'ideation_design_cost':{
              'total_cost':40
           },
           'logistic_operations_cost':{
              'total_cost':40
           },
           'space_booking_cost':[
              {
                 'total_cost':40
                 'supplier_type':46
              },
              {
                 'total_cost':40
                 'supplier_type':45
              }
           ],
           'event_staffing_cost':{
              'total_cost':40      L
           },
           'proposal_master_cost':{
              'discount':40 ,
              'total_cost':40 ,
              'tax':40 ,
              'total_impressions':50,
              'average_cost_per_impression':50 ,
              'agency_cost':40,
              'proposal':u'jogXxEUu'
           },
           'printing_cost':{
              'total_cost':40
           },
           'proposal_metrics':[
              {
                 'supplier_type':45,
                 'metric_name':'Average Cost per Society',
                 'value':40
              },
              {
                 'supplier_type':48,
                 'metric_name':'Average Cost per Salon',
                 'value':40
              },
            ]
   }
    Returns: success if models are saved successfully

    """
    function = save_master_data.__name__
    try:
        with transaction.atomic():
            # save into proposal master cost table first because it's id is required later
            serializer = ui_utils.get_serializer('proposal_master_cost')(data=master_data['proposal_master_cost'])
            if serializer.is_valid():
                serializer.save()
                proposal_master_cost_id = serializer.data['id']
            else:
                return ui_utils.handle_response(function, data=serializer.errors)

            # pull the model names to process except proposal_master_cost which has been done
            model_name_list = list(website_constants.offline_pricing_data.keys())
            model_name_list.remove('proposal_master_cost')

            # get the right serializer and save the data
            for model in model_name_list:
                # differentiate if we have list to save or a dict to save
                if model in website_constants.one_obect_models:
                    # need to set id of proposal master cost as according to model structure
                    master_data[model]['proposal_master_cost'] = proposal_master_cost_id
                    serializer = ui_utils.get_serializer(model)(data=master_data[model])
                else:
                    # need to set id of proposal master cost as according to model structure
                    for data in master_data[model]:
                        data['proposal_master_cost'] = proposal_master_cost_id
                    serializer = ui_utils.get_serializer(model)(data=master_data[model], many=True)

                if serializer.is_valid():
                    serializer.save()
                else:
                    return ui_utils.handle_response(save_master_data.__name__, data=serializer.errors)
        return ui_utils.handle_response(save_master_data.__name__, data='success', success=True)
    except Exception as e:
        return ui_utils.handle_response(save_master_data.__name__, exception_object=e)


def is_empty_row(row):
    """
    Args:
        row: row to be checked if empty or not
          row is row read by openpyxl lib

    Returns: true if empty else False

    """
    for x in row:
        # if x has a value, row is not empty
        if x.value:
            return False
    # return True, row is empty
    return True


def delete_proposal_cost_data(proposal_id):
    """
    Deletes the tables data associated with proposal cost each time the api is hit because we don't want
    duplicates.
    """
    try:
        proposal_master_cost_object = get_object_or_404(models.ProposalMasterCost, proposal__proposal_id=proposal_id)
        models.ProposalMetrics.objects.filter(proposal_master_cost=proposal_master_cost_object).delete()
        models.PrintingCost.objects.filter(proposal_master_cost=proposal_master_cost_object).delete()
        models.DataSciencesCost.objects.filter(proposal_master_cost=proposal_master_cost_object).delete()
        models.EventStaffingCost.objects.filter(proposal_master_cost=proposal_master_cost_object).delete()
        models.SpaceBookingCost.objects.filter(proposal_master_cost=proposal_master_cost_object).delete()
        models.IdeationDesignCost.objects.filter(proposal_master_cost=proposal_master_cost_object).delete()
        models.LogisticOperationsCost.objects.filter(proposal_master_cost=proposal_master_cost_object).delete()
        proposal_master_cost_object.delete()
        return ui_utils.handle_response(delete_proposal_cost_data.__name__, data='success', success=True)
    except Http404:
        # first time call of this function will not fetch object, but must be a success return.
        return ui_utils.handle_response(delete_proposal_cost_data.__name__, data='', success=True)
    except Exception as e:
        return ui_utils.handle_response(delete_proposal_cost_data.__name__, exception_object=e)


def create_basic_proposal(data):
    """

    Args:
        data: data for ProposalInfo

    Returns: success if proposalInfo  is created

    """
    function_name = create_basic_proposal.__name__
    try:
        proposal_serializer = serializers.ProposalInfoSerializer(data=data)
        if proposal_serializer.is_valid():
            proposal_serializer.save()
        else:
            return ui_utils.handle_response(function_name, data=proposal_serializer.errors)
        return ui_utils.handle_response(function_name, data=proposal_serializer.data, success=True)
    except Exception as e:
        return ui_utils.handle_response(function_name, exception_object=e)


def get_geo_object(address):
    """

    Args:
        address: given an address in string, return it's geo object

    Returns:

    """
    function_name = get_geo_object.__name__
    try:
        geocoder = Geocoder(api_key='AIzaSyCy_uR_SVnzgxCQTw1TS6CYbBTQEbf6jOY')
        geo_object = geocoder.geocode(address)
        return ui_utils.handle_response(function_name, data=geo_object, success=True)
    except GeocoderError as e:
        return ui_utils.handle_response(function_name, exception_object=e)
    except Exception as e:
        return ui_utils.handle_response(function_name, exception_object=e)


def save_suppliers_allowed(center_info, proposal_id, center_id):
    """
    Args:
        center_info: One center data
        proposal_id: The proposal_id
        center_id: The newly created center_id

    Returns: saves what suppliers are allowed in each center. and returns on success.
    """
    function_name = save_suppliers_allowed.__name__

    try:
        # fetch all the supplier codes.
        suppliers_codes = center_info['center']['supplier_codes']

        # for all the codes
        for code in suppliers_codes:
            content_type_response = ui_utils.get_content_type(code)
            if not content_type_response.data['status']:
                return content_type_response

            content_type = content_type_response.data['data']

            # prepare the data
            data = {
                'proposal_id': proposal_id,
                'center_id': center_id,
                'supplier_content_type': content_type,
                'supplier_type_code': code
            }
            models.ProposalCenterSuppliers.objects.get_or_create(**data)
        # return success if done
        return ui_utils.handle_response(function_name, data='success', success=True)
    except KeyError as e:
        return ui_utils.handle_response(function_name, exception_object=e)
    except Exception as e:
        return ui_utils.handle_response(function_name, exception_object=e)


def calculate_address(center):
    """
    Args:
        center: makes address for this center
    Returns: address for this center

    """
    function_name = calculate_address.__name__
    try:
        address = center['address'] + "," + center['subarea'] + ',' + center['area'] + ',' + center['city'] + ' ' + \
                  center['pincode']
        return ui_utils.handle_response(function_name, data=address, success=True)

    except Exception as e:
        return ui_utils.handle_response(function_name, exception_object=e)


def save_center_data(proposal_data):
    """

    Args:
        proposal_data: a proposal_data with proposal_id as key must.

    Returns: center data

    """
    function_name = save_center_data.__name__
    try:
        # get the proposal_id
        proposal_id = proposal_data['proposal_id']

        # for all centers
        for center_info in proposal_data['centers']:
            center = center_info['center']

            # prepare center info
            center['proposal'] = proposal_id

            # get address for this center. because address can contain a complicated logic in future, it's in separate
            # function
            address_response = calculate_address(center)
            if not address_response.data['data']:
                return address_response
            address = address_response.data['data']

            # add lat long to center's data based on address calculated
            geo_response = get_geo_object(address)
            if not geo_response.data['status']:
                return geo_response
            geo_object = geo_response.data['data']
            center['latitude'] = geo_object.latitude
            center['longitude'] = geo_object.longitude

            if 'id' in center_info:
                # means an existing center was updated
                center_instance = models.ProposalCenterMapping.objects.get(id=center_info['id'])
                center_serializer = serializers.ProposalCenterMappingSerializer(center_instance, data=center)
            else:
                # means we need to create new center
                center_serializer = serializers.ProposalCenterMappingSerializer(data=center)

            # save center info
            if center_serializer.is_valid():
                center_serializer.save()
                # now save all the suppliers associated with this center
                response = save_suppliers_allowed(center_info, proposal_id, center_serializer.data['id'])
                if not response.data['status']:
                    return response
            else:
                return ui_utils.handle_response(function_name, data=center_serializer.errors)
        return ui_utils.handle_response(function_name, data='success', success=True)
    except Exception as e:
        return ui_utils.handle_response(function_name, exception_object=e)


def save_shortlisted_suppliers(suppliers, fixed_data):
    """
    Args:
        suppliers: a list of suppliers
        fixed_data: The data that will not change.

    Returns: saves the list of suppliers into shortlistedspaces model

    """
    function_name = save_shortlisted_suppliers.__name__
    try:
        center = fixed_data.get('center')
        proposal = fixed_data.get('proposal')
        code = fixed_data.get('supplier_code')
        content_type = fixed_data.get('content_type')

        count = 0
        for supplier in suppliers:

            # make the data to be saved in ShortListedSpaces
            data = {
                'content_type': content_type,
                'object_id': supplier['supplier_id'],
                'center': center,
                'proposal': proposal,
                'supplier_code': code
            }
            shortlisted_space, is_created = models.ShortlistedSpaces.objects.get_or_create(
                **data)  # todo: to be changed if better solution found
            shortlisted_space.status = supplier['status']
            shortlisted_space.save()
            if is_created:
                count += 1
        return ui_utils.handle_response(function_name, data=count, success=True)
    except Exception as e:
        return ui_utils.handle_response(function_name, exception_object=e)


def save_final_proposal(proposal_data, unique_supplier_codes):
    """
    The request is in form:
        [
             {
                  center : { id : 1 , center_name: c1, ...   } ,
                  suppliers: {  'RS' : [ { 'supplier_type_code': 'RS', 'status': 'R', 'supplier_id' : '1'}, {...}, {...} ],  }
                  suppliers_meta: {
                                     'RS': { 'inventory_type_selected' : [ 'PO', 'POST', 'ST' ]  },
                                     'CP': { 'inventory_type_selected':  ['ST']
                  }
             }
        ]
    Args:
        proposal_data: data of the proposal
        proposal_id: proposal_id

    Returns: collects all suppliers in societies array and inserts them into the db

    """
    function_name = save_final_proposal.__name__
    try:
        # get the proposal_id
        proposal_id = proposal_data['proposal_id']

        # get the center id
        center_id = proposal_data['center']['id']

        # get the proposal object
        proposal = models.ProposalInfo.objects.get(proposal_id=proposal_id)

        # get the center object
        center = models.ProposalCenterMapping.objects.get(id=center_id)

        fixed_data = {
            'center': center,
            'proposal': proposal,
        }

        # to keep count of new objects created
        objects_created = {
            'SHORTLISTED_SUPPLIERS': 0,
            'FILTER_OBJECTS': 0
        }

        filter_name = 'inventory_type_selected'

        for code in unique_supplier_codes:

            # get the list of suppliers
            suppliers = proposal_data['suppliers'][code]

            # get the content type for this supplier
            content_type_response = ui_utils.get_content_type(code)
            if not content_type_response.data['status']:
                return content_type_response

            content_type = content_type_response.data['data']

            fixed_data['supplier_code'] = code
            fixed_data['content_type'] = content_type

            # save data of shortlisted suppliers
            response = save_shortlisted_suppliers(suppliers, fixed_data)
            if not response.data['status']:
                return response
            objects_created['SHORTLISTED_SUPPLIERS'] += response.data['data']

            if proposal_data.get('suppliers_meta'):
                fixed_data['filter_name'] = filter_name
                inventories_selected = proposal_data['suppliers_meta'][code][filter_name]

                # save data of inventories selected
                response = save_filter_data(inventories_selected, fixed_data)
                if not response.data['status']:
                    return response
                objects_created['FILTER_OBJECTS'] += response.data['data']

        return ui_utils.handle_response(function_name, data=objects_created,
                                        success=True)
    except KeyError as e:
        return ui_utils.handle_response(function_name, data='Key Error', exception_object=e)
    except ObjectDoesNotExist as e:
        return ui_utils.handle_response(function_name, exception_object=e)
    except Exception as e:
        return ui_utils.handle_response(function_name, exception_object=e)


def save_filter_data(inventories_selected, fixed_data):
    """
    Args:
        inventories_selected: the list of inventories which are selected
        fixed_data: The data that is fixed data and will not change
    Returns:

    """
    function_name = save_filter_data.__name__
    try:

        center = fixed_data.get('center')
        proposal = fixed_data.get('proposal')
        code = fixed_data.get('supplier_code')
        content_type = fixed_data.get('content_type')
        filter_name = fixed_data.get('inventory_type_selected')

        #  to count how many filter objects were created
        count = 0

        for inventory_code in inventories_selected:
            data = {
                'center': center,
                'proposal': proposal,
                'supplier_type': content_type,
                'supplier_type_code': code
            }
            filer_object, is_created = models.Filters.objects.get_or_create(**data)
            filer_object.filter_name = filter_name
            filer_object.filter_code = inventory_code
            filer_object.is_checked = True
            filer_object.save()

            if is_created:
                count += 1

        return ui_utils.handle_response(function_name, data=count, success=True)
    except KeyError as e:
        return ui_utils.handle_response(function_name, data='Key Error', exception_object=e)
    except ObjectDoesNotExist as e:
        return ui_utils.handle_response(function_name, exception_object=e)
    except Exception as e:
        return ui_utils.handle_response(function_name, exception_object=e)


def create_proposal_id(business_id, account_id):
    """
    Args:
        business_id: The business_id
        account_id:  The account id

    Returns: A unique proposal id

    """
    function = create_proposal_id.__name__
    try:
        if not business_id or not account_id:
            return ui_utils.handle_response(function, data='provide business and account ids')
        # get number of business letters to append
        business_letters = website_constants.business_letters
        # get number of account letters to append
        account_letters = website_constants.account_letters
        # make the proposal id.
        proposal_id = business_id[-business_letters:].upper() + account_id[-account_letters:].upper() + (str(uuid.uuid4())[-website_constants.proposal_id_limit:])

        return ui_utils.handle_response(function, data=proposal_id, success=True)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def get_coordinates(radius, latitude, longitude):
    """

    Args:
        delta_dict: radius, latitude

    Returns: min lat, max lat, min long, max long

    """
    function_name = get_coordinates.__name__
    try:
        radius = float(radius)
        latitude = float(latitude)
        longitude = float(longitude)

        delta_dict = get_delta_latitude_longitude(float(radius), float(latitude))

        delta_latitude = delta_dict['delta_latitude']
        min_latitude = latitude - delta_latitude
        max_latitude = latitude + delta_latitude

        delta_longitude = delta_dict['delta_longitude']
        min_longitude = longitude - delta_longitude
        max_longitude = longitude + delta_longitude
        data = {
            'min_lat': float(min_latitude),
            'min_long': float(min_longitude),
            'max_lat': float(max_latitude),
            'max_long': float(max_longitude)
        }
        return ui_utils.handle_response(function_name, data=data, success=True)
    except Exception as e:
        return ui_utils.handle_response(function_name, exception_object=e)


def build_query(min_max_data, supplier_type_code):
    """

    Args:
        min_max_data: data of min, max lat longs.
        supplier_type_code: based on what supplier type code is, it constructs a query which shall be used
        to filter objects.

    Returns: a Q object.
    """
    function_name = build_query.__name__

    try:

        if supplier_type_code == 'RS':
            q = Q(society_latitude__lt=min_max_data['max_lat']) & Q(society_latitude__gt=min_max_data['min_lat']) & Q(
                society_longitude__lt=min_max_data['max_long']) & Q(society_longitude__gt=min_max_data['min_long'])
        else:
            q = Q(latitude__lt=min_max_data['max_lat']) & Q(latitude__gt=min_max_data['min_lat']) & Q(
                longitude__lt=min_max_data['max_long']) & Q(longitude__gt=min_max_data['min_long'])

        return ui_utils.handle_response(function_name, data=q, success=True)
    except Exception as e:
        return ui_utils.handle_response(function_name, exception_object=e)


def get_suppliers(query, supplier_type_code, coordinates):
    """
    Args:
        query. The Q object
        supplier_type_code : 'RS', 'CP'
    Returns: all the suppliers.

    """
    function_name = get_suppliers.__name__
    try:
        radius = coordinates.get('radius', 0)
        latitude = coordinates.get('latitude', 0)
        longitude = coordinates.get('longitude', 0)

        # get the suppliers data within that radius
        supplier_model = ui_utils.get_model(supplier_type_code)
        supplier_objects = supplier_model.objects.filter(query)
        # need to set shortlisted=True for every supplier
        serializer = ui_utils.get_serializer(supplier_type_code)(supplier_objects, many=True)
        # result to store final suppliers
        result = []
        for supplier in serializer.data:
            # replace all society specific keys with common supplier keys
            for society_key, actual_key in website_constants.society_common_keys.iteritems():
                if society_key in supplier.keys():
                    value = supplier[society_key]
                    del supplier[society_key]
                    supplier[actual_key] = value
            if space_on_circle(latitude, longitude, radius, supplier['latitude'], supplier['longitude']):
                supplier['shortlisted'] = True
                # set status= 'S' as suppliers are shortlisted inititially.
                supplier['status'] = 'S'
                result.append(supplier)
        return ui_utils.handle_response(function_name, data=result, success=True)

    except Exception as e:
        return ui_utils.handle_response(function_name, exception_object=e)


def get_filters(data):
    """
    Args:
        proposal_id: The proposal id
        center_id: The center id
        content_type: The content type

    Returns: Filters data

    """
    function_name = get_filters.__name__
    try:

        proposal_id = data['proposal_id']
        center_id = data['center_id']
        supplier_content_type = data['content_type']

        # get the filter's data
        filter_objects = models.Filters.objects.filter(proposal_id=proposal_id, center_id=center_id,
                                                       supplier_type=supplier_content_type)
        filter_serializer = serializers.FiltersSerializer(filter_objects, many=True)
        return ui_utils.handle_response(function_name, data=filter_serializer.data, success=True)
    except Exception as e:
        return ui_utils.handle_response(function_name, exception_object=e)


def handle_single_center(center, result):
    """

    Args:
        center: One center data.
        result : the final result array.

    Returns:

    """
    function_name = handle_single_center.__name__
    try:
        center_data = {}

        center_data['center'] = center

        radius = float(center['radius'])
        latitude = float(center['latitude'])
        longitude = float(center['longitude'])

        response = get_coordinates(radius, latitude, longitude)
        if not response.data['status']:
            return response

        min_max_data = response.data['data']

        # make room for storing supplier data
        center_data['suppliers'] = {}

        # store data for each type of supplier
        for supplier_type_code in center['codes']:
            # make an entry against the code for storing the results
            center_data['suppliers'][supplier_type_code] = {}

            # make a query
            query_response = build_query(min_max_data, supplier_type_code)
            if not query_response.data['status']:
                return query_response
            query = query_response.data['data']

            # prepare coordinates
            coordinates = {
                'radius': radius,
                'latitude': latitude,
                'longitude': longitude
            }

            # get the suppliers data
            response = get_suppliers(query, supplier_type_code, coordinates)
            if not response.data['status']:
                return response
            suppliers_data = response.data['data']

            # set in the result
            center_data['suppliers'][supplier_type_code] = suppliers_data

        result.append(center_data)
        return ui_utils.handle_response(function_name, data=result, success=True)
    except KeyError as e:
        return ui_utils.handle_response(function_name, data='Key Error occurred', exception_object=e)
    except Exception as e:
        return ui_utils.handle_response(function_name, exception_object=e)


def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    function = merge_two_dicts.__name__
    try:
        # update x with keys which are not in x.
        x = x.copy()
        x_keys = x.keys()
        for key, value in y.iteritems():
            if key not in x_keys:
                x[key] = value
        return ui_utils.handle_response(function, data=x, success=True)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def suppliers_within_radius(data):
    """
    Args:
        data: a dict containing proposal_id, center_id, radius, supplier_codes.
        Two kinds of data is prepared and sent as of now:
        suppliers within radius and filters data

    Returns: all the suppliers withing the radius defined.


    """
    function_name = suppliers_within_radius.__name__
    try:
        proposal_id = data['proposal_id']
        center_id = data['center_id']

        business_name = models.ProposalInfo.objects.get(proposal_id=proposal_id).account.business.name
        master_result = {}
        # set the business_name
        master_result['business_name'] = business_name
        # space to store the suppliers
        master_result['suppliers'] = []

        result = []
        # todo: think of better way of separating this logic. looks ugly right now
        if center_id:
            # the queries will change if center_id is provided because we want to process
            # for this center only.
            if not data['radius'] or not data['latitude'] or not data['longitude']:
                return ui_utils.handle_response(function_name, data='if giving center_id, give radius, lat, long too!')

            centers = models.ProposalCenterMapping.objects.filter(id=center_id)
            serializer = serializers.ProposalCenterMappingSerializer(centers, many=True)

            serializer.data[0]['radius'] = data['radius']
            serializer.data[0]['latitude'] = data['latitude']
            serializer.data[0]['longitude'] = data['longitude']
            supplier_type_codes_list = models.ProposalCenterSuppliers.objects.filter(
                center_id=center_id).select_related('center').values('center', 'supplier_type_code')
        else:
            supplier_type_codes_list = models.ProposalCenterSuppliers.objects.filter(
                proposal_id=proposal_id).select_related('center').values('center', 'supplier_type_code')

            # fetch the mapped centers. This centers were saved when CreateInitialproposal was hit.
            center_id_list = [data['center'] for data in supplier_type_codes_list]

            # query the center objects
            centers = models.ProposalCenterMapping.objects.filter(proposal_id=proposal_id, id__in=center_id_list)

            serializer = serializers.ProposalCenterMappingSerializer(centers, many=True)

        # if not center_id, then fetch all the centers. centers can be a list
        # we add an extra attribute for each center object we get. Thats called codes. codes contain a list
        # of supplier_type_codees  like RS, CP.

        supplier_codes_dict = {center['id']: set() for center in serializer.data}
        if not supplier_codes_dict:
            return ui_utils.handle_response(function_name, data='Not found any centers in database against {0}'.format(proposal_id))
        for data in supplier_type_codes_list:
            center_id = data['center']
            code = data['supplier_type_code']
            supplier_codes_dict[center_id].add(code)

        for center in serializer.data:
            center['codes'] = supplier_codes_dict[center['id']]

        for center in serializer.data:
            response = handle_single_center(center, result)
            if not response.data['status']:
                return response
            result = response.data['data']
        
        master_result['suppliers'] = result
        return ui_utils.handle_response(function_name, data=master_result, success=True)
    except KeyError as e:
        return ui_utils.handle_response(function_name, data='Key Error occurred', exception_object=e)
    except Exception as e:
        return ui_utils.handle_response(function_name, exception_object=e)


def child_proposals(data):
    """
    Args:
        data: a dict containing parent_id for which we have to fetch all children proposals data
    Returns: all the proposalInfo data that is children of the given proposal_id

    """
    function_name = child_proposals.__name__
    try:
        # fetch all children of proposal_id and return.
        parent = data['parent']
        proposal_children = models.ProposalInfo.objects.filter(parent=parent).order_by('-created_on')
        serializer = serializers.ProposalInfoSerializer(proposal_children, many=True)
        return ui_utils.handle_response(function_name, data=serializer.data, success=True)
    except Exception as e:
        return ui_utils.handle_response(function_name, exception_object=e)


def construct_proposal_response(proposal_id):
    """
    Args:
        proposal_id: proposal_id for which response structure is built
    appends a list called codes in each center object.

    Returns: constructs the data in required form to be sent back to API response
    """
    function_name = construct_proposal_response.__name__
    try:

        supplier_type_codes_list = models.ProposalCenterSuppliers.objects.filter(
                proposal_id=proposal_id).select_related('center').values('center', 'supplier_type_code')

        # fetch the mapped centers. This centers were saved when CreateInitialproposal was hit.
        center_id_list = [data['center'] for data in supplier_type_codes_list]

        # query the center objects
        centers = models.ProposalCenterMapping.objects.filter(proposal_id=proposal_id, id__in=center_id_list)

        serializer = serializers.ProposalCenterMappingSerializer(centers, many=True)
        supplier_codes_dict = {center['id']: [] for center in serializer.data}
        for data in supplier_type_codes_list:
            center_id = data['center']
            code = data['supplier_type_code']
            supplier_codes_dict[center_id].append(code)

        for center in serializer.data:
            center['codes'] = supplier_codes_dict[center['id']]

        return ui_utils.handle_response(function_name, data=serializer.data, success=True)

    except Exception as e:
        return ui_utils.handle_response(function_name, exception_object=e)


def add_shortlisted_suppliers(supplier_type_code_list, shortlisted_suppliers):
    """

    Args:
        supplier_type_code_list: ['RS', 'CP', 'GY']
        shortlisted_suppliers:  a list of object id's

    Returns: { RS: [], CP: [], GY: [] } a dict containing each type of suppliers in the list

    """
    function_name = add_shortlisted_suppliers.__name__
    try:
        # from the codes, fetch the right supplier model, supplier serializer, and put in the dict against that code
        result = {}
        for code in supplier_type_code_list:
            supplier_model = ui_utils.get_model(code)
            supplier_serializer = ui_utils.get_serializer(code)
            suppliers = supplier_model.objects.filter(supplier_id__in=shortlisted_suppliers)
            serializer = supplier_serializer(suppliers, many=True)
            result[code] = serializer.data

        # return the result
        return ui_utils.handle_response(function_name, data=result, success=True)
    except Exception as e:
        return ui_utils.handle_response(function_name, exception_object=e)


def proposal_shortlisted_spaces(data):
    """
    Args:
        data: a dict containing proposal_id for which we have to fetch all shortlisted spaces

    Returns: all shortlisted spaces
    """
    function_name = proposal_shortlisted_spaces.__name__
    try:
        proposal_id = data['proposal_id']

        # fetch all shortlisted suppliers object id's for this proposal
        shortlisted_suppliers = models.ShortlistedSpaces.objects.filter(proposal_id=proposal_id).select_related(
            'content_object').values_list('object_id')

        # construction of proposal response is isolated
        response = construct_proposal_response(proposal_id)
        if not response.data['status']:
            return response

        # result
        result = []

        # all connected centers data
        centers = response.data['data']

        # add extra information in each center object
        for center in centers:
            # empty dict to store intermediate result
            center_result = {}
            # add shortlisted suppliers for codes available for this center
            response = add_shortlisted_suppliers(center['codes'], shortlisted_suppliers)
            if not response.data['status']:
                return response

            center_result['suppliers'] = response.data['data']
            center_result['center'] = center

            result.append(center_result)

        return ui_utils.handle_response(function_name, data=result, success=True)
    except Exception as e:
        return ui_utils.handle_response(function_name, exception_object=e)


def unique_supplier_type_codes(data):
    """
    because the information that which  supplier types are shortlisted is not in the request,we need to derive it
    from data itself.
    Args:
        data: data
    Returns: unique supplier codes available
    """
    function_name = unique_supplier_type_codes.__name__
    try:
        supplier_type_codes = []
        for center in data:
            codes = center['suppliers'].keys()
            supplier_type_codes.extend(codes)
        return ui_utils.handle_response(function_name, data=list(set(supplier_type_codes)), success=True)
    except Exception as e:
        return ui_utils.handle_response(function_name, exception_object=e)


def extra_header_database_keys(supplier_type_codes, data, result):
    """
    because depending upon inventory types selected for each supplier, the headers can be extended and hence the database
    keys shall be extended hence this function returns a dict for each of the suppliers the extra headers and database keys
    Args:
        data: data
    Returns: a dict containing header and database keys
    """
    function = extra_header_database_keys.__name__
    try:
        for code in supplier_type_codes:
            for center in data:
                if center['suppliers_meta'].get(code):
                    inventory_codes = center['suppliers_meta'][code]['inventory_type_selected']
                else:
                    inventory_codes = []

                response = get_unique_inventory_codes(inventory_codes)
                if not response.data['status']:
                    return response
                unique_inv_codes = response.data['data']

                # extend the header keys with header for supplier type codes
                response = get_union_keys_inventory_code('HEADER', unique_inv_codes)
                if not response.data['status']:
                    return response
                result[code]['header_keys'].extend(response.data['data'])

                # extend the data keys with header for supplier type codes
                response = get_union_keys_inventory_code('DATA', unique_inv_codes)
                if not response.data['status']:
                    return response
                result[code]['data_keys'].extend(response.data['data'])

            # remove duplicates for this supplier code. we hell can't use sets because that thing will destroy the order
            # of the keys which is important and the order must match
            result[code]['header_keys'] = remove_duplicates_preserver_order(result[code]['header_keys'])
            result[code]['data_keys'] = remove_duplicates_preserver_order(result[code]['data_keys'])

            # set the counts for validation.
            result[code]['header_keys_count'] = len(result[code]['header_keys'])
            result[code]['data_keys_count'] = len(result[code]['data_keys'])

        return ui_utils.handle_response(function, data=result, success=True)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def initialize_export_final_response(supplier_type_codes, result):
    """
    because there can be multiple type of supplier_type_codes, this function prepares a dict and sets it to
    keys and values required  for further processing for example with sheet names etc.
    Args:
        supplier_type_codes: ['RS', 'CP']

    Returns: a initialized dict

    """
    function = initialize_export_final_response.__name__
    try:
        for code in supplier_type_codes:

            result[code] = {}
            sheet_name = website_constants.sheet_names[code]
            result[code]['sheet_name'] = sheet_name

            # set fixed headers for center
            response = get_union_keys_inventory_code('HEADER', ['CENTER'])
            if not response.data['status']:
                return response
            result[code]['header_keys'] = response.data['data']

            # set fixed data keys for center
            response = get_union_keys_inventory_code('DATA', ['CENTER'])
            if not response.data['status']:
                return response
            result[code]['data_keys'] = response.data['data']

            # set fixed header keys for supplier
            response = get_union_keys_inventory_code('HEADER', [code])
            if not response.data['status']:
                return response
            result[code]['header_keys'].extend(response.data['data'])

            # set fixed data keys for supplier
            response = get_union_keys_inventory_code('DATA', [code])
            if not response.data['status']:
                return response
            result[code]['data_keys'].extend(response.data['data'])

            result[code]['objects'] = []
        return ui_utils.handle_response(function, data=result, success=True)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def construct_single_supplier_row(object, keys):
    """
    Args:
        object: The  object which is a dict
        keys a list of keys

    Returns: a dict containing final data

    """
    function = construct_single_supplier_row.__name__
    try:
        result = {key: object.get(key) for key in keys}
        return ui_utils.handle_response(function, data=result, success=True)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def make_export_final_response(result, data):
    """
    This function populates the result with 'objects' per supplier_type_codes.
    Args:
        result: result dict where objects will be stored
        data: the entire request.data
    Returns:

    """
    function = make_export_final_response.__name__
    try:
        for center in data:

            response = construct_single_supplier_row(center['center'], website_constants.center_keys)
            if not response.data['status']:
                return response

            # obtain the dict containing centre information
            center_info_dict = response.data['data'].copy()

            for code, supplier_object_list in center['suppliers'].iteritems():

                for supplier_object in supplier_object_list:

                    # obtain the dict containing non-center information
                    response = construct_single_supplier_row(supplier_object, result[code]['data_keys'])
                    if not response.data['status']:
                        return response

                    supplier_info_dict = response.data['data']

                    # merge the two dicts
                    response = merge_two_dicts(center_info_dict, supplier_info_dict)
                    if not response.data['status']:
                        return response

                    # append it to the result
                    result[code]['objects'].append(response.data['data'])

        return ui_utils.handle_response(function, data=result, success=True)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def save_leads(row):
    """
    Args:
        row: a dict representing one row of campaign_leads.

    Returns: tries to save leads data  into lead model and returns either newly created object or old object.

    """
    function = save_leads.__name__
    try:
        lead_data = {lead_key: row[lead_key] for lead_key in website_constants.lead_keys}
        email = lead_data['email']
        if not email:
            return ui_utils.handle_response(function, data='please provide email')
        lead_object, is_created = models.Lead.objects.get_or_create(email=email)
        serializer = serializers.LeadSerializer(lead_object, data=lead_data)
        if serializer.is_valid():
            serializer.save()
            return ui_utils.handle_response(function, data=lead_object, success=True)
        return ui_utils.handle_response(function, data=serializer.errors)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def save_campaign_leads(row):
    """

    Args:
        row: a dict representing one row of campaign_leads sheet.

    Returns: tries to save on campaign_leads table. return the newly created campaign_leads object.

    """
    function = save_campaign_leads.__name__
    try:
        campaign_id = row['campaign_id']
        lead_email = row['email']
        campaign_lead_object, is_created = models.CampaignLeads.objects.get_or_create(campaign_id=campaign_id,
                                                                                      lead_email=lead_email)
        campaign_lead_object.comments = row['comments']
        campaign_lead_object.save()
        return ui_utils.handle_response(function, data=campaign_lead_object, success=True)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def handle_campaign_leads(row):
    """
    Args:
        row: row is a dict containing one row information of campaign-leads sheet.
         currently i am inserting into db directly instead of a bulk_create. will change in future if performance
         is compromised.

    Returns: success in case db hit is success, failure otherwise

    """
    function = save_campaign_leads.__name__
    try:
        with transaction.atomic():
            response = save_leads(row)
            if not response.data['status']:
                return response
            lead_object = response.data['data']

            response = save_campaign_leads(row)
            if not response.data['status']:
                return response

            campaign_lead_object = response.data['data']

            # send some useful information back
            data = {
                'lead_email': lead_object.email,
                'campaign_lead_id': campaign_lead_object.id,
                'campaign_id': row['campaign_id']
            }
            return ui_utils.handle_response(function, data=data, success=True)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def handle_common_filters(common_filters, supplier_type_code):
    """
    This function handles only common filters.
    Args:
        common_filters: { 'latitude': 10, 'longitude': 12, 'radius': 1, 'quality': ['UH', 'H'],
        'quantity': ['VL', 'L'] }

    Returns: a Q object based on above filters

    """
    function = handle_common_filters.__name__
    try:
        if not common_filters:
            return ui_utils.handle_response(function,data=Q(), success=True)

        # we will store field and values in this dict and later on use it to construct Q object
        query = {}

        # fetch the lat long radius
        latitude = float(common_filters['latitude'])
        longitude = float(common_filters['longitude'])
        radius = float(common_filters['radius'])

        response = get_coordinates(radius, latitude, longitude)
        if not response.data['status']:
            return response
        # get the coordinates
        coordinates = response.data['data']

        max_latitude = coordinates['max_lat']
        max_longitude = coordinates['max_long']
        min_latitude = coordinates['min_lat']
        min_longitude = coordinates['min_long']

        # start build the query
        if supplier_type_code == 'RS':
            query['society_latitude__lt'] = max_latitude
            query['society_latitude__gt'] = min_latitude
            query['society_longitude__lt'] = max_longitude
            query['society_longitude__gt'] = min_longitude

        else:
            query['latitude__lt'] = max_latitude
            query['latitude__gt'] = min_latitude
            query['longitude__lt'] = max_longitude
            query['longitude__gt'] = min_longitude
        # the keys like 'locality', 'quantity', 'quality' we receive from front end are already defined in constants
        predefined_common_filter_keys = website_constants.query_dict[supplier_type_code].keys()
        # we may receive a subset of already defined keys. obtain that subset
        received_common_filter_keys = common_filters.keys()
        # iterate over each predefined key and check if it is what we have received.
        for filter_term in predefined_common_filter_keys:
            if filter_term in received_common_filter_keys:
                # if received, obtain the query term for that filter key. query term looks like 'locality_rating__in'
                query_term = website_constants.query_dict[supplier_type_code][filter_term]['query']
                # fetch the query dict associated. it contains the code-value mapping of the filters codes
                query_dict = website_constants.query_dict[supplier_type_code][filter_term]['dict']
                # fetch the filter codes received like ['HH', 'UH']
                filter_codes = common_filters.get(filter_term)
                # get the actual values against these codes for example, 'Ulta High' for 'UH'. These values are defined
                # in the query_dict fetched above.
                filter_term_value_list = [query_dict.get(code) for code in filter_codes]
                # set the query dict to list of values calculated against the db field term
                query[query_term] = filter_term_value_list

        # remove those fields that have False value or Empty values.
        response = remove_empty_fields(query)
        if not response.data['status']:
            return response
        query = response.data['data']

        # build the actual Q object once the fields are fixed
        common_filter_query = Q(**query)

        # return the query
        return ui_utils.handle_response(function, data=common_filter_query, success=True)

    except KeyError as e:
        return ui_utils.handle_response(function, data='Key Error occurred', exception_object=e)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def remove_empty_fields(q_object_dict):
    """
    Args:
        q_object_dict: This function takes a dict called q_object_dict, and removes all those keys that have None value
        against it. This is because we do not want to query against a NULL value as it produces inconsistent
        results.

    Returns: q dict with keys whose value is None removed.

    """
    function = remove_empty_fields.__name__
    try:
        q_object_dict_copy = q_object_dict.copy()
        for key, value in q_object_dict.iteritems():
            if not value:
                del q_object_dict_copy[key]
        return ui_utils.handle_response(function, data=q_object_dict_copy, success=True)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def handle_inventory_filters(inventory_list):
    """
    Args:
        inventory_list: ['PO', 'POST', 'ST' ]

    Returns: a Q object after handling each inventory code
    query = PO | ST | (POST) | CD | (STFL)
    for single codes like 'PO', 'ST', etc the query is just there corresponding db field.
    for complex codes like 'POST', each individual code is extracted and individual database fields are joined by 'and'.
    """
    function = handle_inventory_filters.__name__
    try:
        if not inventory_list:
            return ui_utils.handle_response(function, data=Q(), success=True)

        # final Q object to be returned
        inventory_query = Q()
        # atomic inventories means 'PO', 'ST' etc.
        valid_atomic_inventories = website_constants.inventory_dict.keys()
        # iterate through all the inventory list
        for inventory in inventory_list:
            # if it is atomic, that means you only need to fetch it's db field and set it to Q object
            if inventory in valid_atomic_inventories:
                # the policy is to  OR the atomic inventories
                if inventory_query:
                    inventory_query |= Q(**{website_constants.inventory_dict[inventory]: True})
                else:
                    inventory_query = Q(**{website_constants.inventory_dict[inventory]: True})
                continue
            # come here only it it's non atomic inventory code.
            query = {}
            step = 2
            # split the non atomic inventory code into size of 2 letters.
            individual_codes = [inventory[i:i+step] for i in range(0, len(inventory), step)]
            # for each code
            for code in individual_codes:
                # set the query
                query[website_constants.inventory_dict[code]] = True

            # make a new Q object with query and OR it with previously calculated inventory_query.
            if inventory_query:
                inventory_query |= Q(**query)
            else:
                inventory_query = Q(**query)

        return ui_utils.handle_response(function, data=inventory_query, success=True)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def handle_specific_filters(specific_filters, supplier_type_code):
    """
    This function is called from construct query which handles filters specific to supplier
    Args:
        specific_filters: { 'real_estate_allowed': True, 'total_employee_count': 120, 'flat_type': [ '1RK', '2BHK' ]

          }
    Returns: a Q object based on above filters

    """
    function = handle_specific_filters.__name__
    try:

        if not specific_filters:
            return ui_utils.handle_response(function, data=Q(), success=True)

        # get the predefined dict of specific filters for this supplier
        master_specific_filters = website_constants.supplier_filters[supplier_type_code]

        # construct a dict for storing query values.
        query = {}
        # the following loop stores those fields in received filters which can be mapped directly to db columns.
        for received_filter, filter_value in specific_filters.iteritems():

            # get the database field for this specific filter
            database_field = master_specific_filters.get(received_filter)

            if database_field:
                # set it to the dict
                query[database_field] = filter_value

        # make the query for fields in the request that map directly to model fields.
        specific_filters_query = Q(**query)

        # do if else check on supplier type code to include things particular to that supplier. Things which
        # cannot be mapped to a particular supplier and vary from supplier to supplier
        if supplier_type_code == 'RS':
            if specific_filters.get('flat_type'):
                flat_type_values = [website_constants.flat_type_dict[flat_code] for flat_code in specific_filters.get('flat_type')]
                supplier_ids = models.FlatType.objects.filter(flat_type__in=flat_type_values).values_list('society__supplier_id')
                specific_filters_query &= Q(supplier_id__in=supplier_ids)

        if supplier_type_code == 'CP':
            # well, we can receive a multiple dicts for employee counts. each describing min and max employee counts.
            if specific_filters.get('employees_count'):
                for employees_count_range in specific_filters.get('employees_count'):
                    max = employees_count_range['max']
                    min = employees_count_range['min']
                    if specific_filters_query:
                        specific_filters_query |= Q(totalemployees_count__gte=min, totalemployees_count__lte=max)
                    else:
                        specific_filters_query = Q(totalemployees_count__gte=min, totalemployees_count__lte=max)
        # return it
        return ui_utils.handle_response(function, data=specific_filters_query, success=True)

    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def is_fulltext_index(model_name, column_name, index_type):
    """
    Args:
        model_name: table name
        column_name: column name
        index_type: 'FULLTEXT'

    Returns: True if columnn of table has a FullText index, False otherwise

    """
    function = is_fulltext_index.__name__
    try:
        table_name = model_name._meta.db_table
        raw_query_set = model_name.objects.raw(
            'show index from {0} where column_name={1} and index_type={2}'.format(table_name, column_name, index_type))
        answer = True if raw_query_set else False
        return ui_utils.handle_response(function, data=answer, success=True)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def initialize_area_subarea(result, index):
    """
    Args:
        result: a list
        index: index of the list to initialize with a dict containing 'state', 'city' , 'area', 'subarea'.

    Returns:

    """
    function = initialize_area_subarea.__name__
    try:
        # empty dict
        area_subarea_object = {}
        # set a state dict
        area_subarea_object['state'] = {}
        # set a city dict
        area_subarea_object['city'] = {}
        # set a area dict
        area_subarea_object['area'] = {}
        # set a subarea dict
        area_subarea_object['subarea'] = {}
        # set the final dict to this index
        result[index] = area_subarea_object

        return ui_utils.handle_response(function, data=result, success=True)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def handle_states(result, index, row):
    """
    Args:
        result: The result list
        index: index of the list for which state object is to be modified
        row:  a single row of the sheet

    Returns:

    """
    function = handle_states.__name__
    try:
        state_object = result[index]['state']
        state_object['state_code'] = row['state_code']
        state_object['state_name'] = row['state_name']
        result[index]['state'] = state_object
        return ui_utils.handle_response(function, data=result, success=True)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def handle_city(result, index, row):
    """
    Args:
        result: The result list
        index: index of the list for which city object is to be modified
        row:  a single row of the sheet

    Returns:

    """
    function = handle_city.__name__
    try:
        city_object = result[index]['city']
        city_object['city_code'] = row['city_code']
        city_object['city_name'] = row['city_name']
        result[index]['city'] = city_object
        return ui_utils.handle_response(function, data=result, success=True)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def handle_area(result, index, row):
    """
    Args:
        result: The result list
        index: index of the list for which area object is to be modified
        row:  a single row of the sheet

    Returns:

    """
    function = handle_area.__name__
    try:
        area_object = result[index]['area']
        area_object['area_code'] = row['area_code']
        area_object['label'] = row['area_name']
        result[index]['area'] = area_object
        return ui_utils.handle_response(function, data=result, success=True)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def handle_subarea(result, index, row):
    """
    Args:
        result: The result list
        index: index of the list for which subarea object is to be modified
        row:  a single row of the sheet

    Returns:

    """
    function = handle_subarea.__name__
    try:
        subarea_object = result[index]['subarea']
        subarea_object['subarea_code'] = row['subarea_code']
        subarea_object['subarea_name'] = row['subarea_name']
        subarea_object['locality_rating'] = row.get('locality_rating')
        result[index]['subarea'] = subarea_object
        return ui_utils.handle_response(function, data=result, success=True)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def get_inventory_pricing(supplier_type_code, inventory_names, inventory_types, inventory_durations):
    """
    Args:
        inventory_code: fetches price details for one inventory_code, 'PO', 'ST'.
        inventory_type: 'Canopy', 'Small', 'Large'
        inventory_duration: 'Campaign Weekly', 'Campaign Monthly'.

    Returns: price for that inventory from PriceMappingDefault table
    """
    function = get_inventory_pricing.__name__
    try:
       supplier_content_type = ui_utils.get_content_type(supplier_type_code)
       adinventory_type_objects = models.AdInventoryType.objects.filter(adinventory_name__in=inventory_names, adinventory_type__in=inventory_types)
       duration_type_objects = models.DurationType.objects.filter(duration_name__in=inventory_durations)
       inventory_prices = models.PriceMappingDefault.objects.prefetch_related('content_object').filter(content_type=supplier_content_type).values('object_id', 'business_price', 'adinventory_type__name', 'adinventory_type__type', 'duration__type__name' ).filter(adinventory_type__in=adinventory_type_objects, duration_type__in=duration_type_objects)

       return ui_utils.handle_response(function, data=inventory_prices, success=True)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def set_supplier_extra_attributes(suppliers, supplier_type_code,  inventory_codes):
    """
    Args:
        suppliers: a list containg dict for each supplier

    Returns: modified each supplier by adding some attributes

    """
    function = set_supplier_extra_attributes.__name__
    try:
        inventory_names = []
        inventory_types = []
        inventory_durations = []
        for inventory_code in inventory_codes:
             inventory_duration_dict = website_constants.inventory_duration_dict[inventory_code]
             inventory_types.extend(type_dur_dict['type'] for type_dur_dict in inventory_duration_dict['type_duration'])
             inventory_durations.extend(type_dur_dict['duration'] for type_dur_dict in inventory_duration_dict['type_duration'])
             inventory_names.extend(inventory_duration_dict['name'])

        response = get_inventory_pricing(supplier_type_code, inventory_names, inventory_types, inventory_durations)
        if not response.data['status']:
            return response
        inventory_pricing = response.data['data']
        return ui_utils.handle_response(function, data=suppliers, success=True)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def save_area_subarea(result):
    """
    The result looks like this
     [
        {
          "city": {
            "city_name": "Mumabi",
            "city_code": "BOM"
          },
          "state": {
            "state_code": "MH",
            "state_name": "Maharashtra"
          },
          "subarea": {
            "locality_rating": "high",
            "subarea_code": "AE",
            "subarea_name": "Andheri(E)"
          },
          "area": {
            "area_code": "AE",
            "label": "Andheri(E)"
          }
        },
        {..}
     ]
    Args:
        result: The result

    Returns: success if the data in result is saved, else failure

    """
    function = save_area_subarea.__name__
    try:
        total_new_objects_created = 0
        with transaction.atomic():
            for data in result:
                # make state
                state_object, is_created = models.State.objects.get_or_create(**data['state'])
                if is_created:
                    total_new_objects_created += 1

                data['city']['state_code'] = state_object
                # make city
                city_object, is_created = models.City.objects.get_or_create(**data['city'])
                if is_created:
                    total_new_objects_created += 1

                data['area']['city_code'] = city_object

                # make area
                area, is_created = models.CityArea.objects.get_or_create(**data['area'])
                if is_created:
                    total_new_objects_created += 1

                data['subarea']['area_code'] = area
                # make subarea
                subarea, is_created = models.CitySubArea.objects.get_or_create(**data['subarea'])
                if is_created:
                    total_new_objects_created += 1

            return ui_utils.handle_response(function, data=total_new_objects_created, success=True)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def set_pricing_temproray(suppliers, supplier_ids, supplier_type_code, coordinates):
    """
    Args:
        suppliers: a list of supplier dicts
        supplier_ids: a list of supplier id's
        supplier_type_code: CP, RS

    Returns:

    """
    function = set_pricing_temproray.__name__
    # fetch all inventory_summary objects related to each one of suppliers
    inventory_summary_objects = models.InventorySummary.objects.filter_objects(
        {'supplier_type_code': supplier_type_code}, supplier_ids)
    # generate a mapping from object_id to inv_summ_object in a dict so that right object can be fetched up
    inventory_summary_objects_mapping = {inv_summary_object.object_id: inv_summary_object for inv_summary_object in
                                         inventory_summary_objects}
    radius = float(coordinates['radius'])
    latitude = float(coordinates['latitude'])
    longitude = float(coordinates['longitude'])

    # container to hold final suppliers
    result = []

    try:
        for supplier in suppliers:

            # change the response for societies
            if supplier_type_code == 'RS':
                for society_key, common_key in website_constants.society_common_keys.iteritems():
                    supplier_key_value = supplier[society_key]
                    del supplier[society_key]
                    supplier[common_key] = supplier_key_value

            # include only those suppliers that lie within the circle of radius given
            if space_on_circle(latitude, longitude, radius, supplier['latitude'], supplier['longitude']):
                supplier_inventory_obj = inventory_summary_objects_mapping.get(supplier['supplier_id'])
                supplier['shortlisted'] = True
                supplier['buffer_status'] = False
                # status is shortlisted initially
                supplier['status'] = 'S'
                # do not calculate prices if no inventory summary object exist
                # todo: involves one database hit within calculate_price() function. improve it later if code is slow.
                if supplier_inventory_obj:
                    if supplier_inventory_obj.poster_allowed_nb or supplier_inventory_obj.poster_allowed_lift:
                        supplier['total_poster_count'] = supplier_inventory_obj.total_poster_count
                        response = calculate_price('poster_a4', 'campaign_weekly', supplier['supplier_id'], supplier_type_code)
                        if not response.data['status']:
                            return response
                        supplier['poster_price'] = response.data['data']

                    if supplier_inventory_obj.standee_allowed:
                        supplier['total_standee_count'] = supplier_inventory_obj.total_standee_count
                        response = calculate_price('standee_small', 'campaign_weekly', supplier['supplier_id'], supplier_type_code)
                        if not response.data['status']:
                            return response
                        supplier['standee_price'] = response.data['data']

                    if supplier_inventory_obj.stall_allowed:
                        supplier['total_stall_count'] = supplier_inventory_obj.total_stall_count
                        response = calculate_price('stall_small', 'unit_daily', supplier['supplier_id'], supplier_type_code)
                        if not response.data['status']:
                            return response
                        supplier['stall_price'] = response.data['data']
                        response = calculate_price('car_display_standard', 'unit_daily', supplier['supplier_id'], supplier_type_code)
                        if not response.data['status']:
                            return response
                        supplier['car_display_price'] = response.data['data']

                    if supplier_inventory_obj.flier_allowed:
                        supplier['flier_frequency'] = supplier_inventory_obj.flier_frequency
                        response = calculate_price('flier_door_to_door', 'unit_daily', supplier['supplier_id'], supplier_type_code)
                        if not response.data['status']:
                            return response
                        supplier['flier_price'] = response.data['data']

                result.append(supplier)
        return ui_utils.handle_response(function, data=result, success=True)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def calculate_price(inv_type, dur_type, supplier_id, supplier_type_Code):
    """
    Args:
        inv_type: type of inventory
        dur_type: duration

    Returns: prince for the inventory, for this inventory type and this duration
    """
    function = calculate_price.__name__
    try:
        response = ui_utils.get_content_type(supplier_type_Code)
        if not response.data['data']:
            return response
        content_type = response.data['data']
        adinventory_type_dict = ui_utils.adinventory_func()
        duration_type_dict = ui_utils.duration_type_func()
        price_mapping = PriceMappingDefault.objects.get(adinventory_type=adinventory_type_dict[inv_type], duration_type=duration_type_dict[dur_type], object_id=supplier_id, content_type=content_type )
        return ui_utils.handle_response(function, data=price_mapping.business_price, success=True)
    except ObjectDoesNotExist as e:
        # return zero price if the right object does not exist
        return ui_utils.handle_response(function, data=0, success=True)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def get_file_name(user, proposal_id):
    """
    Args:
        user: The user name
        proposal_id: proposal_id

    Returns: a string that wil be used as file name.

    """
    function = get_file_name.__name__
    try:
        format = website_constants.datetime_format
        now_time = datetime.datetime.now()
        datetime_stamp = now_time.strftime(format)
        proposal = models.ProposalInfo.objects.get(proposal_id=proposal_id) 
        account = proposal.account
        business = account.business
        if user.is_anonymous():
            user_string = 'Anonymous'
            user = None
        else:
            user_string = user.get_username()
        file_name = user_string + '_' + business.name.lower() + '_' + account.name.lower() + '_' + proposal_id + '_' + datetime_stamp + '.xlsx'
        # save this file in db 
        data = {
            'user':  user,
            'business': business,
            'account': account,
            'proposal': proposal,
            'date': now_time,
            'file_name': file_name
        }
        models.GenericExportFileName.objects.get_or_create(**data)
        return ui_utils.handle_response(function, data=file_name, success=True)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def add_metric_sheet(workbook):
    """
    Args:
        workbook: a workbook object
    Returns:  reads a sheet from empty_proposal_cost_data.xlsx, add it to export sheet for metrics.
    """
    function = add_metric_sheet.__name__
    try:
        my_file = open(website_constants.metric_file_path, 'rb')
        wb = openpyxl.load_workbook(my_file)
        # copy first sheet from saved workbook
        first_sheet = wb.get_sheet_by_name(website_constants.metric_sheet_name)
        # create a target sheet where data will be copied
        target_sheet = workbook.create_sheet(index=0, title=website_constants.metric_sheet_name)
        # for each row, copy it to new sheet
        for row in first_sheet.iter_rows():
            target_row_list = [cell.value for cell in row]
            target_sheet.append(target_row_list)
        return ui_utils.handle_response(function, data=workbook, success=True)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def send_excel_file(file_name):
    """
    This sets the appropriate headers in the response for file of type xlsx.
    It also converts the file in binary before sending it.
    """
    function = send_excel_file.__name__
    try:

        if os.path.exists(file_name):
            excel = open(file_name, "rb")
            output = StringIO.StringIO(excel.read())
            out_content = output.getvalue()
            content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            # content_type = 'application/vnd.ms-excel'
            # in order to provide custom headers in response in angularjs, we need to set this header
            # first
            headers = { 
                'Access-Control-Expose-Headers': "file_name, Content-Disposition"
            }
            output.close()
            # remove the file from the disk
            os.remove(file_name)

            # set content_type and make Response() 
            response = Response(data=out_content, headers=headers, content_type=content_type)
            # attach some custom headers 
            response['Content-Disposition'] = 'attachment; filename=%s' % file_name
            response['file_name'] = file_name
            return response
        # return response

    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)

