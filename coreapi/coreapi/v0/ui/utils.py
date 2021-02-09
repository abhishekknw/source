'''

# helper file for ui views. all functions in this file should take a common format of  (request, data)
order of imports
 -native python imports
 -django specific imports
 -third party imports
 -file imports

'''
import json
import datetime
import random
import string
from collections import defaultdict

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.apps import apps
from django.forms.models import model_to_dict
from django.conf import settings
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware
from django.utils import timezone
from django.core.mail import EmailMessage
from django.db.models import Q

from smtplib import SMTPException
from rest_framework.response import Response
from rest_framework import status
from bulk_update.helper import bulk_update

import v0.errors as errors
import v0.constants as v0_constants
import v0.ui.serializers as ui_serializers
from v0.ui.location.models import State, City, CityArea, CitySubArea
from v0.ui.supplier.serializers import (SupplierHordingSerializer, SupplierEducationalInstituteSerializer, SupplierTypeSocietySerializer, SupplierTypeCorporateSerializer, SupplierTypeBusShelterSerializer,
                                        SupplierTypeGymSerializer, SupplierTypeRetailShopSerializer, SupplierTvChannelSerializer, SupplierRadioChannelSerializer,
                                        SupplierGantrySerializer, SupplierBusSerializer, SupplierCorporatesSerializer, SupplierHospitalSerializer,
                                        SupplierTypeSalonSerializer, BusDepotSerializer, SupplierMasterSerializer, AddressMasterSerializer)
from v0.ui.supplier.models import SupplierTypeSociety, SupplierMaster, AddressMaster
from v0.ui.finances.serializers import (IdeationDesignCostSerializer, DataSciencesCostSerializer, EventStaffingCostSerializer,
                                        LogisticOperationsCostSerializer, SpaceBookingCostSerializer, PrintingCostSerializer)
from v0.ui.proposal.serializers import ProposalMetricsSerializer, ProposalMasterCostSerializer
from v0.ui.proposal.models import (ImageMapping)
from v0.ui.inventory.models import (AdInventoryType, InventorySummary, FlyerInventory, StallInventory,
                                    GatewayArchInventory, PosterInventory)
from v0.ui.base.models import DurationType
from v0.ui.finances.models import PriceMappingDefault
from v0.ui.account.models import Profile
from pymodm import MongoModel, fields
from v0.ui.common.models import mongo_client
from v0.ui.b2b.models import Requirement

def handle_response(object_name, data=None, headers=None, content_type=None, exception_object=None, success=False, request=None):
    """
    Args:
        success: determines whether to send success or failure messages
        object_name: The function or class where the error occurs
        data: The user error which you want to display to user's on screens
        exception_object: The exception object caught. an instance of Exception, KeyError etc.
        headers: the dict of headers
        content_type: The content_type.
        request: The request param

        This method can later be used to log the errors.

    Returns: Response object

    """
    if not success:
        # prepare the object to be sent in error response
        data = {
            'general_error': data,
            'system_error': get_system_error(exception_object),
            'culprit_module': object_name,
        }
        if request:
            # fill the data with more information about request
            data['request_data'] = request.data
            data['request_url'] = request.build_absolute_uri()
            data['request_method'] = request.META.get('REQUEST_METHOD')
            data['django_settings_module'] = request.META.get('DJANGO_SETTINGS_MODULE')
            data['http_origin'] = request.META.get('HTTP_ORIGIN')
            data['virtual_env'] = request.META.get('VIRTUAL_ENV')
            data['server_port'] = request.META.get('SERVER_PORT')
            data['user'] = request.user.username if request.user else None

        if isinstance(exception_object, PermissionDenied):
            return Response({'status': False, 'data': data}, headers=headers, content_type=content_type, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'status': False, 'data': data}, headers=headers, content_type=content_type, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'status': True, 'data': data}, headers=headers, content_type=content_type,  status=status.HTTP_200_OK)


def get_system_error(exception_object):
    """
    Takes an exception object and returns system error.
    Args:
        exception_object:

    Returns: system error

    """
    if not exception_object:
        return []
    return str(exception_object.args) if exception_object.args else str(
        exception_object) if exception_object else ""


def save_basic_supplier_details(supplier_type_code, data):
    '''
    Args:
        supplier_type_code: identifies a new supplier whose basic details we need to save
        data: The actual data that's gonna be saved. a request.data object
    Returns: Success or failure depending upon wether data was saved or not
    '''
    function_name = save_basic_supplier_details.__name__
    try:
        if 'supplier_id' in data:

            if not supplier_type_code:
                return handle_response(function_name, data='No supplier_type_code provided')

            # get the model based on supplier_type_code
            model = get_model(supplier_type_code)
            if not model:
                return handle_response(function_name, data='Model not found')

            # get the serializer based on supplier_type_code
            serializer_class = get_serializer(supplier_type_code)
            if not serializer_class:
                return handle_response(function_name, data='Serializer not found')

            # get or create the model instance based on pk
            supplier, is_created = model.objects.get_or_create(supplier_id=data['supplier_id'])

            # update the instance
            serializer = serializer_class(supplier, data=data)
            if serializer.is_valid():
                serializer.save()
                return handle_response(function_name, data=serializer.data, success=True)
            else:
                return handle_response(function_name, data=serializer.errors)
        else:
            return handle_response(function_name, data='No supplier_id in request.data')

    except Exception as e:
        return handle_response(function_name, exception_object=e)


def generate_random_string(stringLength=5):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength)).upper()


