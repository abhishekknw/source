from __future__ import print_function
from __future__ import absolute_import
# python core imports
import csv
import json
import openpyxl

# django imports
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.forms.models import model_to_dict

# third party imports
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import list_route
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .serializers import UISocietySerializer, UITowerSerializer
from v0.ui.events.serializers import EventsSerializer
from v0.ui.supplier.serializers import CorporateBuildingSerializer, CorporateParkCompanySerializer, \
    CorporateBuildingGetSerializer

from v0.ui.events.models import Events, SocietyMajorEvents
from v0.ui.components.models import CommunityHallInfo, LiftDetails, NoticeBoardDetails, SocietyFlat, \
    SwimmingPoolInfo,  SportsInfra, SocietyTower, FlatType, MailboxInfo, CorporateBuildingWing, CompanyFloor
from v0.ui.components.serializers import CommunityHallInfoSerializer, LiftDetailsSerializer, NoticeBoardDetailsSerializer, \
    FlatTypeSerializer, SocietyTowerSerializer, SocietyFlatSerializer, SportsInfraSerializer, \
    SwimmingPoolInfoSerializer, CorporateBuildingWingSerializer
from v0.ui.finances.models import DoorToDoorInfo, PriceMapping, PriceMappingDefault
from v0.ui.finances.serializers import PriceMappingDefaultSerializer, PriceMappingSerializer

from v0.ui.location.models import City, CityArea, CitySubArea, State
from v0.ui.events.serializers import SocietyMajorEventsSerializer
from v0.ui.user.serializers import UserSerializer, UserProfileSerializer
from v0.ui.location.serializers import CitySerializer, CityAreaSerializer, CitySubAreaSerializer, StateSerializer
from v0.ui.account.models import ContactDetails, ContactDetailsGeneric
from v0.ui.account.serializers import (ContactDetailsSerializer, ContactDetailsGenericSerializer)
from .inventory.models import (PosterInventory, InventorySummary, StreetFurniture,
                              StallInventory, FlyerInventory, StandeeInventory, PoleInventory, SupplierTypeSociety,
                              InventorySummary, WallInventory)
from .inventory.serializers import PosterInventorySerializer
from v0.ui.supplier.models import SupplierTypeSociety, SupplierTypeCorporate, SupplierAmenitiesMap, SupplierTypeCode, \
    SupplierTypeSalon, SupplierTypeGym, SupplierTypeBusShelter, CorporateBuilding, CorporateParkCompanyList, \
    RETAIL_SHOP_TYPE
from v0.ui.supplier.serializers import (SupplierTypeCorporateSerializer, SupplierTypeSalonSerializer,
                        SupplierTypeGymSerializer, SupplierTypeBusShelterSerializer, UICorporateSerializer, UISalonSerializer,
                        SupplierTypeCodeSerializer, SupplierTypeSocietySerializer, CorporateCompanyDetails,
                        CorporateParkCompanyListSerializer, RetailShopSerializer, BusDepotSerializer, BusShelterSerializer)
from .inventory.serializers import (StandeeInventorySerializer, WallInventorySerializer, PoleInventorySerializer,
                                   StallInventorySerializer, StreetFurnitureSerializer, FlyerInventorySerializer,
                                   InventorySummarySerializer)
from v0.ui.proposal.models import ImageMapping
from v0.ui.proposal.serializers import ImageMappingSerializer

# project imports
from . import utils as ui_utils
import v0.ui.website.utils as website_utils
from coreapi.settings import BASE_DIR
from v0.ui.user.models import UserAreas, UserCities, UserProfile
from v0.ui.common.models import BaseUser
from v0.constants import keys, decision
from .website.utils import save_price_mapping_default
import v0.constants as v0_constants
from .utils import get_from_dict
from .controller import inventory_summary_insert

class UsersProfilesAPIView(APIView):

    def get(self, request, format=None):
        user = request.user
        if user.user_profile.all().first() and user.user_profile.all().first().is_city_manager:
            users1 = []
            for u in UserProfile.objects.filter(Q(is_normal_user=True)).select_related('user'):
                users1.append(u.user)
            users = []
            cities = [item.city for item in user.cities.all()]
            for u in UserCities.objects.filter(city__in=cities, user__in=users1).select_related('user'):
                users.append(u.user)
            areas = CityArea.objects.filter(city_code__in=cities)
            users1 = []
            for u in UserProfile.objects.filter(Q(is_cluster_manager=True)).select_related('user'):
                users1.append(u.user)
            for u in UserAreas.objects.filter(area__in=areas, user__in=users1).select_related('user'):
                users.append(u.user)
            for u in UserProfile.objects.filter(created_by=user).select_related('user'):
                users.append(u.user)
        else:
            users = BaseUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=200)

    def post(self, request, format=None):
        data = request.data
        data['user_permissions'] = []
        data['groups'] = []

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=400)
        user = BaseUser.objects.get(pk=serializer.data['id'])
        up = UserProfile(user=user, created_by=request.user)
        up.save()
        return Response(serializer.data, status=200)


class getUserData(APIView):

    def get(self, request, id, format=None):
        user = BaseUser.objects.get(pk=id)
        user_profile = user.user_profile.all().first()
        user_serializer = UserSerializer(user)
        serializer = UserProfileSerializer(user_profile)
        # city_ids = UserCities.objects.filter(user__id=id).values_list('city__id', flat=True)
        # area_ids = UserAreas.objects.filter(user__id=id).values_list('area__id', flat=True)
        # result = {'user':user_serializer.data, 'user_profile':serializer.data, 'selectedCities':city_ids, 'selectedAreas': area_ids}
        result = {'user': user_serializer.data, 'user_profile': serializer.data}
        return Response(result, status=200)

    def post(self, request, id, format=None):
        data = request.data
        user = BaseUser.objects.get(pk=id)
        serializer = UserSerializer(user, data=data['user'])
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=400)
        if 'id' in data['user_profile']:
            profile = UserProfile.objects.get(pk=data['user_profile']['id'])
            serializer = UserProfileSerializer(profile, data=data['user_profile'])
        else:
            data['user_profile']['user'] = id
            serializer = UserProfileSerializer(data=data['user_profile'])
        if serializer.is_valid():
            serializer.save(user=user)
        else:
            return Response(serializer.errors, status=400)

        prev_ids = UserCities.objectsself.filter(user__id=id).values_list('city__id', flat=True)
        new_ids = request.data['selectedCities']
        del_diff = list(set(prev_ids) - set(new_ids))
        new_diff = list(set(new_ids) - set(prev_ids))
        if del_diff:
            UserCities.objects.filter(user__id=id, city__id__in=del_diff).delete()
        if len(new_diff) > 0:
            for key in new_diff:
                UserCities.objects.create(user=user, city_id=key)

        prev_ids = UserAreas.objects.filter(user__id=id).values_list('area__id', flat=True)
        new_ids = request.data['selectedAreas']
        del_diff = list(set(prev_ids) - set(new_ids))
        new_diff = list(set(new_ids) - set(prev_ids))
        if del_diff:
            UserAreas.objects.filter(user__id=id, area__id__in=del_diff).delete()
        if len(new_diff) > 0:
            for key in new_diff:
                UserAreas.objects.create(user=user, area_id=key)

        return Response(status=200)

    # to update password
    def put(self, request, id, format=None):
        user = BaseUser.objects.get(pk=id)
        user.set_password(request.data['password'])
        user.save()
        return Response(status=200)

    def delete(self, request, id, format=None):
        try:
            item = BaseUser.objects.get(pk=id)
        except User.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class deleteUsersAPIView(APIView):

    def post(self, request, format=None):
        BaseUser.objects.filter(id__in=request.data).delete()
        return Response(status=204)


