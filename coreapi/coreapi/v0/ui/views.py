# python core imports
import json
import csv

# django imports
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import IntegrityError
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict

# third party imports
import requests
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from v0.permissions import IsOwnerOrManager
from rest_framework import filters
from serializers import UISocietySerializer, UITowerSerializer, UICorporateSerializer, UISalonSerializer, UIGymSerializer
from v0.serializers import ImageMappingSerializer, InventoryLocationSerializer, AdInventoryLocationMappingSerializer, AdInventoryTypeSerializer,\
                    DurationTypeSerializer, PriceMappingDefaultSerializer, PriceMappingSerializer, BannerInventorySerializer,\
                    CommunityHallInfoSerializer, DoorToDoorInfoSerializer, LiftDetailsSerializer, NoticeBoardDetailsSerializer,\
                    PosterInventorySerializer, SocietyFlatSerializer, StandeeInventorySerializer, SwimmingPoolInfoSerializer, WallInventorySerializer,\
                    UserInquirySerializer, CommonAreaDetailsSerializer, ContactDetailsSerializer, EventsSerializer, InventoryInfoSerializer, \
                    MailboxInfoSerializer, OperationsInfoSerializer, PoleInventorySerializer, PosterInventoryMappingSerializer, RatioDetailsSerializer, \
                    SignupSerializer, StallInventorySerializer, StreetFurnitureSerializer, SupplierInfoSerializer, SportsInfraSerializer, \
                    SupplierTypeSocietySerializer, SupplierTypeCorporateSerializer, SocietyTowerSerializer, FlatTypeSerializer,\
                    CorporateBuildingSerializer, CorporateBuildingWingSerializer, CorporateCompanyDetailsSerializer, \
                    CompanyFloorSerializer, CorporateBuildingGetSerializer, CorporateCompanySerializer, CorporateParkCompanySerializer, \
                    SupplierTypeSalonSerializer, SupplierTypeGymSerializer, FlyerInventorySerializer

from v0.models import CorporateParkCompanyList, ImageMapping, InventoryLocation, AdInventoryLocationMapping, AdInventoryType, DurationType, PriceMappingDefault, PriceMapping, BannerInventory, CommunityHallInfo, DoorToDoorInfo, LiftDetails, NoticeBoardDetails, PosterInventory, SocietyFlat, StandeeInventory, SwimmingPoolInfo, WallInventory, UserInquiry, CommonAreaDetails, ContactDetails, Events, InventoryInfo, MailboxInfo, OperationsInfo, PoleInventory, PosterInventoryMapping, RatioDetails, Signup, StallInventory, StreetFurniture, SupplierInfo, SportsInfra, SupplierTypeSociety, SocietyTower, FlatType, SupplierTypeCorporate, ContactDetailsGeneric, CorporateParkCompanyList,FlyerInventory
from v0.models import City, CityArea, CitySubArea,SupplierTypeCode, InventorySummary, SocietyMajorEvents, UserProfile, CorporateBuilding, \
                    CorporateBuildingWing, CorporateBuilding, CorporateCompanyDetails, CompanyFloor, SupplierTypeSalon, SupplierTypeGym
from v0.serializers import CitySerializer, CityAreaSerializer, CitySubAreaSerializer, SupplierTypeCodeSerializer, InventorySummarySerializer, SocietyMajorEventsSerializer, UserSerializer, UserProfileSerializer, ContactDetailsGenericSerializer, CorporateParkCompanyListSerializer
from v0.ui.serializers import SocietyListSerializer

# project imports
import utils as ui_utils
from coreapi.settings import BASE_URL, BASE_DIR
from v0.models import City, CityArea, CitySubArea, UserCities, UserAreas
from constants import keys, decision


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
            users = User.objects.all()
        serializer = UserSerializer(users, many = True)
        return Response(serializer.data, status = 200)

    def post(self, request, format=None):
        data = request.data
        data['user_permissions'] = []
        data['groups'] = []

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=400)
        user = User.objects.get(pk=serializer.data['id'])
        up = UserProfile(user=user, created_by=request.user)
        up.save()
        return Response(serializer.data, status=200)


class getUserData(APIView):

    def get(self, request, id, format=None):
            user = User.objects.get(pk=id)
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
        user = User.objects.get(pk=id)
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
            UserCities.objects.filter(user__id=id,city__id__in=del_diff).delete()
        if len(new_diff) > 0:
            for key in new_diff:
                UserCities.objects.create(user=user, city_id=key)

        prev_ids = UserAreas.objects.filter(user__id=id).values_list('area__id', flat=True)
        new_ids = request.data['selectedAreas']
        del_diff = list(set(prev_ids) - set(new_ids))
        new_diff = list(set(new_ids) - set(prev_ids))
        if del_diff:
            UserAreas.objects.filter(user__id=id,area__id__in=del_diff).delete()
        if len(new_diff) > 0:
            for key in new_diff:
                UserAreas.objects.create(user=user, area_id=key)

        return Response(status=200)

    #to update password
    def put(self, request, id, format=None):
        user = User.objects.get(pk=id)
        user.set_password(request.data['password'])
        user.save()
        return Response(status=200)

    def delete(self, request, id, format=None):
        try:
            item = User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class deleteUsersAPIView(APIView):

    def post(self, request, format=None):
        User.objects.filter(id__in=request.data).delete()
        return Response(status=204)



class getInitialDataAPIView(APIView):
    def get(self, request, format=None):
        try:
            user = request.user
            cities = City.objects.all()
            serializer = CitySerializer(cities, many=True)
            # if user.user_profile.all().first() and user.user_profile.all().first().is_city_manager:
            #     areas = CityArea.objects.filter(city_code__in=[item.city for item in user.cities.all()])
            # else:
            #     areas = CityArea.objects.all()
            # serializer1 = CityAreaSerializer(areas, many=True)
            items = SupplierTypeCode.objects.all()
            serializer2 = SupplierTypeCodeSerializer(items, many=True)
            # result = {'cities':serializer.data, 'city_areas': serializer1.data, 'supplier_types':serializer2.data}
            result = {'cities':serializer.data, 'supplier_types':serializer2.data}
            return Response(result, status=200)
        except :
            return Response(status=404)


class getLocationsAPIView(APIView):
    def get(self, request, id, format=None):
        try:
            type = request.query_params.get('type', None)
            if type=='areas':
                items = CityArea.objects.filter(city_code__id=id)
                serializer = CityAreaSerializer(items, many=True)
            elif type=='sub_areas':
                items = CitySubArea.objects.filter(area_code__id=id)
                serializer = CitySubAreaSerializer(items, many=True)
            return Response(serializer.data)
        except :
            return Response(status=404)

class checkSupplierCodeAPIView(APIView):
    def get(self, request, code, format=None):
        try:
            society = SupplierTypeSociety.objects.get(supplier_code=code)
            if society:
                return Response(status=200)
        except SupplierTypeSociety.DoesNotExist :
            return Response(status=404)