def get_supplier_id(data):
    """
    :param request: request parameter
    :param data: dict containing valid keys . Note the keys should be 'city', 'area', sub_area', 'supplier_type' ,
    'supplier_code' for this to work

    :return:  Response in which data has a key 'supplier_id' containing supplier_id
    """
    function = get_supplier_id.__name__

    error = 'You might want to double check the state name {0} and state code {1} defined in ui constants'.format(v0_constants.state_name, v0_constants.state_code)
    try:
        try:
            # state_object = State.objects.get(state_name=state_name, state_code=state_code)
            city_object = City.objects.get(city_code=data.get('city_code'))
            area_object = CityArea.objects.get(area_code=data.get('area_code'), city_code=city_object)
            subarea_object = CitySubArea.objects.get(subarea_code=data.get('subarea_code'))

        except ObjectDoesNotExist as e:

            city_object = City.objects.get(id=data['city_id'])
            area_object = CityArea.objects.get(id=data['area_id'])
            subarea_object = CitySubArea.objects.get(id=data['subarea_id'])

        supplier_id = city_object.city_code + area_object.area_code + subarea_object.subarea_code + data[
            'supplier_type'] + data['supplier_code']
        supplier_id = generate_random_string(len(supplier_id))
        # Check supplier id in suppliers
        supplier_society = SupplierTypeSociety.objects.filter(pk=supplier_id)
        supplier_master = SupplierMaster.objects.filter(pk=supplier_id)
        if supplier_society or supplier_master:
            supplier_id = generate_random_string(len(supplier_id))
        return supplier_id.strip()

    except KeyError as e:
        raise Exception(function, get_system_error(e))
    except ObjectDoesNotExist as e:
        raise Exception(function, get_system_error(e))
    except Exception as e:
        raise Exception(function, get_system_error(e))

    
def make_supplier_data(data):
    function = make_supplier_data.__name__
    try:
        current_user = data['current_user']
        try:
            state_name = v0_constants.state_name
            state_code = v0_constants.state_code
            state_object = State.objects.get(state_name=state_name, state_code=state_code)
            city = City.objects.get(city_code=data.get('city_code'), state_code=state_object)
            area = CityArea.objects.get(area_code=data.get('area_code'), city_code=city)
            subarea = CitySubArea.objects.get(subarea_code=data.get('subarea_code'))
        except ObjectDoesNotExist as e:
            city = City.objects.get(id=data['city_id'])
            area = CityArea.objects.get(id=data['area_id'])
            subarea = CitySubArea.objects.get(id=data['subarea_id'])

        all_supplier_data = defaultdict(dict)

        for code in v0_constants.valid_supplier_codes:

            if code == v0_constants.society_code:

                all_supplier_data[code] = {

                    'data': {
                         'supplier_code': data['supplier_code'],
                         'society_name': data['supplier_name'],
                         'supplier_id': data['supplier_id'],
                         'created_by': current_user.id,
                         'society_city': city.city_name,
                         'society_subarea': subarea.subarea_name,
                         'society_locality': area.label,
                         'society_state': city.state_code.state_name,
                         'society_location_type': subarea.locality_rating,
                         "landmark": data.get("landmark"),
                         "society_latitude": data.get("latitude"),
                         "society_longitude": data.get("longitude"),
                         "society_zip": data.get("zipcode"),
                         "society_address1": data.get("address1"),
                         "flat_count": data.get("unit_primary_count"),
                         "tower_count": data.get("unit_secondary_count")
                    },

                    'serializer': get_serializer(code)
                }
            else:

                all_supplier_data[code] = {
                    'data': {
                        'supplier_id': data['supplier_id'],
                        'name': data['supplier_name'],
                        'city': city.city_name,
                        'area': area.label,
                        'subarea': subarea.subarea_name,
                        'state': city.state_code.state_name,
                        "landmark": data.get("landmark"),
                        "latitude": data.get("latitude"),
                        "longitude": data.get("longitude"),
                        "zipcode": data.get("zipcode"),
                        "address1": data.get("address1"),
                        "unit_primary_count": data.get("unit_primary_count"),
                        "unit_secondary_count": data.get("unit_secondary_count")
                    },
                    'serializer': get_serializer(code),
                }

        all_supplier_data['supplier_type_code'] = data['supplier_type_code']

        return Response(data={"status": True, "data": all_supplier_data}, status=status.HTTP_200_OK)
    except KeyError as e:
        return handle_response(function, exception_object=e)
    except ObjectDoesNotExist as e:
        return handle_response(function, exception_object=e)
    except Exception as e:
        return handle_response(function, exception_object=e)


def save_supplier_data(user, master_data):
    """
    saves basic data for single supplier
    Args:
        user:  The user instance
        master_data: the data to be saved

    Returns: saved supplier instance
    """
    function_name = save_supplier_data.__name__
    try:
        supplier_code = master_data['supplier_type_code']
        serializer_class = get_serializer(supplier_code)
        supplier_data = master_data[supplier_code]['data']
        serializer = serializer_class(data=supplier_data)
        if serializer.is_valid():
            serializer.save(user=user)
            if supplier_code == 'RS':
                set_default_pricing(serializer.data['supplier_id'], supplier_code)
            if supplier_code != v0_constants.society_code:
                supplier_id = supplier_data.get('supplier_id')
                area = supplier_data.get('area', None)
                subarea = supplier_data.get('subarea', None)
                city = supplier_data.get('city', None)
                state = supplier_data.get('state', None)
                landmark = supplier_data.get('landmark', None)
                longitude = supplier_data.get('longitude', 0.0)
                latitude = supplier_data.get('latitude', 0.0)
                zipcode = supplier_data.get('zipcode', 0)
                address1 = supplier_data.get('address1', "")
                unit_primary_count = supplier_data.get('unit_primary_count', 0)
                unit_secondary_count = supplier_data.get('unit_secondary_count', 0)
                supplier_master_data = {
                    "supplier_id": supplier_id,
                    "supplier_name": supplier_data.get('name', None),
                    "supplier_type": supplier_code,
                    "area": area,
                    "subarea": subarea,
                    "city": city,
                    "state": state,
                    "landmark": landmark,
                    "latitude": latitude,
                    "longitude": longitude,
                    "zipcode": zipcode,
                    "address1": address1,
                    "unit_primary_count": unit_primary_count,
                    "unit_secondary_count": unit_secondary_count,
                    "representative": user.profile.organisation.organisation_id
                }
                supplier_master_serializer = SupplierMasterSerializer(data=supplier_master_data)
                if supplier_master_serializer.is_valid():
                    supplier_master_serializer.save()

                address_master_data = {
                    "supplier": supplier_id,
                    "area": area,
                    "subarea": subarea,
                    "city": city,
                    "state": state,
                    "latitude": latitude,
                    "longitude": longitude,
                    "zipcode": zipcode,
                    "address1": address1
                }
                address_master_serializer = AddressMasterSerializer(data=address_master_data)
                if address_master_serializer.is_valid():
                    address_master_serializer.save()
            return serializer.data
        else:
            raise Exception(function_name, serializer.errors)
    except Exception as e:
       raise Exception(function_name, get_system_error(e))

