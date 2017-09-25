import hashlib
import json
import random
import string
from uuid import uuid4
from types import *

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType

import geocoder
from bulk_update.helper import bulk_update

import models as v0_models
import v0.constants as v0_constants
import v0.ui.utils as ui_utils
import v0.ui.website.utils as website_utils


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

        coordinates_list = []
        delta_dict = website_utils.get_delta_latitude_longitude(radius, origin_lat)

        delta_latitude = delta_dict['delta_latitude']
        delta_longitude = delta_dict['delta_longitude']

        if quadrant_code == v0_constants.first_quadrant_code:
            for i in range(count):
                random_lat = origin_lat + random.uniform(0, delta_latitude)
                random_long = origin_long + random.uniform(0, delta_longitude)
                coordinates_list.append((random_lat, random_long))
        elif quadrant_code == v0_constants.second_quadrant_code:
            for i in range(count):
                random_lat = origin_lat - random.uniform(0, delta_latitude)
                random_long = origin_long + random.uniform(0, delta_longitude)
                coordinates_list.append((random_lat, random_long))
        elif quadrant_code == v0_constants.third_quadrant_code:
            for i in range(count):
                random_lat = origin_lat - random.uniform(0, delta_latitude)
                random_long = origin_long - random.uniform(0, delta_longitude)
                coordinates_list.append((random_lat, random_long))
        else:
            for i in range(count):
                random_lat = origin_lat + random.uniform(0, radius)
                random_long = origin_long - random.uniform(0, radius)
                coordinates_list.append((random_lat, random_long))

        return coordinates_list

    except Exception as e:
        raise Exception(function, ui_utils.get_system_error(e))


def assign_supplier_ids(city_code, supplier_type_code,  coordinates):
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
            supplier_id = city_code + supplier_type_code + website_utils.get_random_pattern(size=3, chars=string.ascii_uppercase) + '_' + str(index)
            detail[supplier_id] = {
                'latitude': lat,
                'longitude': lng
            }
        return detail
    except Exception as e:
        raise Exception(function, ui_utils.get_system_error(e))


def handle_society_flat_detail(flat_detail, suppliers_dict, content_type):
    """

    Returns:

    """
    function = handle_society_flat_detail.__name__
    try:
        supplier_ids = suppliers_dict.keys()
        flat_type_dict = v0_constants.flat_type_dict
        flat_instances = []
        for society_id in supplier_ids:
            total_flat_count = 0
            for flat_type_code, flat_type_value in flat_type_dict.iteritems():
                count_range = flat_detail['detail'][flat_type_code] if flat_detail.get(flat_type_code) else [0, v0_constants.flat_type_default_params[flat_type_code]['count']]
                size_range = flat_detail['detail'][flat_type_code] if flat_detail.get(flat_type_code) else [0, v0_constants.flat_type_default_params[flat_type_code]['size']]
                assert count_range[0] <= count_range[1], "Invalid Count Range"
                assert size_range[0] <= size_range[1], "Invalid Size Range"
                data = {
                    'flat_type': flat_type_value,
                    'object_id': society_id,
                    'content_type': content_type,
                    'flat_count': random.uniform(int(count_range[0]), int(count_range[1])),
                    'size_builtup_area': random.uniform(float(size_range[0]), float(size_range[1]))
                }
                total_flat_count += data['flat_count']
                flat_instances.append(v0_models.FlatType(**data))
            suppliers_dict[society_id]['flat_count'] = total_flat_count
        v0_models.FlatType.objects.all().delete()
        v0_models.FlatType.objects.bulk_create(flat_instances)
        return True
    except Exception as e:
        raise Exception(e, ui_utils.get_system_error(e))