class GenerateSupplierIdAPIView(APIView):
    """
    Generic API that generates unique supplier id and also saves supplier data
    """
    def post(self, request, format=None):
        try:

            data = {
                'city': request.data['city_id'],
                'area': request.data['area_id'],
                'sub_area': request.data['subarea_id'],
                'supplier_type': request.data['supplier_type'],
                'supplier_code': request.data['supplier_code'],
                'supplier_name': request.data['supplier_name'],
            }

            response = ui_utils.get_supplier_id(request, data)
            if not response.data['status']:
                return response

            data['supplier_id'] = response.data['supplier_id']
            data['supplier_type_code'] = request.data['supplier_type']
            data['current_user'] = request.user

            response = ui_utils.make_supplier_data(data)
            if not response.data['status']:
                return response
            all_supplier_data = response.data['data']

            response = ui_utils.save_supplier_data(all_supplier_data)
            if not response.data['status']:
                return response
            return Response(data=response.data['data'], status=status.HTTP_200_OK)

        except ObjectDoesNotExist as e:
            return Response(data={str(e.message) + " Object does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={str(e.message)}, status=status.HTTP_400_BAD_REQUEST)


class SocietyAPIView(APIView):
    # permission_classes = (permissions.IsAuthenticated, IsOwnerOrManager,)

    def get(self, request, id, format=None):
        try:
            response = {}
            item = SupplierTypeSociety.objects.get(pk=id)
            self.check_object_permissions(self.request, item)
            serializer = UISocietySerializer(item)

            #Start : Code changes to display images
            images = ImageMapping.objects.filter(supplier=item)
            image_serializer = ImageMappingSerializer(images, many=True)
            response['society_images'] = image_serializer.data
            #End : Code changes to display images
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
                serializer = SupplierTypeSocietySerializer(society,data=request.data)
            else:

                serializer = SupplierTypeSocietySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=400)

        society = SupplierTypeSociety.objects.filter(pk=serializer.data['supplier_id']).first()

        #here we will start storing contacts
        if request.data and 'basic_contact_available' in request.data and request.data['basic_contact_available']:
            for contact in request.data['basic_contacts']:
                if 'id' in contact:
                   item = ContactDetails.objects.filter(pk=contact['id']).first()
                   contact_serializer = ContactDetailsSerializer(item, data=contact)
                else:
                    contact_serializer = ContactDetailsSerializer(data=contact)
                if contact_serializer.is_valid():
                    contact_serializer.save(supplier=society)

        if request.data and 'basic_reference_available' in request.data and request.data['basic_reference_available']:
            contact = request.data['basic_reference_contacts']
            if 'id' in contact:
                item = ContactDetails.objects.filter(pk=contact['id']).first()
                contact_serializer = ContactDetailsSerializer(item, data=contact)
            else:
                contact_serializer = ContactDetailsSerializer(data=contact)
            if contact_serializer.is_valid():
                contact_serializer.save(supplier = society, contact_type="Reference")


        towercount = SocietyTower.objects.filter(supplier = society).count()
        abc = 0
        if request.data['tower_count'] > towercount:
            abc = request.data['tower_count'] - towercount
        if 'tower_count' in request.data:
            for i in range(abc):
                tower = SocietyTower(supplier = society)
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

        return Response(subarea_serializer.data, status = 200)




class SocietyAPIListView(APIView):
    def get(self, request, format=None):
        try:
            user = request.user
            search_txt = request.query_params.get('search', None)
            if search_txt:
                items = SupplierTypeSociety.objects.filter(Q(supplier_id__icontains=search_txt) | Q(society_name__icontains=search_txt)| Q(society_address1__icontains=search_txt)| Q(society_city__icontains=search_txt)| Q(society_state__icontains=search_txt)).order_by('society_name')
            else:
                if user.is_superuser:
                    items = SupplierTypeSociety.objects.all().order_by('society_name')
                elif user.user_profile.all().first() and user.user_profile.all().first().is_city_manager:
                    items = SupplierTypeSociety.objects.filter(Q(society_city__in=[item.city.city_name for item in user.cities.all()]) | Q(created_by=user.id))

            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(items, request)
            serializer = SocietyListSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)


class CorporateAPIListView(APIView):
    def get(self, request, format=None):
        try:
            user = request.user
            search_txt = request.query_params.get('search', None)

            if search_txt:
                items = SupplierTypeCorporate.objects.filter(Q(supplier_id__icontains=search_txt) | Q(name__icontains=search_txt)| Q(address1__icontains=search_txt)| Q(city__icontains=search_txt)| Q(state__icontains=search_txt)).order_by('name')
            else:
                if user.is_superuser:
                    items = SupplierTypeCorporate.objects.all().order_by('name')
                else:
                    items = SupplierTypeCorporate.objects.filter(created_by=user.id)#todo : No field created by !
            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(items, request)
            serializer = UICorporateSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except SupplierTypeCorporate.DoesNotExist:
            return Response(status=404)
        except Exception as e:
            return Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


class SalonAPIListView(APIView):
    def get(self, request, format=None):
        try:
            user = request.user
            search_txt = request.query_params.get('search', None)
            if search_txt:
                items = SupplierTypeSalon.objects.filter(Q(supplier_id__icontains=search_txt) | Q(name__icontains=search_txt)| Q(address1__icontains=search_txt)| Q(city__icontains=search_txt)| Q(state__icontains=search_txt)).order_by('name')
            else:
                if user.is_superuser:
                    items = SupplierTypeSalon.objects.all().order_by('name')
                else:
                    items = SupplierTypeSalon.objects.filter(created_by=user.id)

            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(items, request)
            serializer = UISalonSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except SupplierTypeSalon.DoesNotExist:
            return Response(status=404)


class GymAPIListView(APIView):
    def get(self, request, format=None):
        try:
            user = request.user
            search_txt = request.query_params.get('search', None)
            if search_txt:
                items = SupplierTypeGym.objects.filter(Q(supplier_id__icontains=search_txt) | Q(name__icontains=search_txt)| Q(address1__icontains=search_txt)| Q(city__icontains=search_txt)| Q(state__icontains=search_txt)).order_by('name')
            else:
                if user.is_superuser:
                    items = SupplierTypeGym.objects.all().order_by('name')
                else:
                    items = SupplierTypeGym.objects.filter(created_by=user.id)

            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(items, request)
            serializer = UIGymSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except SupplierTypeGym.DoesNotExist:
            return Response(status=404)


class SocietyAPIFiltersListView(APIView):

    # self.paginator = None
    # self.serializer = None

    # def get(self,request, format=None):
    #     return self.paginator.get_paginated_response(self.serializer.data)

    def post(self, request, format=None):
        try:
            # two list to disable search on society and flats if all the options in both the fields selected
            allflatquantity = [u'Large', u'Medium', u'Small', u'Very Large']    # in sorted order
            allsocietytype = ['High', 'Medium High', 'Standard', 'Ultra High'] # in sorted order
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

            if (not subareas) and'locationValueModel' in request.data:
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
            if flatquantity == allflatquantity: # sorted comparison to avoid mismatch based on index
                flatquantity = []
            if  societytype == allsocietytype:   # same as above
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
                    if  societytype and flatquantity and inventorytype:
                        items = SupplierTypeSociety.objects.filter(Q(society_subarea__in = citySubArea) & Q(society_type_quality__in = societytype) & Q(society_type_quantity__in = flatquantity))
                    elif societytype and flatquantity:
                        items = SupplierTypeSociety.objects.filter(Q(society_subarea__in = citySubArea) & Q(society_type_quality__in = societytype) & Q(society_type_quantity__in = flatquantity))
                    elif societytype and inventorytype:
                        items = SupplierTypeSociety.objects.filter(Q(society_subarea__in = citySubArea) & Q(society_type_quality__in = societytype))
                    elif flatquantity and inventorytype:
                        items = SupplierTypeSociety.objects.filter(Q(society_subarea__in = citySubArea) & Q(society_type_quantity__in = flatquantity))
                    elif societytype:
                        items = SupplierTypeSociety.objects.filter(Q(society_subarea__in = citySubArea) & Q(society_type_quality__in = societytype))
                    elif flatquantity:
                        items = SupplierTypeSociety.objects.filter(Q(society_subarea__in = citySubArea) & Q(society_type_quantity__in = flatquantity))
                    # elif inventorytype:
                    #     do something
                    else :
                        items = SupplierTypeSociety.objects.filter(society_subarea__in = citySubArea)

                elif areas :
                    if societytype and flatquantity and inventorytype:
                        items = SupplierTypeSociety.objects.filter(Q(society_locality__in = cityArea) & Q(society_type_quality__in = societytype) & Q(society_type_quantity__in = flatquantity))
                    elif societytype and flatquantity:
                        items = SupplierTypeSociety.objects.filter(Q(society_locality__in = cityArea) & Q(society_type_quality__in = societytype) & Q(society_type_quantity__in = flatquantity))
                    elif societytype and inventorytype:
                        items = SupplierTypeSociety.objects.filter(Q(society_locality__in = cityArea) & Q(society_type_quality__in = societytype))
                    elif flatquantity and inventorytype:
                        items = SupplierTypeSociety.objects.filter(Q(society_locality__in = cityArea) & Q(society_type_quantity__in = flatquantity))
                    elif societytype:
                        items = SupplierTypeSociety.objects.filter(Q(society_locality__in = cityArea) & Q(society_type_quality__in = societytype))
                    elif flatquantity:
                        items = SupplierTypeSociety.objects.filter(Q(society_locality__in = cityArea) & Q(society_type_quantity__in = flatquantity))
                    # elif inventorytype:
                    #     do something

                    else:
                        items = SupplierTypeSociety.objects.filter(society_locality__in = cityArea)     

                elif societytype or flatquantity or inventorytype :
                    if societytype and flatquantity and inventorytype:
                        items = SupplierTypeSociety.objects.filter(Q(society_type_quality__in = societytype) & Q(society_type_quantity__in = flatquantity))
                    elif societytype and flatquantity:
                        items = SupplierTypeSociety.objects.filter(Q(society_type_quality__in = societytype) & Q(society_type_quantity__in = flatquantity))
                    elif societytype and inventorytype:
                        items = SupplierTypeSociety.objects.filter(Q(society_type_quality__in = societytype))
                    elif flatquantity and inventorytype:
                        items = SupplierTypeSociety.objects.filter(Q(society_type_quantity__in = flatquantity))
                    elif societytype:
                        items = SupplierTypeSociety.objects.filter(Q(society_type_quality__in = societytype))
                    elif flatquantity:
                        items = SupplierTypeSociety.objects.filter(Q(society_type_quantity__in = flatquantity))
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
                    


            serializer = SocietyListSerializer(items, many= True)
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
    def post(self,request,format=None):
        order = request.query_params.get('order',None)
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
        society_ids = SupplierTypeSociety.objects.all().values_list('supplier_id',flat=True)
        return Response({'society_ids' : society_ids}, status=200)