def update_supplier_master(request_data):
    supplier_master_fields = {
        "supplier_id": "supplier_id",
        "supplier_name": "name", 
        "area": "area",
        "subarea": "subarea", 
        "city": "city", 
        "state": "state", 
        "landmark": "landmark",
        "latitude": "latitude",
        "longitude": "longitude", 
        "zipcode": "zipcode", 
        "address1": "address1", 
        "address2": "address2",
        "unit_primary_count": "unit_primary_count", 
        "unit_secondary_count": "unit_secondary_count",
        "unit_tertiary_count": "unit_tertiary_count",
        "feedback": "feedback", 
        "quality_rating": "quality_rating",
        "locality_rating": "locality_rating",
        "representative": "representative"
    }
    supplier_master_data = {}
    for key, value in supplier_master_fields.items():
        if request_data.get(value):
            supplier_master_data[key] = request_data[value]

    supplier_master = SupplierMaster.objects.filter(supplier_id=request_data["supplier_id"]).first()
    supplier_master_serializer = SupplierMasterSerializer(supplier_master, data=supplier_master_data)

    if supplier_master_serializer.is_valid():
        supplier_master_serializer.save()
        
    address_master_fields = {
        "supplier": "supplier_id",
        "area": "area",
        "subarea": "subarea",
        "city": "city",
        "state": "state",
        "latitude": "latitude",
        "longitude": "longitude",
        "zipcode": "zipcode",
        "address1": "address1",
        "address2": "address2",
        "nearest_landmark": "nearest_landmark"
    }

    address_master_data = {}
    for key, value in address_master_fields.items():
        if request_data.get(value):
            address_master_data[key] = request_data[value]

    address_master = AddressMaster.objects.filter(supplier_id=request_data["supplier_id"]).first()
    address_master_serializer = AddressMasterSerializer(address_master, data=address_master_data)
    if address_master_serializer.is_valid():
        address_master_serializer.save()

