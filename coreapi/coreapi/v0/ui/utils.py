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

import v0.models
import v0.serializers
import v0.models as models
import v0.errors as errors
import v0.constants as v0_constants
import v0.ui.serializers as ui_serializers


def handle_response(object_name, data=None, headers=None, content_type=None, exception_object=None, success=False, request=None):
    """
    Args:
        success: determines wether to send success or failure messages
        object_name: The function or class where the error occurrs
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

        # if the code is deployed on test server, send the mail to developer if any API fails with stack trace.
        if settings.TEST_DEPLOYED:
            try:
                subject = 'Error occurred in an api {0}'.format(request.build_absolute_uri())
                body = data
                to = v0_constants.api_error_mail_to
                email_data = {
                    'subject': subject,
                    'body': json.dumps(body, indent=4, sort_keys=True),
                    'to': (to,)
                }
                send_email(email_data)
            except Exception as e:
                # email sending failed. let it go.
                pass

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
    return str(exception_object.message) if exception_object.message else str(exception_object.args) if exception_object.args else ""


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


def get_supplier_id(request, data, state_name=v0_constants.state_name, state_code=v0_constants.state_code):
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
            state_object = v0.models.State.objects.get(state_name=state_name, state_code=state_code)
            city_object = v0.models.City.objects.get(city_code=data.get('city_code'), state_code=state_object)
            area_object = v0.models.CityArea.objects.get(area_code=data.get('area_code'), city_code=city_object)
            subarea_object = v0.models.CitySubArea.objects.get(subarea_code=data.get('subarea_code'), area_code=area_object)

        except ObjectDoesNotExist as e:
            city_object = v0.models.City.objects.get(id=data['city_id'])
            area_object = v0.models.CityArea.objects.get(id=data['area_id'])
            subarea_object = v0.models.CitySubArea.objects.get(id=data['subarea_id'],
                                                     area_code=area_object)

        supplier_id = city_object.city_code + area_object.area_code + subarea_object.subarea_code + data[
            'supplier_type'] + data[
                          'supplier_code']
        return supplier_id

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
            state_object = v0.models.State.objects.get(state_name=state_name, state_code=state_code)
            city = v0.models.City.objects.get(city_code=data.get('city_code'), state_code=state_object)
            area = v0.models.CityArea.objects.get(area_code=data.get('area_code'), city_code=city)
            subarea = v0.models.CitySubArea.objects.get(subarea_code=data.get('subarea_code'), area_code=area)
        except ObjectDoesNotExist as e:
            city = v0.models.City.objects.get(id=data['city_id'])
            area = v0.models.CityArea.objects.get(id=data['area_id'])
            subarea = v0.models.CitySubArea.objects.get(id=data['subarea_id'], area_code=area)

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
                             'society_location_type': subarea.locality_rating
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
                        'state': city.state_code.state_name
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
            set_default_pricing(serializer.data['supplier_id'], supplier_code)
            return serializer.data
        else:
            raise Exception(function_name, serializer.errors)
    except Exception as e:
        raise Exception(function_name, get_system_error(e))


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
        ad_types = v0.models.AdInventoryType.objects.all()
        duration_types = v0.models.DurationType.objects.all()

        price_mapping_list = []

        for type in ad_types:
            for duration in duration_types:
                if (type.adinventory_name == 'POSTER'):
                    if ((duration.duration_name == 'Unit Daily')):
                        pmdefault = v0.models.PriceMappingDefault(object_id=supplier_id, content_type=content_type,
                                                                  adinventory_type=type, duration_type=duration)
                        price_mapping_list.append(pmdefault)
                    if ((duration.duration_name == 'Campaign Weekly') | (duration.duration_name == 'Campaign Monthly') | (
                                duration.duration_name == 'Unit Monthly') | (duration.duration_name == 'Unit Weekly')):
                        pmdefault = v0.models.PriceMappingDefault(object_id=supplier_id, content_type=content_type,
                                                                  adinventory_type=type, duration_type=duration)
                        price_mapping_list.append(pmdefault)

                if (type.adinventory_name == 'POSTER LIFT'):
                    if ((duration.duration_name == 'Unit Daily')):
                        pmdefault = v0.models.PriceMappingDefault(object_id=supplier_id, content_type=content_type,
                                                                  adinventory_type=type, duration_type=duration)
                        price_mapping_list.append(pmdefault)
                    if ((duration.duration_name == 'Campaign Weekly') | (duration.duration_name == 'Campaign Monthly') | (
                                duration.duration_name == 'Unit Monthly') | (duration.duration_name == 'Unit Weekly')):
                        pmdefault = v0.models.PriceMappingDefault(object_id=supplier_id, content_type=content_type,
                                                                  adinventory_type=type, duration_type=duration)
                        price_mapping_list.append(pmdefault)

                if (type.adinventory_name == 'STANDEE'):
                    if ((duration.duration_name == 'Campaign Monthly') | (duration.duration_name == 'Campaign Weekly') | (
                                duration.duration_name == 'Unit Weekly') | (duration.duration_name == 'Unit Monthly')):
                        if (type.adinventory_type == 'Large'):
                            pmdefault = v0.models.PriceMappingDefault(object_id=supplier_id, content_type=content_type,
                                                                      adinventory_type=type, duration_type=duration)
                            price_mapping_list.append(pmdefault)
                        else:
                            pmdefault = v0.models.PriceMappingDefault(object_id=supplier_id, content_type=content_type,
                                                                      adinventory_type=type, duration_type=duration)
                            price_mapping_list.append(pmdefault)
                if (type.adinventory_name == 'STALL'):
                    if ((duration.duration_name == 'Unit Daily') | (duration.duration_name == '2 Days')):
                        if ((type.adinventory_type == 'Canopy') | (type.adinventory_type == 'Small') | (
                                    type.adinventory_type == 'Large')):
                            pmdefault = v0.models.PriceMappingDefault(object_id=supplier_id, content_type=content_type,
                                                                      adinventory_type=type, duration_type=duration)
                            price_mapping_list.append(pmdefault)
                        if (type.adinventory_type == 'Customize'):
                            pmdefault = v0.models.PriceMappingDefault(object_id=supplier_id, content_type=content_type,
                                                                      adinventory_type=type, duration_type=duration)
                            price_mapping_list.append(pmdefault)
                if (type.adinventory_name == 'CAR DISPLAY'):
                    if ((duration.duration_name == 'Unit Daily') | (duration.duration_name == '2 Days')):
                        if ((type.adinventory_type == 'Standard') | (type.adinventory_type == 'Premium')):
                            pmdefault = v0.models.PriceMappingDefault(object_id=supplier_id, content_type=content_type,
                                                                      adinventory_type=type, duration_type=duration)
                            price_mapping_list.append(pmdefault)
                if ((type.adinventory_name == 'FLIER') & (duration.duration_name == 'Unit Daily')):
                    if ((type.adinventory_type == 'Door-to-Door') | (type.adinventory_type == 'Mailbox') | (
                                type.adinventory_type == 'Lobby')):
                        pmdefault = v0.models.PriceMappingDefault(object_id=supplier_id, content_type=content_type,
                                                                  adinventory_type=type, duration_type=duration)
                        price_mapping_list.append(pmdefault)

        v0.models.PriceMappingDefault.objects.bulk_create(price_mapping_list)
        return True
    except Exception as e:
        raise Exception(function, get_system_error(e))


def adinventory_func():
    """
    :return: functions makes a dict containing adinventory_dict
    """
    adinventory_objects = v0.models.AdInventoryType.objects.all()
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

    return adinventory_dict


def get_supplier_inventory(data, id):
    """
    :param supplier_code: RA, CP, GYM, SA, id = pk of supplier table
    :return:  a dict containing correct inventory and supplier object depending upon the supplier id
    """

    try:
        supplier_code = data['supplier_type_code']
        # supplier_code = 'CP' #todo: change this when get clearity
        if not supplier_code or not id:
            return Response(data={"status": False, "error": "provide supplier code and  supplier id"},
                            status=status.HTTP_400_BAD_REQUEST)

        # supplier_class = v0_constants.suppliers[supplier_code]
        supplier_class = get_model(supplier_code)
        supplier_object = supplier_class.objects.get(pk=id)
        content_type = ContentType.objects.get_for_model(supplier_class)
#       inventory_object = InventorySummary.objects.get(content_object=supplier_object, object_id=id, content_type=content_type)

        (inventory_object, is_created) = v0.models.InventorySummary.objects.get_or_create(object_id=id, content_type=content_type)
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
    duration_type_objects = v0.models.DurationType.objects.all()
    duration_type_dict = {}

    for duration_type in duration_type_objects:
        if duration_type.duration_name == 'Campaign Weekly':
            duration_type_dict['campaign_weekly'] = duration_type
        elif duration_type.duration_name == 'Campaign Monthly':
            duration_type_dict['campaign_montly'] = duration_type
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
            stall = v0.models.StallInventory.objects.get_or_create_objects(data, supplier.supplier_id, supplier_type_code)
            stall.save()

    except Exception as e:
        return Response(data={'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


def save_flyer_locations(c1, c2, supplier, supplier_type_code):
    count = int(c2) + 1

    try:
        for i in range(c1 + 1, count):
            flyer_id = supplier.supplier_id + "0000FL" + str(i).zfill(2)
            data = {
                'adinventory_id': flyer_id,
            }
            flyer = v0.models.FlyerInventory.objects.get_or_create_objects(data, supplier.supplier_id, supplier_type_code)
            flyer.flat_count = supplier.flat_count
            flyer.save()

    except Exception as e:
        return Response(data={'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


def delete(request, id, format=None):
    try:
        invId = request.query_params.get('invId', None)
        stall = v0.models.StallInventory.objects.get(pk=invId)
        stall.delete()
        return Response(status=204)
    except v0.models.StallInventory.DoesNotExist:
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

        for model_class, content_type in content_types.iteritems():
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

            v0_constants.society_code: v0.serializers.SupplierTypeSocietySerializer,
            v0_constants.corporate_code: v0.serializers.SupplierTypeCorporateSerializer,
            v0_constants.gym: v0.serializers.SupplierTypeGymSerializer,
            v0_constants.salon: v0.serializers.SupplierTypeSalonSerializer,
            v0_constants.bus_shelter: v0.serializers.SupplierTypeBusShelterSerializer,
            v0_constants.retail_shop_code: v0.serializers.SupplierTypeRetailShopSerializer,
            v0_constants.bus_depot_code: ui_serializers.BusDepotSerializer,
            'ideation_design_cost': v0.serializers.IdeationDesignCostSerializer,
            'logistic_operations_cost': v0.serializers.LogisticOperationsCostSerializer,
            'space_booking_cost': v0.serializers.SpaceBookingCostSerializer,
            'event_staffing_cost': v0.serializers.EventStaffingCostSerializer,
            'data_sciences_cost': v0.serializers.DataSciencesCostSerializer,
            'printing_cost': v0.serializers.PrintingCostSerializer,
            'proposal_metrics': v0.serializers.ProposalMetricsSerializer,
            'proposal_master_cost': v0.serializers.ProposalMasterCostSerializer

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
        images = v0.models.ImageMapping.objects.filter(object_id__in=supplier_ids)
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
            nb = models.PosterInventory(adinventory_id=nb_id, poster_location=nb_tag, tower_name=nb_tower, supplier=society, object_id=supplier_id, content_type=society_content_type)
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
        city_names = models.City.objects.filter(city_code__in=authorized_region_codes).values_list('city_name', flat=True)
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

        if validate_date_format(date_string, first_format):
            ret = timezone.make_aware(datetime.datetime.strptime(date_string, first_format), timezone.get_default_timezone())
        elif validate_date_format(date_string, second_format):
            ret = parse_datetime(date_string)
        else:
            raise ValueError(errors.INVALID_DATE_FORMAT.format(first_format, second_format))

        return ret
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


# a version is also present in  tasks.py file. But that version sends mail through celery. This version directly sends mail.
def send_email(email_data, attachment=None):
    """
    Args: dict having 'subject', 'body' and 'to' as keys.
    Returns: success if mail is sent else failure
    """
    function = send_email.__name__
    try:
        # check if email_data contains the predefined keys
        email_keys = email_data.keys()
        for key in ['body', 'subject', 'to']:
            if key not in email_keys:
                raise Exception(function,'key {0} not found in the recieved structure'.format(key))
        # construct the EmailMessage class
        email = EmailMessage(email_data['subject'], email_data['body'], to=email_data['to'])
        # attach attachment if available
        if attachment:
            file_to_send = open(attachment['file_name'], 'r')
            email.attach(attachment['file_name'], file_to_send.read(), attachment['mime_type'])
            file_to_send.close()
        return email.send()
    except SMTPException as e:
        raise Exception(function, "Error " + get_system_error(e))
    except Exception as e:
        raise Exception(function, "Error " + get_system_error(e))

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
        gateway_arch = v0.models.GatewayArchInventory.objects.get_or_create_objects(data, supplier.supplier_id, supplier_type_code)
        gateway_arch.save()
    except Exception as e:
        raise Exception(function, "Error " + get_system_error(e))