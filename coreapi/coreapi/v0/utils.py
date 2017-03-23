from types import *
import random
import string

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

import geocoder

import v0.ui.utils as ui_utils
import v0.constants as v0_constants
import models as v0_models
import v0.ui.website.utils as website_utils
import v0.ui.website.constants as website_constants


def do_each_model(myModel, supplier_model, content_type):
    """
    :param myModel: Model whose fields need to be populated
    :param supplier_model: supplier type model
    :param content_type:  the content Type object
    :return: success in case of success, failure otherwise
    """
    function = do_each_model.__name__
    supplier_id = ''
    try:
        fields = myModel._meta.get_all_field_names() 
        field_name = None

        for field in fields:
            if field in ['supplier_id', 'society_id']:
                field_name = field
                break

        if not field_name:
            return ui_utils.handle_response(function, data='The model {0} does not have supplier_id field name'.format(myModel))        

        for row in myModel.objects.all():
            supplier_id = getattr(row, field_name)
            try:
                if supplier_id:
                    supplier_type = supplier_model.objects.get(supplier_id=row.supplier.supplier_id)   
                    row.content_type = content_type
                    row.object_id = row.supplier.supplier_id
                    row.content_object = supplier_type
                    row.save()
            except ObjectDoesNotExist as e:
                try:
                    q = {field_name: supplier_id}
                    myModel.objects.filter(**q).delete()
                    continue
                except Exception as e:
                    return ui_utils.handle_response(function, exception_object=e)
        return ui_utils.handle_response(function, data='success', success=True)
    except Exception as e:
        return ui_utils.handle_response(function, exception_object=e)


def get_group_permission(user, group_code_name):
    """
    Args:
        user: a User instance
        group_code_name: can be'master_users', 'ops_heads', 'bd_heads', 'external_bds'

    Returns: True or False depending weather user belongs to group indicated by group_code_name.

    """
    if not hasattr(user, 'user_code'):
        return False
    if user.user_code not in v0_constants.group_codes[group_code_name]:
        return False
    return True


def get_geo_code_instance(address):

    function = get_geo_code_instance.__name__
    try:
        assert type(address) is UnicodeType, " {0} is not string type".format(address)
        return geocoder.google(address)
    except Exception as e:
        raise Exception(function, ui_utils.get_system_error(e))


def generate_random_number(min_value, max_value):
    """

    Args:
        min_value:
        max_value:

    Returns:
    """
    function = generate_random_number.__name__
    try:
        return random.uniform(min_value, max_value)

    except Exception as e:
        raise Exception(function, ui_utils.get_system_error(e))


def generate_coordinates_in_quadrant(count, origin_lat, origin_long, radius,  quadrant_code=v0_constants.first_quadrant_code):
    """
    generates a list of coordinates in a given quadrant

    Args:
        count:
        origin_lat:
        origin_long:
        quadrant_code:
        radius:
    Returns:

    """
    function = generate_coordinates_in_quadrant.__name__
    try:
        assert type(radius) is FloatType, 'radius is not float type'
        assert type(origin_lat) is FloatType, 'latitude is not float type'
        assert type(origin_long) is FloatType, 'longitude is not float type'

        coordinates = []
        if quadrant_code == v0_constants.first_quadrant_code:
            for i in range(count):
                random_lat = origin_lat + random.uniform(0, radius)
                random_long = origin_long + random.uniform(0, radius)
                coordinates.append((random_lat, random_long))
        elif quadrant_code == v0_constants.second_quadrant_code:
            for i in range(count):
                random_lat = origin_lat - random.uniform(0, radius)
                random_long = origin_long + random.uniform(0, radius)
                coordinates.append((random_lat, random_long))
        elif quadrant_code == v0_constants.third_quadrant_code:
            for i in range(count):
                random_lat = origin_lat - random.uniform(0, radius)
                random_long = origin_long - random.uniform(0, radius)
                coordinates.append((random_lat, random_long))
        else:
            for i in range(count):
                random_lat = origin_lat + random.uniform(0, radius)
                random_long = origin_long - random.uniform(0, radius)
                coordinates.append((random_lat, random_long))

        return coordinates

    except Exception as e:
        raise Exception(function, ui_utils.get_system_error(e))


def assign_supplier_ids(state_code, city_code, supplier_type_code,  coordinates):
    """
    returns a dict containing a unique supplier_id for each of the coordinate in coordinates
    Args:
        state_code:
        city_code:
        supplier_type_code:
        coordinates:

    Returns:

    """
    function = assign_supplier_ids.__name__
    try:
        detail = {}
        for index, coordinate_tuple in enumerate(coordinates):
            lat, lng = coordinate_tuple
            supplier_id = state_code + city_code + supplier_type_code + website_utils.get_random_pattern(size=3, chars=string.ascii_uppercase) + '_' + str(index)
            detail[supplier_id] = {
                'latitude': lat,
                'longitude': lng
            }
        return detail
    except Exception as e:
        raise Exception(function, ui_utils.get_system_error(e))


def handle_society_detail(suppliers_dict, society_detail):
    """

    Args:
        suppliers_dict:
        society_detail:

    Returns:

    """
    function = handle_society_detail.__name__
    try:
        if society_detail.get('flat_detail'):
            supplier_ids = suppliers_dict.keys()
            total_societies = len(supplier_ids)
            total_flat_count = int(society_detail['total_flats'])
            assert total_flat_count >= total_societies, 'total flat count {0} must be greater than total number of societies {1}'.format(total_flat_count, total_societies)

            flat_type_dict = website_constants.flat_type_dict
            total_flat_types = len(flat_type_dict.keys())
            flats_per_society = total_flat_count/total_societies
            flats_of_one_type_per_society = flats_per_society/total_flat_types

    except Exception as e:
        raise Exception(function, ui_utils.get_system_error(e))