def set_default_pricing(supplier_id, supplier_type_code):
    """
    :param supplier_id: supplier uinique id
    :param supplier_type_code: which type of supplier
    :return:  makes an entry into PriceMappingDefault table for the given supplier

    """
    function = set_default_pricing.__name__
    try:
        supplier = get_model(supplier_type_code).objects.get(pk=supplier_id)
        # supplier = supplier_code_filter_params[supplier_type_code]['MODEL'].objects.get(pk=supplier_id)
        content_type = ContentType.objects.get_for_model(supplier)
        # SupplierTypeSociety.objects.get(pk=society_id)
        ad_types = AdInventoryType.objects.all()
        duration_types = DurationType.objects.all()

        price_mapping_list = []

        for type in ad_types:
            for duration in duration_types:
                if (supplier_type_code != 'RS'):
                    if (type.adinventory_name == 'POSTER'):
                        if ((duration.duration_name == 'Campaign Weekly') | (duration.duration_name == 'Campaign Monthly') | (duration.duration_name == 'Campaign Daily')):
                            if (type.adinventory_type == 'A4'):
                                pmdefault = PriceMappingDefault(object_id=supplier_id, content_type=content_type, adinventory_type=type, duration_type=duration)
                                price_mapping_list.append(pmdefault)

                    if (type.adinventory_name == 'POSTER LIFT'):
                        if ((duration.duration_name == 'Campaign Weekly') | (duration.duration_name == 'Campaign Monthly') | (duration.duration_name == 'Campaign Daily')):
                            if (type.adinventory_type == 'A4'):
                                pmdefault = PriceMappingDefault(object_id=supplier_id, content_type=content_type, adinventory_type=type, duration_type=duration)
                                price_mapping_list.append(pmdefault)

                    if (type.adinventory_name == 'STANDEE'):
                        if ((duration.duration_name == 'Campaign Weekly') | (duration.duration_name == 'Campaign Monthly') | (duration.duration_name == 'Campaign Daily')):
                            if (type.adinventory_type == 'Small'):
                                pmdefault = PriceMappingDefault(object_id=supplier_id, content_type=content_type, adinventory_type=type, duration_type=duration)
                                price_mapping_list.append(pmdefault)

                    if (type.adinventory_name == 'STALL'):
                        if ((duration.duration_name == 'Campaign Weekly') | (duration.duration_name == 'Campaign Monthly') | (duration.duration_name == 'Campaign Daily')):
                            if (type.adinventory_type == 'Canopy'):
                                pmdefault = PriceMappingDefault(object_id=supplier_id, content_type=content_type, adinventory_type=type, duration_type=duration)
                                price_mapping_list.append(pmdefault)

                    if (type.adinventory_name == 'CAR DISPLAY'):
                        if ((duration.duration_name == 'Campaign Weekly') | (duration.duration_name == 'Campaign Monthly') | (duration.duration_name == 'Campaign Daily')):
                            if ((type.adinventory_type == 'Standard') | (type.adinventory_type == 'Premium')):
                                pmdefault = PriceMappingDefault(object_id=supplier_id, content_type=content_type, adinventory_type=type, duration_type=duration)
                                price_mapping_list.append(pmdefault)

                    if ((type.adinventory_name == 'FLIER') and (duration.duration_name == 'Unit Daily')):
                        if ((type.adinventory_type == 'Door-to-Door') | (type.adinventory_type == 'Mailbox') | (type.adinventory_type == 'Lobby')):
                            pmdefault = PriceMappingDefault(object_id=supplier_id, content_type=content_type, adinventory_type=type, duration_type=duration)
                            price_mapping_list.append(pmdefault)

                else:
                    if (type.adinventory_name == 'POSTER'):
                        if ((duration.duration_name == 'Unit Daily')):
                            pmdefault = PriceMappingDefault(object_id=supplier_id, content_type=content_type,
                                                                  adinventory_type=type, duration_type=duration)
                            price_mapping_list.append(pmdefault)

                        if ((duration.duration_name == 'Campaign Weekly') | (duration.duration_name == 'Campaign Monthly') | (
                                    duration.duration_name == 'Unit Monthly') | (duration.duration_name == 'Unit Weekly')):
                            pmdefault = PriceMappingDefault(object_id=supplier_id, content_type=content_type,
                                                                    adinventory_type=type, duration_type=duration)
                            price_mapping_list.append(pmdefault)

                    if (type.adinventory_name == 'POSTER LIFT'):
                        if ((duration.duration_name == 'Unit Daily')):
                            pmdefault = PriceMappingDefault(object_id=supplier_id, content_type=content_type,
                                                                    adinventory_type=type, duration_type=duration)
                            price_mapping_list.append(pmdefault)
                        if ((duration.duration_name == 'Campaign Weekly') | (duration.duration_name == 'Campaign Monthly') | (
                                    duration.duration_name == 'Unit Monthly') | (duration.duration_name == 'Unit Weekly')):
                            pmdefault = PriceMappingDefault(object_id=supplier_id, content_type=content_type,
                                                                    adinventory_type=type, duration_type=duration)
                            price_mapping_list.append(pmdefault)

                    if (type.adinventory_name == 'STANDEE'):
                        if ((duration.duration_name == 'Campaign Monthly') | (duration.duration_name == 'Campaign Weekly') | (
                                    duration.duration_name == 'Unit Weekly') | (duration.duration_name == 'Unit Monthly')):
                            if (type.adinventory_type == 'Large'):
                                pmdefault = PriceMappingDefault(object_id=supplier_id, content_type=content_type,
                                                                        adinventory_type=type, duration_type=duration)
                                price_mapping_list.append(pmdefault)
                            else:
                                pmdefault = PriceMappingDefault(object_id=supplier_id, content_type=content_type,
                                                                        adinventory_type=type, duration_type=duration)
                                price_mapping_list.append(pmdefault)
                    if (type.adinventory_name == 'STALL'):
                        if ((duration.duration_name == 'Unit Daily') | (duration.duration_name == '2 Days')):
                            if ((type.adinventory_type == 'Canopy') | (type.adinventory_type == 'Small') | (
                                        type.adinventory_type == 'Large')):
                                pmdefault = PriceMappingDefault(object_id=supplier_id, content_type=content_type,
                                                                        adinventory_type=type, duration_type=duration)
                                price_mapping_list.append(pmdefault)
                            if (type.adinventory_type == 'Customize'):
                                pmdefault = PriceMappingDefault(object_id=supplier_id, content_type=content_type,
                                                                        adinventory_type=type, duration_type=duration)
                                price_mapping_list.append(pmdefault)
                    if (type.adinventory_name == 'CAR DISPLAY'):
                        if ((duration.duration_name == 'Unit Daily') | (duration.duration_name == '2 Days')):
                            if ((type.adinventory_type == 'Standard') | (type.adinventory_type == 'Premium')):
                                pmdefault = PriceMappingDefault(object_id=supplier_id, content_type=content_type,
                                                                        adinventory_type=type, duration_type=duration)
                                price_mapping_list.append(pmdefault)
                    if ((type.adinventory_name == 'FLIER') & (duration.duration_name == 'Unit Daily')):
                        if ((type.adinventory_type == 'Door-to-Door') | (type.adinventory_type == 'Mailbox') | (
                                    type.adinventory_type == 'Lobby')):
                            pmdefault = PriceMappingDefault(object_id=supplier_id, content_type=content_type,
                                                                    adinventory_type=type, duration_type=duration)
                            price_mapping_list.append(pmdefault)

        PriceMappingDefault.objects.bulk_create(price_mapping_list)
        return True
    except Exception as e:
        raise Exception(function, get_system_error(e))