def handle_tower_details(tower_detail, suppliers_dict, content_type):
    """
    Args:
        tower_detail:
        suppliers_dict:
        content_type:

    Returns: True if creates zero or more instances of Tower successfully. False otherwise.

    """
    function = handle_tower_details.__name__
    try:
        if not tower_detail or (not suppliers_dict) or (not content_type):
            return False
        tower_range = tower_detail['count'] if tower_detail.get('count') else [1, v0_constants.default_tower_range]
        assert tower_range[0] <= tower_range[1], "Invalid Tower Range"
        supplier_ids = suppliers_dict.keys()
        tower_instances = []
        for supplier_id, detail in suppliers_dict.iteritems():
            total_tower_count = random.randint(int(tower_range[0]), int(tower_range[1]))
            for tower_number in range(total_tower_count):
                data = {
                    'object_id': supplier_id,
                    'content_type': content_type,
                    'tower_name': v0_constants.default_tower_base_name + str(tower_number),
                }
                tower_instances.append(v0_models.SocietyTower(**data))
            suppliers_dict[supplier_id]['tower_count'] = total_tower_count
        v0_models.SocietyTower.objects.all().delete()
        v0_models.SocietyTower.objects.bulk_create(tower_instances)
        return True
    except Exception as e:
        raise Exception(function, ui_utils.get_system_error(e))


def handle_supplier_amenities(amenities, suppliers_dict, content_type):
    """
    Assigns Amenities to suppliers.
    Args:
        amenities:
        suppliers_dict:
        content_type:

    Returns:

    """
    function = handle_supplier_amenities.__name__
    try:
        if not amenities or (not suppliers_dict) or (not content_type):
            return False
        supplier_ids = suppliers_dict.keys()
        v0_models.SupplierAmenitiesMap.objects.all().delete()
        amenities = v0_models.Amenity.objects.filter(code__in=amenities)
        if not amenities:
            return False
        amenities_map = {amenity.code: amenity for amenity in amenities}
        supplier_amenity_objects = []
        # assign a random count of amenity to each supplier
        for supplier_id in supplier_ids:
            amenity_count = random.randint(1, len(amenities))
            for index in range(amenity_count):
                data = {
                    'content_type': content_type,
                    'object_id': supplier_id,
                    'amenity': amenities_map[amenities[random.randint(0, len(amenities)-1)]]
                }
                supplier_amenity_objects.append(v0_models.SupplierAmenitiesMap(**data))
        v0_models.SupplierAmenitiesMap.objects.all().delete()
        v0_models.SupplierAmenitiesMap.objects.bulk_create(supplier_amenity_objects)
        return True
    except Exception as e:
        raise Exception(function, ui_utils.get_system_error(e))


def make_inventory_id(inventory_code, supplier_type_code):
    """
    returns a unique inventory id
    Args:
        inventory_code:
        supplier_type_code:

    Returns:
    """
    function = make_inventory_id.__name__
    try:
        return inventory_code + supplier_type_code + str(uuid4())[-7:]

    except Exception as e:
        raise Exception(function, ui_utils.get_system_error(e))


