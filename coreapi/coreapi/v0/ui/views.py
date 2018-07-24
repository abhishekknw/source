# python core imports
import csv
import json
import openpyxl

# django imports
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
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
from serializers import UISocietySerializer, UITowerSerializer, UICorporateSerializer, UISalonSerializer, \
    BusShelterSerializer
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
from v0.ui.user.models import UserProfile
from v0.ui.location.models import City, CityArea, CitySubArea, ImageMapping
from v0.ui.events.serializers import SocietyMajorEventsSerializer
from v0.ui.serializers import SocietyListSerializer, RetailShopSerializer, BusDepotSerializer
from v0.ui.user.serializers import UserSerializer, UserProfileSerializer
from v0.ui.location.serializers import CitySerializer, CityAreaSerializer, CitySubAreaSerializer, StateSerializer, \
    ImageMappingSerializer
from v0.ui.account.models import ContactDetails, ContactDetailsGeneric
from v0.ui.account.serializers import (ContactDetailsSerializer, ContactDetailsGenericSerializer)
from inventory.models import PosterInventory, InventorySummary, StreetFurniture, \
    StallInventory, FlyerInventory, StandeeInventory, PoleInventory
from inventory.serializers import PosterInventorySerializer
from v0.ui.website.serializers import SupplierAmenitiesMapSerializer
from v0.ui.supplier.models import SupplierTypeSociety, SupplierTypeCorporate, SupplierAmenitiesMap, SupplierTypeCode, \
    SupplierTypeSalon, SupplierTypeGym, SupplierTypeBusShelter, CorporateBuilding, CorporateParkCompanyList
from v0.ui.supplier.serializers import (SupplierTypeCorporateSerializer, SupplierTypeSalonSerializer,
                                        SupplierTypeGymSerializer, SupplierTypeBusShelterSerializer,
                                        SupplierTypeCodeSerializer, SupplierTypeSocietySerializer, CorporateCompanyDetails,
                                        CorporateParkCompanyListSerializer)
from inventory.serializers import (StandeeInventorySerializer, WallInventorySerializer, PoleInventorySerializer,
                                   StallInventorySerializer, StreetFurnitureSerializer, FlyerInventorySerializer,
                                   InventorySummarySerializer)

# project imports
import utils as ui_utils
import website.utils as website_utils
from coreapi.settings import BASE_DIR
from v0.ui.user.models import UserAreas, UserCities
from v0.constants import keys, decision
from website.utils import save_price_mapping_default
import v0.models as models
import v0.constants as v0_constants


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
            users = models.BaseUser.objects.all()
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
        user = models.BaseUser.objects.get(pk=serializer.data['id'])
        up = UserProfile(user=user, created_by=request.user)
        up.save()
        return Response(serializer.data, status=200)


class getUserData(APIView):

    def get(self, request, id, format=None):
        user = models.BaseUser.objects.get(pk=id)
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
        user = models.BaseUser.objects.get(pk=id)
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
        user = models.BaseUser.objects.get(pk=id)
        user.set_password(request.data['password'])
        user.save()
        return Response(status=200)

    def delete(self, request, id, format=None):
        try:
            item = models.BaseUser.objects.get(pk=id)
        except User.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class deleteUsersAPIView(APIView):

    def post(self, request, format=None):
        models.BaseUser.objects.filter(id__in=request.data).delete()
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