def adinventory_func():
    """
    :return: functions makes a dict containing adinventory_dict
    """
    adinventory_objects = AdInventoryType.objects.all()
    adinventory_dict = {}
    for adinventory in adinventory_objects:
        if adinventory.adinventory_name == 'POSTER':
            if adinventory.adinventory_type == 'A4':
                adinventory_dict['poster_a4'] = adinventory
            elif adinventory.adinventory_type == 'A3':
                adinventory_dict['poster_a3'] = adinventory
        elif adinventory.adinventory_name == 'POSTER LIFT':
            if adinventory.adinventory_type == 'A4':
                adinventory_dict['poster_lift_a4'] = adinventory
            elif adinventory.adinventory_type == 'A3':
                adinventory_dict['poster_lift_a3'] = adinventory
        elif adinventory.adinventory_name == 'STANDEE':
            if adinventory.adinventory_type == 'Small':
                adinventory_dict['standee_small'] = adinventory
            elif adinventory.adinventory_type == 'Medium':
                adinventory_dict['standee_medium'] = adinventory
            elif adinventory.adinventory_type == 'Large':
                adinventory_dict['standee_large'] = adinventory
        elif adinventory.adinventory_name == 'STALL':
            if adinventory.adinventory_type == 'Canopy':
                adinventory_dict['stall_canopy'] = adinventory
            elif adinventory.adinventory_type == 'Small':
                adinventory_dict['stall_small'] = adinventory
            elif adinventory.adinventory_type == 'Large':
                adinventory_dict['stall_large'] = adinventory
            elif adinventory.adinventory_type == 'Customize':
                adinventory_dict['stall_customize'] = adinventory
        elif adinventory.adinventory_name == 'CAR DISPLAY':
            if adinventory.adinventory_type == 'Standard':
                adinventory_dict['car_display_standard'] = adinventory
            elif adinventory.adinventory_type == 'Premium':
                adinventory_dict['car_display_premium'] = adinventory
        elif adinventory.adinventory_name == 'FLIER':
            if adinventory.adinventory_type == 'Door-to-Door':
                adinventory_dict['flier_door_to_door'] = adinventory
            elif adinventory.adinventory_type == 'Mailbox':
                adinventory_dict['flier_mailbox'] = adinventory
            elif adinventory.adinventory_type == 'Lobby':
                adinventory_dict['flier_lobby'] = adinventory
        elif adinventory.adinventory_name == 'BANNER':
            if adinventory.adinventory_type == 'Small':
                adinventory_dict['banner_small'] = adinventory
            elif adinventory.adinventory_type == 'Medium':
                adinventory_dict['banner_medium'] = adinventory
            elif adinventory.adinventory_type == 'Large':
                adinventory_dict['banner_large'] = adinventory
        elif adinventory.adinventory_name == 'BANNER':
            if adinventory.adinventory_type == 'Small':
                adinventory_dict['banner_small'] = adinventory
            elif adinventory.adinventory_type == 'Medium':
                adinventory_dict['banner_medium'] = adinventory
            elif adinventory.adinventory_type == 'Large':
                adinventory_dict['banner_large'] = adinventory
        elif adinventory.adinventory_name == 'SUNBOARD':
            adinventory_dict['sun_board_allowed'] = adinventory
        elif adinventory.adinventory_name == 'HOARDING':
            adinventory_dict['hoarding'] = adinventory
        elif adinventory.adinventory_name == 'GANTRY':
            adinventory_dict['gantry'] = adinventory
        elif adinventory.adinventory_name == 'BUS SHELTER':
            adinventory_dict['bus_shelter'] = adinventory
        elif adinventory.adinventory_name == 'BUS BACK':
            adinventory_dict['bus_back'] = adinventory
        elif adinventory.adinventory_name == 'BUS RIGHT':
            adinventory_dict['bus_right'] = adinventory
        elif adinventory.adinventory_name == 'BUS LEFT':
            adinventory_dict['bus_left'] = adinventory
        elif adinventory.adinventory_name == 'BUS WRAP':
            adinventory_dict['bus_wrap'] = adinventory
        elif adinventory.adinventory_name == 'FLOOR':
            adinventory_dict['floor'] = adinventory
        elif adinventory.adinventory_name == 'CEILING':
            adinventory_dict['ceiling'] = adinventory
        elif adinventory.adinventory_name == 'BILLING':
            adinventory_dict['billing'] = adinventory
        elif adinventory.adinventory_name == 'COUNTER DISPLAY':
            adinventory_dict['counter_display'] = adinventory
        elif adinventory.adinventory_name == 'TENT CARD':
            adinventory_dict['tent_card'] = adinventory
        elif adinventory.adinventory_name == 'TABLE':
            adinventory_dict['table'] = adinventory
        elif adinventory.adinventory_name == 'WALL':
            adinventory_dict['wall'] = adinventory
        elif adinventory.adinventory_name == 'HOARDING LIT':
            adinventory_dict['hoarding_lit'] = adinventory
        elif adinventory.adinventory_name == 'BUS SHELTER LIT':
            adinventory_dict['bus_shelter_lit'] = adinventory
        elif adinventory.adinventory_name == 'GANTRY LIT':
            adinventory_dict['gantry_lit'] = adinventory
    return adinventory_dict