def handle_supplier_inventory_detail(inventory_detail, supplier_ids, content_type):
    """
    handles inventory detail
    must be called after societies and towers are filled up
    Args:
        inventory_detail:
        supplier_ids:
        content_type:

    Returns:
    """
    function = handle_supplier_inventory_detail.__name__
    try:
        if not inventory_detail or (not supplier_ids) or (not content_type):
            return False
        inventories_allowed = inventory_detail['inventories_allowed']
        society_instances_map = v0_models.SupplierTypeSociety.objects.in_bulk(supplier_ids)
        tower_instances = v0_models.SocietyTower.objects.filter(object_id__in=supplier_ids, content_type=content_type)
        tower_instances_map = {}
        # each society will have list of towers
        for tower_instance in tower_instances:
            if not tower_instances_map.get(tower_instance.object_id):
                tower_instances_map[tower_instance.object_id] = []
            tower_instances_map[tower_instance.object_id].append(tower_instance)

        inv_summary_objects = []
        poster_objects = []  # depends on towers
        standee_objects = []  # depends on towers
        stall_objects = []  # independent of towers
        flier_objects = []  # independent of towers

        for supplier_id in supplier_ids:
            inv_summary_data = {
                'object_id': supplier_id,
                'content_type': content_type
            }
            for inv_code in inventories_allowed:
                inv_summary_data[v0_constants.inventory_dict[inv_code]]= True
                tower_count = society_instances_map[supplier_id].tower_count

                for index in range(tower_count):  # handle inventories which directly depend on towers
                    if inv_code == v0_constants.inventory_name_to_code['poster']:
                        for poster_index in range(v0_constants.default_poster_per_tower):
                            data = {
                                'adinventory_id': make_inventory_id(inv_code, v0_constants.society),
                                'tower': tower_instances_map[supplier_id][index],
                                'content_type': content_type,
                                'object_id': supplier_id
                            }
                            poster_objects.append(v0_models.PosterInventory(**data))
                    elif inv_code == v0_constants.inventory_name_to_code['standee']:
                        for standee_index in range(v0_constants.default_standee_per_tower):
                            data = {
                                'adinventory_id': make_inventory_id(inv_code, v0_constants.society),
                                'tower': tower_instances_map[supplier_id][index],
                                'content_type': content_type,
                                'object_id': supplier_id
                            }
                            standee_objects.append(v0_models.StandeeInventory(**data))

                # handle inventories which do not depend on towers
                if inv_code == v0_constants.inventory_name_to_code['stall']:
                    for stall_index in range(v0_constants.default_stall_per_society):
                        data = {
                            'adinventory_id': make_inventory_id(inv_code, v0_constants.society),
                            'content_type': content_type,
                            'object_id': supplier_id
                        }
                        stall_objects.append(v0_models.StallInventory(**data))

                elif inv_code == v0_constants.inventory_name_to_code['flier']:
                    for flier_frequency in range(v0_constants.default_flier_frequency_per_society):
                        data = {
                            'adinventory_id': make_inventory_id(inv_code, v0_constants.society),
                            'content_type': content_type,
                            'object_id': supplier_id
                        }
                        flier_objects.append(v0_models.FlyerInventory(**data))
                    inv_summary_data['flier_frequency'] = v0_constants.default_flier_frequency_per_society

            inv_summary_objects.append(v0_models.InventorySummary(**inv_summary_data))

        v0_models.InventorySummary.objects.all().delete()
        v0_models.InventorySummary.objects.bulk_create(inv_summary_objects)

        v0_models.PosterInventory.objects.all().delete()
        v0_models.FlyerInventory.objects.all().delete()
        v0_models.StallInventory.objects.all().delete()
        v0_models.StandeeInventory.objects.all().delete()

        v0_models.PosterInventory.objects.bulk_create(poster_objects)
        v0_models.StandeeInventory.objects.bulk_create(standee_objects)
        v0_models.StallInventory.objects.bulk_create(stall_objects)
        v0_models.FlyerInventory.objects.bulk_create(flier_objects)

        return True
    except Exception as e:
        raise Exception(function, ui_utils.get_system_error(e))


