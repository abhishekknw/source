import json
from openpyxl import load_workbook
from pathlib import Path
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import list_route
from v0.ui.utils import (get_supplier_id, handle_response, get_content_type, save_flyer_locations, make_supplier_data,
                         get_model, get_serializer, save_supplier_data, get_region_based_query, get_supplier_image,
                         save_basic_supplier_details)
from v0.ui.website.utils import manipulate_object_key_values
from models import (SupplierTypeSociety, SupplierAmenitiesMap, SupplierTypeCorporate, SupplierTypeGym,
                    SupplierTypeRetailShop, CorporateParkCompanyList, CorporateBuilding, SupplierTypeBusDepot,
                    SupplierTypeCode, SupplierTypeBusShelter, CorporateCompanyDetails, RETAIL_SHOP_TYPE)
from serializers import (UICorporateSerializer, SupplierTypeSocietySerializer, SupplierAmenitiesMapSerializer,
                         UISalonSerializer, SupplierTypeSalon, SupplierTypeGymSerializer, RetailShopSerializer,
                         SupplierInfoSerializer, SupplierInfo, SupplierTypeCorporateSerializer,
                         CorporateBuildingGetSerializer, CorporateParkCompanyListSerializer, CorporateBuildingSerializer,
                         SupplierTypeSalonSerializer, BusDepotSerializer, CorporateParkCompanySerializer,
                         BusShelterSerializer, SupplierTypeBusShelterSerializer)
from v0.ui.location.models import City, CityArea, CitySubArea
from v0.ui.location.serializers import CityAreaSerializer
from v0.ui.account.models import ContactDetails
from v0.ui.inventory.models import AdInventoryType
from v0.ui.finances.models import PriceMappingDefault
from v0.ui.base.models import DurationType
from v0.ui.serializers import (UISocietySerializer, SocietyListSerializer)
from v0.ui.proposal.serializers import ImageMappingSerializer
from v0.ui.proposal.models import ImageMapping
from v0.ui.account.serializers import (ContactDetailsSerializer, ContactDetailsGenericSerializer)
from v0.ui.account.models import ContactDetailsGeneric
from v0.ui.components.models import (SocietyTower, CorporateBuildingWing, CompanyFloor)
from v0.ui.components.serializers import CorporateBuildingWingSerializer
import v0.constants as v0_constants
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from v0.ui.utils import get_from_dict
from v0.ui.controller import inventory_summary_insert
import v0.ui.utils as ui_utils
from v0.ui.inventory.models import InventorySummary
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


def get_state_map():
    all_city = City.objects.all()
    state_map = {}
    for city in all_city:
        state_map[city.city_code] = {'state_name': city.state_code.state_name, 'state_code': city.state_code.state_code}
    return state_map


def get_city_map():
    all_city = City.objects.all()
    city_map = {}
    for city in all_city:
        city_map[city.city_code] = city.city_name
    return city_map


def get_city_area_map():
    all_city_area = CityArea.objects.all()
    city_area_map = {}
    for city_area in all_city_area:
        city_area_map[city_area.area_code] = city_area.label
    return city_area_map


def get_city_subarea_map():
    all_city_subarea = CitySubArea.objects.all()
    city_subarea_map = {}
    for city_subarea in all_city_subarea:
        city_subarea_map[city_subarea.subarea_code] = city_subarea.subarea_name
    return city_subarea_map


def create_price_mapping_default(days_count, adinventory_name, adinventory_type, new_society,
                                 actual_supplier_price, content_type, supplier_id):
    duration_type = DurationType.objects.get(days_count=days_count)
    adinventory_type = AdInventoryType.objects.get(adinventory_name=adinventory_name, adinventory_type=adinventory_type)
    PriceMappingDefault.objects.get_or_create(supplier=new_society, duration_type=duration_type,
                                              adinventory_type=adinventory_type,
                                              actual_supplier_price=actual_supplier_price,
                                              content_type=content_type,
                                              object_id=supplier_id)


@method_decorator(csrf_exempt, name='dispatch')
class SocietyDataImport(APIView):
    """

    """

    def post(self, request):
        source_file = request.data['file']
        wb = load_workbook(source_file)
        ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
        society_data_list = []
        for index, row in enumerate(ws.iter_rows()):
            if index > 0:
                society_data_list.append({
                    'society_name': row[0].value if row[0].value else None,
                    'society_city': str(row[1].value) if row[1].value else None,
                    'society_locality': row[2].value if row[2].value else None,
                    'society_subarea': row[3].value if row[3].value else None,
                    'supplier_code': row[4].value if row[4].value else None,
                    'society_zip': int(row[5].value) if row[5].value else None,
                    'society_latitude': float(row[6].value) if row[6].value else None,
                    'society_longitude': float(row[7].value) if row[7].value else None,
                    'tower_count': int(row[8].value) if row[8].value else None,
                    'flat_count': int(row[9].value) if row[9].value else None,
                    'designation': row[10].value if row[10].value else None,
                    'salutation': row[11].value if row[11].value else None,
                    'contact_name': row[12].value if row[12].value else None,
                    'email': row[13].value if row[13].value else None,
                    'mobile': row[14].value if row[14].value else None,
                    'name_for_payment': row[15].value if row[15].value else None,
                    'ifsc_code': row[16].value if row[16].value else None,
                    'bank_name': row[17].value if row[17].value else None,
                    'account_no': row[18].value if row[18].value else None,
                    'stall_allowed': True if row[19].value in ['Y', 'y', 't', 'T', 'true', 'True'] else False,
                    'total_stall_count': row[20].value if row[20].value else None,
                    'poster_allowed_nb': True if row[21].value in ['Y', 'y', 't', 'T', 'true', 'True'] else False,
                    'nb_per_tower': int(row[22].value) if row[22].value else None,
                    'poster_allowed_lift': True if row[23].value in ['Y', 'y', 't', 'T', 'true', 'True'] else False,
                    'lift_per_tower': int(row[24].value) if row[24].value else None,
                    'flier_allowed': True if row[25].value in ['Y', 'y', 't', 'T', 'true', 'True'] else False,
                    'flier_frequency': int(row[26].value) if row[26].value else None,
                    'stall_price': float(row[27].value) if row[27].value else None,
                    'poster_price': float(row[28].value) if row[28].value else None,
                    'flier_price': float(row[29].value) if row[29].value else None,
                    'status': row[30].value,
                    'comments': row[31].value,
                })
        all_states_map = get_state_map()
        all_city_map = get_city_map()
        all_city_area_map = get_city_area_map()
        all_city_subarea_map = get_city_subarea_map()
        for society in society_data_list:
            if society['supplier_code'] is not None:
                data = {
                    'city_code': society['society_city'],
                    'area_code': society['society_locality'],
                    'subarea_code': society['society_subarea'],
                    'supplier_type': 'RS',
                    'supplier_code': society['supplier_code'],
                    'supplier_name': society['society_name']
                }
                supplier_id = get_supplier_id(data, state_name=all_states_map[society['society_city']]['state_name'],
                                              state_code=all_states_map[society['society_city']]['state_code'])
                new_society = SupplierTypeSociety(**{
                    'supplier_id': supplier_id,
                    'society_name': society['society_name'],
                    'society_locality': all_city_area_map[society['society_locality']],
                    'society_city': all_city_map[society['society_city']],
                    'society_state': all_states_map[society['society_city']]['state_name'],
                    'society_subarea': all_city_subarea_map[society['society_subarea']],
                    'supplier_code': society['supplier_code'],
                    'society_zip': society['society_zip'],
                    'society_latitude': society['society_latitude'],
                    'society_longitude': society['society_longitude'],
                    'tower_count': society['tower_count'],
                    'flat_count': society['flat_count'],
                    'name_for_payment': society['name_for_payment'],
                    'ifsc_code': society['ifsc_code'],
                    'bank_name': society['bank_name'],
                    'account_no': society['account_no'],
                    'stall_allowed': society['stall_allowed'],
                    'supplier_status': society['status'],
                    'comments': society['comments'],
                })
                new_society.save()
                new_contact_data = {
                    'name': society['contact_name'],
                    'email': society['email'],
                    'designation': society['designation'],
                    'salutation': society['salutation'],
                    'mobile': society['mobile'],
                    'content_type': get_content_type('RS').data['data'],
                    'object_id': supplier_id
                }
                obj, is_created = ContactDetails.objects.get_or_create(**new_contact_data)
                obj.save()
                rs_content_type = get_content_type('RS').data['data']
                create_price_mapping_default('1', "STALL", "Small", new_society,
                                             society['stall_price'], rs_content_type, supplier_id)
                create_price_mapping_default('3', "POSTER", "A4", new_society,
                                             society['poster_price'], rs_content_type, supplier_id)
                save_flyer_locations(0, 1, new_society, society['supplier_code'])
                create_price_mapping_default('1', "FLIER", "Door-to-Door", new_society,
                                             society['flier_price'], rs_content_type, supplier_id)

                inventory_obj = InventorySummary.objects.filter(object_id=supplier_id).first()
                inventory_id = inventory_obj.id if inventory_obj else None
                request_data = {
                    'id': inventory_id,
                    'd2d_allowed': True,
                    'poster_allowed_nb': True,
                    'supplier_type_code': 'RS',
                    'lift_count': society['tower_count'] * society['lift_per_tower'],
                    'stall_allowed': True,
                    'object_id': supplier_id,
                    'flier_allowed': True,
                    'nb_count': society['tower_count'] * society['nb_per_tower'],
                    'user': 1,
                    'content_type': 46,
                    'flier_frequency': society['flier_frequency'],
                    'total_stall_count': society['total_stall_count'],
                    'poster_allowed_lift': True,
                }
                class_name = self.__class__.__name__
                response = ui_utils.get_supplier_inventory(request_data.copy(), supplier_id)
                supplier_inventory_data = response.data['data']['request_data']

                if not response.data['status']:
                    return response

                supplier_inventory_data = response.data['data']['request_data']
                final_data = {
                    'id': get_from_dict(request_data, supplier_id),
                    'supplier_object': get_from_dict(response.data['data'], 'supplier_object'),
                    'inventory_object': get_from_dict(response.data['data'], 'inventory_object'),
                    'supplier_type_code': get_from_dict(request_data, 'supplier_type_code'),
                    'poster_allowed_nb': get_from_dict(request_data, 'poster_allowed_nb'),
                    'nb_count': get_from_dict(request_data, 'nb_count'),
                    'poster_campaign': get_from_dict(request_data, 'poster_campaign'),
                    'lift_count': get_from_dict(request_data, 'lift_count'),
                    'poster_allowed_lift': get_from_dict(request_data, 'poster_allowed_lift'),
                    'standee_allowed': get_from_dict(request_data, 'standee_allowed'),
                    'total_standee_count': get_from_dict(request_data, 'total_standee_count'),
                    'stall_allowed': get_from_dict(request_data, 'stall_allowed'),
                    'total_stall_count': get_from_dict(request_data, 'total_stall_count'),
                    'flier_allowed': get_from_dict(request_data, 'flier_allowed'),
                    'flier_frequency': get_from_dict(request_data, 'flier_frequency'),
                    'flier_campaign': get_from_dict(request_data, 'flier_campaign'),
                }
                try:
                    inventory_summary_insert(final_data, supplier_inventory_data)
                except ObjectDoesNotExist as e:
                    print e
                    # return ui_utils.handle_response(class_name, exception_object=e, request=request)
                except Exception as e:
                    print e
                    # return Response(data={"status": False, "error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
        return handle_response({}, data='success', success=True)