def get_supplier_inventory(data, id):
    """
    :param supplier_code: RA, CP, GYM, SA, id = pk of supplier table
    :return:  a dict containing correct inventory and supplier object depending upon the supplier id
    """

    try:
        supplier_code = data['supplier_type_code']
        if not supplier_code or not id:
            return Response(data={"status": False, "error": "provide supplier code and  supplier id"},
                            status=status.HTTP_400_BAD_REQUEST)
        # Get supplier from supplier master if it is not Society
        supplier_class = SupplierMaster
        if supplier_code == 'RS':
            supplier_class = SupplierTypeSociety
        try:
            supplier_object = supplier_class.objects.get(pk=id)
        except Exception as e:
            return Response(data={"status": False, "error": "Supplier id {id} does not exists for {supplier_type_code}".format(id=id,supplier_type_code=supplier_code)},
                            status=status.HTTP_400_BAD_REQUEST)

        content_type = ContentType.objects.get_for_model(supplier_class)
        inventory_object, is_created = InventorySummary.objects.get_or_create(object_id=id, content_type=content_type)
        data['object_id'] = id
        data['content_type'] = content_type.id

        return Response(
            data={"status": True, "data": {"inventory_object": inventory_object, "supplier_object": supplier_object, "request_data": data}},
            status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return Response(data={"status": False, "error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(data={"status": False, "error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)

#
# def get_inventory_object(request_data, id):
#     """
#     :param request_data: request param containing supplier_type_code
#     :param id: id of supplier
#     :return: correct inventory object for that supplier id
#     """
#     try:
#         data = request_data.data.copy()
#         # supplier_code = data['supplier_type_code']
#         supplier_code = 'RS'  # todo: change this when get clearity
#         if not supplier_code or not id:
#             return Response(data={"status": False, "error": "provide supplier code and  supplier id"},
#                             status=status.HTTP_400_BAD_REQUEST)
#         supplier_class = v0_constants.suppliers[supplier_code]
#         content_type = ContentType.objects.get_for_model(supplier_class)
#
#         inventory_object = InventorySummary.objects.get(object_id=id,
#                                                         content_type=content_type)
#
#         return Response(
#             data={"status": True, "data": {"inventory_object": inventory_object}},
#             status=status.HTTP_200_OK)
#     except ObjectDoesNotExist as e:
#         return Response(data={"status": False, "error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response(data={"status": False, "error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
#

def duration_type_func():
    duration_type_objects = DurationType.objects.all()
    duration_type_dict = {}

    for duration_type in duration_type_objects:
        if duration_type.duration_name == 'Campaign Weekly':
            duration_type_dict['campaign_weekly'] = duration_type
        elif duration_type.duration_name == 'Campaign Monthly':
            duration_type_dict['campaign_monthly'] = duration_type
        elif duration_type.duration_name == 'Campaign Daily':
            duration_type_dict['campaign_daily'] = duration_type
        elif duration_type.duration_name == 'Unit Weekly':
            duration_type_dict['unit_weekly'] = duration_type
        elif duration_type.duration_name == 'Unit Monthly':
            duration_type_dict['unit_monthly'] = duration_type
        elif duration_type.duration_name == 'Unit Daily':
            duration_type_dict['unit_daily'] = duration_type
        elif duration_type.duration_name == '2 Days':
            duration_type_dict['2_days'] = duration_type
        elif duration_type.duration_name == 'Unit Quaterly':
            duration_type_dict['unit_quaterly'] = duration_type

    return duration_type_dict


def save_stall_locations(c1, c2, supplier, supplier_type_code):
    try:

        count = int(c2) + 1
        for i in range(c1 + 1, count):
            stall_id = supplier.supplier_id + "CA0000ST" + str(i).zfill(2)
            data = {
                'adinventory_id': stall_id,
            }
            stall = StallInventory.objects.get_or_create_objects(data, supplier.supplier_id, supplier_type_code)
            stall.save()

    except Exception as e:
        return Response(data={'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


def save_flyer_locations(c1, c2, supplier, supplier_type_code):
    count = int(c2) + 1
    try:
        for i in range(c1 + 1, count+1):
            flyer_id = supplier.supplier_id + "0000FL" + str(i).zfill(2)
            data = {
                'adinventory_id': flyer_id,
            }
            flyer = FlyerInventory.objects.get_or_create_objects(data, supplier.supplier_id, supplier_type_code)
            flyer.flat_count = supplier.flat_count if supplier.flat_count else 0
            flyer.save()

    except Exception as e:
        return Response(data={'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


def delete(request, id, format=None):
    try:
        invId = request.query_params.get('invId', None)
        stall = StallInventory.objects.get(pk=invId)
        stall.delete()
        return Response(status=204)
    except StallInventory.DoesNotExist:
        return Response(status=404)

def make_dict_manager(adinvenory_type, duration_type):
    """
    :param adinvenory_type:
    :param duration_type:
    :return: dict containing these as keys
    """
    return {'adinventory_type' : adinvenory_type, 'duration_type': duration_type}


def save_price_data(price_object, posprice):
    """
    :param posprice, buisiness_price are data to be saved.
    :return: saves the PriceMappingDefault  object

    """
    try:
        if price_object:
            price_object.actual_supplier_price = posprice
            price_object.save()
    except Exception as e:
        raise Exception("Error occurred in saving PMD {0}".format(e.message))


def get_tower_count(supplier_object, supplier_type_code):
    """
    Args:
        supplier_type_code: RS, CP, GY

    Returns: tower count in case the supplier object has tower count attribute. which attribute of supplier object refers to a
    tower count is defined in constants.py. also the right supplier object is fetched from constants.py.
    """
    try:
        count = 1
        #supplier_object = v0_constants.suppliers[supplier_type_code]
        # supplier_object = get_model(supplier_type_code)
        attr = v0_constants.tower_count_attribute_mapping[supplier_type_code]
        if attr != 'none':
            count = getattr(supplier_object, attr)
        return Response(data={'status': True, 'data': count}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(data={'status': False, 'error': 'Error in fetching tower count'}, status=status.HTTP_400_BAD_REQUEST)


def get_content_type(code):
    """
    deprecated in favor of fetch_content_type.
    Args:
        code: supplier_type_code

    Returns: The right content type object for the given supplier_type_code

    """
    function = get_content_type.__name__
    try:
        if not code:
            return Response({'status': False, 'error': 'No supplier type code provided'}, status=status.HTTP_400_BAD_REQUEST)
        ContentType = apps.get_model('contenttypes', 'ContentType')
        load_model = get_model(code)
        content_type = ContentType.objects.get_for_model(load_model)
        return handle_response(function, data=content_type, success=True)
    except Exception as e:
        return handle_response(function, exception_object=e)


def fetch_content_type(code):
    """
    Use this instead of get_content_type. it does not return a Response. straight content type
    Args:
        code:

    Returns: Content type instance
    """
    function = fetch_content_type.__name__
    try:
        if not code:
            raise Exception('No code provided')
        ContentType = apps.get_model('contenttypes', 'ContentType')

        load_model = get_model(code)
        content_type = ContentType.objects.get_for_model(load_model)
        return content_type
    except Exception as e:
        raise Exception(function, get_system_error(e))


def get_content_types(codes):
    """
    Args:
        codes: a list of codes

    Returns: a list of content_types mapped against each code

    """
    function = get_content_types.__name__
    try:
        response = get_models(codes)
        if not response.data['status']:
            return response

        model_classes = response.data['data'].values()
        ContentType = apps.get_model('contenttypes', 'ContentType')
        content_types = ContentType.objects.get_for_models(*model_classes)
        final_content_types = {}
        for model_class, content_type in content_types.items():
            model_code = v0_constants.model_to_codes[model_class.__name__]
            final_content_types[model_code] = content_type
        return handle_response(function, data=final_content_types, success=True)
    except Exception as e:
        return handle_response(function, exception_object=e)


def get_models(codes):
    """
    Args:
        codes: a list of codes.

    Returns: a dict of codes against models.

    """
    function = get_models.__name__
    try:
        model_names = [v0_constants.codes_to_model_names[code] for code in codes]
        all_models = apps.get_models()
        model_classes = {}
        for model in all_models:
            if model.__name__ in model_names:
                code = v0_constants.model_to_codes[model.__name__]
                model_classes[code] = model
        return handle_response(function, data=model_classes, success=True)
    except Exception as e:
        return handle_response(function, exception_object=e)


def get_model(supplier_type_code):
    """
    Args:
        supplier_type_code: RS, CP

    Returns: loads the right model from supplier_type_code

    """
        
    function = get_model.__name__
    try:
        suppliers = v0_constants.codes_to_model_names
        load_model = apps.get_model('v0', suppliers[supplier_type_code])
        return load_model
    except Exception as e:
        raise Exception(function, get_system_error(e))


def get_serializer(query):
    """
    Args:
        query: CP, RS or table name in db

    Returns: right SerializerClass

    """
    function = get_serializer.__name__
    try:
        serializers = {

            v0_constants.hording_code: SupplierHordingSerializer,
            v0_constants.educational_institute_code: SupplierEducationalInstituteSerializer,
            v0_constants.society_code: SupplierTypeSocietySerializer,
            v0_constants.corporate_code: SupplierTypeCorporateSerializer,
            v0_constants.gym: SupplierTypeGymSerializer,
            v0_constants.salon: SupplierTypeSalonSerializer,
            v0_constants.bus_shelter: SupplierTypeBusShelterSerializer,
            v0_constants.retail_shop_code: SupplierTypeRetailShopSerializer,
            v0_constants.bus_depot_code: BusDepotSerializer,
            v0_constants.bus: SupplierBusSerializer,
            v0_constants.gantry: SupplierGantrySerializer,
            v0_constants.radio_channel: SupplierRadioChannelSerializer,
            v0_constants.tv_channel: SupplierTvChannelSerializer,
            v0_constants.corporates: SupplierCorporatesSerializer,
            v0_constants.hospital: SupplierHospitalSerializer,
            'ideation_design_cost': IdeationDesignCostSerializer,
            'logistic_operations_cost': LogisticOperationsCostSerializer,
            'space_booking_cost': SpaceBookingCostSerializer,
            'event_staffing_cost': EventStaffingCostSerializer,
            'data_sciences_cost': DataSciencesCostSerializer,
            'printing_cost': PrintingCostSerializer,
            'proposal_metrics': ProposalMetricsSerializer,
            'proposal_master_cost': ProposalMasterCostSerializer
        }
        return serializers[query]
    except Exception as e:
        raise Exception(function, get_system_error(e))


def get_supplier_image(supplier_objects, supplier_name):
    """
    Args:
        supplier_objects : SupplierTypeSociety, SupplierTypeCorporate
        supplier_type_code: CP, RS

    Returns: list of supplier_objects by appending image_url

    """
    function = get_supplier_image.__name__
    try:
        supplier_ids = [data['supplier_id'] for data in supplier_objects]
        images = ImageMapping.objects.filter(object_id__in=supplier_ids)
        image_dict = {instance.object_id: instance.image_url for instance in images}
        for data in supplier_objects:
            supplier_id = data['supplier_id']
            data['image_url'] = image_dict.get(supplier_id, '')
        return supplier_objects
    except Exception as e:
        raise Exception(function, get_system_error(e))


def generate_poster_objects(count, nb, society, society_content_type):

    function = generate_poster_objects.__name__
    try:
        nb_tag = nb['notice_board_tag']
        nb_tower = nb['tower_name']
        pos = int(count) + 1
        for i in range(1, pos):
            nb_id = society.supplier_id + nb_tag + "PO" + str(i).zfill(2)
            supplier_id = society.supplier_id
            nb = PosterInventory(adinventory_id=nb_id, poster_location=nb_tag, tower_name=nb_tower, supplier=society, object_id=supplier_id, content_type=society_content_type)
            nb.save()
        return handle_response(function, data='success', success=True)
    except Exception as e:
        return handle_response(function, exception_object=e)


def check_city_level_permission(user, supplier_type_code, city_code, permission_type):
    """
    checking city level permission on a given user
    Args:
        user: BaseUser instance
        supplier_type_code: RS, CP
        city_code: MUM
        permission_type: 'create', 'read', 'update' etc

    Returns: True or False depending on weather this user has this permission or not
    """
    function = check_city_level_permission.__name__
    custom_permission = ''
    try:

        if user.is_superuser:
            return True

        # make custom permission here. we will check for this permission for the user
        custom_permission = settings.APP_NAME + '.' + permission_type.lower() + '_' + city_code.lower() + '_' + supplier_type_code.lower()

        if user.has_perm(custom_permission):
            return True
        return False

    except Exception as e:
        raise Exception(e, custom_permission, function)


def get_region_based_query(user, region, supplier_type_code):
    """
    Returns a Q object specific for Forms. Q object contain region based query, currently only 'city' is supported.
    Checks all groups within the user, which start with 'Form' and check the region corresponding to that and form
    a Q based query and return.

    :param user:
    :param region: 'city', 'area' etc
    :param supplier_type_code: 'RS', 'CP' etc
    :return:
    """
    function = get_region_based_query.__name__
    try:
        authorized_region_codes = [group.split('-')[2] for group in user.groups.all().values_list('name', flat=True) if group.startswith("Form-" + region)]
        city_names = City.objects.filter(city_code__in=authorized_region_codes).values_list('city_name', flat=True)
        if supplier_type_code == 'RS':
            city_query = Q(society_city__in=city_names)
        else:
            city_query = Q(city__in=city_names)
        return city_query
    except Exception as e:
        raise Exception(function, get_system_error(e))


def validate_date_format(date_string, date_format):
    """
    Validates a raw string date against a given format
    Args:
        date_string:
        date_format:
    Returns: True or False depending weather the date_string matches the format or not.
    """
    try:
        datetime.datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        return False


def get_aware_datetime_from_string(date_string):
    """
    converts string to django's datetime
    Args:
        date_string: "2017-02-25"
    Returns: DateTimeField which can be put into Django's model DateTimeField
    """
    function = get_aware_datetime_from_string.__name__
    try:
        first_format = "%Y-%m-%d"
        second_format = "%Y-%m-%dT%H:%M:%SZ"
        if date_string:
            if validate_date_format(date_string, first_format):
                ret = timezone.make_aware(datetime.datetime.strptime(date_string, first_format), timezone.get_default_timezone())
            elif validate_date_format(date_string, second_format):
                ret = parse_datetime(date_string)
            else:
                raise ValueError(errors.INVALID_DATE_FORMAT.format(first_format, second_format))

            return ret
        return date_string
    except Exception as e:
        raise Exception(e, function)


def get_date_string_from_datetime(datetime_instance, required_format="%Y-%m-%d"):
    """

    Args:
        datetime_instance:
        required_format:

    Returns:
    """
    function = get_date_string_from_datetime.__name__
    try:
        return datetime_instance.strftime(required_format)

    except Exception as e:
        raise Exception(e, function)


def save_gateway_arch_location(supplier, supplier_type_code):
    """

    :param supplier:
    :param supplier_type_code:
    :return:
    """
    function = save_gateway_arch_location.__name__
    try:
        gateway_arch_id = supplier.supplier_id + "GA01"
        data = {
            'adinventory_id': gateway_arch_id,
        }
        gateway_arch = GatewayArchInventory.objects.get_or_create_objects(data, supplier.supplier_id, supplier_type_code)
        gateway_arch.save()
    except Exception as e:
        raise Exception(function, "Error " + get_system_error(e))

def check_payment_headers(headers):
    """

    :param headers:
    :return:
    """
    function = check_payment_headers.__name__
    try:
        for header in headers:
            if not v0_constants.society_payment_headers[header.value]:
                return False
        return True
    except Exception as e:
        raise Exception(function, "Error " + get_system_error(e))

def save_society_payment_details(data):
    """

    :param headers:
    :return:
    """
    function = check_payment_headers.__name__
    try:
        society_ids = [cell[1].value for cell in data]
        data_by_society_ids = {cell[1].value:cell for cell in data}
        society_objects = SupplierTypeSociety.objects.filter(supplier_id__in=society_ids)
        for society in society_objects:
            society.name_for_payment = data_by_society_ids[society.supplier_id][2].value
            society.ifsc_code = data_by_society_ids[society.supplier_id][3].value
            society.bank_name = data_by_society_ids[society.supplier_id][4].value
            society.account_no = data_by_society_ids[society.supplier_id][5].value
        bulk_update(society_objects)

        return True
    except Exception as e:
        raise Exception(function, "Error " + get_system_error(e))


def get_from_dict(dict, key):
    if key in dict:
        if dict[key]:
            return dict[key]
    else:
        return None


def calculate_percentage(numerator, denominator):
    numerator = float(numerator)
    denominator = float(denominator)
    if denominator > 0:
        return round(numerator/denominator*100, 3)
    else:
        return 0


def get_user_organisation_id(user):
    profile_id = user.profile_id
    profile = Profile.objects.filter(id=profile_id).all()
    if len(profile) == 0:
        return None
    return profile[0].organisation_id


def create_validation_msg(dict_of_required_attributes):
    is_valid = True
    validation_msg_dict = {'missing_data':[]}
    for key, value in dict_of_required_attributes.items():
        if value is None:
            is_valid = False
            validation_msg_dict['missing_data'].append(key)
    return (is_valid, validation_msg_dict)


def validate_attributes(attributes_dict):
    is_valid = True
    names = [x['name'] for x in attributes_dict if 'name' in x]
    types = [x['type'] for x in attributes_dict if 'type' in x]
    attribute_validation_dict = {'unknown_keys': [], 'unknown_types': []}
    all_keys = list(set([item for sublist in attributes_dict for item in sublist]))
    allowed_keys = ['name', 'type', 'is_required', 'options']
    allowed_types = ['INT', 'FLOAT', 'STRING', 'DATE', 'EMAIL', 'DROPDOWN', 'MULTISELECT']
    # if not (all_keys=={('type','name')} or all_keys=={('name','type')}):
    duplicate_names = list(set([x for x in names if names.count(x)>1]))
    if not duplicate_names == []:
        is_valid = False
        attribute_validation_dict['duplicate_names'] = duplicate_names
    for key in all_keys:
        if key not in allowed_keys:
            is_valid = False
            attribute_validation_dict['unknown_keys'].append(key)
    for curr_type in types:
        if curr_type not in allowed_types:
            is_valid = False
            attribute_validation_dict['unknown_types'].append(curr_type)
    return (is_valid, attribute_validation_dict)


# this is under testing
def is_user_permitted(permission_type, user, **kwargs):
    is_permitted = True
    validation_msg_dict = {'msg': None}
    leads_form_id = kwargs['leads_form_id'] if 'leads_form_id' in kwargs else None
    camaign_id = kwargs['campaign_id'] if 'campaign_id' in kwargs else None
    model_name = kwargs['model_name'] if 'model_name' in kwargs else None
    permission_list = list(getattr(model_name).objects.raw({'user_id': user.id}))
    if len(permission_list) == 0:
        is_permitted = True
        validation_msg_dict['msg'] = 'no_permission_document'
        return is_permitted, validation_msg_dict
    else:
        permission_obj = permission_list[0]
        leads_permissions = permission_obj.leads_permissions
        if permission_type not in leads_permissions:
            is_permitted = False
            validation_msg_dict['msg'] = 'not_permitted'
            return is_permitted, validation_msg_dict


# Generate random string
def getRandomString():
    return ''.join((random.choice(string.ascii_letters) for i in range(3)))


def campaignState(state):
    if state in v0_constants.campaign_state:
        return v0_constants.campaign_state[state]


def create_pricing_mapping_default(data, inventory_type, supplier_type_code, supplier_id, adinventory, duration_type):
    if get_from_dict(data, inventory_type):
        price = PriceMappingDefault.objects.create_price_mapping_object(
            make_dict_manager(adinventory,duration_type), supplier_id,
            supplier_type_code)
        save_price_data(price, 1)

        price = PriceMappingDefault.objects.create_price_mapping_object(
            make_dict_manager(adinventory,duration_type), supplier_id, supplier_type_code)
        save_price_data(price, 1)

def create_supplier_from_master(master_data, supplier_type_code):
    serializer_class = get_serializer(supplier_type_code)
    master_keys = v0_constants.supplier_master_diff_table[supplier_type_code]

    insert_data = {}
    for key, value in master_data.items():
        key1 = key

        if master_keys.get(key):
            key1 = master_keys[key]
        
        insert_data[key1] = value
        
    serializer = serializer_class(data=insert_data)
    if serializer.is_valid():
        serializer.save()

    return

def create_api_cache(slug, slugType, resData):
    if slug and resData:
        mongo_client.api_cache.insert({
            "slug": slug,
            "slugType": slugType,
            "resData": resData,
            "exp": datetime.datetime.now() + datetime.timedelta(days=1)
        })
    

def get_api_cache(slug):
    data = mongo_client.api_cache.find_one({"slug": slug})

    if data:
        if data["exp"] > datetime.datetime.now():
            return data["resData"]
        else:
            mongo_client.api_cache.remove({"slug": slug})
