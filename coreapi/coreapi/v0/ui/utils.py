'''

# helper file for ui views. all functions in this file should take a common format of  (request, data)
order of imports
 -native python imports
 -django specific imports
 -third party imports
 -file imports

'''
import json

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

from rest_framework.response import Response
from rest_framework import status

import v0.models
import v0.serializers

import constants as ui_constants


def handle_response(object_name, data='some error occurred', exception_object=Exception, success=False):
    """
    Args:
        success: determines wether to send success or failure messages
        object_name: The function or class where the error occurrs
        data: The user error which you want to display to user's on screens
        exception_object: The exception object caught. an instance of Exception, KeyError etc.

        This method can later be used to log the errors.

    Returns: Response object

    """
    if not success:
        # prepare the object to be sent in error response
        data = {
            'general_error': data,
            'system_error': str(exception_object.message) if exception_object.message else str(exception_object.args) if exception_object.args else "",
            'culprit_module': object_name
        }
        return Response({'status': False, 'data': data}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'status': True, 'data': data}, status=status.HTTP_200_OK)


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


def get_supplier_id(request, data):
    """
    :param request: request parameter
    :param data: dict containing valid keys . Note the keys should be 'city', 'area', sub_area', 'supplier_type' ,
    'supplier_code' for this to work
    :return:  Response in which data has a key 'supplier_id' containing supplier_id
    """
    try:

        try:

            city_object = v0.models.City.objects.get(city_name=data['city'])
            area_object = v0.models.CityArea.objects.get(label=data['area'])
            subarea_object = v0.models.CitySubArea.objects.get(subarea_name=data['sub_area'],
                                                     area_code=area_object)
        except ObjectDoesNotExist:
            city_object = v0.models.City.objects.get(id=data['city'])
            area_object = v0.models.CityArea.objects.get(id=data['area'])
            subarea_object = v0.models.CitySubArea.objects.get(id=data['sub_area'],
                                                     area_code=area_object)

        supplier_id = city_object.city_code + area_object.area_code + subarea_object.subarea_code + data[
            'supplier_type'] + data[
                          'supplier_code']
    except KeyError as e:
        return Response(data={'status': False, 'error': str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist as e:
        return Response(data={'status': False, 'error': str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(data={'status': False, 'error': str(e.message)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(data={'status': True, 'supplier_id': supplier_id}, status=status.HTTP_200_OK)


def make_supplier_data(data):
    try:

        try:
            city = v0.models.City.objects.get(city_name=data['city'])
            area = v0.models.CityArea.objects.get(label=data['area'])
            subarea = v0.models.CitySubArea.objects.get(subarea_name=data['sub_area'],
                                                     area_code=area)
        except ObjectDoesNotExist:
            city = v0.models.City.objects.get(id=data['city'])
            area = v0.models.CityArea.objects.get(id=data['area'])
            subarea = v0.models.CitySubArea.objects.get(id=data['sub_area'],
                                                     area_code=area)

        current_user = data['current_user']

        all_supplier_data = {

            "RS": {

                'data': {'supplier_code': data['supplier_code'],
                         'society_name': data['supplier_name'],
                         'supplier_id': data['supplier_id'],
                         'created_by': current_user.id,
                         'society_city': city.city_name,
                         'society_subarea': subarea.subarea_name,
                         'society_locality': area.label,
                         'society_state': city.state_code.state_name,
                         },

                'serializer': get_serializer('RS')

            },

            "CP": {
                'data': {
                    'supplier_id': data['supplier_id'],
                    'name': data['supplier_name'],
                    'city': city.city_name,
                    'locality': area.label,
                    'subarea': subarea.subarea_name,
                    'state': city.state_code.state_name
                },
                'serializer': get_serializer('CP')
            },
            "SA": {
                'data': {
                    'supplier_id': data['supplier_id'],
                    'name': data['supplier_name'],
                    'city': city.city_name,
                    'locality': area.label,
                    'subarea': subarea.subarea_name,
                    'state': city.state_code.state_name
                },
                'serializer': get_serializer('SA')
            },

            "GY": {
                'data': {
                    'supplier_id': data['supplier_id'],
                    'name': data['supplier_name'],
                    'city': city.city_name,
                    'locality': area.label,
                    'subarea': subarea.subarea_name,
                    'state': city.state_code.state_name
                },
                'serializer': get_serializer('GY')
            },

            "supplier_type_code": data['supplier_type_code']
        }
        return Response(data={"status": True, "data": all_supplier_data}, status=status.HTTP_200_OK)
    except KeyError as e:
        return Response(data={"status": False, "error": "Key error {0} ".format(str(e.message))},
                        status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist as e:
        return Response(data={"status": False, "error": "Object does not exist {0}".format(str(e.message))},
                        status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(data={"status": False, "error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)


def save_supplier_data(master_data):
    """
    :param master_data containing data for all suppliers
    :return: saves corresponding supplier code data
    """
    try:
        supplier_code = master_data['supplier_type_code']
        serializer_class = get_serializer(supplier_code)
        # serializer_class = master_data[supplier_code]['serializer']
        supplier_data = master_data[supplier_code]['data']
        serializer = serializer_class(data=supplier_data)
        if serializer.is_valid():
            serializer.save()
            response = set_default_pricing(serializer.data['supplier_id'], supplier_code)
            if not response.data['status']:
                return response
            return Response(data={"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(data={"status": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response(data={"status": False, "error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)


def set_default_pricing(supplier_id, supplier_type_code):
    """
    :param supplier_id: supplier uinique id
    :param supplier_type_code: which type of supplier
    :return:  makes an entry into PriceMappingDefault table for the given supplier

    """
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
                                                        adinventory_type=type, duration_type=duration,
                                                        supplier_price=-1, business_price=-1)
                        price_mapping_list.append(pmdefault)
                    if ((duration.duration_name == 'Campaign Weekly') | (duration.duration_name == 'Campaign Monthly') | (
                                duration.duration_name == 'Unit Monthly') | (duration.duration_name == 'Unit Weekly')):
                        pmdefault = v0.models.PriceMappingDefault(object_id=supplier_id, content_type=content_type,
                                                        adinventory_type=type, duration_type=duration,
                                                        supplier_price=0, business_price=0)
                        price_mapping_list.append(pmdefault)

                if (type.adinventory_name == 'POSTER LIFT'):
                    if ((duration.duration_name == 'Unit Daily')):
                        pmdefault = v0.models.PriceMappingDefault(object_id=supplier_id, content_type=content_type,
                                                        adinventory_type=type, duration_type=duration,
                                                        supplier_price=-1, business_price=-1)
                        price_mapping_list.append(pmdefault)
                    if ((duration.duration_name == 'Campaign Weekly') | (duration.duration_name == 'Campaign Monthly') | (
                                duration.duration_name == 'Unit Monthly') | (duration.duration_name == 'Unit Weekly')):
                        pmdefault = v0.models.PriceMappingDefault(object_id=supplier_id, content_type=content_type,
                                                        adinventory_type=type, duration_type=duration,
                                                        supplier_price=0, business_price=0)
                        price_mapping_list.append(pmdefault)

                if (type.adinventory_name == 'STANDEE'):
                    if ((duration.duration_name == 'Campaign Monthly') | (duration.duration_name == 'Campaign Weekly') | (
                                duration.duration_name == 'Unit Weekly') | (duration.duration_name == 'Unit Monthly')):
                        if (type.adinventory_type == 'Large'):
                            pmdefault = v0.models.PriceMappingDefault(object_id=supplier_id, content_type=content_type,
                                                            adinventory_type=type, duration_type=duration,
                                                            supplier_price=-1, business_price=-1)
                            price_mapping_list.append(pmdefault)
                        else:
                            pmdefault = v0.models.PriceMappingDefault(object_id=supplier_id, content_type=content_type,
                                                            adinventory_type=type, duration_type=duration,
                                                            supplier_price=0, business_price=0)
                            price_mapping_list.append(pmdefault)
                if (type.adinventory_name == 'STALL'):
                    if ((duration.duration_name == 'Unit Daily') | (duration.duration_name == '2 Days')):
                        if ((type.adinventory_type == 'Canopy') | (type.adinventory_type == 'Small') | (
                                    type.adinventory_type == 'Large')):
                            pmdefault = v0.models.PriceMappingDefault(object_id=supplier_id, content_type=content_type,
                                                            adinventory_type=type, duration_type=duration,
                                                            supplier_price=0, business_price=0)
                            price_mapping_list.append(pmdefault)
                        if (type.adinventory_type == 'Customize'):
                            pmdefault = v0.models.PriceMappingDefault(object_id=supplier_id, content_type=content_type,
                                                            adinventory_type=type, duration_type=duration,
                                                            supplier_price=-1, business_price=-1)
                            price_mapping_list.append(pmdefault)
                if (type.adinventory_name == 'CAR DISPLAY'):
                    if ((duration.duration_name == 'Unit Daily') | (duration.duration_name == '2 Days')):
                        if ((type.adinventory_type == 'Standard') | (type.adinventory_type == 'Premium')):
                            pmdefault = v0.models.PriceMappingDefault(object_id=supplier_id, content_type=content_type,
                                                            adinventory_type=type, duration_type=duration,
                                                            supplier_price=0, business_price=0)
                            price_mapping_list.append(pmdefault)
                if ((type.adinventory_name == 'FLIER') & (duration.duration_name == 'Unit Daily')):
                    if ((type.adinventory_type == 'Door-to-Door') | (type.adinventory_type == 'Mailbox') | (
                                type.adinventory_type == 'Lobby')):
                        pmdefault = v0.models.PriceMappingDefault(object_id=supplier_id, content_type=content_type,
                                                        adinventory_type=type, duration_type=duration,
                                                        supplier_price=0, business_price=0)
                        price_mapping_list.append(pmdefault)

        v0.models.PriceMappingDefault.objects.bulk_create(price_mapping_list)
        return Response({'status': True, 'data': 'success'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


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
        #supplier_code = data['supplier_type_code']
        supplier_code = 'CP' #todo: change this when get clearity
        if not supplier_code or not id:
            return Response(data={"status": False, "error": "provide supplier code and  supplier id"},
                            status=status.HTTP_400_BAD_REQUEST)

        # supplier_class = ui_constants.suppliers[supplier_code]
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
#         supplier_class = ui_constants.suppliers[supplier_code]
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


def save_price_data(price_object, posprice, buisiness_price):
    """
    :param posprice, buisiness_price are data to be saved.
    :return: saves the PriceMappingDefault  object

    """
    try:
        price_object.business_price = posprice
        price_object.supplier_price = buisiness_price
        price_object.save()
    except Exception as e:
        pass


def get_tower_count(supplier_object, supplier_type_code):
    """
    Args:
        supplier_type_code: RS, CP, GY

    Returns: tower count in case the supplier object has tower count attribute. which attribute of supplier object refers to a
    tower count is defined in constants.py. also the right supplier object is fetched from constants.py.
    """
    try:
        count = 1
        #supplier_object = ui_constants.suppliers[supplier_type_code]
        # supplier_object = get_model(supplier_type_code)
        attr = ui_constants.tower_count_attribute_mapping[supplier_type_code]
        if attr != 'none':
            count = getattr(supplier_object, attr)
        return Response(data={'status': True, 'data': count}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(data={'status': False, 'error': 'Error in fetching tower count'}, status=status.HTTP_400_BAD_REQUEST)


def get_content_type(supplier_type_code):
    """
    Args:
        supplier_type_code: supplier_type_code

    Returns: The right content type object for the given supplier_type_code

    """
    try:
        if not supplier_type_code:
            return Response({'status': False, 'error': 'No supplier type code provided'}, status=status.HTTP_400_BAD_REQUEST)
        ContentType = apps.get_model('contenttypes', 'ContentType')
        load_model = get_model(supplier_type_code)
        content_type = ContentType.objects.get_for_model(load_model)
        return Response({'status': True, 'data': content_type}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


def get_model(supplier_type_code):
    """
    Args:
        supplier_type_code: RS, CP

    Returns: loads the right model from supplier_type_code

    """
    try:
        suppliers = ui_constants.string_suppliers
        load_model = apps.get_model('v0', suppliers[supplier_type_code])
        return load_model
    except Exception as e:
        return None


def get_serializer(query):
    """
    Args:
        query: CP, RS or table name in db

    Returns: right SerializerClass

    """

    try:

        serializers = {

            'RS': v0.serializers.SupplierTypeSocietySerializer,
            'CP': v0.serializers.SupplierTypeCorporateSerializer,
            'GY': v0.serializers.SupplierTypeGymSerializer,
            'SA': v0.serializers.SupplierTypeSalonSerializer,
            'BS': v0.serializers.SupplierTypeBusShelterSerializer,
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
        return None