class TransactionDataImport(APIView):
    def post(self, request):
        source_file = request.data['file']
        wb = load_workbook(source_file)
        ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
        transaction_data_list = []
        for index, row in enumerate(ws.iter_rows()):
            if index > 0:
                transaction_data_list.append({
                    'supplier_id': int(row[0].value) if row[0].value else None,
                    'poster_allowed': str(row[1].value) if row[1].value else None,
                    'poster_count': int(row[2].value) if row[2].value else None,
                    'poster_price': float(row[3].value) if row[3].value else None,
                    'standee_allowed': row[4].value if row[4].value else None,
                    'standee_count': int(row[5].value) if row[5].value else None,
                    'standee_price': float(row[6].value) if row[6].value else None,
                    'flier_allowed': row[7].value if row[7].value else None,
                    'flier_frequency': int(row[8].value) if row[8].value else None,
                    'flier_price': float(row[9].value) if row[9].value else None,
                    'stall_allowed': row[10].value if row[10].value else None,
                    'stall_duration': int(row[11].value) if row[11].value else None,
                    'arch_allowed': row[12].value if row[12].value else None,
                    'arch_price': row[13].value if row[13].value else None,
                    # 'comment': row[27].value,
                })
        return handle_response({}, data='transaction-success', success=True)


class checkSupplierCodeAPIView(APIView):
    def get(self, request, code, format=None):
        try:
            society = SupplierTypeSociety.objects.get(supplier_code=code)
            if society:
                return Response(status=200)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)


class GenerateSupplierIdAPIView(APIView):
    """
    Generic API that generates unique supplier id and also saves supplier data
    """

    def post(self, request):

        class_name = self.__class__.__name__
        try:
            user = request.user
            supplier_type_code = request.data['supplier_type']

            data = {
                'city_id': request.data['city_id'],
                'area_id': request.data['area_id'],
                'subarea_id': request.data['subarea_id'],
                'supplier_type': request.data['supplier_type'],
                'supplier_code': request.data['supplier_code'],
                'supplier_name': request.data['supplier_name'],
            }

            city_object = City.objects.get(id=data['city_id'])
            city_code = city_object.city_code

            data['supplier_id'] = get_supplier_id(data)
            data['supplier_type_code'] = request.data['supplier_type']
            data['current_user'] = request.user
            response = make_supplier_data(data)
            if not response.data['status']:
                return response
            all_supplier_data = response.data['data']
            return handle_response(class_name, data=save_supplier_data(user, all_supplier_data),
                                            success=True)
        except ObjectDoesNotExist as e:
            return handle_response(class_name, exception_object=e)
        except Exception as e:
            return handle_response(class_name, exception_object=e)

class SupplierImageDetails(APIView):
    """
    This API gives supplier data and all images for supllier which are used to display on supplier
    Details page.
    """

    def get(self, request, id, format=None):

        class_name = self.__class__.__name__

        try:
            result = {}

            supplier_type_code = request.query_params.get('supplierTypeCode')
            if not supplier_type_code:
                return handle_response(class_name, data='No Supplier type code provided')

            content_type_response = get_content_type(supplier_type_code)
            if not content_type_response.data['status']:
                return handle_response(class_name, data='No content type found')

            content_type = content_type_response.data['data']
            supplier_object = get_model(supplier_type_code).objects.get(pk=id)

            serializer_class = get_serializer(supplier_type_code)
            serializer = serializer_class(supplier_object)
            result['supplier_data'] = serializer.data

            images = ImageMapping.objects.filter(object_id=id, content_type=content_type)
            image_serializer = ImageMappingSerializer(images, many=True)
            result['supplier_images'] = image_serializer.data

            amenities = SupplierAmenitiesMap.objects.filter(object_id=id, content_type=content_type)
            amenity_serializer = SupplierAmenitiesMapSerializer(amenities, many=True)
            result['amenities'] = amenity_serializer.data

            return handle_response(class_name, data=result, success=True)

        except Exception as e:
            return handle_response(class_name, exception_object=e, request=request)

