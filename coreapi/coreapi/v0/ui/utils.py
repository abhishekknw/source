'''

# helper file for ui views. all functions in this file should take a common format of  (request, data)
order of imports
 -native python imports
 -django specific imports
 -third party imports
 -file imports

'''

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType

from rest_framework.response import Response
from rest_framework import status

from v0.models import City, CityArea, CitySubArea, AdInventoryType, FlyerInventory, DurationType, StallInventory, \
    InventorySummary, SupplierTypeSociety, PriceMappingDefault
import constants as ui_constants
from v0.serializers import SupplierTypeSocietySerializer, SupplierTypeGymSerializer, SupplierTypeCorporateSerializer, \
    SupplierTypeSalonSerializer


def get_supplier_id(request, data):
    """
    :param request: request parameter
    :param data: dict containing valid keys . Note the keys should be 'city', 'area', sub_area', 'supplier_type' ,
    'supplier_code' for this to work
    :return:  Response in which data has a key 'supplier_id' containing supplier_id
    """
    try:

        try:

            city_object = City.objects.get(city_name=data['city'])
            area_object = CityArea.objects.get(label=data['area'])
            subarea_object = CitySubArea.objects.get(subarea_name=data['sub_area'],
                                                     area_code=area_object)
        except ObjectDoesNotExist:
            city_object = City.objects.get(id=data['city'])
            area_object = CityArea.objects.get(id=data['area'])
            subarea_object = CitySubArea.objects.get(id=data['sub_area'],
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
            city = City.objects.get(city_name=data['city'])
            area = CityArea.objects.get(label=data['area'])
            subarea = CitySubArea.objects.get(subarea_name=data['sub_area'],
                                                     area_code=area)
        except ObjectDoesNotExist:
            city = City.objects.get(id=data['city'])
            area = CityArea.objects.get(id=data['area'])
            subarea = CitySubArea.objects.get(id=data['sub_area'],
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

                'serializer': SupplierTypeSocietySerializer

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
                'serializer': SupplierTypeCorporateSerializer
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
                'serializer': SupplierTypeSalonSerializer
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
                'serializer': SupplierTypeGymSerializer
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
        serializer_class = master_data[supplier_code]['serializer']
        supplier_data = master_data[supplier_code]['data']
        serializer = serializer_class(data=supplier_data)
        if serializer.is_valid():
            serializer.save()
            if supplier_code == 'RS':
                set_default_pricing(serializer.data['supplier_id'])
            return Response(data={"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(data={"status": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response(data={"status": False, "error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)


def set_default_pricing(society_id):
    print "inside def"
    society = SupplierTypeSociety.objects.get(pk=society_id)
    ad_types = AdInventoryType.objects.all()
    duration_types = DurationType.objects.all()
    price_mapping_list = []
    for type in ad_types:
        for duration in duration_types:
            if (type.adinventory_name == 'POSTER'):
                if ((duration.duration_name == 'Unit Daily')):
                    pmdefault = PriceMappingDefault(supplier=society, adinventory_type=type, duration_type=duration,
                                                    society_price=-1, business_price=-1)
                    price_mapping_list.append(pmdefault)
                if ((duration.duration_name == 'Campaign Weekly') | (duration.duration_name == 'Campaign Monthly') | (
                            duration.duration_name == 'Unit Monthly') | (duration.duration_name == 'Unit Weekly')):
                    pmdefault = PriceMappingDefault(supplier=society, adinventory_type=type, duration_type=duration,
                                                    society_price=0, business_price=0)
                    price_mapping_list.append(pmdefault)

            if (type.adinventory_name == 'POSTER LIFT'):
                if ((duration.duration_name == 'Unit Daily')):
                    pmdefault = PriceMappingDefault(supplier=society, adinventory_type=type, duration_type=duration,
                                                    society_price=-1, business_price=-1)
                    price_mapping_list.append(pmdefault)
                if ((duration.duration_name == 'Campaign Weekly') | (duration.duration_name == 'Campaign Monthly') | (
                            duration.duration_name == 'Unit Monthly') | (duration.duration_name == 'Unit Weekly')):
                    pmdefault = PriceMappingDefault(supplier=society, adinventory_type=type, duration_type=duration,
                                                    society_price=0, business_price=0)
                    price_mapping_list.append(pmdefault)

            if (type.adinventory_name == 'STANDEE'):
                if ((duration.duration_name == 'Campaign Monthly') | (duration.duration_name == 'Campaign Weekly') | (
                            duration.duration_name == 'Unit Weekly') | (duration.duration_name == 'Unit Monthly')):
                    if (type.adinventory_type == 'Large'):
                        pmdefault = PriceMappingDefault(supplier=society, adinventory_type=type, duration_type=duration,
                                                        society_price=-1, business_price=-1)
                        price_mapping_list.append(pmdefault)
                    else:
                        pmdefault = PriceMappingDefault(supplier=society, adinventory_type=type, duration_type=duration,
                                                        society_price=0, business_price=0)
                        price_mapping_list.append(pmdefault)
            if (type.adinventory_name == 'STALL'):
                if ((duration.duration_name == 'Unit Daily') | (duration.duration_name == '2 Days')):
                    if ((type.adinventory_type == 'Canopy') | (type.adinventory_type == 'Small') | (
                                type.adinventory_type == 'Large')):
                        pmdefault = PriceMappingDefault(supplier=society, adinventory_type=type, duration_type=duration,
                                                        society_price=0, business_price=0)
                        price_mapping_list.append(pmdefault)
                    if (type.adinventory_type == 'Customize'):
                        pmdefault = PriceMappingDefault(supplier=society, adinventory_type=type, duration_type=duration,
                                                        society_price=-1, business_price=-1)
                        price_mapping_list.append(pmdefault)
            if (type.adinventory_name == 'CAR DISPLAY'):
                if ((duration.duration_name == 'Unit Daily') | (duration.duration_name == '2 Days')):
                    if ((type.adinventory_type == 'Standard') | (type.adinventory_type == 'Premium')):
                        pmdefault = PriceMappingDefault(supplier=society, adinventory_type=type, duration_type=duration,
                                                        society_price=0, business_price=0)
                        price_mapping_list.append(pmdefault)
            if ((type.adinventory_name == 'FLIER') & (duration.duration_name == 'Unit Daily')):
                if ((type.adinventory_type == 'Door-to-Door') | (type.adinventory_type == 'Mailbox') | (
                            type.adinventory_type == 'Lobby')):
                    pmdefault = PriceMappingDefault(supplier=society, adinventory_type=type, duration_type=duration,
                                                    society_price=0, business_price=0)
                    price_mapping_list.append(pmdefault)

    PriceMappingDefault.objects.bulk_create(price_mapping_list)
    return Response(status=200)


def adinventory_func():
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

    return adinventory_dict


def get_supplier_inventory(data, id):
    """
    :param supplier_code: RA, CP, GYM, SA, id = pk of supplier table
    :return:  a dict containing correct inventory and supplier object depending upon the supplier id
    """
    '''
        my_supported = SupportedProgram.objects.get(id=instance_id_goes_here)
        ct_supported = ContentType.objects.get_for_model(SupportedProgram))
        primary_citations = FullCitation.objects.filter(content_object=my_supported, content_type=ct_supported, is_primary=True)

    '''
    try:
        #supplier_code = data['supplier_type_code']
        supplier_code = 'CP' #todo: change this when get clearity
        if not supplier_code or not id:
            return Response(data={"status": False, "error": "provide supplier code and  supplier id"},
                            status=status.HTTP_400_BAD_REQUEST)
        supplier_class = ui_constants.suppliers[supplier_code]
        supplier_object = supplier_class.objects.get(pk=id)
        content_type = ContentType.objects.get_for_model(supplier_class)
#       inventory_object = InventorySummary.objects.get(content_object=supplier_object, object_id=id, content_type=content_type)

        (inventory_object, is_created) = InventorySummary.objects.get_or_create(object_id=id, content_type=content_type)
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
    duration_type_objects = DurationType.objects.all()
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


def save_stall_locations(c1, c2, society):
    count = int(c2) + 1
    for i in range(c1 + 1, count):
        stall_id = society.supplier_id + "CA0000ST" + str(i).zfill(2)
        (stall, is_created) = StallInventory.objects.get_or_create(adinventory_id=stall_id, supplier_id=society.supplier_id)
        stall.save()


def save_flyer_locations(c1, c2, society):
    count = int(c2) + 1

    try:
        for i in range(c1 + 1, count):
            flyer_id = society.supplier_id + "0000FL" + str(i).zfill(2)
            (flyer, is_created) = FlyerInventory.objects.get_or_create(adinventory_id=flyer_id,  supplier_id=society.supplier_id)
            flyer.flat_count = society.flat_count
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