class GetInitialDataAPIView(APIView):

    def get(self, request):
        class_name = self.__class__.__name__
        try:
            cities = City.objects.all()
            city_serializer = CitySerializer(cities, many=True)
            items = SupplierTypeCode.objects.all()
            supplier_code_serializer = SupplierTypeCodeSerializer(items, many=True)
            result = {'cities': city_serializer.data, 'supplier_types': supplier_code_serializer.data}
            return Response(result, status=200)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


class LocationsAPIView(APIView):
    def get(self, request, id, format=None):
        class_name = self.__class__.__name__
        try:
            type = request.query_params.get('type', None)
            if type == 'city':
                items = City.objects.filter(state_code__id=id)
                serializer = CitySerializer(items, many=True)
            elif type == 'areas':
                items = CityArea.objects.filter(city_code__id=id)
                serializer = CityAreaSerializer(items, many=True)
            elif type == 'sub_areas':
                items = CitySubArea.objects.filter(area_code__id=id)
                serializer = CitySubAreaSerializer(items, many=True)
            return Response(serializer.data)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    def post(self, request, id, format=None):
        class_name = self.__class__.__name__
        request_data = request.data
        city_name = request_data.get("city_name", None)
        city_id = request_data.get("city_id", None)
        city_code = request_data.get("city_code", None)
        area_name = request_data.get("area_name", None)
        subarea_name = request_data.get("subarea_name", None)
        area_id = request_data.get("area_id", None)
        
        try:
            if not city_id:
                city_dict ={}
                city_dict['city_name'] = city_name.title()
                city_dict['city_code'] = city_code.upper()
                city_dict['state_code'] = int(id)
                city_serializer = CitySerializer(data=city_dict)
                if city_serializer.is_valid():
                    city_instance = city_serializer.save()
                    city_id = city_instance.id
                else:
                    return Response({"message":"City already exists!"}, status=400)

            if not area_id:
                area_dict ={}
                area_dict['label'] = area_name.title()
                area_dict['area_code'] = area_name.upper()[:2]
                area_dict['city_code'] = city_id
                area_serializer = CityAreaSerializer(data=area_dict)
                if area_serializer.is_valid():
                    area_instance = area_serializer.save()
                    area_id = area_instance.id
            
            subarea_dict ={}
            subarea_dict['subarea_name'] = subarea_name.title()
            subarea_dict['subarea_code'] = subarea_name.upper()[:2]
            subarea_dict['area_code'] = area_id
            subarea_dict['locality_rating'] = 'Standard'
            subarea_serializer = CitySubAreaSerializer(data=subarea_dict)
            if subarea_serializer.is_valid():
                subarea_instance = subarea_serializer.save()
                response = { "message": "Already exists!" }
                if subarea_instance and subarea_instance.area_code:
                    response["message"] = "Successfully added"
                return Response(response, status=201)

            return Response(city_serializer.errors, status=400)

        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)



class SocietyAPIFilterSubAreaView(APIView):
    def post(self, request, format=None):

        areas_id = []
        subareas = []
        for item in request.data:
            id = int(item['id'])
            areas_id.append(id)

        areas = CityArea.objects.filter(id__in=areas_id)
        for area in areas:
            subarea = area.areacode.all()
            subareas.extend(subarea)

        subarea_serializer = CitySubAreaSerializer(subareas, many=True)

        return Response(subarea_serializer.data, status=200)

class FlatTypeAPIView(APIView):
    def get(self, request, id, format=None):
        try:
            society = SupplierTypeSociety.objects.get(pk=id)
            flatType = SupplierTypeSociety.objects.get(pk=id).flatTypes.all()
            serializer = FlatTypeSerializer(flatType, many=True)
            count = len(serializer.data)

            if count > 0:
                flat_details_available = True
            else:
                flat_details_available = False

            response = {}
            response['flat_type_count'] = count
            response['flat_details_available'] = flat_details_available
            response['flat_details'] = serializer.data
            response['total_flat'] = society.flat_count

            return Response(response, status=200)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        except FlatType.DoesNotExist:
            return Response(status=404)

    def post(self, request, id, format=None):
        society = SupplierTypeSociety.objects.get(pk=id)
        num = 0.0
        den = 0.0
        totalFlats = 0
        flag = True
        content_type = ui_utils.fetch_content_type(v0_constants.society_code)
        if request.data['flat_details_available']:
            for key in request.data['flat_details']:
                if 'size_builtup_area' in key and 'flat_rent' in key and key['size_builtup_area'] > 0 and key[
                    'flat_rent'] > 0:
                    rent = key['flat_rent']
                    area = key['size_builtup_area']
                    key['average_rent_per_sqft'] = rent / area
                    if 'flat_count' in key:
                        count = key['flat_count']
                        num = num + (count * key['average_rent_per_sqft'])
                        den = den + count
                    else:
                        flag = False
                else:
                    flag = False

                if 'size_builtup_area' in key and key['size_builtup_area'] > 0:
                    builtup = key['size_builtup_area'] / 1.2
                    key['size_carpet_area'] = builtup

                if 'flat_count' in key and key['flat_count'] > 0:
                    totalFlats = totalFlats + key['flat_count']

            if flag:
                avgRentpsf = num / den
                society.average_rent = avgRentpsf
                society.flat_type_count = request.data['flat_type_count']
                society.save()

            if request.data['flat_type_count'] != len(request.data['flat_details']):
                return Response({'message': 'No of Flats entered does not match flat type count'}, status=400)
            if totalFlats > 0 and society.flat_count != totalFlats:
                return Response({'message': 'No of Flats entered does not match total flat count of society'},
                                status=400)

        for key in request.data['flat_details']:
            if 'id' in key:
                item = FlatType.objects.get(pk=key['id'])
                serializer = FlatTypeSerializer(item, data=key)
            else:
                serializer = FlatTypeSerializer(data=key)
            if serializer.is_valid():
                serializer.save(society=society, content_type=content_type, object_id=society.supplier_id)
            else:
                return Response(serializer.errors, status=400)

        return Response(status=201)

    def delete(self, request, id, format=None):
        try:
            invid = request.query_params.get('flatid', None)

            society = SupplierTypeSociety.objects.get(pk=id)

            flat = FlatType.objects.filter(pk=invid)
            flat.delete()
            return Response(status=204)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        except FlatType.DoesNotExist:
            return Response(status=404)