def handle_society_detail(suppliers_dict, society_detail):
    """

    Args:
        suppliers_dict: supplier_id --> supplier_detail mapping
        society_detail: The dict holding society_detail information such as Flat detail, Inventories information etc

    Returns: True on success. True meaning flat details were added and societies being updated.

    """
    function = handle_society_detail.__name__
    try:
        if not suppliers_dict or (not society_detail):
            return False

        supplier_ids = suppliers_dict.keys()
        societies = v0_models.SupplierTypeSociety.objects.filter(supplier_id__in=supplier_ids)
        response = ui_utils.get_content_type(v0_constants.society)
        if not response.data['status']:
            return response
        content_type = response.data['data']

        if society_detail.get('flat_detail'):
            flat_detail = society_detail['flat_detail']
            handle_society_flat_detail(flat_detail, suppliers_dict, content_type)
            #  set the remaining params if present
            for society in societies:
                society.flat_count = suppliers_dict[society.supplier_id].get('flat_count')

        if society_detail.get('tower_detail'):
            tower_detail = society_detail['tower_detail']
            handle_tower_details(tower_detail, suppliers_dict, content_type)
            #  set the remaining params if present
            for society in societies:
                society.tower_count = suppliers_dict[society.supplier_id].get('tower_count')

        if society_detail.get('amenities'):
            amenities = society_detail['amenities']
            handle_supplier_amenities(amenities, suppliers_dict, content_type)

        if society_detail.get('direct_society_details'):

            direct_society_detail_key = 'direct_society_details'
            society_type_list = society_detail[direct_society_detail_key]['society_type'] if society_detail[direct_society_detail_key].get('society_type') else v0_constants.quality_dict.keys()
            society_location_type_list = society_detail[direct_society_detail_key]['society_location'] if society_detail[direct_society_detail_key].get('society_location') else v0_constants.locality_dict.keys()
            society_size_list = society_detail[direct_society_detail_key]['society_size'] if society_detail[direct_society_detail_key].get('society_size') else v0_constants.quantity_dict.keys()
            possession_year_range = society_detail[direct_society_detail_key]['possession_year'] if society_detail[direct_society_detail_key].get('possession_year') else v0_constants.default_possession_year_range
            flat_avg_rental_persqft_range = society_detail[direct_society_detail_key]['flat_avg_rental_persqft'] if society_detail[direct_society_detail_key].get('flat_avg_rental_persqft') else v0_constants.default_flat_avg_rental_persqft_range
            flat_sale_cost_persqft_range = society_detail[direct_society_detail_key]['flat_sale_cost_persqft'] if society_detail[direct_society_detail_key].get('flat_sale_cost_persqft') else v0_constants.default_flat_sale_cost_persqft_range
            percentage_range_of_tenants_to_flat = society_detail['direct_society_details']['percentage_range_of_tenants_to_flat'] if society_detail[direct_society_detail_key].get('percentage_range_of_tenants_to_flat') else v0_constants.default_percentage_range_of_tenants_to_flat

            assert percentage_range_of_tenants_to_flat[0] <= percentage_range_of_tenants_to_flat[1], "First Value must be less than Second Value."
            assert possession_year_range[0] <= possession_year_range[1], "Invalid Possession Year Range"
            assert flat_avg_rental_persqft_range[0] <= flat_avg_rental_persqft_range[1], "Flat Average rental Invalid Range"
            assert flat_sale_cost_persqft_range[0] <= flat_sale_cost_persqft_range[1], "Flat Average Sale Cost Invalid Range"

            for society in societies:
                society.society_type_quality = v0_constants.quality_dict[society_type_list[random.randint(0, len(society_type_list)-1)]]
                society.society_location_type = v0_constants.locality_dict[society_location_type_list[random.randint(0, len(society_location_type_list)-1)]]
                society.society_type_quantity = v0_constants.quantity_dict[society_size_list[random.randint(0, len(society_size_list)-1)]]
                society.age_of_society = random.randint(possession_year_range[0], possession_year_range[1])
                society.total_tenant_flat_count = int((random.uniform(percentage_range_of_tenants_to_flat[0], percentage_range_of_tenants_to_flat[1]) * society.flat_count)/100)
                society.flat_avg_rental_persqft = random.randint(flat_avg_rental_persqft_range[0], flat_avg_rental_persqft_range[1])
                society.flat_sale_cost_persqft = random.randint(flat_sale_cost_persqft_range[0], flat_sale_cost_persqft_range[1])

        bulk_update(societies)
        return True
    except Exception as e:
        raise Exception(function, ui_utils.get_system_error(e))