class SocietyAPIView(APIView):
    # permission_classes = (permissions.IsAuthenticated, IsOwnerOrManager,)

    def get(self, request, id, format=None):
        try:
            response = {}
            item = SupplierTypeSociety.objects.get(pk=id)
            self.check_object_permissions(self.request, item)
            serializer = UISocietySerializer(item)

            # Start : Code changes to display images
            # todo : also write code for content_type
            # below code commented due to generic API SupplierImageDetails created to get all images
            # images = ImageMapping.objects.filter(object_id=id)
            # image_serializer = ImageMappingSerializer(images, many=True)
            # response['society_images'] = image_serializer.data
            # End : Code changes to display images
            # inventory_summary = InventorySummary.objects.get(supplier=item)
            # inventory_serializer = InventorySummarySerializer(inventory_summary)

            ###### Check if to use filter or get

            # poster = PosterInventory.objects.filter(supplier=item)
            # print "poster.adinventory_id is :",poster.adinventory_id
            # poster_serializer = PosterInventorySerializer(poster)

            # stall = StallInventory.objects.filter(supplier=item)
            # stall_serializer = StallInventorySerializer(stall)

            # doorToDoor = DoorToDoorInfo.objects.filter(**** how to filter on tower foreignkey  ***** )
            # doorToDoor_serializer = DoorToDoorInfoserializer(doorToDoor)

            # mailbox = MailboxInfo.objects.filter(**** how to filter on tower foreignkey  *****)
            # mailbox_serializer = MailboxInfoSerializer(mailbox)

            # response['society'] = serializer.data
            # response['inventory'] = inventory_serializer.data
            # response['poster'] = poster_serializer.data
            # response['doorToDoor'] = doorToDoor_serializer.data
            # response['mailbox'] = mailbox_serializer.data

            # return Response(response, status=200)

            response['society_data'] = serializer.data
            return Response(response, status=200)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)

    def delete(self, request, id, format=None):
        try:
            item = SupplierTypeSociety.objects.get(pk=id)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        contacts = item.get_contact_list()
        for contact in contacts:
            contact.delete()
        item.delete()
        return Response(status=204)

    def post(self, request, format=None):
        current_user = request.user
        if 'supplier_id' in request.data:
            society = SupplierTypeSociety.objects.filter(pk=request.data['supplier_id']).first()
            if society:
                serializer = SupplierTypeSocietySerializer(society, data=request.data)
            else:

                serializer = SupplierTypeSocietySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=400)

        society = SupplierTypeSociety.objects.filter(pk=serializer.data['supplier_id']).first()
        object_id = serializer.data['supplier_id']
        content_type = ContentType.objects.get_for_model(SupplierTypeSociety)

        # here we will start storing contacts
        if request.data and 'basic_contact_available' in request.data and request.data['basic_contact_available']:
            for contact in request.data['basic_contacts']:
                if 'id' in contact:
                    item = ContactDetails.objects.filter(pk=contact['id']).first()
                    contact_serializer = ContactDetailsSerializer(item, data=contact)
                else:
                    contact_serializer = ContactDetailsSerializer(data=contact)
                if contact_serializer.is_valid():
                    contact_serializer.save(object_id=object_id, content_type=content_type)

        if request.data and 'basic_reference_available' in request.data and request.data['basic_reference_available']:
            contact = request.data['basic_reference_contacts']
            if 'id' in contact:
                item = ContactDetails.objects.filter(pk=contact['id']).first()
                contact_serializer = ContactDetailsSerializer(item, data=contact)
            else:
                contact_serializer = ContactDetailsSerializer(data=contact)
            if contact_serializer.is_valid():
                contact_serializer.save(contact_type="Reference", object_id=object_id, content_type=content_type)

        towercount = SocietyTower.objects.filter(supplier=society).count()
        abc = 0
        if request.data['tower_count'] > towercount:
            abc = request.data['tower_count'] - towercount
        if 'tower_count' in request.data:
            for i in range(abc):
                tower = SocietyTower(supplier=society, object_id=object_id, content_type=content_type)
                tower.save()
        return Response(serializer.data, status=201)

class SocietyAPIFiltersView(APIView):

    def get(self, request, format=None):
        try:
            item = CityArea.objects.all()
            serializer = CityAreaSerializer(item, many=True)
            return Response(serializer.data)
        except CityArea.DoesNotExist:
            return Response(status=404)

class SocietyList(APIView):
    """
    API to list all societies for a given user. This is new api and hence should be preferred over other.
    """

    def get(self, request):
        class_name = self.__class__.__name__
        try:
            user = request.user

            if user.is_superuser:
                society_objects = SupplierTypeSociety.objects.all().order_by('society_name')
            else:
                city_query = get_region_based_query(user, v0_constants.valid_regions['CITY'],
                                                             v0_constants.society)
                society_objects = SupplierTypeSociety.objects.filter(city_query)

            serializer = SupplierTypeSocietySerializer(society_objects, many=True)
            suppliers = manipulate_object_key_values(serializer.data)
            societies_with_images = get_supplier_image(suppliers, v0_constants.society_name)

            data = {
                'count': len(societies_with_images),
                'societies': societies_with_images
            }

            return handle_response(class_name, data=data, success=True)
        except Exception as e:
            return handle_response(class_name, exception_object=e, request=request)