class FlatTypeAPIView(APIView):
    def get(self, request, id, format=None):
        try:
            society=SupplierTypeSociety.objects.get(pk=id)
            flatType = SupplierTypeSociety.objects.get(pk=id).flatTypes.all()
            serializer = FlatTypeSerializer(flatType, many=True)
            count = len(serializer.data)

            if count > 0:
                flat_details_available=True
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
        society=SupplierTypeSociety.objects.get(pk=id)
        num = 0.0
        den = 0.0
        totalFlats = 0
        flag = True
        if request.data['flat_details_available']:
            for key in request.data['flat_details']:
                if 'size_builtup_area' in key and 'flat_rent' in key and key['size_builtup_area'] > 0 and key['flat_rent'] > 0:
                    rent = key['flat_rent']
                    area = key['size_builtup_area']
                    key['average_rent_per_sqft'] = rent/area
                    if 'flat_count' in key:
                        count = key['flat_count']
                        num = num+(count*key['average_rent_per_sqft'])
                        den = den+count
                    else:
                        flag = False
                else:
                    flag = False

                if 'size_builtup_area' in key and key['size_builtup_area'] > 0:
                    builtup = key['size_builtup_area']/1.2
                    key['size_carpet_area'] = builtup

                if 'flat_count' in key and key['flat_count'] > 0:
                    totalFlats = totalFlats+key['flat_count']

            if flag:
                avgRentpsf = num/den
                society.average_rent = avgRentpsf
                society.flat_type_count = request.data['flat_type_count']
                society.save()

            if request.data['flat_type_count'] != len(request.data['flat_details']):
                return Response({'message':'No of Flats entered does not match flat type count'},status=400)
            if totalFlats > 0 and society.flat_count != totalFlats:
                return Response({'message':'No of Flats entered does not match total flat count of society'},status=400)


        for key in request.data['flat_details']:
            if 'id' in key:
                item = FlatType.objects.get(pk=key['id'])
                serializer = FlatTypeSerializer(item, data=key)
            else:
                serializer = FlatTypeSerializer(data=key)
            if serializer.is_valid():
                serializer.save(society=society)
            else:
                return Response(serializer.errors, status=400)

        return Response(status=201)

    def delete(self, request, id, format=None):
        try:
            invid = request.query_params.get('flatid', None)

            society = SupplierTypeSociety.objects.get(pk=id)

            flat = FlatType.objects.filter(pk =invid)
            flat.delete()
            return Response(status=204)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        except FlatType.DoesNotExist:
            return Response(status=404)


class SaveSummaryData(APIView):
    """
    Saves inventory summary data from csv sheet.

    """

    def get(self, request):
        """
        returns success or failure depending on weather the data was successfully saved or not.
        the csv file should be named 'inventory_summary.csv and should be parallel to manage.py file

        """

        with transaction.atomic():

            source_file = open(BASE_DIR + '/inventory_summary.csv', 'rb')
            error_file = open(BASE_DIR + '/inventory_summary_errors.csv', 'w')

            try:
                reader = csv.reader(source_file)
                failure_count = 0  # to report failure rows
                total_count = sum(1 for row in reader) - 1
                source_file.seek(0)

                sess = requests.Session()

                for num, row in enumerate(reader):
                    data = {}
                    if num == 0:
                        continue
                    else:
                        for index, key in enumerate(keys):
                            if row[index] == '':
                                data[key] = None
                            elif row[index].lower() == decision["YES"]:
                                data[key] = True
                            elif row[index].lower() == decision["NO"]:
                                data[key] = False
                            else:
                                data[key] = row[index]

                        response = ui_utils.get_supplier_id(request, data)
                        # this method of handing error code will  change in future
                        if response.status_code == status.HTTP_200_OK:
                            data['supplier_id'] = response.data['supplier_id']
                            url = BASE_URL + 'v0/ui/society/' + data['supplier_id'] + '/inventory_summary/'  # verify
                            r = sess.post(url, data=data, timeout=5)

                            if r.status_code != status.HTTP_200_OK:
                                error_file.write(
                                    "POST API failed for entry of row index {0} and error is {1} \n ------------\n".format(num,
                                                                                                                  r.text))
                                failure_count += 1
                                continue
                        else:
                            error_file.write("Error in making supplier id {0} for row number {1} \n".format(response.data['error'], num))
                            failure_count += 1
                            continue

            except Exception as e:
                return Response(data=str(e.message), status=status.HTTP_400_BAD_REQUEST)
            finally:
                source_file.close()
                error_file.close()

        return Response(data="Information:  out of {0} rows, {1} successfully saved and {2} failed ".format(total_count,
                                                                                                       total_count - failure_count,
                                                                                                       failure_count),
                        status=status.HTTP_200_OK)