class GetLocationsAPIView(APIView):
    def get(self, request, id, format=None):
        class_name = self.__class__.__name__
        try:
            type = request.query_params.get('type', None)
            if type == 'areas':
                items = CityArea.objects.filter(city_code__id=id)
                serializer = CityAreaSerializer(items, many=True)
            elif type == 'sub_areas':
                items = CitySubArea.objects.filter(area_code__id=id)
                serializer = CitySubAreaSerializer(items, many=True)
            return Response(serializer.data)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


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

            city_object = models.City.objects.get(id=data['city_id'])
            city_code = city_object.city_code

            data['supplier_id'] = ui_utils.get_supplier_id(data)
            data['supplier_type_code'] = request.data['supplier_type']
            data['current_user'] = request.user
            response = ui_utils.make_supplier_data(data)
            if not response.data['status']:
                return response
            all_supplier_data = response.data['data']
            return ui_utils.handle_response(class_name, data=ui_utils.save_supplier_data(user, all_supplier_data),
                                            success=True)
        except ObjectDoesNotExist as e:
            return ui_utils.handle_response(class_name, exception_object=e)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


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
                return ui_utils.handle_response(class_name, data='No Supplier type code provided')

            content_type_response = ui_utils.get_content_type(supplier_type_code)
            if not content_type_response.data['status']:
                return ui_utils.handle_response(class_name, data='No content type found')

            content_type = content_type_response.data['data']
            supplier_object = ui_utils.get_model(supplier_type_code).objects.get(pk=id)

            serializer_class = ui_utils.get_serializer(supplier_type_code)
            serializer = serializer_class(supplier_object)
            result['supplier_data'] = serializer.data

            images = ImageMapping.objects.filter(object_id=id, content_type=content_type)
            image_serializer = ImageMappingSerializer(images, many=True)
            result['supplier_images'] = image_serializer.data

            amenities = SupplierAmenitiesMap.objects.filter(object_id=id, content_type=content_type)
            amenity_serializer = SupplierAmenitiesMapSerializer(amenities, many=True)
            result['amenities'] = amenity_serializer.data

            return ui_utils.handle_response(class_name, data=result, success=True)

        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


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
        content_type = models.ContentType.objects.get_for_model(SupplierTypeSociety)

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
                    city_query = ui_utils.get_region_based_query(user, v0_constants.valid_regions['CITY'],
                                                                 v0_constants.society)
                    society_objects = SupplierTypeSociety.objects.filter(city_query)

            # modify items to have society images data
            society_objects = ui_utils.get_supplier_image(society_objects, 'Society')
            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(society_objects, request)
            paginator_response = paginator.get_paginated_response(result_page)
            data = {
                'count': len(society_objects),
                'societies': paginator_response.data
            }
            return ui_utils.handle_response(class_name, data=data, success=True)
        except SupplierTypeSociety.DoesNotExist:
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
                city_query = ui_utils.get_region_based_query(user, v0_constants.valid_regions['CITY'],
                                                             v0_constants.society)
                society_objects = SupplierTypeSociety.objects.filter(city_query)

            serializer = SupplierTypeSocietySerializer(society_objects, many=True)
            suppliers = website_utils.manipulate_object_key_values(serializer.data)
            societies_with_images = ui_utils.get_supplier_image(suppliers, v0_constants.society_name)
            data = {
                'count': len(societies_with_images),
                'societies': societies_with_images
            }
            return ui_utils.handle_response(class_name, data=data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


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
                city_query = ui_utils.get_region_based_query(user, v0_constants.valid_regions['CITY'],
                                                             v0_constants.corporate_code)
                corporates = SupplierTypeCorporate.objects.filter(city_query)

            serializer = UICorporateSerializer(corporates, many=True)
            corporates_with_images = ui_utils.get_supplier_image(serializer.data, 'Corporate')
            # disabling pagination as search cannot be performed on whole data set
            # paginator = PageNumberPagination()
            # result_page = paginator.paginate_queryset(corporates_with_images, request)
            # paginator_response = paginator.get_paginated_response(result_page)
            data = {
                'count': len(corporates_with_images),
                'corporates': corporates_with_images
            }
            return ui_utils.handle_response(class_name, data=data, success=True)
        except ObjectDoesNotExist as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    def retrieve(self, request, pk=None):
        """
        Retrieve Corporate
        """
        class_name = self.__class__.__name__
        try:
            corporate_instance = SupplierTypeCorporate.objects.get(pk=pk)
            serializer = UICorporateSerializer(corporate_instance)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except ObjectDoesNotExist as e:
            return ui_utils.handle_response(class_name, data=pk, exception_object=e)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

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
                return ui_utils.handle_response(class_name, data=serializer.data, success=True)
            return ui_utils.handle_response(class_name, data=serializer.errors)
        except ObjectDoesNotExist as e:
            return ui_utils.handle_response(class_name, data=pk, exception_object=e)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

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
                return ui_utils.handle_response(class_name, data=serializer.data, success=True)
            return ui_utils.handle_response(class_name, data=serializer.errors)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

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

            corporates_with_images = ui_utils.get_supplier_image(serializer.data, 'Corporate')
            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(corporates_with_images, request)

            paginator_response = paginator.get_paginated_response(result_page)
            data = {
                'count': len(corporates_with_images),
                'corporates': paginator_response.data
            }
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


class SalonViewSet(viewsets.ViewSet):

    def list(self, request):

        class_name = self.__class__.__name__
        try:
            user = request.user
            if user.is_superuser:
                salon_objects = SupplierTypeSalon.objects.all().order_by('name')
            else:
                city_query = ui_utils.get_region_based_query(user, v0_constants.valid_regions['CITY'],
                                                             v0_constants.salon)
                salon_objects = SupplierTypeSalon.objects.filter(city_query)

            salon_serializer = UISalonSerializer(salon_objects, many=True)
            items = ui_utils.get_supplier_image(salon_serializer.data, 'Salon')
            # disabling pagination because search cannot be performed on whole data set
            # paginator = PageNumberPagination()
            # result_page = paginator.paginate_queryset(items, request)
            # paginator_response = paginator.get_paginated_response(result_page)
            data = {
                'count': len(salon_serializer.data),
                'salons': items
            }
            return ui_utils.handle_response(class_name, data=data, success=True)
        except ObjectDoesNotExist as e:
            return ui_utils.handle_response(class_name, data='Salon does not exist', exception_object=e)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


class GymViewSet(viewsets.ViewSet):

    def list(self, request):

        class_name = self.__class__.__name__
        try:
            user = request.user
            if user.is_superuser:
                gym_objects = SupplierTypeGym.objects.all().order_by('name')
            else:
                city_query = ui_utils.get_region_based_query(user, v0_constants.valid_regions['CITY'], v0_constants.gym)
                gym_objects = SupplierTypeGym.objects.filter(city_query)

            gym_shelter_serializer = SupplierTypeGymSerializer(gym_objects, many=True)
            items = ui_utils.get_supplier_image(gym_shelter_serializer.data, 'Gym')
            # disabling pagination because search cannot be performed on whole data set
            # paginator = PageNumberPagination()
            # result_page = paginator.paginate_queryset(items, request)
            # paginator_response = paginator.get_paginated_response(result_page)
            data = {
                'count': len(gym_shelter_serializer.data),
                'gyms': items
            }
            return ui_utils.handle_response(class_name, data=data, success=True)
        except ObjectDoesNotExist as e:
            return ui_utils.handle_response(class_name, data='Gym does not exist', exception_object=e)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


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
                        supplier_instance = models.SupplierTypeSociety.objects.get(supplier_id=data['supplier_id'])
                    except ObjectDoesNotExist:
                        supplier_instance = None
                    if not supplier_instance:
                        continue

                    data['object_id'] = data['supplier_id']
                    obj, created = models.InventorySummary.objects.update_or_create(supplier_id=supplier_instance,
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
        class_name = self.__class__.__name__
        try:

            response = ui_utils.get_supplier_inventory(request.data.copy(), id)

            if not response.data['status']:
                return response

            data = response.data['data']['request_data']

            supplier_object = response.data['data']['supplier_object']
            inventory_object = response.data['data']['inventory_object']
            supplier_type_code = request.data['supplier_type_code']
            # supplier_type_code = 'CP'
            # society = SupplierTypeSociety.objects.get(pk=id)
            # item = InventorySummary.objects.get(supplier=society)
            tower_response = ui_utils.get_tower_count(supplier_object, supplier_type_code)
            if not tower_response.data['status']:
                return tower_response
            towercount = tower_response.data['data']

            poster_campaign = 0
            standee_campaign = 0
            stall_campaign = 0
            flier_campaign = 0
            total_campaign = 0

            with transaction.atomic():
                if request.data.get('poster_allowed_nb'):
                    if request.data.get('nb_count'):
                        supplier_object.poster_allowed_nb = True
                        poster_campaign = int(request.data.get('nb_count'))
                        request.data['poster_campaign'] = poster_campaign
                    else:
                        supplier_object.poster_allowed_nb = False
                else:
                    supplier_object.poster_allowed_nb = False

                if request.data.get('lift_count') and request.data.get('poster_allowed_lift'):
                    if request.data.get('lift_count') > 0:
                        supplier_object.poster_allowed_lift = True
                        poster_campaign = poster_campaign + int(request.data.get('lift_count'))
                        request.data['poster_campaign'] = poster_campaign
                    else:
                        supplier_object.poster_allowed_lift = False
                else:
                    supplier_object.poster_allowed_lift = False

                if request.data.get('standee_allowed'):
                    if request.data.get('total_standee_count'):
                        supplier_object.standee_allowed = True
                        standee_campaign = int(request.data.get('total_standee_count'))
                        request.data['standee_campaign'] = standee_campaign
                    else:
                        supplier_object.standee_allowed = False
                else:
                    supplier_object.standee_allowed = False

                if request.data.get('stall_allowed') or request.data.get('car_display_allowed'):
                    if request.data.get('total_stall_count'):
                        stall_campaign = int(request.data.get('total_stall_count'))
                        request.data['stall_or_cd_campaign'] = stall_campaign

                if request.data.get('flier_allowed'):
                    if request.data.get('flier_frequency'):
                        supplier_object.flier_allowed = True
                        flier_campaign = int(request.data.get('flier_frequency'))
                        request.data['flier_campaign'] = flier_campaign
                    else:
                        supplier_object.flier_allowed = False
                else:
                    supplier_object.flier_allowed = False

                # flier creation

                flag1 = True
                if 'id' in request.data:
                    flag1 = False
                    if request.data.get('flier_allowed'):
                        if request.data.get('flier_frequency') and inventory_object.flier_frequency < request.data.get(
                                'flier_frequency'):
                            if not inventory_object.flier_frequency:
                                ui_utils.save_flyer_locations(0, request.data.get('flier_frequency'), supplier_object,
                                                              supplier_type_code)
                            else:
                                ui_utils.save_flyer_locations(inventory_object.flier_frequency,
                                                              request.data.get('flier_frequency'), supplier_object,
                                                              supplier_type_code)
                        serializer = InventorySummarySerializer(inventory_object, data=data)
                else:
                    if flag1 and request.data.get('flier_frequency'):
                        ui_utils.save_flyer_locations(0, request.data['flier_frequency'], supplier_object,
                                                      supplier_type_code)
                    serializer = InventorySummarySerializer(data=data)

                supplier_object.stall_allowed = True if request.data.get('stall_allowed') else False
                supplier_object.car_display_allowed = True if request.data.get('car_display_allowed') else False

                # society = SupplierTypeSociety.objects.get(pk=id)
                supplier_object.total_campaign = poster_campaign + standee_campaign + stall_campaign + flier_campaign
                supplier_object.save()

                # stall creation
                flag = True
                if 'id' in request.data:
                    flag = False
                    if request.data.get('stall_allowed'):
                        if request.data.get(
                                'total_stall_count') and inventory_object.total_stall_count < request.data.get(
                            'total_stall_count'):
                            if not inventory_object.total_stall_count:
                                ui_utils.save_stall_locations(0, request.data.get('total_stall_count'), supplier_object,
                                                              supplier_type_code)
                            else:
                                ui_utils.save_stall_locations(inventory_object.total_stall_count,
                                                              request.data.get('total_stall_count'), supplier_object,
                                                              supplier_type_code)
                    serializer = InventorySummarySerializer(inventory_object, data=data)

                else:
                    if flag and request.data.get('total_stall_count'):
                        ui_utils.save_stall_locations(0, request.data.get('total_stall_count'), supplier_object,
                                                      supplier_type_code)
                        #
                        # serializer = InventorySummarySerializer(data=data)
                        # if serializer.is_valid():
                        #     serializer.save(supplier=supplier_object)
                        # else :
                        #     return Response({'error': serializer.errors},status=400)

                adinventory_dict = ui_utils.adinventory_func()
                duration_type_dict = ui_utils.duration_type_func()
                price_list = []
                if request.data.get('poster_price_week_nb'):

                    posPrice = int(request.data.get('poster_price_week_nb'))
                    if request.data.get('poster_allowed_nb'):
                        if request.data.get('nb_A3_allowed'):
                            price = PriceMappingDefault.objects.get_price_mapping_object(
                                ui_utils.make_dict_manager(adinventory_dict['poster_a3'],
                                                           duration_type_dict['campaign_weekly']), id,
                                supplier_type_code)
                            ui_utils.save_price_data(price, posPrice)

                            price = PriceMappingDefault.objects.get_price_mapping_object(
                                ui_utils.make_dict_manager(adinventory_dict['poster_a3'],
                                                           duration_type_dict['unit_weekly']), id, supplier_type_code)
                            ui_utils.save_price_data(price, posPrice / towercount)

                        if request.data.get('nb_A4_allowed'):
                            price = PriceMappingDefault.objects.get_price_mapping_object(
                                ui_utils.make_dict_manager(adinventory_dict['poster_a4'],
                                                           duration_type_dict['campaign_weekly']), id,
                                supplier_type_code)
                            ui_utils.save_price_data(price, posPrice)

                            price = PriceMappingDefault.objects.get_price_mapping_object(
                                ui_utils.make_dict_manager(adinventory_dict['poster_a4'],
                                                           duration_type_dict['unit_weekly']), id, supplier_type_code)
                            ui_utils.save_price_data(price, posPrice / towercount)

                if request.data.get('poster_price_week_lift'):
                    posPrice = int(request.data.get('poster_price_week_lift'))
                    if request.data.get('poster_allowed_lift'):
                        price = PriceMappingDefault.objects.get_price_mapping_object(
                            ui_utils.make_dict_manager(adinventory_dict['poster_lift_a3'],
                                                       duration_type_dict['campaign_weekly']), id, supplier_type_code)
                        ui_utils.save_price_data(price, posPrice)

                        price = PriceMappingDefault.objects.get_price_mapping_object(
                            ui_utils.make_dict_manager(adinventory_dict['poster_lift_a3'],
                                                       duration_type_dict['unit_weekly']), id, supplier_type_code)
                        ui_utils.save_price_data(price, posPrice / towercount)

                        price = PriceMappingDefault.objects.get_price_mapping_object(
                            ui_utils.make_dict_manager(adinventory_dict['poster_lift_a4'],
                                                       duration_type_dict['campaign_weekly']), id, supplier_type_code)
                        ui_utils.save_price_data(price, posPrice)

                        price = PriceMappingDefault.objects.get_price_mapping_object(
                            ui_utils.make_dict_manager(adinventory_dict['poster_lift_a4'],
                                                       duration_type_dict['unit_weekly']), id, supplier_type_code)
                        ui_utils.save_price_data(price, posPrice / towercount)

                if request.data.get('standee_price_week'):
                    stanPrice = int(request.data.get('standee_price_week'))
                    if request.data.get('standee_allowed'):
                        if request.data.get('standee_small'):
                            price = PriceMappingDefault.objects.get_price_mapping_object(
                                ui_utils.make_dict_manager(adinventory_dict['standee_small'],
                                                           duration_type_dict['campaign_weekly']), id,
                                supplier_type_code)

                            ui_utils.save_price_data(price, stanPrice)

                            price = PriceMappingDefault.objects.get_price_mapping_object(
                                ui_utils.make_dict_manager(adinventory_dict['standee_small'],
                                                           duration_type_dict['unit_weekly']), id, supplier_type_code)
                            ui_utils.save_price_data(price, stanPrice / towercount)

                        if request.data.get('standee_medium'):
                            price = PriceMappingDefault.objects.get_price_mapping_object(
                                ui_utils.make_dict_manager(adinventory_dict['standee_medium'],
                                                           duration_type_dict['campaign_weekly']), id,
                                supplier_type_code)

                            ui_utils.save_price_data(price, stanPrice)

                            price = PriceMappingDefault.objects.get_price_mapping_object(
                                ui_utils.make_dict_manager(adinventory_dict['standee_medium'],
                                                           duration_type_dict['unit_weekly']), id, supplier_type_code)
                            ui_utils.save_price_data(price, stanPrice / towercount)

                if request.data.get('stall_allowed'):
                    if request.data.get('stall_small'):
                        if request.data.get('stall_price_day_small'):
                            stallPrice = int(request.data.get('stall_price_day_small'))

                            price = PriceMappingDefault.objects.get_price_mapping_object(
                                ui_utils.make_dict_manager(adinventory_dict['stall_small'],
                                                           duration_type_dict['unit_daily']), id, supplier_type_code)
                            ui_utils.save_price_data(price, stallPrice)

                            price = PriceMappingDefault.objects.get_price_mapping_object(
                                ui_utils.make_dict_manager(adinventory_dict['stall_canopy'],
                                                           duration_type_dict['unit_daily']), id, supplier_type_code)
                            ui_utils.save_price_data(price, stallPrice)

                    if request.data.get('stall_large'):
                        if request.data.get('stall_price_day_large'):
                            stallPrice = int(request.data.get('stall_price_day_large'))

                            price = PriceMappingDefault.objects.get_price_mapping_object(
                                ui_utils.make_dict_manager(adinventory_dict['stall_large'],
                                                           duration_type_dict['unit_daily']), id, supplier_type_code)
                            ui_utils.save_price_data(price, stallPrice)

                if request.data.get('car_display_allowed'):
                    if request.data.get('cd_standard'):
                        if request.data.get('cd_price_day_standard'):
                            cdPrice = int(request.data['cd_price_day_standard'])

                            price = PriceMappingDefault.objects.get_price_mapping_object(
                                ui_utils.make_dict_manager(adinventory_dict['car_display_standard'],
                                                           duration_type_dict['unit_daily']), id, supplier_type_code)
                            ui_utils.save_price_data(price, cdPrice)

                    if request.data.get('cd_premium'):
                        if request.data.get('cd_price_day_premium'):
                            cdPrice = int(request.data.get('cd_price_day_premium'))

                            price = PriceMappingDefault.objects.get_price_mapping_object(
                                ui_utils.make_dict_manager(adinventory_dict['car_display_premium'],
                                                           duration_type_dict['unit_daily']), id, supplier_type_code)
                            ui_utils.save_price_data(price, cdPrice)

                if request.data.get('flier_price_day'):
                    flierPrice = int(request.data.get('flier_price_day'))
                    if request.data.get('mailbox_allowed'):
                        price = PriceMappingDefault.objects.get_price_mapping_object(
                            ui_utils.make_dict_manager(adinventory_dict['flier_mailbox'],
                                                       duration_type_dict['unit_daily']), id, supplier_type_code)
                        ui_utils.save_price_data(price, flierPrice)

                    if request.data.get('d2d_allowed'):
                        price = PriceMappingDefault.objects.get_price_mapping_object(
                            ui_utils.make_dict_manager(adinventory_dict['flier_door_to_door'],
                                                       duration_type_dict['unit_daily']), id, supplier_type_code)
                        ui_utils.save_price_data(price, flierPrice)

                    if request.data.get('flier_lobby_allowed'):
                        try:
                            price = PriceMappingDefault.objects.get_price_mapping_object(
                                ui_utils.make_dict_manager(adinventory_dict['flier_lobby'],
                                                           duration_type_dict['unit_daily']), id, supplier_type_code)
                            ui_utils.save_price_data(price, flierPrice)

                        except KeyError as e:
                            raise KeyError(e.message)
                if request.data.get('gateway_arch_allowed'):
                    ui_utils.save_gateway_arch_location(supplier_object, supplier_type_code)

                serializer = InventorySummarySerializer(inventory_object, data=data)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)
        except Exception as e:
            return Response(data={"status": False, "error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)


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

                basic_item['supplier'] = basic_select_item.__dict__['_supplier_cache'].__dict__ if \
                basic_select_item.__dict__['_supplier_cache'] else None
                basic_item['adinventory_type'] = basic_select_item.__dict__['_adinventory_type_cache'].__dict__
                basic_item['duration_type'] = basic_select_item.__dict__['_duration_type_cache'].__dict__

                if basic_item['adinventory_type']:
                    basic_item['adinventory_type'].pop("_state", None)
                if basic_item['duration_type']:
                    basic_item['duration_type'].pop("_state", None)
                if basic_item['supplier']:
                    basic_item['supplier'].pop("_state", None)

            response['tower_count'] = tower_count
            response['prices'] = basic_prices

            return Response(response, status=200)

        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        except PriceMappingDefault.DoesNotExist:
            return Response(status=404)
        except Exception as e:
            return Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)

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
        society_content_type = models.ContentType.objects.get_for_model(SupplierTypeSociety)
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
                flyer_serializer = FlyerInventorySerializer(data=flier)

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
                    return ui_utils.handle_response(class_name, data=serializer.errors)

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
            return ui_utils.handle_response(class_name, data='Invalid Gym Info data')

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
            return ui_utils.handle_response(class_name, data='provide supplier type code', success=False)
        data = request.data.copy()
        data['supplier_id'] = id
        basic_details_response = ui_utils.save_basic_supplier_details(supplier_type_code, data)
        if not basic_details_response.data['status']:
            return basic_details_response
        return ui_utils.handle_response(class_name, data=basic_details_response.data['data'], success=True)

    def get(self, request):
        # fetch all and list Bus Shelters 

        class_name = self.__class__.__name__

        try:
            user = request.user

            if user.is_superuser:
                bus_objects = SupplierTypeBusShelter.objects.all().order_by('name')
            else:
                city_query = ui_utils.get_region_based_query(user, v0_constants.valid_regions['CITY'],
                                                             v0_constants.bus_shelter)
                bus_objects = SupplierTypeBusShelter.objects.filter(city_query)

            bus_shelter_serializer = BusShelterSerializer(bus_objects, many=True)
            items = ui_utils.get_supplier_image(bus_shelter_serializer.data, 'Bus Shelter')
            # disabling pagination because search cannot be performed in whole data set.
            # paginator = PageNumberPagination()
            # result_page = paginator.paginate_queryset(items, request)
            # paginator_response = paginator.get_paginated_response(result_page)
            data = {
                'count': len(bus_shelter_serializer.data),
                'busshelters': items
            }
            return ui_utils.handle_response(class_name, data=data, success=True)
        except SupplierTypeBusShelter.DoesNotExist as e:
            return ui_utils.handle_response(class_name, data='Bus Shelter object does not exist', exception_object=e)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


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
                return ui_utils.handle_response(class_name, data='Search Text is not provided')
            items = SupplierTypeBusShelter.objects.filter(
                Q(supplier_id__icontains=search_txt) | Q(name__icontains=search_txt) | Q(
                    address1__icontains=search_txt) | Q(city__icontains=search_txt) | Q(
                    state__icontains=search_txt)).order_by('name')
            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(items, request)
            serializer = SupplierTypeBusShelterSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except SupplierTypeBusShelter.DoesNotExist as e:
            return ui_utils.handle_response(class_name, data='Bus Shelter object does not exist', exception_object=e)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


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
            events = models.Events.objects.filter(object_id=supplier_id, content_type=content_type)
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
            serializer = EventsSerializer(models.Events.objects.get(pk=pk))
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
            event = models.Events.objects.get(pk=pk)
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

            event, is_created = models.Events.objects.get_or_create(event_name=event_name, object_id=supplier_id,
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
            models.Events.objects.get(pk=pk).delete()
            return ui_utils.handle_response(class_name, data=pk, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


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
            valid_supplier_type_code_instances = models.SupplierTypeCode.objects.all()
            data = {}

            for instance in valid_supplier_type_code_instances:
                supplier_type_code = instance.supplier_type_code
                error = False
                try:
                    model_name = ui_utils.get_model(supplier_type_code)
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
                    data[supplier_type_code]['retail_shop_types'] = [tup[0] for tup in models.RETAIL_SHOP_TYPE]

            return ui_utils.handle_response(class_name, data=data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


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
                return ui_utils.handle_response(class_name, data=serializer.data, success=True)
            return ui_utils.handle_response(class_name, data=serializer.errors)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    def list(self, request):
        class_name = self.__class__.__name__
        try:
            # all retail_shop_objects sorted by name
            user = request.user
            if user.is_superuser:
                retail_shop_objects = models.SupplierTypeRetailShop.objects.all().order_by('name')
            else:
                city_query = ui_utils.get_region_based_query(user, v0_constants.valid_regions['CITY'],
                                                             v0_constants.retail_shop_code)
                retail_shop_objects = models.SupplierTypeRetailShop.objects.filter(city_query)
            serializer = RetailShopSerializer(retail_shop_objects, many=True)
            retail_shop_with_images = ui_utils.get_supplier_image(serializer.data, 'Retail Shop')

            # disabling paginators because search cannot be performed in front end in whole data set
            # paginator = PageNumberPagination()
            # result_page = paginator.paginate_queryset(retail_shop_with_images, request)
            # paginator_response = paginator.get_paginated_response(result_page)
            data = {
                'count': len(serializer.data),
                'retail_shop_objects': retail_shop_with_images
            }
            return ui_utils.handle_response(class_name, data=data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    def update(self, request, pk):
        class_name = self.__class__.__name__
        try:
            retail_shop_instance = models.SupplierTypeRetailShop.objects.get(pk=pk)
            serializer = RetailShopSerializer(instance=retail_shop_instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return ui_utils.handle_response(class_name, data=serializer.data, success=True)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    def retrieve(self, request, pk):
        class_name = self.__class__.__name__
        try:
            retail_shop_instance = models.SupplierTypeRetailShop.objects.get(pk=pk)
            serializer = RetailShopSerializer(instance=retail_shop_instance)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
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
            instances = models.ImageMapping.objects.filter(location_id=supplier_id, content_type=content_type)
            serializer = ImageMappingSerializer(instances, many=True)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    def update(self, request, pk):
        class_name = self.__class__.__name__
        try:
            instance = models.ImageMapping.objects.get(pk=pk)
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
            image_instance = models.ImageMapping.objects.get(pk=data['id'])
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
            states = models.State.objects.all()
            serializer = StateSerializer(states, many=True)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


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
                return ui_utils.handle_response(class_name, data=serializer.data, success=True)
            return ui_utils.handle_response(class_name, data=serializer.errors)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    def list(self, request):
        class_name = self.__class__.__name__
        try:
            bus_depots = models.SupplierTypeBusDepot.objects.all()
            serializer = BusDepotSerializer(bus_depots, many=True)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    def update(self, request, pk=None):
        class_name = self.__class__.__name__
        try:
            instance = models.SupplierTypeBusDepot.objects.get(pk=pk)
            serializer = BusDepotSerializer(instance=instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return ui_utils.handle_response(class_name, data=serializer.data, success=True)
            return ui_utils.handle_response(class_name, data=serializer.errors)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    def retrieve(self, request, pk=None):
        class_name = self.__class__.__name__
        try:
            instance = models.SupplierTypeBusDepot.objects.get(pk=pk)
            serializer = BusDepotSerializer(instance=instance)
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