def handle_inventory_pricing(supplier_ids, content_type, price_dict):
    """
    sets pricing for each inventory type
    Args:
        supplier_ids:
        content_type:
        price_dict:  A dict of prices of all inventory kinds
    Returns:
    """
    function = handle_inventory_pricing.__name__
    try:
        inventory_summary_instances = v0_models.InventorySummary.objects.filter(object_id__in=supplier_ids, content_type=content_type)
        inventory_summary_instance_map = {instance.object_id: instance for instance in inventory_summary_instances}

        price_mapping_instances_list = []
        for supplier_id in supplier_ids:
            inventory_summary_instance = inventory_summary_instance_map[supplier_id]
            if inventory_summary_instance.poster_allowed_nb:
                price_mapping_instances_list.extend(create_price_mapping_instances(supplier_id, content_type, v0_constants.poster,   price_dict))

            if inventory_summary_instance.standee_allowed:
                price_mapping_instances_list.extend(create_price_mapping_instances(supplier_id, content_type, v0_constants.standee,  price_dict))

            if inventory_summary_instance.stall_allowed:
                price_mapping_instances_list.extend(create_price_mapping_instances(supplier_id, content_type, v0_constants.stall,  price_dict))

            if inventory_summary_instance.flier_allowed:
                price_mapping_instances_list.extend(create_price_mapping_instances(supplier_id, content_type, v0_constants.flier,  price_dict))
        v0_models.PriceMappingDefault.objects.all().delete()
        v0_models.PriceMappingDefault.objects.bulk_create(price_mapping_instances_list)
        return True
    except Exception as e:
        raise Exception(function, ui_utils.get_system_error(e))


def create_price_mapping_instances(supplier_id, content_type,  inventory_name, price_dict):
    """
    sets supplier price for the incoming inventory
    Args:
        supplier_id:
        inventory_name:
        price_dict:
        content_type

    Returns:

    """
    function = create_price_mapping_instances.__name__
    try:
        ad_inventory_instances = v0_models.AdInventoryType.objects.filter(adinventory_name=inventory_name)
        duration_type_instances = v0_models.DurationType.objects.all()
        pmd_instances = []
        for ad_inventory_instance in ad_inventory_instances:
            for duration_type_instance in duration_type_instances:
                data = {
                    'adinventory_type': ad_inventory_instance,
                    'duration_type': duration_type_instance,
                    'actual_supplier_price': random.randint(price_dict[inventory_name][0], price_dict[inventory_name][1]),
                    'suggested_supplier_price': 0,
                    'object_id': supplier_id,
                    'content_type': content_type
                }
                pmd_instances.append(v0_models.PriceMappingDefault(**data))
        return pmd_instances
    except Exception as e:
        raise Exception(function, ui_utils.get_system_error(e))


def create_cache_key(module_name, *args):
    """
    creates a cache key. each cache key is prefixed by module_name.
    Args:
        module_name: name of function or module name
        *args: list of arguments

    Returns: returns the cache key

    """
    function = create_cache_key.__name__
    try:
        final_string = ''
        for item in args:
            try:
                final_string += json.dumps(item)
            except TypeError:
                final_string += str(item)
        return module_name + '_' + hashlib.sha1(final_string).hexdigest()
    except Exception as e:
        raise Exception(e, function)


def check_object_permission(user, model, permission):
    """
    checks weather a a given 'user' has 'permission' on  a given 'model'
    returns True if user has a permission, false otherwise

    :param user: instance of BaseUser model
    :param model:  model itself
    :param permission: 'create', 'view', etc. Fields of ObjectLevelPermission model
    :return:
    """
    function = check_object_permission.__name__
    try:
        error = ''
        if not user.profile:
            raise Exception('Every User must have associated profile')
        content_type = ContentType.objects.get_for_model(model)
        instance = v0_models.ObjectLevelPermission.objects.get(profile=user.profile, content_type=content_type)
        if instance.__dict__[permission]:
            return True, error
        error = 'This user does not have permission of ' + permission + ' on this model ' + model.__class__.__name__
        return False, error
    except Exception as e:
        raise Exception(e, function)