class InventorySummaryAPIView(APIView):
    """
    This api provides summary of all the inventories associated with a supplier
    supplierTypeCode -- supplier type code RS, CP etc

    """

    def get(self, request, id):
        try:
            supplier_type_code = request.query_params.get('supplierTypeCode', None)
            data = request.data.copy()
            data['supplier_type_code'] = supplier_type_code
            inventory_object = InventorySummary.objects.get_inventory_object(data, id)
            if not inventory_object:
                return Response(data={'Inventory object does not exist for this supplier id {0}'.format(id)},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(model_to_dict(inventory_object), status=status.HTTP_200_OK)
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
        try:

            response = ui_utils.get_supplier_inventory(request.data.copy(), id)

            if not response.data['status']:
                return response
            data = response.data['data']['request_data']
            supplier_object = response.data['data']['supplier_object']
            inventory_object = response.data['data']['inventory_object']
            #supplier_type_code = request.data['supplier_type_code']
            supplier_type_code = 'CP'

            # society = SupplierTypeSociety.objects.get(pk=id)
            # item = InventorySummary.objects.get(supplier=society)
            tower_response = ui_utils.get_tower_count(supplier_object, supplier_type_code)
            if not tower_response.data['data']:
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
                                ui_utils.save_flyer_locations(0, request.data.get('flier_frequency'), supplier_object, supplier_type_code)
                            else:
                                ui_utils.save_flyer_locations(inventory_object.flier_frequency,
                                                              request.data.get('flier_frequency'), supplier_object, supplier_type_code)
                        serializer = InventorySummarySerializer(inventory_object, data=data)
                else:
                    if flag1 and request.data.get('flier_frequency'):
                        ui_utils.save_flyer_locations(0, request.data['flier_frequency'], supplier_object, supplier_type_code)
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
                                ui_utils.save_stall_locations(0, request.data.get('total_stall_count'), supplier_object, supplier_type_code)
                            else:
                                ui_utils.save_stall_locations(inventory_object.total_stall_count,
                                                              request.data.get('total_stall_count'), supplier_object, supplier_type_code)
                    serializer = InventorySummarySerializer(inventory_object, data=data)

                else:
                    if flag and request.data.get('total_stall_count'):
                        ui_utils.save_stall_locations(0, request.data.get('total_stall_count'), supplier_object, supplier_type_code)
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
                    posPrice = request.data.get('poster_price_week_nb')
                    if request.data.get('poster_allowed_nb'):
                        if request.data.get('nb_A3_allowed'):
                            price = PriceMappingDefault.objects.get_price_mapping_object(
                                ui_utils.make_dict_manager(adinventory_dict['poster_a3'],
                                                           duration_type_dict['campaign_weekly']), id, supplier_type_code)
                            ui_utils.save_price_data(price, posPrice, price.business_price)

                            price = PriceMappingDefault.objects.get_price_mapping_object(
                                ui_utils.make_dict_manager(adinventory_dict['poster_a3'],
                                                           duration_type_dict['unit_weekly']), id, supplier_type_code)
                            ui_utils.save_price_data(price, posPrice / towercount, price.business_price)

                        if request.data.get('nb_A4_allowed'):
                            price = PriceMappingDefault.objects.get_price_mapping_object(
                                ui_utils.make_dict_manager(adinventory_dict['poster_a3'],
                                                           duration_type_dict['campaign_weekly']), id, supplier_type_code)
                            ui_utils.save_price_data(price, posPrice, price.business_price)


                            price = PriceMappingDefault.objects.get_price_mapping_object(
                                ui_utils.make_dict_manager(adinventory_dict['poster_a4'],
                                                           duration_type_dict['unit_weekly']), id, supplier_type_code)

                            ui_utils.save_price_data(price, posPrice / towercount, price.business_price)

                if request.data.get('poster_price_week_lift'):
                    posPrice = request.data.get('poster_price_week_lift')
                    if request.data.get('poster_allowed_lift'):
                        price = PriceMappingDefault.objects.get_price_mapping_object(
                            ui_utils.make_dict_manager(adinventory_dict['poster_lift_a3'],
                                                       duration_type_dict['campaign_weekly']), id, supplier_type_code)
                        ui_utils.save_price_data(price, posPrice, price.business_price)

                        price = PriceMappingDefault.objects.get_price_mapping_object(
                            ui_utils.make_dict_manager(adinventory_dict['poster_lift_a3'],
                                                       duration_type_dict['unit_weekly']), id, supplier_type_code)

                        ui_utils.save_price_data(price, posPrice / towercount, price.business_price)

                        price = PriceMappingDefault.objects.get_price_mapping_object(
                            ui_utils.make_dict_manager(adinventory_dict['poster_lift_a4'],
                                                       duration_type_dict['campaign_weekly']), id, supplier_type_code)

                        ui_utils.save_price_data(price, posPrice, price.business_price)

                        price = PriceMappingDefault.objects.get_price_mapping_object(
                            ui_utils.make_dict_manager(adinventory_dict['poster_lift_a4'],
                                                       duration_type_dict['unit_weekly']), id, supplier_type_code)

                        ui_utils.save_price_data(price, posPrice / towercount, price.business_price)

                if request.data.get('standee_price_week'):
                    stanPrice = request.data.get('standee_price_week')
                    if request.data.get('standee_allowed'):
                        if request.data.get('standee_small'):
                            price = PriceMappingDefault.objects.get_price_mapping_object(
                                ui_utils.make_dict_manager(adinventory_dict['standee_small'],
                                                           duration_type_dict['campaign_weekly']), id, supplier_type_code)

                            ui_utils.save_price_data(price, stanPrice, price.business_price)

                            price = PriceMappingDefault.objects.get_price_mapping_object(
                                ui_utils.make_dict_manager(adinventory_dict['standee_small'],
                                                           duration_type_dict['unit_weekly']), id, supplier_type_code)

                            ui_utils.save_price_data(price, stanPrice / towercount, price.business_price)

                        if request.data.get('standee_medium'):
                            price = PriceMappingDefault.objects.get_price_mapping_object(
                                ui_utils.make_dict_manager(adinventory_dict['standee_medium'],
                                                           duration_type_dict['campaign_weekly']), id, supplier_type_code)

                            ui_utils.save_price_data(price, stanPrice, price.business_price)

                            price = PriceMappingDefault.objects.get_price_mapping_object(
                                ui_utils.make_dict_manager(adinventory_dict['standee_medium'],
                                                           duration_type_dict['unit_weekly']), id, supplier_type_code)

                            ui_utils.save_price_data(price, stanPrice / towercount, price.business_price)

                if request.data.get('stall_allowed'):
                    if request.data.get('stall_small'):
                        if request.data.get('stall_price_day_small'):
                            stallPrice = request.data.get('stall_price_day_small')

                            price = PriceMappingDefault.objects.get_price_mapping_object(
                                ui_utils.make_dict_manager(adinventory_dict['stall_small'],
                                                           duration_type_dict['unit_daily']), id, supplier_type_code)

                            ui_utils.save_price_data(price, stallPrice, price.business_price)

                            price = PriceMappingDefault.objects.get_price_mapping_object(
                                ui_utils.make_dict_manager(adinventory_dict['stall_canopy'],
                                                           duration_type_dict['unit_daily']), id, supplier_type_code)

                            ui_utils.save_price_data(price, stallPrice, price.business_price)

                    if request.data.get('stall_large'):
                        if request.data.get('stall_price_day_large'):
                            stallPrice = request.data.get('stall_price_day_large')

                            price = PriceMappingDefault.objects.get_price_mapping_object(
                                ui_utils.make_dict_manager(adinventory_dict['stall_large'],
                                                           duration_type_dict['unit_daily']), id, supplier_type_code)

                            ui_utils.save_price_data(price, stallPrice, price.business_price)

                if request.data.get('car_display_allowed'):
                    if request.data.get('cd_standard'):
                        if request.data.get('cd_price_day_standard'):
                            cdPrice = request.data['cd_price_day_standard']

                            price = PriceMappingDefault.objects.get_price_mapping_object(
                                ui_utils.make_dict_manager(adinventory_dict['car_display_standard'],
                                                           duration_type_dict['unit_daily']), id, supplier_type_code)

                            ui_utils.save_price_data(price, cdPrice, price.business_price)

                    if request.data.get('cd_premium'):
                        if request.data.get('cd_price_day_premium'):
                            cdPrice = request.data.get('cd_price_day_premium')

                            price = PriceMappingDefault.objects.get_price_mapping_object(
                                ui_utils.make_dict_manager(adinventory_dict['car_display_premium'],
                                                           duration_type_dict['unit_daily']), id, supplier_type_code)

                            ui_utils.save_price_data(price, cdPrice, price.business_price)

                if request.data.get('flier_price_day'):
                    flierPrice = request.data.get('flier_price_day')
                    if request.data.get('mailbox_allowed'):
                        price = PriceMappingDefault.objects.get_price_mapping_object(
                            ui_utils.make_dict_manager(adinventory_dict['flier_mailbox'],
                                                       duration_type_dict['unit_daily']), id, supplier_type_code)

                        ui_utils.save_price_data(price, flierPrice, price.business_price)

                    if request.data.get('d2d_allowed'):
                        price = PriceMappingDefault.objects.get_price_mapping_object(
                            ui_utils.make_dict_manager(adinventory_dict['flier_door_to_door'],
                                                       duration_type_dict['unit_daily']), id, supplier_type_code)

                        ui_utils.save_price_data(price, flierPrice, price.business_price)

                    if request.data.get('flier_lobby_allowed'):
                        try:
                            price = PriceMappingDefault.objects.get_price_mapping_object(
                                ui_utils.make_dict_manager(adinventory_dict['flier_lobby'],
                                                           duration_type_dict['unit_daily']), id, supplier_type_code)

                            ui_utils.save_price_data(price, flierPrice, price.business_price)

                        except KeyError as e:
                            pass

                serializer = InventorySummarySerializer(inventory_object, data=data)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(data={"status": False, "error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)


class BasicPricingAPIView(APIView):

            
    def get(self, request, id, format=None):
        response = {}
        try:
            # basic_prices = PriceMappingDefault.objects.select_related().filter(supplier__supplier_id=id)

            basic_prices_select = PriceMappingDefault.objects.select_related('supplier','adinventory_type','duration_type').filter(supplier_id=id)
            basic_prices = PriceMappingDefault.objects.filter(supplier_id=id).values()
            
            for basic_item, basic_select_item in zip(basic_prices, basic_prices_select):
                basic_item['supplier'] = basic_select_item.__dict__['_supplier_cache'].__dict__
                basic_item['supplier'].pop("_state",None)
                basic_item['adinventory_type'] = basic_select_item.__dict__['_adinventory_type_cache'].__dict__
                basic_item['adinventory_type'].pop("_state",None)
                basic_item['duration_type'] =  basic_select_item.__dict__['_duration_type_cache'].__dict__
                basic_item['duration_type'].pop("_state",None)


            towercount = SupplierTypeSociety.objects.get(pk=id).tower_count

            response['tower_count'] = towercount

            response['prices'] = basic_prices
           
            return Response(response, status=200)

        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        except PriceMappingDefault.DoesNotExist:
            return Response(status=404)
       

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

        return Response(serializer.data, status=201)


class InventoryPricingAPIView(APIView):
    """
    Not used
    """
    def get(self, request, id, format=None):
        try:
            inv_prices = PriceMapping.objects.select_related().filter(supplier__supplier_id=id)
            #count = PriceMapping.objects.filter(supplier__supplier_id=id).count()
            #basic_prices = SupplierTypeSociety.objects.get(pk=id).default_prices.all()
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
            towers = SupplierTypeSociety.objects.get(pk=id).towers.all()
            serializer_tower = UITowerSerializer(towers, many=True)
            #inventory_summary = InventorySummary.objects.get(supplier_id=id)

            inventory_summary = InventorySummary.objects.get_inventory_object(request.data.copy(), id)
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

        society=SupplierTypeSociety.objects.get(pk=id)

        # checking of notice board in tower == inventory summary nb_count
        total_nb_count = 0

        total_lift_count = 0
        total_standee_count = 0
        for tower in request.data['TowerDetails']:
            total_nb_count += tower['notice_board_count_per_tower']
            total_lift_count += tower['lift_count']
            total_standee_count += tower['standee_count']

        try:

            inventory_obj = InventorySummary.objects.get_inventory_object(request.data.copy(), id)
            if not inventory_obj:
                return Response(data={"Inventory Summary object does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            #inventory_obj = InventorySummary.objects.get(supplier=society)
        except InventorySummary.DoesNotExist:
            return Response({'message' : 'Please fill Inventory Summary Tab','inventory':'true'},status=404)

        if total_nb_count !=0 and total_nb_count != inventory_nb_count:

            return Response({'message' : 'Total Notice Board Count should equal to Notice Board Count in Inventory Summary Tab'}, status=404)
        if total_lift_count !=0 and total_lift_count != inventory_obj.lift_count:
            return Response({'message' : 'Total Lift Count should equal to Lift Count in Inventory Summary Tab'}, status=404)
        if total_standee_count !=0 and total_standee_count != inventory_obj.total_standee_count:
            return Response({'message' : 'Total Standee Count should equal to Standee Count in Inventory Summary Tab'}, status=404)


        # checking ends here

        for key in request.data['TowerDetails']:
            if 'tower_id' in key:

                try:
                    item = SocietyTower.objects.get(pk=key['tower_id'])
                    tower_dict = {
                        'tower_tag' : key['tower_tag'],
                        'tower_name' : key['tower_name'],
                        'tower_id' :  key['tower_id'],
                        'lift_count' : item.lift_count,
                        'nb_count' : item.notice_board_count_per_tower,
                        'standee_count' : item.standee_count,
                    }

                except SocietyTower.DoesNotExist:
                    return Response({'status': False, 'error': 'Society tower does not exist'}, status=400)

                serializer = SocietyTowerSerializer(item, data=key)
                if serializer.is_valid():
                    serializer.save(supplier=society)

                else:
                    return Response(serializer.errors, status=400)

                if tower_dict['lift_count'] < key['lift_count']:
                    self.save_lift_locations(tower_dict['lift_count'], key['lift_count'], tower_dict, society)
                if tower_dict['nb_count'] < key['notice_board_count_per_tower']:
                    self.save_nb_locations(tower_dict['nb_count'], key['notice_board_count_per_tower'], tower_dict, society)
                if tower_dict['standee_count'] < key['standee_count']:
                    self.save_standee_locations(tower_dict['standee_count'], key['standee_count'], tower_dict, society)

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
                        flat_serializer=SocietyFlatSerializer(flat_item,data=flat)
                        flatLen = len(key['flat_type_details'])
                        flat = key['flat_type_count']
                        if flat!=flatLen:
                            return Response({'message':'No of flat details entered does not match flat type count'},status=400)

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

            towerId =  request.query_params.get('towId', None)
            item = SocietyTower.objects.get(pk=towerId)
            item.delete()

            return Response(status=204)
        except SocietyTower.DoesNotExist:
            return Response(status=404)


    def save_lift_locations(self, c1, c2, tower, society):
        i = c1 + 1
        tow_name = tower['tower_name']
        while i <= c2:
            lift_tag = tower['tower_tag'] + "00L" + str(i)
            adId = society.supplier_id + lift_tag + "PO01"
            lift = LiftDetails(adinventory_id=adId, lift_tag=lift_tag, tower_id=int(tower['tower_id']))
            lift_inv = PosterInventory(adinventory_id=adId, poster_location=lift_tag, tower_name=tow_name, supplier=society)
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

    def save_standee_locations(self, c1, c2, tower, society):
        i = c1 + 1
        while i <= c2:
            sd_tag = society.supplier_id + tower['tower_tag'] + "0000SD" + str(i).zfill(2)
            sd = StandeeInventory(adinventory_id=sd_tag, tower_id=int(tower['tower_id']))
            sd.save()
            i += 1



class PosterAPIView(APIView):
    def get(self, request, id, format=None):
        lifts = []
        notice_boards = []
        disable = {}
        try:
            towers = SupplierTypeSociety.objects.get(pk=id).towers.all()
            society = SupplierTypeSociety.objects.get(pk=id)
            posters = PosterInventory.objects.filter(supplier=society)

            item = InventorySummary.objects.get_inventory_object(request.data.copy(), id)
            if not item:
                return Response(data={"Inventory Summary object does not exist"}, status=status.HTTP_400_BAD_REQUEST)


            #item = InventorySummary.objects.get(supplier=society)

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
            result = {"lift_details_available": lifts_available, "lift_details": serializer.data, "nb_a4_available":nb_available, "disable_nb": item.poster_allowed_nb, "disable_lift": item.poster_allowed_lift}
            serializer = NoticeBoardDetailsSerializer(notice_boards, many = True)
            result['nb_details'] = serializer.data
            serializer = PosterInventorySerializer(posters, many = True)
            result['poster_details'] = serializer.data

            return Response(result, status=200)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)

    def post(self, request, id, format=None):
            society=SupplierTypeSociety.objects.get(pk=id)
            if request.data['nb_a4_available']:
                 for notice_board in request.data['nb_details']:
                     data = request.data['nb_common_details']
                     data.update(notice_board)
                     if 'id' in notice_board:
                         notice_item = NoticeBoardDetails.objects.get(pk=notice_board['id'])
                         posCount =  notice_board['total_poster_per_notice_board']
                         if posCount != None:
                             self.adId_nb(posCount, notice_board, society)

                         notice_serializer = NoticeBoardDetailsSerializer(notice_item, data=data)
                     else:
                         notice_serializer = NoticeBoardDetailsSerializer(data=data)
                         #populate location and ad inventory table
                     '''for i in range(notice_board['total_poster_per_notice_board']):
                        ad_inv = AdInventoryLocationMapping(adinventory_id = notice_tag+'PO'+str(i), adinventory_name = 'POSTER', location = nb_location)
                        ad_inv.save("Poster", society)'''
                     if notice_serializer.is_valid():
                         notice_serializer.save()
                     else:
                         #transaction.rollback()
                         return Response(notice_serializer.errors, status=400)

            if request.data['lift_details_available']:
                 for lift in request.data['lift_details']:
                     if 'id' in lift:
                         lift_item = LiftDetails.objects.get(pk=lift['id'])
                         lift_serializer = LiftDetailsSerializer(lift_item,data=lift)
                         #if lift!=liftLen:
                          #   return Response({'message':'No of lift details entered does not match lift count'},status=400)
                     else:
                         lift_serializer = LiftDetailsSerializer(data=lift)
                         #populate location and ad inventory table
                     if lift_serializer.is_valid():
                         lift_serializer.save()
                     else:
                         return Response(lift_serializer.errors, status=400)
            return Response(status=200)


    def adId_nb(self, count, nb, society):
       nb_tag = nb['notice_board_tag']
       nb_tower = nb['tower_name']
       pos = int(count) + 1
       for i in range(1, pos):
           nb_id = society.supplier_id + nb_tag + "PO" + str(i).zfill(2)
           nb = PosterInventory(adinventory_id=nb_id, poster_location=nb_tag, tower_name=nb_tower, supplier=society)
           nb.save()

    def delete(self, request, id, format=None):
        try:
            invId = request.query_params.get('invId', None)
            invType = request.query_params.get('type', None)
            society = SupplierTypeSociety.objects.get(pk=id)

            if invType=='lift':
                item = LiftDetails.objects.get(pk=invId)
                tag = item.lift_tag
                posters = PosterInventory.objects.filter(supplier=society, poster_location=tag)
                posters.delete()
                item.delete()
            if invType=='notice':
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
            society = SupplierTypeSociety.objects.get(pk=id)
            flyers = FlyerInventory.objects.filter(supplier=id)
            response['flat_count'] = society.flat_count

            serializer = FlyerInventorySerializer(flyers, many=True)
            response['flyers_data'] = serializer.data
            towers = SupplierTypeSociety.objects.get(pk=id).towers.all().values()

            item = InventorySummary.objects.get_inventory_object(request.data.copy(), id)
            if not item:
                return Response(data={"Inventory Summary object does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            
            #item = InventorySummary.objects.get(supplier=society)

            #mail_boxes = SupplierTypeSociety.objects.get(pk=id).mail_boxes.all().values()
            
            
            response['flyer_available'] = society.flier_allowed
            #fliers.extend(towers)
            #fliers.extend(mail_boxes)
            #serializer = MailboxInfoSerializer(mail_boxes, many=True)
            #mail_box_available = get_availability(serializer.data)
            #mail_box_available = item.mailbox_allowed
            #response['mail_box_available'] = item.mailbox_allowed
            #response['mail_box_details'] = fliers
            #response['tower_data'] = towers

            


            #door_to_doors = SupplierTypeSociety.objects.get(pk=id).door_to_doors.all()
            #serializer = DoorToDoorInfoSerializer(door_to_doors, many=True)
            #door_to_door_allowed = get_availability(serializer.data)
            #response['d2d_available'] = item.d2d_allowed
            #response['door_to_door_details'] = serializer.data

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
            #mail = request.data['flyers_data']
            #society.tower_id = mail['tower_id']
            #if request.data['mail_box_available']:
                #response = post_data(MailboxInfo, MailboxInfoSerializer, request.data['mail_box_details'], society)
                #response = post_data(MailboxInfo, MailboxInfoSerializer, request.data['tower_data'], society)
                #print request.data['tower_data']
                #if response == False:
              #      return Response(status=400)

            #if request.data['door_to_door_allowed']:
                #response = post_data(DoorToDoorInfo, DoorToDoorInfoSerializer, request.data['door_to_door_details'], society)
                #if response == False:
                 #   return Response(status=400)

            #return Response(status=201)
            for flyer in request.data['flyers_data']:
                    #print request.data['tower_data']
                if 'id' in flyer:
                        
                    flyer_item = FlyerInventory.objects.get(pk=flyer['id'])
                    flyer_serializer = FlyerInventorySerializer(flyer_item,data=flyer)

                else:
                    flyer_serializer = FlyerInventorySerializer(data=flier)

                if flyer_serializer.is_valid():
                    flyer_serializer.save()
                else:
                    return Response(flyer_serializer.errors, status=400)

            return Response(status=200)

    def delete(self, request, id, format=None):
        try:
            #invId = request.query_params.get('invId', None)
            adinventory_id = request.query_params.get('adinventory_id', None)
            #invType = request.query_params.get('type', None)
            #adinventory_type = request.query_params.get('type', None)
            society = SupplierTypeSociety.objects.get(pk=id)

            flyer = FlyerInventory.objects.filter(supplier=society, pk =adinventory_id)
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


        towers = SupplierTypeSociety.objects.get(pk=id).towers.all()
        society = SupplierTypeSociety.objects.get(pk=id)

        item = InventorySummary.objects.get_inventory_object(request.data.copy(), id)
        if not item:
            return Response(data={"Inventory Summary object does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        #item = InventorySummary.objects.get(supplier=society)

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
                standee_serializer = StandeeInventorySerializer(standee_item,data=standee)

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

        society = SupplierTypeSociety.objects.get(pk=id)
        stalls = StallInventory.objects.filter(supplier=id)

        #item = InventorySummary.objects.get(supplier=society)

        item = InventorySummary.objects.get_inventory_object(request.data.copy(), id)
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
        society.electricity_available =  True if stall['electricity_available'] == 'Yes' else False
        if society.electricity_available:

           society.daily_electricity_charges = stall['electricity_charges_daily']


        society.save()

        for stall in request.data['stall_details']:
            if 'id' in stall:
                stall_item = StallInventory.objects.get(pk=stall['id'])
                stall_serializer = StallInventorySerializer(stall_item,data=stall)

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
                event_details_available=True
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
        ##print request.data
        society=SupplierTypeSociety.objects.get(pk=id)
        '''if request.data['event_details_available']:
            if request.data['events_count_per_year'] != len(request.data['event_details']):
                return Response({'message':'No of Events entered does not match event count'},status=400)
        '''
        for key in request.data['event_details']:
            if 'event_id' in key:
                item = Events.objects.get(pk=key['event_id'])
                serializer = EventsSerializer(item, data=key)
            else:
                serializer = EventsSerializer(data=key)
            if serializer.is_valid():
                serializer.save(supplier=society)
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
            response = post_data(CommunityHallInfo, CommunityHallInfoSerializer, request.data['community_hall_details'], society)
            if response == False:
                return Response(status=400)

        if request.data['swimming_pool_available']:
            response = post_data(SwimmingPoolInfo, SwimmingPoolInfoSerializer, request.data['swimming_pool_details'], society)
            if response == False:
                return Response(status=400)


        if request.data['street_furniture_available']:
            response = post_data(StreetFurniture, StreetFurnitureSerializer, request.data['street_furniture_details'], society)
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
            response.append({"location_id":society.supplier_id, "name":society.society_name, "location_type":"Society"})
            towers = SupplierTypeSociety.objects.get(pk=id).towers.all()
            for key in towers:
                response.append({"location_id":key.tower_id, "name":key.tower_name, "location_type":"tower"})
                nb = key.notice_boards.all()
                for item in nb:
                    response.append({"location_id":item.id, "name":key.tower_name + item.notice_board_tag, "location_type":"NoticeBoard"})
                nb = key.lifts.all()
                for item in nb:
                    response.append({"location_id":item.id, "name":key.tower_name + item.lift_tag, "location_type":"Lift"})

            return Response(response, status=200)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        except SocietyTower.DoesNotExist:
            return Response(status=404)

        return Response({"response":response}, status=201)


class ImageMappingAPIView(APIView):
    def get(self, request, id, format=None):
        try:
            images = SupplierTypeSociety.objects.get(pk=id).images.all()
            serializer = ImageMappingSerializer(images, many=True)

            return Response(serializer.data, status=200)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        except ImageMapping.DoesNotExist:
            return Response(status=404)

    def post(self, request, id, format=None):
        #print request.data
        society=SupplierTypeSociety.objects.get(pk=id)
        for key in request.data['image_details']:
            if 'id' in key:
                item = ImageMapping.objects.get(pk=key['id'])
                serializer = ImageMappingSerializer(item, data=key)
            else:
                serializer = ImageMappingSerializer(data=key)

            if serializer.is_valid():
                serializer.save(supplier=society)
            else:
                return Response(serializer.errors, status=400)

        return Response(serializer.data, status=201)



def generate_location_tag(initial_tag, type, index):
    return ''.join((initial_tag.upper() , type.upper()[:3], str(index)))



def post_data(model, model_serializer, inventory_data, foreign_value=None):
    for key in inventory_data:
        if 'id' in key:
            item = model.objects.get(pk=key['id'])
            serializer = model_serializer(item,data=key)
        else:
            serializer = model_serializer(data=key)
        if serializer.is_valid():
            serializer.save(supplier=foreign_value)
        else:
            #print serializer.errors
            return False
    return True



def get_availability(data):
     if len(data) > 0:
        return True
     else:
         return False

# This API is for saving basic tab details of corporate space. Divided into four parts mentioned in the comments.

class saveBasicCorporateDetailsAPIView(APIView):

    def post(self, request,id,format=None):
        try:

            companies = []
            error = {}

            #Round 1 Saving basic data
            if 'supplier_id' in request.data:
                corporate = SupplierTypeCorporate.objects.filter(pk=request.data['supplier_id']).first()
                if corporate:
                    corporate_serializer = SupplierTypeCorporateSerializer(corporate,data=request.data)
                else:
                    corporate_serializer = SupplierTypeCorporateSerializer(data=request.data)
                if corporate_serializer.is_valid():
                    corporate_serializer.save()
                else:
                    error['message'] ='Invalid Corporate Info data'
                    error = json.dumps(error)
                    return Response(corporate_serializer.errors, status=406)
            else:
                return Response({"status": False, "error": "No supplier id in request.data"}, status=status.HTTP_400_BAD_REQUEST)

            # Round 2 Saving List of companies


            corporate_id = request.data['supplier_id']

            companies_name = request.data['list1']
            company_ids = list(CorporateParkCompanyList.objects.filter(supplier_id=corporate_id).values_list('id',flat=True))

            for company_name in companies_name:
                if 'id' in company_name:
                    company = CorporateParkCompanyList.objects.get(id=id)
                    company.name = company_name
                    company_ids.remove(company.id)
                    companies.append(company)
                else:
                    company = CorporateParkCompanyList(supplier_id_id=corporate_id,name=company_name)
                    companies.append(company)

            CorporateParkCompanyList.objects.bulk_create(companies)
            CorporateParkCompanyList.objects.filter(id__in=company_ids).delete()


            # Round 3 - Saving contacts

            try:
                instance = SupplierTypeCorporate.objects.get(supplier_id=id)
            except SupplierTypeCorporate.DoesNotExist:
                return Response({'message': 'This corporate park does not exist'}, status=406)

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
            if request.data['building_count'] > buildingcount:
                diff_count = request.data['building_count'] - buildingcount
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
            data1 = SupplierTypeCorporate.objects.get(supplier_id=id)
            serializer = SupplierTypeCorporateSerializer(data1)
            data2 = CorporateParkCompanyList.objects.filter(supplier_id=id)
            serializer1 = CorporateParkCompanyListSerializer(data2, many=True)
            data3 = ContactDetailsGeneric.objects.filter(object_id=id)
            serializer2 = ContactDetailsGenericSerializer(data3, many=True)
            result = {'basicData' : serializer.data , 'companyList' : serializer1.data , 'contactData' : serializer2.data}
            return Response(result)
        except SupplierTypeCorporate.DoesNotExist:
            return Response(status=404)
        except SupplierTypeCorporate.MultipleObjectsReturned:
            return Response(status=406)


# class ContactDetailsGenericAPIView(APIView):

#     def post(self,request,id=None,format=None):
#         print "Hello  ", id
#         # instance = get_object_or_404(SupplierTypeCorporate, supplier_id=id)
#         try:
#             instance = SupplierTypeCorporate.objects.get(supplier_id=id)
#         except SupplierTypeCorporate.DoesNotExist:
#             print "id does not exist in database"
#             return Response({'message': 'This corporate park does not exist'}, status=406)

#         print "Hello123"
#         content_type = ContentType.objects.get_for_model(SupplierTypeCorporate)
#         print request.data
#         request.data['contact']['object_id'] = instance.supplier_id
#         serializer = ContactDetailsGenericSerializer(data=request.data['contact'])
#         if serializer.is_valid():
#             print serializer.validated_data
#             serializer.save(content_type=content_type)
#             print "serializer saved"
#             return Response(serializer.data, status=200)
#         return Response(serializers.errors, status=400)


# This API is for saving the buildings and wings details of a corporate space
class SaveBuildingDetailsAPIView(APIView):

    def get(self,request,id, format=None):
        try:
            corporate = SupplierTypeCorporate.objects.get(supplier_id=id)
        except SupplierTypeCorporate.DoesNotExist:
            return Response({'message': 'Invalid Corporate ID'}, status=406)

        buildings = corporate.get_buildings()
        building_serializer = CorporateBuildingGetSerializer(buildings, many=True)
        return Response(building_serializer.data, status = 200)

    def post(self,request,id,format=None):

        try:
            corporate_object = SupplierTypeCorporate.objects.get(supplier_id=id)
        except SupplierTypeCorporate.DoesNotExist:
            return Response({'message': 'Invalid Corporate ID'}, status=404)

        try:

            building_count = len(request.data)
            if corporate_object.building_count != building_count:
                corporate_object.building_count = building_count
                corporate_object.save()

            buildings_ids = set(CorporateBuilding.objects.filter(corporatepark_id=corporate_object).values_list('id',flat=True))
            wing_ids_superset = set()

            #Logic for delete - Put all currently present fields in the database into a list.
            #Check the received data from front-end, if ID of any field matches with any in the list, remove that field from list.
            #In the end, delete all the fields left in the list.

            for building in request.data:
                if 'id' in building:
                    basic_data_instance = CorporateBuilding.objects.get(id=building['id'])
                    buildings_ids.remove(building['id'])
                    building_serializer = CorporateBuildingSerializer(basic_data_instance,data=building)
                else :
                    building_serializer = CorporateBuildingSerializer(data=building)

                if building_serializer.is_valid():
                    building_object = building_serializer.save()
                else:
                    return Response(status=406)

                wings_ids = set(CorporateBuildingWing.objects.filter(building_id=building_object).values_list('id',flat=True))

                for wing in building['wingInfo']:

                    if 'id' in wing:
                        wing_object = CorporateBuildingWing.objects.get(id=wing['id'])
                        wings_ids.remove(wing_object.id)
                        wing_serializer = CorporateBuildingWingSerializer(wing_object,data=wing)
                    else:
                        wing_serializer = CorporateBuildingWingSerializer(data=wing)

                    if wing_serializer.is_valid():
                        wing_serializer.save(building_id=building_object)
                    else:
                        return Response({'message' : 'Invalid Wing Data' , \
                                'errors' : wing_serializer.errors}, status=406)

                if wings_ids :
                    wing_ids_superset = wing_ids_superset.union(wings_ids)

            if wing_ids_superset:
                CorporateBuildingWing.objects.filter(id__in=wing_ids_superset).delete()
            if buildings_ids:
                CorporateBuilding.objects.filter(id__in=buildings_ids).delete()

        except KeyError as e:
            return Response({"status": False, "error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            return Response({"status": False, "error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": False, "error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": True, "data": ""}, status=status.HTTP_200_OK)


# This API is for fetching the companies and buildings of a specific corporate space.
class CompanyDetailsAPIView(APIView):
    def get(self, request, id, format=True):
        company = SupplierTypeCorporate.objects.get(supplier_id=id)
        company_list = CorporateParkCompanyList.objects.filter(supplier_id_id=company)
        serializer = CorporateParkCompanyListSerializer(company_list,many=True)
        building = SupplierTypeCorporate.objects.get(supplier_id=id)
        building_list = CorporateBuilding.objects.filter(corporatepark_id_id=building)
        serializer1 = CorporateBuildingGetSerializer(building_list,many=True)
        response_dict = {'companies' : serializer.data , 'buildings' : serializer1.data}
        return Response(response_dict,status=200)


# This API is for saving details of all companies belonging to a specific corporate space.
class CorporateCompanyDetailsAPIView(APIView):
    def get(self, request, id=None, format=None):
        try:
            corporate = SupplierTypeCorporate.objects.get(supplier_id=id)
        except SupplierTypeCorporate.DoesNotExist:
            return Response({'message': 'No such Corporate'},status=406)

        companies = corporate.get_corporate_companies()
        companies_serializer = CorporateParkCompanySerializer(companies,many=True)

        return Response(companies_serializer.data, status=200)


    def post(self, request, id, format=True):
        try:
            corporate = SupplierTypeCorporate.objects.get(supplier_id=id)
        except SupplierTypeCorporate.DoesNotExist:
            return Response({'message' : "Corporate Doesn't Exist" }, status=404)


        company_detail_list = []
        floor_list = []
        company_detail_ids = set(CorporateCompanyDetails.objects.filter(company_id__supplier_id=corporate).values_list('id',flat=True))
        floor_superset = set()
        company_detail_set = set()
        flag = False
        
        for company in request.data:
            for company_detail in company['companyDetailList']:
                try:
                    if not company_detail['building_name']:
                        continue
                    company_detail_instance = CorporateCompanyDetails.objects.get(id=company_detail['id'])
                    company_detail['company_id'] = company['id']
                    company_detail_ids.remove(company_detail['id'])
                    company_detail_instance.__dict__.update(company_detail)
                    company_detail_instance.save()
                    flag = True
                except KeyError:
                    company_detail_instance = CorporateCompanyDetails(company_id_id=company['id'],building_name=company_detail['building_name'],wing_name=company_detail['wing_name'])
                    # company_detail_list.append(company_detail_instance)
                    # uncomment this line if error occurs
                    company_detail_instance.save()
                    flag = False
            
                if flag:
                    floor_ids = set(CompanyFloor.objects.filter(company_details_id_id=company_detail_instance.id).values_list('id',flat=True))
                    for floor in company_detail['listOfFloors']:
                        try:
                            floor_instance = CompanyFloor.objects.get(id=floor['id'])
                            floor_ids.remove(floor_instance.id)
                            if floor_instance.floor_number == floor['floor_number']:
                                continue
                            floor_instance.company_detail_id, floor_instance.floor_number = company_detail_instance, floor['floor_number']
                            
                            # floor_instance.__dict__.update(floor)
                            floor_instance.save()
                        except KeyError:
                            floor_list_instance = CompanyFloor(company_details_id=company_detail_instance,floor_number=floor['floor_number'])
                            floor_list.append(floor_list_instance)
                    floor_superset = floor_superset.union(floor_ids)


                else:
                    for floor in company_detail['listOfFloors']:
                        floor_list_instance = CompanyFloor(company_details_id=company_detail_instance,floor_number=floor['floor_number'])
                        floor_list.append(floor_list_instance)


        # floor_list = []
        #         for floor in company_detail['listOfFloors']:
        #             floor_list_instance = CompanyFloor(company_details_id=company_detail_instance,floor_number=floor)
        #             floor_list.append(floor_list_instance)
        #         CompanyFloor.objects.bulk_create(floor_list)

        # CorporateCompanyDetails.objects.bulk_create(company_detail_list)
        CompanyFloor.objects.filter(id__in=floor_superset).delete()
        CorporateCompanyDetails.objects.filter(id__in=company_detail_ids).delete()
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
            result = {'basicData' : serializer.data , 'contactData' : serializer1.data}
            return Response(result)
        except SupplierTypeSalon.DoesNotExist:
            return Response(status=404)
        except SupplierTypeSalon.MultipleObjectsReturned:
            return Response(status=406)


    def post(self, request,id,format=None):
        error = {}
        if 'supplier_id' in request.data:
            salon = SupplierTypeSalon.objects.filter(pk=request.data['supplier_id']).first()
            if salon:
                salon_serializer = SupplierTypeSalonSerializer(salon,data=request.data)
            else:
                salon_serializer = SupplierTypeSalonSerializer(data=request.data)
        if salon_serializer.is_valid():
            salon_serializer.save()
        else:
            error['message'] ='Invalid Salon Info data'
            error = json.dumps(error)
            return Response(response, status=406)


        # Now saving contacts
        try:
            instance = SupplierTypeSalon.objects.get(supplier_id=id)
        except SupplierTypeSalon.DoesNotExist:
            return Response({'message': 'This salon does not exist'}, status=406)

        content_type = ContentType.objects.get_for_model(SupplierTypeSalon)
        
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
            result = {'basicData' : serializer.data , 'contactData' : serializer1.data}
            return Response(result)
        except SupplierTypeGym.DoesNotExist:
            return Response(status=404)
        except SupplierTypeGym.MultipleObjectsReturned:
            return Response(status=406)


    def post(self, request,id,format=None):
        error = {}
        if 'supplier_id' in request.data:
            gym = SupplierTypeGym.objects.filter(pk=request.data['supplier_id']).first()
            if gym:
                gym_serializer = SupplierTypeGymSerializer(gym,data=request.data)
            else:
                gym_serializer = SupplierTypeGymSerializer(data=request.data)
        if gym_serializer.is_valid():
            gym_serializer.save()
        else:
            error['message'] ='Invalid Gym Info data'
            error = json.dumps(error)
            return Response(response, status=406)


        # Now saving contacts
        try:
            instance = SupplierTypeGym.objects.get(supplier_id=id)
        except SupplierTypeGym.DoesNotExist:
            return Response({'message': 'This gym does not exist'}, status=406)

        content_type = ContentType.objects.get_for_model(SupplierTypeGym)
        
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
        return Response(status=200)

        # End of contact Saving