class CorporateViewSet(viewsets.ViewSet):
    """
    A view set around corporates
    """

    def list(self, request):
        class_name = self.__class__.__name__
        try:
            # all corporates sorted by name
            user = request.user
            if user.is_superuser:
                corporates = SupplierTypeCorporate.objects.all().order_by('name')
            else:
                city_query = get_region_based_query(user, v0_constants.valid_regions['CITY'],
                                                             v0_constants.corporate_code)
                corporates = SupplierTypeCorporate.objects.filter(city_query)

            serializer = UICorporateSerializer(corporates, many=True)
            corporates_with_images = get_supplier_image(serializer.data, 'Corporate')
            # disabling pagination as search cannot be performed on whole data set
            # paginator = PageNumberPagination()
            # result_page = paginator.paginate_queryset(corporates_with_images, request)
            # paginator_response = paginator.get_paginated_response(result_page)
            data = {
                'count': len(corporates_with_images),
                'corporates': corporates_with_images
            }
            return handle_response(class_name, data=data, success=True)
        except ObjectDoesNotExist as e:
            return handle_response(class_name, exception_object=e, request=request)

        except Exception as e:
            return handle_response(class_name, exception_object=e, request=request)

    def retrieve(self, request, pk=None):
        """
        Retrieve Corporate
        """
        class_name = self.__class__.__name__
        try:
            corporate_instance = SupplierTypeCorporate.objects.get(pk=pk)
            serializer = UICorporateSerializer(corporate_instance)
            return handle_response(class_name, data=serializer.data, success=True)
        except ObjectDoesNotExist as e:
            return handle_response(class_name, data=pk, exception_object=e)
        except Exception as e:
            return handle_response(class_name, exception_object=e, request=request)

    def update(self, request, pk=None):
        """
        Update a corporate
        Args:
            request: A request body
            pk: pk value

        Returns: updated one object

        """
        class_name = self.__class__.__name__
        try:
            corporate_instance = SupplierTypeCorporate.objects.get(pk=pk)
            serializer = UICorporateSerializer(corporate_instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return handle_response(class_name, data=serializer.data, success=True)
            return handle_response(class_name, data=serializer.errors)
        except ObjectDoesNotExist as e:
            return handle_response(class_name, data=pk, exception_object=e)
        except Exception as e:
            return handle_response(class_name, exception_object=e, request=request)

    def create(self, request):
        """
        Create a corporate
        Args:
            request:  Request body

        Returns: Created Corporate
        """
        class_name = self.__class__.__name__
        try:
            serializer = UICorporateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return handle_response(class_name, data=serializer.data, success=True)
            return handle_response(class_name, data=serializer.errors)
        except Exception as e:
            return handle_response(class_name, exception_object=e, request=request)

    @list_route(methods=['GET'])
    def search(self, request):
        """
        search a corporate
        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            query = request.query_params['query']

            corporates = SupplierTypeCorporate.objects.filter(
                Q(supplier_id__icontains=query) | Q(name__icontains=query) | Q(address1__icontains=query) | Q(
                    city__icontains=query) | Q(state__icontains=query)).order_by('name')
            serializer = UICorporateSerializer(corporates, many=True)

            corporates_with_images = get_supplier_image(serializer.data, 'Corporate')
            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(corporates_with_images, request)

            paginator_response = paginator.get_paginated_response(result_page)
            data = {
                'count': len(corporates_with_images),
                'corporates': paginator_response.data
            }
            return handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return handle_response(class_name, exception_object=e, request=request)

class SalonViewSet(viewsets.ViewSet):

    def list(self, request):

        class_name = self.__class__.__name__
        try:
            user = request.user
            if user.is_superuser:
                salon_objects = SupplierTypeSalon.objects.all().order_by('name')
            else:
                city_query = get_region_based_query(user, v0_constants.valid_regions['CITY'],
                                                             v0_constants.salon)
                salon_objects = SupplierTypeSalon.objects.filter(city_query)

            salon_serializer = UISalonSerializer(salon_objects, many=True)
            items = get_supplier_image(salon_serializer.data, 'Salon')
            # disabling pagination because search cannot be performed on whole data set
            # paginator = PageNumberPagination()
            # result_page = paginator.paginate_queryset(items, request)
            # paginator_response = paginator.get_paginated_response(result_page)
            data = {
                'count': len(salon_serializer.data),
                'salons': items
            }
            return handle_response(class_name, data=data, success=True)
        except ObjectDoesNotExist as e:
            return handle_response(class_name, data='Salon does not exist', exception_object=e)
        except Exception as e:
            return handle_response(class_name, exception_object=e, request=request)

class GymViewSet(viewsets.ViewSet):

    def list(self, request):

        class_name = self.__class__.__name__
        try:
            user = request.user
            if user.is_superuser:
                gym_objects = SupplierTypeGym.objects.all().order_by('name')
            else:
                city_query = get_region_based_query(user, v0_constants.valid_regions['CITY'], v0_constants.gym)
                gym_objects = SupplierTypeGym.objects.filter(city_query)

            gym_shelter_serializer = SupplierTypeGymSerializer(gym_objects, many=True)
            items = get_supplier_image(gym_shelter_serializer.data, 'Gym')
            # disabling pagination because search cannot be performed on whole data set
            # paginator = PageNumberPagination()
            # result_page = paginator.paginate_queryset(items, request)
            # paginator_response = paginator.get_paginated_response(result_page)
            data = {
                'count': len(gym_shelter_serializer.data),
                'gyms': items
            }
            return handle_response(class_name, data=data, success=True)
        except ObjectDoesNotExist as e:
            return handle_response(class_name, data='Gym does not exist', exception_object=e)
        except Exception as e:
            return handle_response(class_name, exception_object=e, request=request)

class SocietyAPIFiltersListView(APIView):

    # self.paginator = None
    # self.serializer = None

    # def get(self,request, format=None):
    #     return self.paginator.get_paginated_response(self.serializer.data)

    def post(self, request, format=None):
        try:
            # two list to disable search on society and flats if all the options in both the fields selected
            allflatquantity = [u'Large', u'Medium', u'Small', u'Very Large']  # in sorted order
            allsocietytype = ['High', 'Medium High', 'Standard', 'Ultra High']  # in sorted order
            cityArea = []
            societytype = []
            flatquantity = []
            inventorytype = []
            citySubArea = []
            filter_present = False
            subareas = False
            areas = False

            if 'subLocationValueModel' in request.data:
                for key in request.data['subLocationValueModel']:
                    citySubArea.append(key['subarea_name'])
                    # filter_present = True
                subareas = True if citySubArea else False

            if (not subareas) and 'locationValueModel' in request.data:
                for key in request.data['locationValueModel']:
                    cityArea.append(key['label'])
                    # filter_present = True
                areas = True if cityArea else False

            if 'typeValuemodel' in request.data:
                for key in request.data['typeValuemodel']:
                    societytype.append(key['label'])
                    # filter_present = True

            if 'checkboxes' in request.data:
                for key in request.data['checkboxes']:
                    if key['checked']:
                        flatquantity.append(key['name'])
                        # filter_present = True

            if 'types' in request.data:
                for key in request.data['types']:
                    if key['checked']:
                        inventorytype.append(key['inventoryname'])
                        # filter_present = True

            flatquantity.sort()
            societytype.sort()
            if flatquantity == allflatquantity:  # sorted comparison to avoid mismatch based on index
                flatquantity = []
            if societytype == allsocietytype:  # same as above
                societytype = []

            if subareas or areas or societytype or flatquantity or inventorytype:
                filter_present = True

            if filter_present:
                # if subareas:
                #     items = SupplierTypeSociety.objects.filter(Q(society_subarea__in = citySubArea) & Q(society_type_quality__in = societytype) & Q(society_type_quantity__in = flatquantity))
                # else :
                #     items = SupplierTypeSociety.objects.filter(Q(society_locality__in = cityArea) & Q(society_type_quality__in = societytype) & Q(society_type_quantity__in = flatquantity))
                # serializer = UISocietySerializer(items, many= True)

                # Sample Code

                if subareas:
                    if societytype and flatquantity and inventorytype:
                        items = SupplierTypeSociety.objects.filter(
                            Q(society_subarea__in=citySubArea) & Q(society_type_quality__in=societytype) & Q(
                                society_type_quantity__in=flatquantity))
                    elif societytype and flatquantity:
                        items = SupplierTypeSociety.objects.filter(
                            Q(society_subarea__in=citySubArea) & Q(society_type_quality__in=societytype) & Q(
                                society_type_quantity__in=flatquantity))
                    elif societytype and inventorytype:
                        items = SupplierTypeSociety.objects.filter(
                            Q(society_subarea__in=citySubArea) & Q(society_type_quality__in=societytype))
                    elif flatquantity and inventorytype:
                        items = SupplierTypeSociety.objects.filter(
                            Q(society_subarea__in=citySubArea) & Q(society_type_quantity__in=flatquantity))
                    elif societytype:
                        items = SupplierTypeSociety.objects.filter(
                            Q(society_subarea__in=citySubArea) & Q(society_type_quality__in=societytype))
                    elif flatquantity:
                        items = SupplierTypeSociety.objects.filter(
                            Q(society_subarea__in=citySubArea) & Q(society_type_quantity__in=flatquantity))
                    # elif inventorytype:
                    #     do something
                    else:
                        items = SupplierTypeSociety.objects.filter(society_subarea__in=citySubArea)

                elif areas:
                    if societytype and flatquantity and inventorytype:
                        items = SupplierTypeSociety.objects.filter(
                            Q(society_locality__in=cityArea) & Q(society_type_quality__in=societytype) & Q(
                                society_type_quantity__in=flatquantity))
                    elif societytype and flatquantity:
                        items = SupplierTypeSociety.objects.filter(
                            Q(society_locality__in=cityArea) & Q(society_type_quality__in=societytype) & Q(
                                society_type_quantity__in=flatquantity))
                    elif societytype and inventorytype:
                        items = SupplierTypeSociety.objects.filter(
                            Q(society_locality__in=cityArea) & Q(society_type_quality__in=societytype))
                    elif flatquantity and inventorytype:
                        items = SupplierTypeSociety.objects.filter(
                            Q(society_locality__in=cityArea) & Q(society_type_quantity__in=flatquantity))
                    elif societytype:
                        items = SupplierTypeSociety.objects.filter(
                            Q(society_locality__in=cityArea) & Q(society_type_quality__in=societytype))
                    elif flatquantity:
                        items = SupplierTypeSociety.objects.filter(
                            Q(society_locality__in=cityArea) & Q(society_type_quantity__in=flatquantity))
                    # elif inventorytype:
                    #     do something

                    else:
                        items = SupplierTypeSociety.objects.filter(society_locality__in=cityArea)

                elif societytype or flatquantity or inventorytype:
                    if societytype and flatquantity and inventorytype:
                        items = SupplierTypeSociety.objects.filter(
                            Q(society_type_quality__in=societytype) & Q(society_type_quantity__in=flatquantity))
                    elif societytype and flatquantity:
                        items = SupplierTypeSociety.objects.filter(
                            Q(society_type_quality__in=societytype) & Q(society_type_quantity__in=flatquantity))
                    elif societytype and inventorytype:
                        items = SupplierTypeSociety.objects.filter(Q(society_type_quality__in=societytype))
                    elif flatquantity and inventorytype:
                        items = SupplierTypeSociety.objects.filter(Q(society_type_quantity__in=flatquantity))
                    elif societytype:
                        items = SupplierTypeSociety.objects.filter(Q(society_type_quality__in=societytype))
                    elif flatquantity:
                        items = SupplierTypeSociety.objects.filter(Q(society_type_quantity__in=flatquantity))
                    # elif inventorytype:
                    #     do something

                else:
                    items = SupplierTypeSociety.objects.all()

                ## UISocietySerializer --> SocietyListSerializer
                # serializer = SocietyListSerializer(items, many= True)
                # Sample Code
            else:
                items = SupplierTypeSociety.objects.all()
                ## UISocietySerializer --> SocietyListSerializer

            serializer = SocietyListSerializer(items, many=True)
            # paginator = PageNumberPagination()
            # result_page = paginator.paginate_queryset(items, request)
            # serializer = SocietyListSerializer(result_page, many=True)

            # return paginator.get_paginated_response(serializer.data)

            return Response(serializer.data, status=200)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)

        # def set_paginator(self, paginator, serializer):
        #     self.filter_socities_paginator = paginator
        #     self.filter_socities_serializer = serializer

        # def get_paginator(self):
        #     return self.filter_socities_paginator,

class SocietyAPISortedListView(APIView):
    def post(self, request, format=None):
        order = request.query_params.get('order', None)
        society_ids = request.data

        if order == 'asc':
            societies = SupplierTypeSociety.objects.filter(supplier_id__in=society_ids).order_by('society_name')
            serializer = SocietyListSerializer(societies, many=True)
            return Response(serializer.data, status=200)
        elif order == 'desc':
            societies = SupplierTypeSociety.objects.filter(supplier_id__in=society_ids).order_by('-society_name')
            serializer = SocietyListSerializer(societies, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response(status=200)

class SocietyAPISocietyIdsView(APIView):
    def get(self, request, format=None):
        society_ids = SupplierTypeSociety.objects.all().values_list('supplier_id', flat=True)
        return Response({'society_ids': society_ids}, status=200)

class SupplierInfoAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = SupplierInfo.objects.get(pk=id)
            serializer = SupplierInfoSerializer(item)
            return Response(serializer.data)
        except SupplierInfo.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = SupplierInfo.objects.get(pk=id)
        except SupplierInfo.DoesNotExist:
            return Response(status=404)
        serializer = SupplierInfoSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = SupplierInfo.objects.get(pk=id)
        except SupplierInfo.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)

class SupplierInfoAPIListView(APIView):

    def get(self, request, format=None):
        items = SupplierInfo.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = SupplierInfoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = SupplierInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class SupplierTypeSocietyAPIListView(APIView):

    def get(self, request, format=None):
        items = SupplierTypeSociety.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = SupplierTypeSocietySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        """
        Args:
            request: request param containg society data
            format: none

        Returns: The data created by this particular user
        """
        serializer = SupplierTypeSocietySerializer(data=request.data)
        current_user = request.user
        if serializer.is_valid():
            serializer.save(created_by=current_user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class SupplierTypeSocietyAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = SupplierTypeSociety.objects.get(pk=id)
            serializer = SupplierTypeSocietySerializer(item)
            return Response(serializer.data)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = SupplierTypeSociety.objects.get(pk=id)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        serializer = SupplierTypeSocietySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = SupplierTypeSociety.objects.get(pk=id)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)

class RetailShopViewSet(viewsets.ViewSet):
    """
    View Set around RetailShop
    """

    def create(self, request):

        class_name = self.__class__.__name__
        try:
            serializer = RetailShopSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return handle_response(class_name, data=serializer.data, success=True)
            return handle_response(class_name, data=serializer.errors)
        except Exception as e:
            return handle_response(class_name, exception_object=e, request=request)

    def list(self, request):
        class_name = self.__class__.__name__
        try:
            # all retail_shop_objects sorted by name
            user = request.user
            if user.is_superuser:
                retail_shop_objects = SupplierTypeRetailShop.objects.all().order_by('name')
            else:
                city_query = get_region_based_query(user, v0_constants.valid_regions['CITY'],
                                                             v0_constants.retail_shop_code)
                retail_shop_objects = SupplierTypeRetailShop.objects.filter(city_query)
            serializer = RetailShopSerializer(retail_shop_objects, many=True)
            retail_shop_with_images = get_supplier_image(serializer.data, 'Retail Shop')

            # disabling paginators because search cannot be performed in front end in whole data set
            # paginator = PageNumberPagination()
            # result_page = paginator.paginate_queryset(retail_shop_with_images, request)
            # paginator_response = paginator.get_paginated_response(result_page)
            data = {
                'count': len(serializer.data),
                'retail_shop_objects': retail_shop_with_images
            }
            return handle_response(class_name, data=data, success=True)
        except Exception as e:
            return handle_response(class_name, exception_object=e, request=request)

    def update(self, request, pk):
        class_name = self.__class__.__name__
        try:
            retail_shop_instance = SupplierTypeRetailShop.objects.get(pk=pk)
            serializer = RetailShopSerializer(instance=retail_shop_instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return handle_response(class_name, data=serializer.data, success=True)
            return handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return handle_response(class_name, exception_object=e, request=request)

    def retrieve(self, request, pk):
        class_name = self.__class__.__name__
        try:
            retail_shop_instance = SupplierTypeRetailShop.objects.get(pk=pk)
            serializer = RetailShopSerializer(instance=retail_shop_instance)
            return handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return handle_response(class_name, exception_object=e, request=request)

class SaveBasicCorporateDetailsAPIView(APIView):

    def post(self, request, id, format=None):
        class_name = self.__class__.__name__

        try:

            companies = []
            error = {}

            # Round 1 Saving basic data
            if 'supplier_id' in request.data:
                corporate = SupplierTypeCorporate.objects.filter(pk=request.data['supplier_id']).first()
                if corporate:
                    corporate_serializer = SupplierTypeCorporateSerializer(corporate, data=request.data)
                else:
                    corporate_serializer = SupplierTypeCorporateSerializer(data=request.data)
                if corporate_serializer.is_valid():
                    corporate_serializer.save()
                else:
                    error['message'] = 'Invalid Corporate Info data'
                    error = json.dumps(error)
                    return Response(corporate_serializer.errors, status=406)
            else:
                return Response({"status": False, "error": "No supplier id in request.data"},
                                status=status.HTTP_400_BAD_REQUEST)

            # Round 2 Saving List of companies

            corporate_id = request.data['supplier_id']

            companies_name = request.data.get('list1')
            company_ids = list(
                CorporateParkCompanyList.objects.filter(supplier_id=corporate_id).values_list('id', flat=True))

            for company_name in companies_name:
                if 'id' in company_name:
                    company = CorporateParkCompanyList.objects.get(id=id)
                    company.name = company_name
                    company_ids.remove(company.id)
                    companies.append(company)
                else:
                    company = CorporateParkCompanyList(supplier_id_id=corporate_id, name=company_name)
                    companies.append(company)

            CorporateParkCompanyList.objects.bulk_create(companies)
            CorporateParkCompanyList.objects.filter(id__in=company_ids).delete()

            # Round 3 - Saving contacts

            try:
                instance = SupplierTypeCorporate.objects.get(supplier_id=id)
            except SupplierTypeCorporate.DoesNotExist:
                return Response({'message': 'This corporate park does not exist'}, status=406)

            content_type = ContentType.objects.get_for_model(SupplierTypeCorporate)
            object_id = instance.supplier_id
            # in order to save get calls in a loop, prefetch all the contacts for this supplier beforehand
            # making a dict which key is object id and contains another
            contact_detail_objects = {contact.id: contact for contact in
                                      ContactDetails.objects.filter(content_type=content_type, object_id=object_id)}

            # get all contact id's in a set. Required for contact deletion
            contact_detail_ids = set([contact_id for contact_id in contact_detail_objects.keys()])

            for contact in request.data.get('contacts'):

                # make the data you want to save in contacts
                contact_data = {
                    'name': contact.get('name'),
                    'country_code': contact.get('countrycode'),
                    'std_code': contact.get('std_code'),
                    'mobile': contact.get('mobile'),
                    'contact_type': contact.get('contact_type'),
                    'object_id': object_id,
                    'content_type': content_type.id,
                    'email': contact.get('email'),
                    'salutation': contact.get('salutation'),
                    'landline': contact.get('landline'),
                }

                # get the contact instance to be updated if id was present else create a brand new instance
                contact_instance = contact_detail_objects[contact['id']] if 'id' in contact else None

                # if contact instance was there this means this is an update request. we need to remove this id
                # from the set of id's we are maintaining because we do not want this instance to be deleted.

                if contact_instance:
                    contact_detail_ids.remove(contact['id'])

                # save the data
                serializer = ContactDetailsSerializer(contact_instance, data=contact_data)

                if serializer.is_valid():
                    serializer.save()
                else:
                    return handle_response(class_name, data=serializer.errors)

            # in the end we need to delete the crossed out contacts. all contacts now in the list of ids are
            # being deleted by the user hence we delete it from here too.
            ContactDetails.objects.filter(id__in=contact_detail_ids).delete()

            # todo: to be changed later
            '''

            content_type = ContentType.objects.get_for_model(SupplierTypeCorporate)

            contacts_ids = ContactDetailsGeneric.objects.filter(content_type=content_type, object_id=instance.supplier_id).values_list('id',flat=True)
            contacts_ids = list(contacts_ids)


            for contact in request.data['contacts']:
                if 'id' in contact:
                    contact_instance = ContactDetailsGeneric.objects.get(id=contact['id'])
                    contacts_ids.remove(contact_instance.id)
                    serializer = ContactDetailsGenericSerializer(contact_instance, data=contact)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return Response(status=404)

                else:
                    contact['object_id'] = instance.supplier_id
                    serializer = ContactDetailsGenericSerializer(data=contact)
                    if serializer.is_valid():
                        serializer.save(content_type=content_type)
                    else:
                        return Response(status=404)

            ContactDetailsGeneric.objects.filter(id__in=contacts_ids).delete()

            '''
            # Round 4 - Creating number of fields in front end in Building Model.
            buildingcount = CorporateBuilding.objects.filter(corporatepark_id=request.data['supplier_id']).count()
            diff_count = 0
            new_list = []
            building_count_recieved = int(request.data['building_count'])
            if building_count_recieved > buildingcount:
                diff_count = building_count_recieved - buildingcount
            if 'building_count' in request.data:
                for i in range(diff_count):
                    instance = CorporateBuilding(corporatepark_id_id=request.data['supplier_id'])
                    new_list.append(instance)

            CorporateBuilding.objects.bulk_create(new_list)

        except KeyError as e:
            return Response({"status": False, "error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            return Response({"status": False, "error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": False, "error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=200)

    def get(self, request, id, format=None):
        try:

            supplier = SupplierTypeCorporate.objects.get(supplier_id=id)
            serializer = SupplierTypeCorporateSerializer(supplier)
            companies = CorporateParkCompanyList.objects.filter(supplier_id=id)
            corporate_serializer = CorporateParkCompanyListSerializer(companies, many=True)
            content_type = ContentType.objects.get_for_model(model=SupplierTypeCorporate)
            contacts = ContactDetails.objects.filter(content_type=content_type, object_id=id)
            contacts_serializer = ContactDetailsSerializer(contacts, many=True)
            result = {'basicData': serializer.data, 'companyList': corporate_serializer.data,
                      'contactData': contacts_serializer.data}
            return Response(result)

        except ObjectDoesNotExist as e:
            return Response({"status": False, "error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
        except MultipleObjectsReturned as e:
            return Response({"status": False, "error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": False, "error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)


# This API is for saving the buildings and wings details of a corporate space

class SaveBuildingDetailsAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            corporate = SupplierTypeCorporate.objects.get(supplier_id=id)
        except SupplierTypeCorporate.DoesNotExist:
            return Response({'message': 'Invalid Corporate ID'}, status=status.HTTP_400_BAD_REQUEST)

        buildings = corporate.get_buildings()
        building_serializer = CorporateBuildingGetSerializer(buildings, many=True)
        return Response(building_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id, format=None):

        try:
            corporate_object = SupplierTypeCorporate.objects.get(supplier_id=id)
        except SupplierTypeCorporate.DoesNotExist:
            return Response({'message': 'Invalid Corporate ID'}, status=status.HTTP_400_BAD_REQUEST)

        try:

            building_count = len(request.data)
            if corporate_object.building_count != building_count:
                corporate_object.building_count = building_count
                corporate_object.save()

            buildings_ids = set(
                CorporateBuilding.objects.filter(corporatepark_id=corporate_object).values_list('id', flat=True))
            wing_ids_superset = set()

            # Logic for delete - Put all currently present fields in the database into a list.
            # Check the received data from front-end, if ID of any field matches with any in the list, remove that field from list.
            # In the end, delete all the fields left in the list.

            for building in request.data:
                if 'id' in building:
                    basic_data_instance = CorporateBuilding.objects.get(id=building['id'])
                    buildings_ids.remove(building['id'])
                    building_serializer = CorporateBuildingSerializer(basic_data_instance, data=building)
                else:
                    building_serializer = CorporateBuildingSerializer(data=building)

                if building_serializer.is_valid():
                    building_object = building_serializer.save()
                else:
                    return Response(status=406)

                wings_ids = set(
                    CorporateBuildingWing.objects.filter(building_id=building_object).values_list('id', flat=True))

                for wing in building['wingInfo']:

                    if 'id' in wing:
                        wing_object = CorporateBuildingWing.objects.get(id=wing['id'])
                        wings_ids.remove(wing_object.id)
                        wing_serializer = CorporateBuildingWingSerializer(wing_object, data=wing)
                    else:
                        wing_serializer = CorporateBuildingWingSerializer(data=wing)

                    if wing_serializer.is_valid():
                        wing_serializer.save(building_id=building_object)
                    else:
                        return Response({'message': 'Invalid Wing Data', \
                                         'errors': wing_serializer.errors}, status=406)

                if wings_ids:
                    wing_ids_superset = wing_ids_superset.union(wings_ids)

            if wing_ids_superset:
                CorporateBuildingWing.objects.filter(id__in=wing_ids_superset).delete()
            if buildings_ids:
                CorporateBuilding.objects.filter(id__in=buildings_ids).delete()

            return Response({"status": True, "data": ""}, status=status.HTTP_200_OK)

        except KeyError as e:
            return Response({"status": False, "error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            return Response({"status": False, "error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": False, "error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)


# This API is for fetching the companies and buildings of a specific corporate space.
class CompanyDetailsAPIView(APIView):
    def get(self, request, id, format=True):
        company = SupplierTypeCorporate.objects.get(supplier_id=id)
        company_list = CorporateParkCompanyList.objects.filter(supplier_id_id=company)
        serializer = CorporateParkCompanyListSerializer(company_list, many=True)
        building = SupplierTypeCorporate.objects.get(supplier_id=id)
        building_list = CorporateBuilding.objects.filter(corporatepark_id_id=building)
        serializer1 = CorporateBuildingGetSerializer(building_list, many=True)
        response_dict = {'companies': serializer.data, 'buildings': serializer1.data}
        return Response(response_dict, status=200)


class CorporateCompanyDetailsAPIView(APIView):
    '''
    This API is for saving details of all companies belonging to a specific corporate space.
    '''

    def get(self, request, id=None, format=None):
        try:
            corporate = SupplierTypeCorporate.objects.get(supplier_id=id)
        except SupplierTypeCorporate.DoesNotExist:
            return Response({'message': 'No such Corporate'}, status=406)

        companies = corporate.get_corporate_companies()
        companies_serializer = CorporateParkCompanySerializer(companies, many=True)

        return Response(companies_serializer.data, status=200)

    def post(self, request, id, format=True):
        try:
            corporate = SupplierTypeCorporate.objects.get(supplier_id=id)
        except SupplierTypeCorporate.DoesNotExist:
            return Response({'message': "Corporate Doesn't Exist"}, status=404)

        company_detail_list = []
        floor_list = []
        company_detail_ids = set(
            CorporateCompanyDetails.objects.filter(company_id__supplier_id=corporate).values_list('id', flat=True))
        floor_superset = set()
        company_detail_set = set()
        flag = False

        for company in request.data:
            for company_detail in company['companyDetailList']:
                try:
                    if not company_detail['building_name']:
                        continue
                    # get the right CorporateCompanyDetails object if 'id' exist in the company_detail object.
                    company_detail_instance = CorporateCompanyDetails.objects.get(id=company_detail['id'])

                    # set the id of the company for which this object belongs to
                    company_detail['company_id'] = company['id']

                    # remove the id of CorporateCompanyDetails object from the set of id's.
                    company_detail_ids.remove(company_detail['id'])

                    # update this instance with new data
                    company_detail_instance.__dict__.update(company_detail)

                    # save
                    company_detail_instance.save()

                    flag = True
                except KeyError:
                    # create the CorporateCompanyDetails object if 'id' is not in company_detail object
                    company_detail_instance = CorporateCompanyDetails(company_id_id=company['id'],
                                                                      building_name=company_detail['building_name'],
                                                                      wing_name=company_detail['wing_name'])
                    # company_detail_list.append(company_detail_instance)
                    # uncomment this line if error occurs
                    company_detail_instance.save()
                    flag = False
                # if the CorporateCompanyDetails object was updated
                if flag:
                    # for a given building, find all the floors
                    floor_ids = set(
                        CompanyFloor.objects.filter(company_details_id_id=company_detail_instance.id).values_list('id',
                                                                                                                  flat=True))

                    # for each floor object in company_details['listOfFloors']
                    for floor in company_detail['listOfFloors']:
                        try:
                            # get the floor object
                            floor_instance = CompanyFloor.objects.get(id=floor['id'])

                            # remove the floor id from set of floor id's
                            floor_ids.remove(floor_instance.id)

                            # if the floor number for this building is same as new floor number no point in updating
                            if floor_instance.floor_number == floor['floor_number']:
                                continue

                            # else update the new floor number and also save for which building ( CorporateCompanyDetails ) this floor was updated
                            floor_instance.company_detail_id, floor_instance.floor_number = company_detail_instance, \
                                                                                            floor['floor_number']

                            # floor_instance.__dict__.update(floor)
                            floor_instance.save()
                        except KeyError:
                            # if we do not find the floor object , create a new Floor object for this building instance
                            floor_list_instance = CompanyFloor(company_details_id=company_detail_instance,
                                                               floor_number=floor['floor_number'])

                            # append the floor instance to floor_list
                            floor_list.append(floor_list_instance)
                    floor_superset = floor_superset.union(floor_ids)

                # if CorporateCompanydetails was not updated , it was created fresh new, then create new floor objects
                else:
                    # for each floor
                    for floor in company_detail['listOfFloors']:
                        # create a new floor object
                        floor_list_instance = CompanyFloor(company_details_id=company_detail_instance,
                                                           floor_number=floor['floor_number'])
                        floor_list.append(floor_list_instance)

        # floor_list = []
        #         for floor in company_detail['listOfFloors']:
        #             floor_list_instance = CompanyFloor(company_details_id=company_detail_instance,floor_number=floor)
        #             floor_list.append(floor_list_instance)
        #         CompanyFloor.objects.bulk_create(floor_list)

        # CorporateCompanyDetails.objects.bulk_create(company_detail_list)
        CompanyFloor.objects.filter(id__in=floor_superset).delete()
        CorporateCompanyDetails.objects.filter(id__in=company_detail_ids).delete()
        # create all the floor objects at once
        CompanyFloor.objects.bulk_create(floor_list)
        return Response(status=200)


# Saving and fetching basic data of a salon.
class saveBasicSalonDetailsAPIView(APIView):
    def get(self, request, id, format=None):
        try:
            data1 = SupplierTypeSalon.objects.get(supplier_id=id)
            serializer = SupplierTypeSalonSerializer(data1)
            data2 = ContactDetailsGeneric.objects.filter(object_id=id)
            serializer1 = ContactDetailsGenericSerializer(data2, many=True)
            result = {'basicData': serializer.data, 'contactData': serializer1.data}
            return Response(result)
        except SupplierTypeSalon.DoesNotExist:
            return Response(status=404)
        except SupplierTypeSalon.MultipleObjectsReturned:
            return Response(status=406)

    def post(self, request, id, format=None):
        error = {}
        if 'supplier_id' in request.data:
            salon = SupplierTypeSalon.objects.filter(pk=request.data['supplier_id']).first()
            if salon:
                salon_serializer = SupplierTypeSalonSerializer(salon, data=request.data)
            else:
                salon_serializer = SupplierTypeSalonSerializer(data=request.data)
        if salon_serializer.is_valid():
            salon_serializer.save()
        else:
            error['message'] = 'Invalid Salon Info data'
            error = json.dumps(error)
            return Response(response, status=406)

        # Now saving contacts
        try:
            instance = SupplierTypeSalon.objects.get(supplier_id=id)
        except SupplierTypeSalon.DoesNotExist:
            return Response({'message': 'This salon does not exist'}, status=406)

        content_type = ContentType.objects.get_for_model(SupplierTypeSalon)

        contacts_ids = ContactDetailsGeneric.objects.filter(content_type=content_type,
                                                            object_id=instance.supplier_id).values_list('id', flat=True)
        contacts_ids = list(contacts_ids)

        for contact in request.data['contacts']:
            if 'id' in contact:
                contact_instance = ContactDetailsGeneric.objects.get(id=contact['id'])
                contacts_ids.remove(contact_instance.id)
                serializer = ContactDetailsGenericSerializer(contact_instance, data=contact)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(status=404)

            else:
                contact['object_id'] = instance.supplier_id
                serializer = ContactDetailsGenericSerializer(data=contact)
                if serializer.is_valid():
                    serializer.save(content_type=content_type)
                else:
                    return Response(status=404)

        ContactDetailsGeneric.objects.filter(id__in=contacts_ids).delete()
        return Response(status=200)

        # End of contact saving


# Saving and fetching basic data of a gym.
class saveBasicGymDetailsAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            data1 = SupplierTypeGym.objects.get(supplier_id=id)
            serializer = SupplierTypeGymSerializer(data1)
            data2 = ContactDetailsGeneric.objects.filter(object_id=id)
            serializer1 = ContactDetailsGenericSerializer(data2, many=True)
            result = {'basicData': serializer.data, 'contactData': serializer1.data}
            return Response(result)
        except SupplierTypeGym.DoesNotExist:
            return Response(status=404)
        except SupplierTypeGym.MultipleObjectsReturned:
            return Response(status=406)

    def post(self, request, id, format=None):
        error = {}
        class_name = self.__class__.__name__
        if 'supplier_id' in request.data:
            gym = SupplierTypeGym.objects.filter(pk=request.data['supplier_id']).first()
            if gym:
                gym_serializer = SupplierTypeGymSerializer(gym, data=request.data)
            else:
                gym_serializer = SupplierTypeGymSerializer(data=request.data)
        if gym_serializer.is_valid():
            gym_serializer.save()
        else:
            return handle_response(class_name, data='Invalid Gym Info data')

        # Now saving contacts
        try:
            instance = SupplierTypeGym.objects.get(supplier_id=id)
        except SupplierTypeGym.DoesNotExist:
            return Response({'message': 'This gym does not exist'}, status=406)

        content_type = ContentType.objects.get_for_model(SupplierTypeGym)

        contacts_ids = ContactDetailsGeneric.objects.filter(content_type=content_type,
                                                            object_id=instance.supplier_id).values_list('id', flat=True)
        contacts_ids = list(contacts_ids)

        for contact in request.data['contacts']:
            if 'id' in contact:
                contact_instance = ContactDetailsGeneric.objects.get(id=contact['id'])
                contacts_ids.remove(contact_instance.id)
                serializer = ContactDetailsGenericSerializer(contact_instance, data=contact)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(status=404)

            else:
                contact['object_id'] = instance.supplier_id
                serializer = ContactDetailsGenericSerializer(data=contact)
                if serializer.is_valid():
                    serializer.save(content_type=content_type)
                else:
                    return Response(status=404)

        ContactDetailsGeneric.objects.filter(id__in=contacts_ids).delete()
        return Response(status=200)

        # End of contact Saving


class BusShelter(APIView):
    """
    The class provides api's for fetching and saving Bus Shelter details
    """

    def post(self, request, id):

        """
        API saves Bus Shelter details
        ---
        parameters:
        - name: supplier_type_code
          required: true
        - name: lit_status
        - name: halt_buses_count
        - name: name
        """

        # save the name of the class you are in to be useful for logging purposes
        class_name = self.__class__.__name__

        # check for supplier_type_code
        supplier_type_code = request.data.get('supplier_type_code')
        if not supplier_type_code:
            return handle_response(class_name, data='provide supplier type code', success=False)
        data = request.data.copy()
        data['supplier_id'] = id
        basic_details_response = save_basic_supplier_details(supplier_type_code, data)
        if not basic_details_response.data['status']:
            return basic_details_response
        return handle_response(class_name, data=basic_details_response.data['data'], success=True)

    def get(self, request):
        # fetch all and list Bus Shelters

        class_name = self.__class__.__name__

        try:
            user = request.user

            if user.is_superuser:
                bus_objects = SupplierTypeBusShelter.objects.all().order_by('name')
            else:
                city_query = get_region_based_query(user, v0_constants.valid_regions['CITY'],
                                                             v0_constants.bus_shelter)
                bus_objects = SupplierTypeBusShelter.objects.filter(city_query)

            bus_shelter_serializer = BusShelterSerializer(bus_objects, many=True)
            items = get_supplier_image(bus_shelter_serializer.data, 'Bus Shelter')
            # disabling pagination because search cannot be performed in whole data set.
            # paginator = PageNumberPagination()
            # result_page = paginator.paginate_queryset(items, request)
            # paginator_response = paginator.get_paginated_response(result_page)
            data = {
                'count': len(bus_shelter_serializer.data),
                'busshelters': items
            }
            return handle_response(class_name, data=data, success=True)
        except SupplierTypeBusShelter.DoesNotExist as e:
            return handle_response(class_name, data='Bus Shelter object does not exist', exception_object=e)
        except Exception as e:
            return handle_response(class_name, exception_object=e, request=request)


class BusShelterSearchView(APIView):
    """
    Searches particular bus shelters on the basis of search query
    """

    def get(self, request, format=None):
        """
        GET api fetches all bus shelters on search query. later it's implentation will be changed.
        """

        class_name = self.__class__.__name__
        try:
            user = request.user
            search_txt = request.query_params.get('search', None)
            if not search_txt:
                return handle_response(class_name, data='Search Text is not provided')
            items = SupplierTypeBusShelter.objects.filter(
                Q(supplier_id__icontains=search_txt) | Q(name__icontains=search_txt) | Q(
                    address1__icontains=search_txt) | Q(city__icontains=search_txt) | Q(
                    state__icontains=search_txt)).order_by('name')
            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(items, request)
            serializer = SupplierTypeBusShelterSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except SupplierTypeBusShelter.DoesNotExist as e:
            return handle_response(class_name, data='Bus Shelter object does not exist', exception_object=e)
        except Exception as e:
            return handle_response(class_name, exception_object=e, request=request)


class SocietyAPIListView(APIView):

    def get(self, request):
        class_name = self.__class__.__name__
        try:
            user = request.user

            search_txt = request.query_params.get('search', None)
            if search_txt:
                society_objects = SupplierTypeSociety.objects.filter(
                    Q(supplier_id__icontains=search_txt) | Q(society_name__icontains=search_txt) | Q(
                        society_address1__icontains=search_txt) | Q(society_city__icontains=search_txt) | Q(
                        society_state__icontains=search_txt)).order_by('society_name')
            else:
                if user.is_superuser:
                    society_objects = SupplierTypeSociety.objects.all().order_by('society_name')
                else:
                    city_query = get_region_based_query(user, v0_constants.valid_regions['CITY'],
                                                        v0_constants.society)
                    society_objects = SupplierTypeSociety.objects.filter(city_query)

            # modify items to have society images data
            society_objects = get_supplier_image(society_objects, 'Society')
            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(society_objects, request)
            paginator_response = paginator.get_paginated_response(result_page)
            data = {
                'count': len(society_objects),
                'societies': paginator_response.data
            }
            return handle_response(class_name, data=data, success=True)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)


class SuppliersMeta(APIView):
    """
    Fetches meta information about suppliers. How many are there in the system, count of each one of them how many
    of them have pricing, how many don't
    """

    def get(self, request):
        """

        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            valid_supplier_type_code_instances = SupplierTypeCode.objects.all()
            data = {}

            for instance in valid_supplier_type_code_instances:
                supplier_type_code = instance.supplier_type_code
                error = False
                try:
                    model_name = get_model(supplier_type_code)
                    count = model_name.objects.all().count()
                except Exception:
                    count = 0
                    error = True

                data[supplier_type_code] = {
                    'count': count,
                    'name': instance.supplier_type_name,
                    'error': error
                }
                if supplier_type_code == v0_constants.retail_shop_code:
                    data[supplier_type_code]['retail_shop_types'] = [tup[0] for tup in RETAIL_SHOP_TYPE]

            return handle_response(class_name, data=data, success=True)
        except Exception as e:
            return handle_response(class_name, exception_object=e, request=request)


class BusDepotViewSet(viewsets.ViewSet):
    """
    ViewSet around Bus depot
    """

    def create(self, request):
        class_name = self.__class__.__name__
        try:
            data = request.data
            serializer = BusDepotSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return handle_response(class_name, data=serializer.data, success=True)
            return handle_response(class_name, data=serializer.errors)
        except Exception as e:
            return handle_response(class_name, exception_object=e, request=request)

    def list(self, request):
        class_name = self.__class__.__name__
        try:
            bus_depots = SupplierTypeBusDepot.objects.all()
            serializer = BusDepotSerializer(bus_depots, many=True)
            return handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return handle_response(class_name, exception_object=e, request=request)

    def update(self, request, pk=None):
        class_name = self.__class__.__name__
        try:
            instance = SupplierTypeBusDepot.objects.get(pk=pk)
            serializer = BusDepotSerializer(instance=instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return handle_response(class_name, data=serializer.data, success=True)
            return handle_response(class_name, data=serializer.errors)
        except Exception as e:
            return handle_response(class_name, exception_object=e, request=request)

    def retrieve(self, request, pk=None):
        class_name = self.__class__.__name__
        try:
            instance = SupplierTypeBusDepot.objects.get(pk=pk)
            serializer = BusDepotSerializer(instance=instance)
            return handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return handle_response(class_name, exception_object=e, request=request)