class ImportSummaryData(APIView):
    """
    Saves inventory summary data from csv sheet.
    """

    def get(self, request):
        """
        returns success or failure depending on weather the data was successfully saved or not.
        the csv file should be named 'inventory_summary.csv and should be parallel to manage.py file
        """
        class_name = self.__class__.__name__
        try:
            source_file = open(BASE_DIR + '/files/inventory_summary_new.csv', 'rb')
            error_list = []

            reader = csv.reader(source_file)
            source_file.seek(0)
            for num, row in enumerate(reader):
                data = {}
                if num == 0:
                    continue
                else:
                    if len(row) != len(keys):
                        error = 'length of row read {0} does not match with number of predefined keys {1}'.format(
                            len(row), len(keys))
                        return ui_utils.handle_response(class_name, data=error)

                    for index, key in enumerate(keys):
                        if row[index] == '':
                            data[key] = None
                        elif row[index].lower() == decision["YES"]:
                            data[key] = True
                        elif row[index] == decision["NO"]:
                            data[key] = False
                        else:
                            data[key] = row[index]

                    # make the data in order to make supplier_id
                    # supplier_id_data = {
                    #     'city_code': data['city_code'],
                    #     'area_code': data['area_code'],
                    #     'subarea_code': data['subarea_code'],
                    #     'supplier_type': data['supplier_type'],
                    #     'supplier_code': data['supplier_code']
                    # }

                    data['supplier_id'] = row[0]
                    supplier_type_code = 'RS'

                    # save pricing information in price_mapping_default table
                    response = save_price_mapping_default(data['supplier_id'], supplier_type_code, row)
                    if not response.data['status']:
                        return response

                    request = InventoryPricingAPIView.as_view()
                    content_type_response = ui_utils.get_content_type(supplier_type_code)
                    if not content_type_response.data['status']:
                        return None
                    data['content_type'] = content_type_response.data['data']
                    try:
                        supplier_instance = SupplierTypeSociety.objects.get(supplier_id=data['supplier_id'])
                    except ObjectDoesNotExist:
                        supplier_instance = None
                    if not supplier_instance:
                        continue

                    data['object_id'] = data['supplier_id']
                    obj, created = InventorySummary.objects.update_or_create(supplier_id=supplier_instance,
                                                                                    defaults=data)
                    obj.save()
                    # view = InventorySummaryAPIView.as_view()
                    # response = view(data, {'id': data['supplier_id']})

            source_file.close()

            return ui_utils.handle_response(class_name, data=error_list, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


class InventorySummaryAPIView(APIView):
    """
    This api provides summary of a  ll the inventories associated with a supplier
    supplierTypeCode -- supplier type code RS, CP etc

    """

    def get(self, request, id):
        try:
            # Start: code added and changed for getting supplier_type_code
            supplier_type_code = request.query_params.get('supplierTypeCode', None)
            # supplier_type_code = 'CP'
            data = request.data.copy()
            data['supplier_type_code'] = supplier_type_code
            inventory_object = InventorySummary.objects.get_supplier_type_specific_object(data, id)
            # End: code added and changed for getting supplier_type_code
            if not inventory_object:
                return Response(data={},
                                status=status.HTTP_200_OK)
            result = {}
            result['inventory'] = model_to_dict(inventory_object)
            inventory_allowed_codes = website_utils.get_inventories_allowed(inventory_object)
            result['inventories_allowed_codes'] = inventory_allowed_codes
            return Response(data=result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"status": False, "error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, id):
        """
        creates summary for given supplier id
        ---
        parameters:
        - name: supplier_type_code
          description: RS, CP, etc
          required: true
        - name: poster_allowed_nb
          description: poster allowed or not
        - name: nb_count
          description: count of notice boards
        - name: lift_count
          description: count of lifts
        - name: standee_allowed
          description: standee allowed or not
        - name: total_standee_count
          description: total standee count
        - name: stall_allowed
          description: stall allowed or not
        - name: total_stall_count
          description: total stall count
        - name: flier_allowed
          description: flier allowed or not
        - name: flier_frequency
          description: frequency of fliers
        - name: car_display_allowed
          description: car display allowed or not
        - name: poster_price_week_nb
          description: poster price for a week per notice board
        - name: nb_A3_allowed
          description: A3 sheets allowed on notice board or not
        - name: nb_A4_allowed
          description: A4 sheets allowed on notice boards or not
        - name: standee_price_week
          description: standee price per week
        - name: standee_small
          description: small standee allowed or not
        - name: standee_medium
          description: medium standee allowed or not
        - name: standee_large
          description: medium standee allowed or not
        - name: stall_small
          description: small stalls allowed or not
        - name: stall_large
          description: large stalls allowed or not
        - name: stall_price_day_small
          description: price of small stall for a day
        - name: stall_price_day_large
          description: price of large stall for a day
        - name: cd_standard
          description: car display standard
        - name: cd_price_day_standard
          description: price of standard car display
        - name: cd_premium
          description: premium car display allowed or not
        - name: cd_price_day_premium
          description: price of premium car display
        - name: flier_price_day
          description: price of flier per day
        - name: mailbox_allowed
          description: mailbox allowed or not
        - name: d2d_allowed
          description: door to door service is allowed or not
        - name: flier_lobby_allowed
          description : flier lobby allowed or not

        """
        print(request.data)
        class_name = self.__class__.__name__
        response = ui_utils.get_supplier_inventory(request.data.copy(), id)

        if not response.data['status']:
            return response

        supplier_inventory_data = response.data['data']['request_data']

        final_data = {
            'id': get_from_dict(request.data, 'id'),
            'supplier_object': get_from_dict(response.data['data'], 'supplier_object'),
            'inventory_object': get_from_dict(response.data['data'], 'inventory_object'),
            'supplier_type_code': get_from_dict(request.data, 'supplier_type_code'),
            'poster_allowed_nb': get_from_dict(request.data, 'poster_allowed_nb'),
            'nb_count': get_from_dict(request.data, 'nb_count'),
            'poster_campaign': get_from_dict(request.data, 'poster_campaign'),
            'lift_count': get_from_dict(request.data, 'lift_count'),
            'poster_allowed_lift': get_from_dict(request.data, 'poster_allowed_lift'),
            'standee_allowed': get_from_dict(request.data, 'standee_allowed'),
            'total_standee_count': get_from_dict(request.data, 'total_standee_count'),
            'standee_campaign': get_from_dict(request.data, 'standee_campaign'),
            'stall_allowed': get_from_dict(request.data, 'stall_allowed'),
            'car_display_allowed': get_from_dict(request.data, 'car_display_allowed'),
            'total_stall_count': get_from_dict(request.data, 'total_stall_count'),
            'stall_or_cd_campaign': get_from_dict(request.data, 'stall_or_cd_campaign'),
            'flier_allowed': get_from_dict(request.data, 'flier_allowed'),
            'flier_frequency': get_from_dict(request.data, 'flier_frequency'),
            'flier_campaign': get_from_dict(request.data, 'flier_campaign'),
            'poster_price_week_nb': get_from_dict(request.data, 'poster_price_week_nb'),
            'nb_A3_allowed': get_from_dict(request.data, 'nb_A3_allowed'),
            'nb_A4_allowed': get_from_dict(request.data, 'nb_A4_allowed'),
            'poster_price_week_lift': get_from_dict(request.data, 'poster_price_week_lift'),
            'standee_price_week': get_from_dict(request.data, 'standee_price_week'),
            'standee_small': get_from_dict(request.data, 'standee_small'),
            'standee_medium': get_from_dict(request.data, 'standee_medium'),
            'stall_price_day_small': get_from_dict(request.data, 'stall_price_day_small'),
            'stall_large': get_from_dict(request.data, 'stall_large'),
            'stall_price_day_large': get_from_dict(request.data, 'stall_price_day_large'),
            'cd_standard': get_from_dict(request.data, 'cd_standard'),
            'cd_price_day_standard': get_from_dict(request.data, 'cd_price_day_standard'),
            'cd_premium': get_from_dict(request.data, 'cd_premium'),
            'cd_price_day_premium': get_from_dict(request.data, 'cd_price_day_premium'),
            'flier_price_day': get_from_dict(request.data, 'flier_price_day'),
            'mailbox_allowed': get_from_dict(request.data, 'mailbox_allowed'),
            'd2d_allowed': get_from_dict(request.data, 'd2d_allowed'),
            'flier_lobby_allowed': get_from_dict(request.data, 'flier_lobby_allowed'),
            'gateway_arch_allowed': get_from_dict(request.data, 'gateway_arch_allowed'),
        }
        return inventory_summary_insert(final_data,supplier_inventory_data)
        # try:
        # except ObjectDoesNotExist as e:
        #     return ui_utils.handle_response(class_name, exception_object=e, request=request)
        # except Exception as e:
        #     return Response(data={"status": False, "error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)

class PostInventorySummary(APIView):
    """

    """

    def post(self, request):
        """

        Args:
            request:

        Returns:

        """
        class_name = self.__class__.__name__
        try:

            pass

        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


class BasicPricingAPIView(APIView):

    def get(self, request, id, format=None):
        response = {}
        try:

            # get the supplier_type_code
            supplier_type_code = request.query_params.get('supplierTypeCode', None)
            # supplier_type_code = request.data.get('supplier_type_code')
            # supplier_type_code = 'RS' #todo: change this when get supplier_type_code
            if not supplier_type_code:
                return Response({'status': False, 'error': 'Provide supplier_type_code'},
                                status=status.HTTP_400_BAD_REQUEST)

            # get the content_type_response and content_type
            content_type_response = ui_utils.get_content_type(supplier_type_code)
            if not content_type_response.data['status']:
                return None
            content_type = content_type_response.data['data']

            basic_prices = PriceMappingDefault.objects.filter(object_id=id, content_type=content_type).values()
            selected_prices = PriceMappingDefault.objects.select_related('supplier', 'adinventory_type',
                                                                         'duration_type').filter(object_id=id,
                                                                                                 content_type=content_type)
            supplier_object = ui_utils.get_model(supplier_type_code).objects.get(pk=id)
            towercount_response = ui_utils.get_tower_count(supplier_object, supplier_type_code)
            if not towercount_response.data['status']:
                return towercount_response
            tower_count = towercount_response.data['data']
            for basic_item, basic_select_item in zip(basic_prices, selected_prices):
                if basic_select_item.supplier:
                    basic_item['supplier'] = basic_select_item.supplier.__dict__
                basic_item['adinventory_type'] = basic_select_item.adinventory_type.__dict__
                basic_item['duration_type'] = basic_select_item.duration_type.__dict__
                if basic_item['adinventory_type']:
                    basic_item['adinventory_type'].pop("_state", None)
                if 'supplier' in basic_item and basic_item['supplier']:
                    basic_item['supplier'].pop("_state", None)
                if basic_item['duration_type']:
                    basic_item['duration_type'].pop("_state", None)
            response['tower_count'] = tower_count
            response['prices'] = basic_prices

            return Response(response, status=200)

        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        except PriceMappingDefault.DoesNotExist:
            return Response(status=404)
        except Exception as e:
            print("ex", e)
            return Response({'status': False, 'error': e}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, id, format=None):

        for key in request.data:
            if 'id' in key:
                item = PriceMappingDefault.objects.get(pk=key['id'])
                serializer = PriceMappingDefaultSerializer(item, data=key)
            else:
                serializer = PriceMappingDefaultSerializer(data=key)
            try:
                if serializer.is_valid():
                    serializer.save()
            except:
                return Response(serializer.errors, status=400)
        return Response({'status': True, 'data': 'success'}, status=201)


class InventoryPricingAPIView(APIView):
    """
    Not used
    """

    def get(self, request, id, format=None):
        try:
            inv_prices = PriceMapping.objects.select_related().filter(supplier__supplier_id=id)
            # count = PriceMapping.objects.filter(supplier__supplier_id=id).count()
            # basic_prices = SupplierTypeSociety.objects.get(pk=id).default_prices.all()
            serializer = PriceMappingSerializer(inv_prices, many=True)
            return Response(serializer.data)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        except PriceMapping.DoesNotExist:
            return Response(status=404)

    def post(self, request, id, format=None):

        for key in request.data:
            if 'id' in key:
                item = PriceMapping.objects.get(pk=key['id'])
                serializer = PriceMappingSerializer(item, data=key)
            else:
                serializer = PriceMappingSerializer(data=key)
            try:
                if serializer.is_valid():
                    serializer.save()
            except:
                return Response(serializer.errors, status=400)
            return Response(serializer.data, status=201)
        return Response({'No data'}, status=201)


class TowerAPIView(APIView):
    def get(self, request, id, format=None):
        try:
            supplier_type_code = request.query_params.get('supplierTypeCode', None)
            data = request.data.copy()
            data['supplier_type_code'] = supplier_type_code

            towers = SupplierTypeSociety.objects.get(pk=id).towers.all()
            serializer_tower = UITowerSerializer(towers, many=True)

            inventory_summary = InventorySummary.objects.get_supplier_type_specific_object(data, id)
            if not inventory_summary:
                return Response(data={"Inventory Summary object does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            serializer_inventory = InventorySummarySerializer(inventory_summary)

            response = {
                'tower': serializer_tower.data,
                'inventory': serializer_inventory.data,
            }

            return Response(response, status=200)
        except SupplierTypeSociety.DoesNotExist:
            return Response({'message': 'Invalid Society ID'}, status=404)
        except InventorySummary.DoesNotExist:
            return Response({'message': 'Please fill Inventory Summary Tab', 'inventory': 'true'}, status=404)

    def post(self, request, id, format=None):

        society = SupplierTypeSociety.objects.get(pk=id)

        # checking of notice board in tower == inventory summary nb_count
        total_nb_count = 0

        total_lift_count = 0
        total_standee_count = 0
        for tower in request.data['TowerDetails']:
            total_nb_count += tower['notice_board_count_per_tower']
            total_lift_count += tower['lift_count']
            total_standee_count += tower['standee_count']

        try:
            supplier_type_code = request.query_params.get('supplierTypeCode', None)
            data = request.data.copy()
            data['supplier_type_code'] = supplier_type_code
            content_type_response = ui_utils.get_content_type(supplier_type_code)
            if not content_type_response.data['status']:
                return None
            content_type = content_type_response.data['data']
            # End: code added and changed for getting supplier_type_code
            inventory_obj = InventorySummary.objects.get_supplier_type_specific_object(data, id)
            if not inventory_obj:
                return Response(data={"Inventory Summary object does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except InventorySummary.DoesNotExist:
            return Response({'message': 'Please fill Inventory Summary Tab', 'inventory': 'true'}, status=404)

        if total_nb_count != 0 and total_nb_count != inventory_obj.nb_count:
            return Response(
                {'message': 'Total Notice Board Count should equal to Notice Board Count in Inventory Summary Tab'},
                status=404)
        if total_lift_count != 0 and total_lift_count != inventory_obj.lift_count:
            return Response({'message': 'Total Lift Count should equal to Lift Count in Inventory Summary Tab'},
                            status=404)
        if total_standee_count != 0 and total_standee_count != inventory_obj.total_standee_count:
            return Response({'message': 'Total Standee Count should equal to Standee Count in Inventory Summary Tab'},
                            status=404)

        # checking ends here

        for key in request.data['TowerDetails']:

            if 'tower_id' in key:
                # update code
                try:
                    item = SocietyTower.objects.get(pk=key['tower_id'])
                    tower_dict = {
                        'tower_tag': key['tower_tag'],
                        'tower_name': key['tower_name'],
                        'tower_id': key['tower_id'],
                        'lift_count': item.lift_count,
                        'nb_count': item.notice_board_count_per_tower,
                        'standee_count': item.standee_count,
                    }

                except SocietyTower.DoesNotExist:
                    return Response({'status': False, 'error': 'Society tower does not exist'}, status=400)

                serializer = SocietyTowerSerializer(item, data=key)
                if serializer.is_valid():
                    serializer.save(supplier=society, content_type=content_type, object_id=society.supplier_id)
                else:
                    return Response(serializer.errors, status=400)

                if tower_dict['lift_count'] < key['lift_count']:
                    self.save_lift_locations(tower_dict['lift_count'], key['lift_count'], tower_dict, society,
                                             content_type)
                if tower_dict['nb_count'] < key['notice_board_count_per_tower']:
                    self.save_nb_locations(tower_dict['nb_count'], key['notice_board_count_per_tower'], tower_dict,
                                           society)
                if tower_dict['standee_count'] < key['standee_count']:
                    self.save_standee_locations(tower_dict['standee_count'], key['standee_count'], tower_dict, society,
                                                content_type)

            # else:
            #     serializer = SocietyTowerSerializer(data=key)

            try:
                tower_data = SocietyTower.objects.get(pk=serializer.data['tower_id'])
            except SocietyTower.DoesNotExist:
                return Response(status=404)

            '''#create automated IDs for lift, notice boards, standees
            if flag:
                print "lift count : ",key['lift_count']
                self.save_lift_locations(0, key['lift_count'], tower_data, society)
                self.save_nb_locations(0, key['notice_board_count_per_tower'], tower_data, society)
                self.save_standee_locations(0, key['standee_count'], tower_data, society)'''

            if key['flat_type_details_available']:
                for index, flat in enumerate(key['flat_type_details'], start=1):
                    if 'id' in flat:
                        flat_item = SocietyFlat.objects.get(pk=flat['id'])
                        flat_serializer = SocietyFlatSerializer(flat_item, data=flat)
                        flatLen = len(key['flat_type_details'])
                        flat = key['flat_type_count']
                        if flat != flatLen:
                            return Response({'message': 'No of flat details entered does not match flat type count'},
                                            status=400)

                    else:
                        flat['tower'] = tower_data.tower_id
                        flat_serializer = SocietyFlatSerializer(data=flat)

                    if flat_serializer.is_valid():
                        flat_serializer.save()

                    else:
                        return Response(flat_serializer.errors, status=400)

        return Response(status=201)

    def delete(self, request, id, format=None):
        try:
            society = SupplierTypeSociety.objects.get(pk=id)
            tower = SocietyTower.objects.get(tower_id=9).tower_name
            posters = PosterInventory.objects.filter(supplier=society, tower_name=tower)
            posters.delete()

            towerId = request.query_params.get('towId', None)
            item = SocietyTower.objects.get(pk=towerId)
            item.delete()

            return Response(status=204)
        except SocietyTower.DoesNotExist:
            return Response(status=404)

    def save_lift_locations(self, c1, c2, tower, society, content_type):
        i = c1 + 1
        tow_name = tower['tower_name']
        while i <= c2:
            lift_tag = tower['tower_tag'] + "00L" + str(i)
            adId = society.supplier_id + lift_tag + "PO01"
            lift = LiftDetails(adinventory_id=adId, lift_tag=lift_tag, tower_id=int(tower['tower_id']))
            lift_inv = PosterInventory(adinventory_id=adId, poster_location=lift_tag, tower_name=tow_name,
                                       supplier=society, tower_id=int(tower['tower_id']), object_id=society.supplier_id,
                                       content_type=content_type)
            lift.save()
            lift_inv.save()
            i += 1

    def save_nb_locations(self, c1, c2, tower, society):
        i = c1 + 1
        while i <= c2:
            nb_tag = tower['tower_tag'] + "00N" + str(i)
            nb = NoticeBoardDetails(notice_board_tag=nb_tag, tower_id=int(tower['tower_id']))
            nb.save()
            i += 1

    def save_standee_locations(self, c1, c2, tower, society, content_type):
        i = c1 + 1
        while i <= c2:
            sd_tag = society.supplier_id + tower['tower_tag'] + "0000SD" + str(i).zfill(2)
            sd = StandeeInventory(adinventory_id=sd_tag, tower_id=int(tower['tower_id']), object_id=society.supplier_id,
                                  content_type=content_type)
            sd.save()
            i += 1


class PosterAPIView(APIView):

    def get(self, request, id, format=None):
        lifts = []
        notice_boards = []
        disable = {}
        try:
            # code added and changed for getting supplier_type_code
            supplier_type_code = request.query_params.get('supplierTypeCode', None)
            data = request.data.copy()
            data['supplier_type_code'] = supplier_type_code
            towers = SupplierTypeSociety.objects.get(pk=id).towers.all()
            society = SupplierTypeSociety.objects.get(pk=id)
            posters = PosterInventory.objects.filter(supplier=society)

            item = InventorySummary.objects.get_supplier_type_specific_object(data, id)
            if not item:
                return Response(data={"Inventory Summary object does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            # item = InventorySummary.objects.get(supplier=society)

            for tower in towers:
                lifts.extend(tower.lifts.all())
                notice_boards.extend(tower.notice_boards.all())

            if len(lifts) > 0:
                lifts_available = True
            else:
                lifts_available = False
            if len(notice_boards) > 0:
                nb_available = True
            else:
                nb_available = False

            serializer1 = InventorySummarySerializer(item, many=True)
            serializer = LiftDetailsSerializer(lifts, many=True)
            result = {"lift_details_available": lifts_available, "lift_details": serializer.data,
                      "nb_a4_available": nb_available, "disable_nb": item.poster_allowed_nb,
                      "disable_lift": item.poster_allowed_lift}
            serializer = NoticeBoardDetailsSerializer(notice_boards, many=True)
            result['nb_details'] = serializer.data
            serializer = PosterInventorySerializer(posters, many=True)
            result['poster_details'] = serializer.data

            return Response(result, status=200)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)

    def post(self, request, id, format=None):
        society = SupplierTypeSociety.objects.get(pk=id)
        society_content_type = ContentType.objects.get_for_model(SupplierTypeSociety)
        if request.data['nb_a4_available']:
            for notice_board in request.data['nb_details']:
                data = request.data['nb_common_details']
                data.update(notice_board)
                if 'id' in notice_board:
                    notice_item = NoticeBoardDetails.objects.get(pk=notice_board['id'])
                    posCount = notice_board['total_poster_per_notice_board']
                    if posCount != None:
                        response = ui_utils.generate_poster_objects(posCount, notice_board, society,
                                                                    society_content_type)
                        if not response.data['status']:
                            return response

                    notice_serializer = NoticeBoardDetailsSerializer(notice_item, data=data)
                else:
                    notice_serializer = NoticeBoardDetailsSerializer(data=data)
                    # populate location and ad inventory table
                '''for i in range(notice_board['total_poster_per_notice_board']):
                   ad_inv = AdInventoryLocationMapping(adinventory_id = notice_tag+'PO'+str(i), adinventory_name = 'POSTER', location = nb_location)
                   ad_inv.save("Poster", society)'''
                if notice_serializer.is_valid():
                    notice_serializer.save()
                else:
                    # transaction.rollback()
                    return Response(notice_serializer.errors, status=400)

        if request.data['lift_details_available']:
            for lift in request.data['lift_details']:
                if 'id' in lift:
                    lift_item = LiftDetails.objects.get(pk=lift['id'])
                    lift_serializer = LiftDetailsSerializer(lift_item, data=lift)
                    # if lift!=liftLen:
                    #   return Response({'message':'No of lift details entered does not match lift count'},status=400)
                else:
                    lift_serializer = LiftDetailsSerializer(data=lift)
                    # populate location and ad inventory table
                if lift_serializer.is_valid():
                    lift_serializer.save()
                else:
                    return Response(lift_serializer.errors, status=400)
        return Response(status=200)

    def delete(self, request, id, format=None):
        try:
            invId = request.query_params.get('invId', None)
            invType = request.query_params.get('type', None)
            society = SupplierTypeSociety.objects.get(pk=id)

            if invType == 'lift':
                item = LiftDetails.objects.get(pk=invId)
                tag = item.lift_tag
                posters = PosterInventory.objects.filter(supplier=society, poster_location=tag)
                posters.delete()
                item.delete()
            if invType == 'notice':
                item = NoticeBoardDetails.objects.get(pk=invId)
                tag = item.notice_board_tag
                posters = PosterInventory.objects.filter(supplier=society, poster_location=tag)
                posters.delete()
                item.delete()
            return Response(status=204)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        except NoticeBoardDetails.DoesNotExist:
            return Response(status=404)
        except LiftDetails.DoesNotExist:
            return Response(status=404)
        except PosterInventory.DoesNotExist:
            return Response(status=404)


class FlierAPIView(APIView):
    def get(self, request, id, format=None):
        response = {}
        fliers = []
        try:
            # code added and changed for getting supplier_type_code
            supplier_type_code = request.query_params.get('supplierTypeCode', None)
            data = request.data.copy()
            data['supplier_type_code'] = supplier_type_code

            society = SupplierTypeSociety.objects.get(pk=id)
            flyers = FlyerInventory.objects.filter(object_id=id)
            response['flat_count'] = society.flat_count

            serializer = FlyerInventorySerializer(flyers, many=True)
            response['flyers_data'] = serializer.data
            towers = SupplierTypeSociety.objects.get(pk=id).towers.all().values()

            item = InventorySummary.objects.get_supplier_type_specific_object(data, id)
            if not item:
                return Response(data={"Inventory Summary object does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            # item = InventorySummary.objects.get(supplier=society)

            # mail_boxes = SupplierTypeSociety.objects.get(pk=id).mail_boxes.all().values()

            response['flyer_available'] = society.flier_allowed
            # fliers.extend(towers)
            # fliers.extend(mail_boxes)
            # serializer = MailboxInfoSerializer(mail_boxes, many=True)
            # mail_box_available = get_availability(serializer.data)
            # mail_box_available = item.mailbox_allowed
            # response['mail_box_available'] = item.mailbox_allowed
            # response['mail_box_details'] = fliers
            # response['tower_data'] = towers

            # door_to_doors = SupplierTypeSociety.objects.get(pk=id).door_to_doors.all()
            # serializer = DoorToDoorInfoSerializer(door_to_doors, many=True)
            # door_to_door_allowed = get_availability(serializer.data)
            # response['d2d_available'] = item.d2d_allowed
            # response['door_to_door_details'] = serializer.data

            return Response(response, status=200)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        except FlyerInventory.DoesNotExist:
            return Response(status=404)
        # except MailboxInfo.DoesNotExist:
        # return Response(status=404)
        # except DoorToDoorInfo.DoesNotExist:
        # MultipleObjectsReturnedrn Response(status=404)

    def post(self, request, id, format=None):
        society = SupplierTypeSociety.objects.get(supplier_id=id)
        # mail = request.data['flyers_data']
        # society.tower_id = mail['tower_id']
        # if request.data['mail_box_available']:
        # response = post_data(MailboxInfo, MailboxInfoSerializer, request.data['mail_box_details'], society)
        # response = post_data(MailboxInfo, MailboxInfoSerializer, request.data['tower_data'], society)
        # print request.data['tower_data']
        # if response == False:
        #      return Response(status=400)

        # if request.data['door_to_door_allowed']:
        # response = post_data(DoorToDoorInfo, DoorToDoorInfoSerializer, request.data['door_to_door_details'], society)
        # if response == False:
        #   return Response(status=400)

        # return Response(status=201)
        for flyer in request.data['flyers_data']:
            # print request.data['tower_data']
            if 'id' in flyer:

                flyer_item = FlyerInventory.objects.get(pk=flyer['id'])
                flyer_serializer = FlyerInventorySerializer(flyer_item, data=flyer)

            else:
                flyer_serializer = FlyerInventorySerializer(data=flyer)

            if flyer_serializer.is_valid():
                flyer_serializer.save()
            else:
                return Response(flyer_serializer.errors, status=400)

        return Response(status=200)

    def delete(self, request, id, format=None):
        try:
            # invId = request.query_params.get('invId', None)
            adinventory_id = request.query_params.get('adinventory_id', None)
            # invType = request.query_params.get('type', None)
            # adinventory_type = request.query_params.get('type', None)
            society = SupplierTypeSociety.objects.get(pk=id)

            flyer = FlyerInventory.objects.filter(object_id=society, pk=adinventory_id)
            flyer.delete()
            return Response(status=204)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        except FlyerInventory.DoesNotExist:
            return Response(status=404)


class StandeeBannerAPIView(APIView):
    def get(self, request, id, format=None):
        # response = {}
        standees = []

        # code added and changed for getting supplier_type_code
        supplier_type_code = request.query_params.get('supplierTypeCode', None)
        data = request.data.copy()
        data['supplier_type_code'] = supplier_type_code

        towers = SupplierTypeSociety.objects.get(pk=id).towers.all()
        society = SupplierTypeSociety.objects.get(pk=id)

        item = InventorySummary.objects.get_supplier_type_specific_object(data, id)
        if not item:
            return Response(data={"Inventory Summary object does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        # item = InventorySummary.objects.get(supplier=society)

        for tower in towers:
            tower_standees = tower.standees.all().values()
            for standee in tower_standees:
                standee['tower_name'] = tower.tower_name
            standees.extend(tower_standees)

        response = {"disable_standee": item.standee_allowed}
        response['standee_details'] = standees

        return Response(response, status=200)

    def post(self, request, id, format=None):
        for standee in request.data['standee_details']:
            if 'id' in standee:
                standee_item = StandeeInventory.objects.get(pk=standee['id'])
                standee_serializer = StandeeInventorySerializer(standee_item, data=standee)

            else:
                standee_serializer = StandeeInventorySerializer(data=standee)

            if standee_serializer.is_valid():
                standee_serializer.save()
            else:
                return Response(standee_serializer.errors, status=400)

        return Response(status=200)


class StallAPIView(APIView):
    def get(self, request, id, format=None):
        response = {}
        stall = []

        # code added and changed for getting supplier_type_code
        supplier_type_code = request.query_params.get('supplierTypeCode', None)
        data = request.data.copy()
        data['supplier_type_code'] = supplier_type_code

        society = SupplierTypeSociety.objects.get(pk=id)
        stalls = StallInventory.objects.filter(object_id=id)

        # item = InventorySummary.objects.get(supplier=society)

        item = InventorySummary.objects.get_supplier_type_specific_object(data, id)
        if not item:
            return Response(data={"Inventory Summary object does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        serializer1 = InventorySummarySerializer(item, many=True)
        response = {"disable_stall": item.stall_allowed}
        serializer = StallInventorySerializer(stalls, many=True)
        response['stall_details'] = serializer.data

        response['furniture_available'] = 'Yes' if society.street_furniture_available else 'No'
        response['stall_timing'] = society.stall_timing
        response['sound_system_allowed'] = 'Yes' if society.sound_available else 'No'
        response['electricity_available'] = 'Yes' if society.electricity_available else 'No'
        response['electricity_charges_daily'] = society.daily_electricity_charges

        return Response(response, status=200)

    def post(self, request, id, format=None):

        stall = request.data
        society = SupplierTypeSociety.objects.get(supplier_id=id)

        society.street_furniture_available = True if stall['furniture_available'] == 'Yes' else False
        society.stall_timing = stall['stall_timing']
        society.sound_available = True if stall['sound_system_allowed'] == 'Yes' else False
        society.electricity_available = True if stall['electricity_available'] == 'Yes' else False
        if society.electricity_available:
            society.daily_electricity_charges = stall['electricity_charges_daily']

        society.save()

        for stall in request.data['stall_details']:
            if 'id' in stall:
                stall_item = StallInventory.objects.get(pk=stall['id'])
                stall_serializer = StallInventorySerializer(stall_item, data=stall)

            else:
                stall_serializer = StallInventorySerializer(data=stall)

            if stall_serializer.is_valid():
                stall_serializer.save()
            else:
                return Response(stall_serializer.errors, status=400)

        return Response(status=200)


'''class CarDisplayAPIView(APIView):
    def get(self, request, id, format=None):
        try:
            car_displays = SupplierTypeSociety.objects.get(pk=id).car_displays.all()
            serializer = CarDisplayInventorySerializer(car_displays, many=True)
            len(serializer.data)
            if len(serializer.data) > 0:
                car_display_available=True
            else:
                car_display_available = False

            response = {}
            response['car_display_available'] = car_display_available
            response['car_display_details'] = serializer.data

            return Response(response, status=200)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        except CarDisplayInventory.DoesNotExist:
            return Response(status=404)

    def post(self, request, id, format=None):
        ##print request.data
        society=SupplierTypeSociety.objects.get(pk=id)

        for key in request.data['car_display_details']:
            if 'id' in key:
                item = CarDisplayInventory.objects.get(pk=key['id'])
                serializer = CarDisplayInventorySerializer(item, data=key)
            else:
                serializer = CarDisplayInventorySerializer(data=key)
            if serializer.is_valid():
                serializer.save(supplier=society)
            else:
                return Response(serializer.errors, status=400)

        return Response(serializer.data, status=201)'''


class EventAPIView(APIView):
    def get(self, request, id, format=None):
        try:
            events = SupplierTypeSociety.objects.get(pk=id).events.all()
            serializer = EventsSerializer(events, many=True)
            count = len(serializer.data)
            if count > 0:
                event_details_available = True
            else:
                event_details_available = False
            society_events = SupplierTypeSociety.objects.get(pk=id).society_events.first()
            serializer1 = SocietyMajorEventsSerializer(society_events)

            response = {}
            response['society_events'] = serializer1.data
            response['past_major_events'] = serializer1.data['past_major_events']
            response['event_details_available'] = event_details_available
            response['event_details'] = serializer.data

            return Response(response, status=200)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        except Events.DoesNotExist:
            return Response(status=404)

    def post(self, request, id, format=None):
        society = SupplierTypeSociety.objects.get(pk=id)
        content_type = ui_utils.fetch_content_type(v0_constants.society_code)

        for key in request.data['event_details']:
            if 'event_id' in key:
                item = Events.objects.get(pk=key['event_id'])
                serializer = EventsSerializer(item, data=key)
            else:
                serializer = EventsSerializer(data=key)
            if serializer.is_valid():
                serializer.save(supplier=society, object_id=id, content_type=content_type)
            else:
                return Response(serializer.errors, status=400)

        data = {}
        if 'society_events' in request.data:
            data = request.data['society_events']
        if 'past_major_events' in request.data:
            data['past_major_events'] = request.data['past_major_events']
        if 'id' in request.data['society_events']:
            events = SocietyMajorEvents.objects.get(pk=request.data['society_events']['id'])
            serializer = SocietyMajorEventsSerializer(events, data=data)
        else:
            serializer = SocietyMajorEventsSerializer(data=data)
        if serializer.is_valid():
            serializer.save(supplier=society)
        else:
            return Response(serializer.errors, status=400)

        return Response(serializer.data, status=201)


class OtherInventoryAPIView(APIView):
    def get(self, request, id, format=None):
        response = {}
        try:
            poles = SupplierTypeSociety.objects.get(pk=id).poles.all()
            serializer = PoleInventorySerializer(poles, many=True)
            pole_available = get_availability(serializer.data)
            response['pole_available'] = pole_available
            response['pole_display_details'] = serializer.data

            walls = SupplierTypeSociety.objects.get(pk=id).walls.all()
            serializer = WallInventorySerializer(walls, many=True)
            wall_available = get_availability(serializer.data)
            response['wall_available'] = wall_available
            response['wall_display_details'] = serializer.data

            community_halls = SupplierTypeSociety.objects.get(pk=id).community_halls.all()
            serializer = CommunityHallInfoSerializer(community_halls, many=True)
            community_hall_available = get_availability(serializer.data)
            response['community_hall_available'] = community_hall_available
            response['community_hall_details'] = serializer.data

            swimming_pools = SupplierTypeSociety.objects.get(pk=id).swimming_pools.all()
            serializer = SwimmingPoolInfoSerializer(swimming_pools, many=True)
            swimming_pool_available = get_availability(serializer.data)
            response['swimming_pool_available'] = swimming_pool_available
            response['swimming_pool_details'] = serializer.data

            street_furniture = SupplierTypeSociety.objects.get(pk=id).street_furniture.all()
            serializer = StreetFurnitureSerializer(street_furniture, many=True)
            street_furniture_available = get_availability(serializer.data)
            response['street_furniture_available'] = street_furniture_available
            response['street_furniture_details'] = serializer.data

            sports = SupplierTypeSociety.objects.get(pk=id).sports.all()
            serializer = SportsInfraSerializer(sports, many=True)
            sports_available = get_availability(serializer.data)
            response['sports_available'] = sports_available
            response['sports_details'] = serializer.data

            return Response(response, status=200)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        except PoleInventory.DoesNotExist:
            return WallInventory(status=404)
        except CommunityHallInfo.DoesNotExist:
            return Response(status=404)
        except SwimmingPoolInfo.DoesNotExist:
            return Response(status=404)
        except MailboxInfo.DoesNotExist:
            return Response(status=404)
        except DoorToDoorInfo.DoesNotExist:
            return Response(status=404)
        except WallInventory.DoesNotExist:
            return Response(status=404)
        except StreetFurniture.DoesNotExist:
            return Response(status=404)
        except SportsInfra.DoesNotExist:
            return Response(status=404)

    def post(self, request, id, format=None):
        ##print request.data
        society = SupplierTypeSociety.objects.get(pk=id)

        if request.data['pole_available']:
            response = post_data(PoleInventory, PoleInventorySerializer, request.data['pole_display_details'], society)
            if response == False:
                return Response(status=400)

        if request.data['wall_available']:
            response = post_data(WallInventory, WallInventorySerializer, request.data['wall_display_details'], society)
            if response == False:
                return Response(status=400)

        if request.data['community_hall_available']:
            response = post_data(CommunityHallInfo, CommunityHallInfoSerializer, request.data['community_hall_details'],
                                 society)
            if response == False:
                return Response(status=400)

        if request.data['swimming_pool_available']:
            response = post_data(SwimmingPoolInfo, SwimmingPoolInfoSerializer, request.data['swimming_pool_details'],
                                 society)
            if response == False:
                return Response(status=400)

        if request.data['street_furniture_available']:
            response = post_data(StreetFurniture, StreetFurnitureSerializer, request.data['street_furniture_details'],
                                 society)
            if response == False:
                return Response(status=400)

        if request.data['sports_available']:
            response = post_data(SportsInfra, SportsInfraSerializer, request.data['sports_details'], society)
            if response == False:
                return Response(status=400)

        return Response(status=201)


class ImageLocationsAPIView(APIView):
    def get(self, request, id, format=None):
        try:
            response = []
            society = SupplierTypeSociety.objects.get(pk=id)
            response.append(
                {"location_id": society.supplier_id, "name": society.society_name, "location_type": "Society"})
            towers = SupplierTypeSociety.objects.get(pk=id).towers.all()
            for key in towers:
                response.append({"location_id": key.tower_id, "name": key.tower_name, "location_type": "tower"})
                nb = key.notice_boards.all()
                for item in nb:
                    response.append({"location_id": item.id, "name": key.tower_name + item.notice_board_tag,
                                     "location_type": "NoticeBoard"})
                nb = key.lifts.all()
                for item in nb:
                    response.append(
                        {"location_id": item.id, "name": key.tower_name + item.lift_tag, "location_type": "Lift"})

            return Response(response, status=200)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        except SocietyTower.DoesNotExist:
            return Response(status=404)

        return Response({"response": response}, status=201)


def generate_location_tag(initial_tag, type, index):
    return ''.join((initial_tag.upper(), type.upper()[:3], str(index)))


def post_data(model, model_serializer, inventory_data, foreign_value=None):
    for key in inventory_data:
        if 'id' in key:
            item = model.objects.get(pk=key['id'])
            serializer = model_serializer(item, data=key)
        else:
            serializer = model_serializer(data=key)
        if serializer.is_valid():
            serializer.save(supplier=foreign_value)
        else:
            # print serializer.errors
            return False
    return True


def get_availability(data):
    if len(data) > 0:
        return True
    else:
        return False


# This API is for saving basic tab details of corporate space. Divided into four parts mentioned in the comments.


class EventViewSet(viewsets.ViewSet):
    """
    Event View Set
    """

    def list(self, request):
        """
        Lists all events
        Args:
            request:

        Returns:

        """
        class_name = self.__class__.__name__
        try:
            supplier_id = request.query_params['supplier_id']
            supplier_type_code = request.query_params['supplier_type_code']
            content_type = ui_utils.fetch_content_type(supplier_type_code)
            events = Events.objects.filter(object_id=supplier_id, content_type=content_type)
            serializer = EventsSerializer(events, many=True)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    def retrieve(self, request, pk=None):
        """

        Args:
            request:
            pk:

        Returns:

        """
        class_name = self.__class__.__name__
        try:
            serializer = EventsSerializer(Events.objects.get(pk=pk))
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    def update(self, request, pk=None):
        """
        updates a single event object
        Args:
            request:

        Returns:

        """
        class_name = self.__class__.__name__
        try:
            event = Events.objects.get(pk=pk)
            serializer = EventsSerializer(event, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return ui_utils.handle_response(class_name, data=serializer.data, success=True)
            return ui_utils.handle_response(class_name, data=serializer.errors, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    def create(self, request):
        """
        creates a single event
        Args:
            request:

        Returns:

        """
        class_name = self.__class__.__name__
        try:
            event_name = request.data['event_name']
            supplier_id = request.data['supplier_id']
            supplier_type_code = request.data['supplier_type_code']
            supplier_class = ui_utils.get_model(supplier_type_code)

            # see if the supplier actually exist
            supplier_class.objects.get(pk=supplier_id)

            event, is_created = Events.objects.get_or_create(event_name=event_name, object_id=supplier_id,
                                                                    content_type=ui_utils.fetch_content_type(
                                                                        supplier_type_code))
            data = request.data.copy()
            # remove this keys as serializer would throw error if they don't match with db fields
            data.pop('event_name')
            data.pop('supplier_id')
            data.pop('supplier_type_code')
            serializer = EventsSerializer(event, data=data)
            if serializer.is_valid():
                serializer.save()
                return ui_utils.handle_response(class_name, data=serializer.data, success=True)
            return ui_utils.handle_response(class_name, data=serializer.errors, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    def destroy(self, request, pk=None):
        """
        deletes an event object
        Args:
            request:
            pk:

        Returns:

        """
        class_name = self.__class__.__name__
        try:
            Events.objects.get(pk=pk).delete()
            return ui_utils.handle_response(class_name, data=pk, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

class ImageMappingViewSet(viewsets.ViewSet):
    """
    Image Mapping View Set
    """

    def list(self, request, pk=None):
        """
        Lists all images
        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            supplier_id = request.query_params.get('supplier_id', None)
            supplier_type_code = request.query_params.get('supplier_type_code', None)
            content_type = ui_utils.fetch_content_type(supplier_type_code)
            instances = ImageMapping.objects.filter(Q(location_id=supplier_id) | Q(object_id=supplier_id),content_type=content_type)
            serializer = ImageMappingSerializer(instances, many=True)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    def update(self, request, pk):
        class_name = self.__class__.__name__
        try:
            instance = ImageMapping.objects.get(pk=pk)
            serializer = ImageMappingSerializer(instance=instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return ui_utils.handle_response(class_name, data=serializer.data, success=True)
            return ui_utils.handle_response(class_name, data=serializer.errors)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    def create(self, request):
        class_name = self.__class__.__name__
        try:
            supplier_type_code = request.query_params['supplier_type_code']
            content_type = ui_utils.fetch_content_type(supplier_type_code)
            data = request.data.copy()
            data['content_type'] = content_type.pk
            serializer = ImageMappingSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return ui_utils.handle_response(class_name, data=serializer.data, success=True)
            return ui_utils.handle_response(class_name, data=serializer.errors)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    @list_route(methods=['POST'])
    def save_image_tag(self, request, pk=None):
        """

        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            data = request.data
            image_instance = ImageMapping.objects.get(pk=data['id'])
            serializer = ImageMappingSerializer(image_instance, data=data)
            if serializer.is_valid():
                serializer.save()
                return ui_utils.handle_response(class_name, data=serializer.data, success=True)
            return ui_utils.handle_response(class_name, data=serializer.errors)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


class StateViewSet(viewsets.ViewSet):
    """
    ViewSet around states
    """

    def list(self, request):
        """

        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            states = State.objects.all()
            serializer = StateSerializer(states, many=True)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

class ImportSocietyPaymentDetails(APIView):
    """
    API which will save payment details of society by sheet
    """

    def post(self, request, pk=None):
        """

        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            if not request.FILES:
                return ui_utils.handle_response(class_name, data='No File Found')
            my_file = request.FILES['file']
            wb = openpyxl.load_workbook(my_file)
            sheet = wb['society_payment_sheet']
            data = []
            for index, row in enumerate(sheet.iter_rows()):
                if index == 0:
                    response = ui_utils.check_payment_headers(row)
                    if not response:
                        return ui_utils.handle_response(class_name, data='No Headers Matching')
                else:
                    data.append(row)

            if data:
                response = ui_utils.save_society_payment_details(data)
                if not response:
                    return ui_utils.handle_response(class_name, data='Error')
            return ui_utils.handle_response(class_name, data={}, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)
