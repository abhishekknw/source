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
from django.db.models import Q
from django.contrib.auth.models import User
import json
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.db import IntegrityError
from django.db import transaction
from itertools import izip

from v0.ui.serializers import SocietyListSerializer


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
            result = {'user':user_serializer.data, 'user_profile':serializer.data}
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


class generateSupplierIdAPIView(APIView):
    def post(self, request, format=None):
        # try:
            city = City.objects.get(pk=request.data['city_id'])
            area = CityArea.objects.get(pk=request.data['area_id'])
            sub_area = CitySubArea.objects.get(pk=request.data['subarea_id'])

            try:
                society = SupplierTypeSociety.objects.get(supplier_code=request.data['supplier_code'], society_locality=area.label)
                if society:
                    return Response(status=409)
            except SupplierTypeSociety.DoesNotExist:
                print "No such society"
            current_user = request.user
            supplier_id = city.city_code + area.area_code + sub_area.subarea_code + request.data['supplier_type'] + request.data['supplier_code']

            if request.data['supplier_type'] == 'RS':
                supplier = {'supplier_id':supplier_id,
                        'society_name':request.data['supplier_name'],
                        'society_city':city.city_name,
                        'society_subarea':sub_area.subarea_name,
                        'society_locality':area.label,
                        'society_state' : city.state_code.state_name,
                        'created_by': current_user.id
                        } 
                serializer = SupplierTypeSocietySerializer(data=supplier)
                if serializer.is_valid():
                    serializer.save()
                    #populate default pricing table
                    print "calling def"
                    set_default_pricing(serializer.data['supplier_id'])
                    return Response(serializer.data, status=200)
                else:
                    return Response(serializer.errors, status=400)

            #saving corporate in corporate model
            if request.data['supplier_type'] == 'CP':
                supplier1 = {'supplier_id': supplier_id,
                            'name':request.data['supplier_name'],
                            'city':city.city_name,
                            'locality':area.label,
                            'subarea':sub_area.subarea_name,
                            'state' : city.state_code.state_name
                            }
                serializer1 = SupplierTypeCorporateSerializer(data=supplier1) 
                if serializer1.is_valid():
                    print serializer1.validated_data
                    serializer1.save()
                    return Response(serializer1.data, status=200)
                else:
                    return Response(serializer1.errors, status=400) 

            #saving salon in salon model
            if request.data['supplier_type'] == 'SA':
                supplier1 = {'supplier_id': supplier_id,
                            'name':request.data['supplier_name'],
                            'city':city.city_name,
                            'locality':area.label,
                            'subarea':sub_area.subarea_name,
                            'state' : city.state_code.state_name
                            }
                serializer2 = SupplierTypeSalonSerializer(data=supplier1) 
                if serializer2.is_valid():
                    print serializer2.validated_data
                    serializer2.save()
                    return Response(serializer2.data, status=200)
                else:
                    return Response(serializer2.errors, status=400) 

            #saving gym in gym model
            if request.data['supplier_type'] == 'GY':
                supplier1 = {'supplier_id': supplier_id,
                            'name':request.data['supplier_name'],
                            'city':city.city_name,
                            'locality':area.label,
                            'subarea':sub_area.subarea_name,
                            'state' : city.state_code.state_name
                            }
                serializer3 = SupplierTypeGymSerializer(data=supplier1) 
                if serializer3.is_valid():
                    print serializer3.validated_data
                    serializer3.save()
                    return Response(serializer3.data, status=200)
                else:
                    return Response(serializer3.errors, status=400) 
        # except :
            # return Response(status=404)


class SocietyAPIView(APIView):
    # permission_classes = (permissions.IsAuthenticated, IsOwnerOrManager,)

    def get(self, request, id, format=None):
        try:
            response = {}
            item = SupplierTypeSociety.objects.get(pk=id)
            self.check_object_permissions(self.request, item)
            serializer = UISocietySerializer(item)
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


            return Response(serializer.data, status=200)
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
        #print request.data
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
        print request.data
        print "\n\n\n"

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




def set_default_pricing(society_id):
    print "inside def"
    society = SupplierTypeSociety.objects.get(pk=society_id)
    ad_types = AdInventoryType.objects.all()
    duration_types = DurationType.objects.all()
    price_mapping_list = []
    for type in ad_types:
        for duration in duration_types:
            if (type.adinventory_name=='POSTER'):
                if((duration.duration_name=='Unit Daily')):
                    pmdefault = PriceMappingDefault(supplier= society, adinventory_type=type, duration_type=duration, society_price=-1, business_price=-1)
                    price_mapping_list.append(pmdefault)
                if((duration.duration_name=='Campaign Weekly')|(duration.duration_name=='Campaign Monthly')|(duration.duration_name=='Unit Monthly')|(duration.duration_name=='Unit Weekly')):
                    pmdefault = PriceMappingDefault(supplier= society, adinventory_type=type, duration_type=duration, society_price=0, business_price=0)
                    price_mapping_list.append(pmdefault)

            if (type.adinventory_name=='POSTER LIFT'):
                if((duration.duration_name=='Unit Daily')):
                    pmdefault = PriceMappingDefault(supplier= society, adinventory_type=type, duration_type=duration, society_price=-1, business_price=-1)
                    price_mapping_list.append(pmdefault)
                if((duration.duration_name=='Campaign Weekly')|(duration.duration_name=='Campaign Monthly')|(duration.duration_name=='Unit Monthly')|(duration.duration_name=='Unit Weekly')):
                    pmdefault = PriceMappingDefault(supplier= society, adinventory_type=type, duration_type=duration, society_price=0, business_price=0)
                    price_mapping_list.append(pmdefault)
           
            if (type.adinventory_name=='STANDEE'):
                if((duration.duration_name=='Campaign Monthly')|(duration.duration_name=='Campaign Weekly')|(duration.duration_name=='Unit Weekly')|(duration.duration_name=='Unit Monthly')):
                    if(type.adinventory_type=='Large'):
                        pmdefault = PriceMappingDefault(supplier= society, adinventory_type=type, duration_type=duration, society_price=-1, business_price=-1)
                        price_mapping_list.append(pmdefault)
                    else:
                        pmdefault = PriceMappingDefault(supplier= society, adinventory_type=type, duration_type=duration, society_price=0, business_price=0)
                        price_mapping_list.append(pmdefault)
            if (type.adinventory_name=='STALL'):
                if((duration.duration_name=='Unit Daily')|(duration.duration_name=='2 Days')):
                    if ((type.adinventory_type=='Canopy')|(type.adinventory_type=='Small')|(type.adinventory_type=='Large')):
                        pmdefault = PriceMappingDefault(supplier= society, adinventory_type=type, duration_type=duration, society_price=0, business_price=0)
                        price_mapping_list.append(pmdefault)
                    if(type.adinventory_type=='Customize'):
                        pmdefault = PriceMappingDefault(supplier= society, adinventory_type=type, duration_type=duration, society_price=-1, business_price=-1)
                        price_mapping_list.append(pmdefault)
            if (type.adinventory_name=='CAR DISPLAY'):
                if((duration.duration_name=='Unit Daily')|(duration.duration_name=='2 Days')):
                    if ((type.adinventory_type=='Standard')|(type.adinventory_type=='Premium')):
                        pmdefault = PriceMappingDefault(supplier= society, adinventory_type=type, duration_type=duration, society_price=0, business_price=0)
                        price_mapping_list.append(pmdefault)
            if ((type.adinventory_name=='FLIER')&(duration.duration_name=='Unit Daily')):
                if ((type.adinventory_type=='Door-to-Door')|(type.adinventory_type=='Mailbox')|(type.adinventory_type=='Lobby')):
                    pmdefault = PriceMappingDefault(supplier= society, adinventory_type=type, duration_type=duration, society_price=0, business_price=0)
                    price_mapping_list.append(pmdefault)

    PriceMappingDefault.objects.bulk_create(price_mapping_list)
    return Response(status=200)


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
                    print user.user_profile.all().first().is_city_manager
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
                    items = SupplierTypeCorporate.objects.filter(created_by=user.id)

            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(items, request)
            serializer = UICorporateSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except SupplierTypeCorporate.DoesNotExist:
            return Response(status=404)


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
        print request.data
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
                # print inventorytype

            flatquantity.sort()
            societytype.sort()
            if flatquantity == allflatquantity: # sorted comparison to avoid mismatch based on index
                flatquantity = []
            if  societytype == allsocietytype:   # same as above
                societytype = []                

            if subareas or areas or societytype or flatquantity or inventorytype:
                filter_present = True

            print "cityArea : ", cityArea
            print "citySubArea : ", citySubArea
            print "societytype : ", societytype
            print "flatquantity : ", flatquantity
            print "inventorytype : ", inventorytype
            print "filter present : ", filter_present

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
        print "Order received is ", order
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
            print society.flat_count


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
        #print request.data
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
            #else:
                #return Response(serializer.errors, status=400)

        return Response(status=201)

    def delete(self, request, id, format=None):
        try:
            invid = request.query_params.get('flatid', None)
            print invid
           
            society = SupplierTypeSociety.objects.get(pk=id)

            flat = FlatType.objects.filter(pk =invid)
            print "in flat delete"
            flat.delete()
            return Response(status=204)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        except FlatType.DoesNotExist:
            return Response(status=404)


class InventorySummaryAPIView(APIView):
    def get(self, request, id, format=None):
        try:
            inv_summary = InventorySummary.objects.select_related().filter(supplier__supplier_id=id).first()
            serializer = InventorySummarySerializer(inv_summary)
            return Response(serializer.data)
        except InventorySummary.DoesNotExist:
            return Response(status=404)


    def post(self, request, id, format=None):
        try:
            print request.data
            society = SupplierTypeSociety.objects.get(pk=id)
            towercount = society.tower_count

            poster_campaign = 0
            standee_campaign = 0
            stall_campaign = 0
            flier_campaign = 0
            total_campaign = 0

            with transaction.atomic():
                if request.data['poster_allowed_nb']:
                    if request.data['nb_count']!=None and request.data['nb_count'] > 0:
                        society.poster_allowed_nb = True
                        poster_campaign = request.data['nb_count']
                        request.data['poster_campaign'] = poster_campaign
                    else:
                        society.poster_allowed_nb = False
                else :
                    society.poster_allowed_nb = False

                if request.data['lift_count']!=None and request.data['poster_allowed_lift']:
                    if request.data['lift_count'] > 0:
                        society.poster_allowed_lift = True
                        poster_campaign = poster_campaign + request.data['lift_count']
                        request.data['poster_campaign'] = poster_campaign
                    else:
                        society.poster_allowed_lift = False
                else:
                    society.poster_allowed_lift = False

                if request.data['standee_allowed']:
                    if request.data['total_standee_count']!=None and request.data['total_standee_count'] > 0:
                        society.standee_allowed = True
                        standee_campaign = request.data['total_standee_count']
                        request.data['standee_campaign'] = standee_campaign
                    else:
                        society.standee_allowed = False
                else:
                    society.standee_allowed = False

                if request.data['stall_allowed'] or request.data['car_display_allowed']:
                    if request.data['total_stall_count']!=None and request.data['total_stall_count'] > 0:
                        stall_campaign = request.data['total_stall_count']
                        request.data['stall_or_cd_campaign'] = stall_campaign



                if request.data['flier_allowed']:
                    if request.data['flier_frequency']!=None and request.data['flier_frequency'] > 0:
                        society.flier_allowed = True
                        flier_campaign = request.data['flier_frequency']
                        request.data['flier_campaign'] = flier_campaign
                    else:
                        society.flier_allowed = False
                else:
                    society.flier_allowed = False


#flier creation


                print "entering after flier flag"
                flag1 = True
                if 'id' in request.data:
                    flag1 = False
                    item = InventorySummary.objects.get(supplier=society)
                    if request.data['flier_allowed']==True:
                        if request.data['flier_frequency']!=None and item.flier_frequency < request.data['flier_frequency']:
                            if item.flier_frequency == None:
                                self.save_flyer_locations(0, request.data['flier_frequency'], society)
                            else:
                                self.save_flyer_locations(item.flier_frequency, request.data['flier_frequency'], society)
                        serializer = InventorySummarySerializer(item, data=request.data)
                else:
                    if flag1 and request.data['flier_frequency']!=None:
                        self.save_flyer_locations(0, request.data['flier_frequency'], society)
                    serializer = InventorySummarySerializer(data=request.data)
















                society.stall_allowed = True if request.data['stall_allowed'] else False
                society.car_display_allowed = True if request.data['car_display_allowed'] else False

                #society = SupplierTypeSociety.objects.get(pk=id)
                society.total_campaign = poster_campaign+standee_campaign+stall_campaign+flier_campaign
                society.save()

                
                print "entering after flag"
                flag = True
                if 'id' in request.data:
                    flag = False
                    item = InventorySummary.objects.get(supplier=society)
                    if request.data['stall_allowed']==True:
                        if request.data['total_stall_count']!=None and item.total_stall_count < request.data['total_stall_count']:
                            if item.total_stall_count == None:
                                self.save_stall_locations(0, request.data['total_stall_count'], society)
                            else:
                                self.save_stall_locations(item.total_stall_count, request.data['total_stall_count'], society)
                    serializer = InventorySummarySerializer(item, data=request.data)

                else:
                    if flag and request.data['total_stall_count']!=None:
                        self.save_stall_locations(0, request.data['total_stall_count'], society)
                    serializer = InventorySummarySerializer(data=request.data)


                if serializer.is_valid():
                    serializer.save(supplier=society)
                else :
                    return Response({'message': 'Invalid InventorySummary Serializer'},status=400)


                adinventory_dict =  self.adinventory_func()
                duration_type_dict = self.duration_type_func()
                price_list = []
                # print 'adinventory_dict : ', adinventory_dict

                if request.data['poster_price_week_nb']!= None:
                    posPrice = request.data['poster_price_week_nb']
                    if request.data['poster_allowed_nb']==True:
                        if request.data['nb_A3_allowed']== True:
                            price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['poster_a3'], duration_type=duration_type_dict['campaign_weekly'])
                            price.business_price = posPrice
                            price.society_price = price.business_price
                            price.save()
                            price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['poster_a3'], duration_type=duration_type_dict['unit_weekly'])
                            price.business_price = posPrice/towercount
                            price.society_price = price.business_price
                            price.save()

                        if request.data['nb_A4_allowed']== True:
                            price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['poster_a4'], duration_type=duration_type_dict['campaign_weekly'])
                            price.business_price = posPrice
                            price.society_price = price.business_price
                            price.save()
                            price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['poster_a4'], duration_type=duration_type_dict['unit_weekly'])
                            price.business_price = posPrice/towercount
                            price.society_price = price.business_price
                            price.save()

                if request.data['poster_price_week_lift']:
                    print "lift"
                    posPrice = request.data['poster_price_week_lift']
                    if request.data['poster_allowed_lift']==True:
                        price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['poster_lift_a3'],duration_type=duration_type_dict['campaign_weekly'])
                        print price
                        price.business_price = posPrice
                        price.society_price = price.business_price
                        price.save()
                        price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['poster_lift_a3'],duration_type=duration_type_dict['unit_weekly'])
                        price.business_price = posPrice/towercount
                        price.society_price = price.business_price
                        price.save()
                        price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['poster_lift_a4'],duration_type=duration_type_dict['campaign_weekly'])
                        price.business_price = posPrice
                        price.society_price = price.business_price
                        price.save()
                        price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['poster_lift_a4'],duration_type=duration_type_dict['unit_weekly'])
                        price.business_price = posPrice/towercount
                        price.society_price = price.business_price
                        price.save()


                if request.data['standee_price_week']!=None:
                    stanPrice = request.data['standee_price_week']
                    if request.data['standee_allowed']==True:
                        if request.data['standee_small']== True:
                            price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['standee_small'], duration_type=duration_type_dict['campaign_weekly'])
                            price.business_price = stanPrice
                            price.society_price = price.business_price
                            price.save()
                            
                            price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['standee_small'], duration_type=duration_type_dict['unit_weekly'])
                            price.business_price = stanPrice/towercount
                            price.society_price = price.business_price
                            price.save()

                        if request.data['standee_medium']== True:
                            price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['standee_medium'], duration_type=duration_type_dict['campaign_weekly'])
                            price.business_price = stanPrice
                            price.society_price = price.business_price
                            price.save()
                        
                            price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['standee_medium'], duration_type=duration_type_dict['unit_weekly'])
                            price.business_price = stanPrice/towercount
                            price.society_price = price.business_price
                            price.save()

                if request.data['stall_allowed']==True:
                    if request.data['stall_small']== True:
                        if request.data['stall_price_day_small']!=None:
                            stallPrice = request.data['stall_price_day_small']
                            price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['stall_small'], duration_type=duration_type_dict['unit_daily'])
                            price.business_price = stallPrice
                            price.society_price = price.business_price
                            price.save()
                    
                            price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['stall_canopy'], duration_type=duration_type_dict['unit_daily'])
                            price.business_price = stallPrice
                            price.society_price = price.business_price
                            price.save()

                    if request.data['stall_large']== True:
                        if request.data['stall_price_day_large']!=None:
                            stallPrice = request.data['stall_price_day_large']
                            price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['stall_large'], duration_type=duration_type_dict['unit_daily'])
                            price.business_price = stallPrice
                            price.society_price = price.business_price
                            price.save()

                if request.data['car_display_allowed']==True:
                    if request.data['cd_standard']== True:
                        if request.data['cd_price_day_standard']!=None:
                            cdPrice = request.data['cd_price_day_standard']
                            price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['car_display_standard'], duration_type=duration_type_dict['unit_daily'])
                            price.business_price = cdPrice
                            price.society_price = price.business_price
                            price.save()

                    if request.data['cd_premium']== True:
                        if request.data['cd_price_day_premium']!=None:
                            cdPrice = request.data['cd_price_day_premium']
                            price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['car_display_premium'], duration_type=duration_type_dict['unit_daily'])
                            price.business_price = cdPrice
                            price.society_price = price.business_price
                            price.save()

                if request.data['flier_price_day']!=None:
                    flierPrice = request.data['flier_price_day']
                    if request.data['mailbox_allowed']== True:
                        price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['flier_mailbox'], duration_type=duration_type_dict['unit_daily'])
                        price.business_price = flierPrice
                        price.society_price = price.business_price
                        price.save()

                    if request.data['d2d_allowed']== True:
                        price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['flier_door_to_door'], duration_type=duration_type_dict['unit_daily'])
                        price.business_price = flierPrice
                        price.society_price = price.business_price
                        price.save()

                    if request.data['flier_lobby_allowed']== True:
                        print "\n\nInside of flier lobby allowed"
                        try:
                            price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['flier_lobby'], duration_type=duration_type_dict['unit_daily'])
                            price.business_price = flierPrice
                            price.society_price = price.business_price
                            price.save()
                        except KeyError as e:
                            print "\n\nKey Error happened here\n\n"
                    
                
                try:
                    inventory_obj = InventorySummary.objects.get(supplier=society)
                    serilaizer_new = InventorySummarySerializer(inventory_obj)
                    return Response(serilaizer_new.data, status=200)
                except InventorySummary.DoesNotExist:
                    return Response({'message' : 'Error fetching inventory summary object'},status=406)

                # return Response(serializer.validated_data, status=200)
            print "404 Ist"
            return Response(status=404)
        # except:
        #     print "404 2nd"
        #     return Response(status=404)
        except InventorySummary.DoesNotExist:
            print "404 2nd"
            #   return Response(status=404)


    def adinventory_func(self):
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

    def duration_type_func(self):
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
        


    def save_stall_locations(self, c1, c2, society):
        count = int(c2) + 1
        for i in range(c1+1, count):
            stall_id = society.supplier_id + "CA0000ST" + str(i).zfill(2)
            print stall_id
            stall = StallInventory(adinventory_id=stall_id, supplier_id=society.supplier_id)
            stall.save()

    def save_flyer_locations(self, c1, c2, society):
        count = int(c2) + 1
        for i in range(c1+1, count):
            flyer_id = society.supplier_id + "0000FL" + str(i).zfill(2)
            print flyer_id
            print society.flat_count
            flyer = FlyerInventory(adinventory_id=flyer_id,flat_count=society.flat_count, supplier_id=society.supplier_id)
            flyer.save()

    def delete(self, request, id, format=None):
        try:
            print "hi"
            invId = request.query_params.get('invId', None)
            print invId
            stall = StallInventory.objects.get(pk=invId)
            print stall
            stall.delete()

            return Response(status=204)
        except StallInventory.DoesNotExist:
            return Response(status=404)

        # return Response(status=201)


class InventorySummaryAPIView(APIView):
    def get(self, request, id, format=None):
        try:
            inv_summary = InventorySummary.objects.select_related().filter(supplier__supplier_id=id).first()
            serializer = InventorySummarySerializer(inv_summary)
            return Response(serializer.data)
        except InventorySummary.DoesNotExist:
            return Response(status=404)


    def post(self, request, id, format=None):
        try:
            print request.data
            society = SupplierTypeSociety.objects.get(pk=id)
            towercount = society.tower_count

            poster_campaign = 0
            standee_campaign = 0
            stall_campaign = 0
            flier_campaign = 0
            total_campaign = 0

            with transaction.atomic():
                if request.data['poster_allowed_nb']:
                    if request.data['nb_count']!=None and request.data['nb_count'] > 0:
                        society.poster_allowed_nb = True
                        poster_campaign = request.data['nb_count']
                        request.data['poster_campaign'] = poster_campaign
                    else:
                        society.poster_allowed_nb = False
                else :
                    society.poster_allowed_nb = False

                if request.data['lift_count']!=None and request.data['poster_allowed_lift']:
                    if request.data['lift_count'] > 0:
                        society.poster_allowed_lift = True
                        poster_campaign = poster_campaign + request.data['lift_count']
                        request.data['poster_campaign'] = poster_campaign
                    else:
                        society.poster_allowed_lift = False
                else:
                    society.poster_allowed_lift = False

                if request.data['standee_allowed']:
                    if request.data['total_standee_count']!=None and request.data['total_standee_count'] > 0:
                        society.standee_allowed = True
                        standee_campaign = request.data['total_standee_count']
                        request.data['standee_campaign'] = standee_campaign
                    else:
                        society.standee_allowed = False
                else:
                    society.standee_allowed = False

                if request.data['stall_allowed'] or request.data['car_display_allowed']:
                    if request.data['total_stall_count']!=None and request.data['total_stall_count'] > 0:
                        stall_campaign = request.data['total_stall_count']
                        request.data['stall_or_cd_campaign'] = stall_campaign



                if request.data['flier_allowed']:
                    if request.data['flier_frequency']!=None and request.data['flier_frequency'] > 0:
                        society.flier_allowed = True
                        flier_campaign = request.data['flier_frequency']
                        request.data['flier_campaign'] = flier_campaign
                    else:
                        society.flier_allowed = False
                else:
                    society.flier_allowed = False


                society.stall_allowed = True if request.data['stall_allowed'] else False
                society.car_display_allowed = True if request.data['car_display_allowed'] else False

                #society = SupplierTypeSociety.objects.get(pk=id)
                society.total_campaign = poster_campaign+standee_campaign+stall_campaign+flier_campaign
                society.save()

                
                print "entering after flag"
                flag = True
                if 'id' in request.data:
                    flag = False
                    item = InventorySummary.objects.get(supplier=society)
                    if request.data['stall_allowed']==True:
                        if request.data['total_stall_count']!=None and item.total_stall_count < request.data['total_stall_count']:
                            if item.total_stall_count == None:
                                self.save_stall_locations(0, request.data['total_stall_count'], society)
                            else:
                                self.save_stall_locations(item.total_stall_count, request.data['total_stall_count'], society)
                    serializer = InventorySummarySerializer(item, data=request.data)

                else:
                    if flag and request.data['total_stall_count']!=None:
                        self.save_stall_locations(0, request.data['total_stall_count'], society)
                    serializer = InventorySummarySerializer(data=request.data)


                if serializer.is_valid():
                    serializer.save(supplier=society)
                else :
                    return Response({'message': 'Invalid InventorySummary Serializer'},status=400)


                adinventory_dict =  self.adinventory_func()
                duration_type_dict = self.duration_type_func()
                price_list = []
                # print 'adinventory_dict : ', adinventory_dict

                if request.data['poster_price_week_nb']!= None:
                    posPrice = request.data['poster_price_week_nb']
                    if request.data['poster_allowed_nb']==True:
                        if request.data['nb_A3_allowed']== True:
                            price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['poster_a3'], duration_type=duration_type_dict['campaign_weekly'])
                            price.business_price = posPrice
                            price.society_price = price.business_price
                            price.save()
                            price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['poster_a3'], duration_type=duration_type_dict['unit_weekly'])
                            price.business_price = posPrice/towercount
                            price.society_price = price.business_price
                            price.save()

                        if request.data['nb_A4_allowed']== True:
                            price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['poster_a4'], duration_type=duration_type_dict['campaign_weekly'])
                            price.business_price = posPrice
                            price.society_price = price.business_price
                            price.save()
                            price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['poster_a4'], duration_type=duration_type_dict['unit_weekly'])
                            price.business_price = posPrice/towercount
                            price.society_price = price.business_price
                            price.save()

                if request.data['poster_price_week_lift']:
                    print "lift"
                    posPrice = request.data['poster_price_week_lift']
                    if request.data['poster_allowed_lift']==True:
                        price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['poster_lift_a3'],duration_type=duration_type_dict['campaign_weekly'])
                        print price
                        price.business_price = posPrice
                        price.society_price = price.business_price
                        price.save()
                        price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['poster_lift_a3'],duration_type=duration_type_dict['unit_weekly'])
                        price.business_price = posPrice/towercount
                        price.society_price = price.business_price
                        price.save()
                        price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['poster_lift_a4'],duration_type=duration_type_dict['campaign_weekly'])
                        price.business_price = posPrice
                        price.society_price = price.business_price
                        price.save()
                        price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['poster_lift_a4'],duration_type=duration_type_dict['unit_weekly'])
                        price.business_price = posPrice/towercount
                        price.society_price = price.business_price
                        price.save()


                if request.data['standee_price_week']!=None:
                    stanPrice = request.data['standee_price_week']
                    if request.data['standee_allowed']==True:
                        if request.data['standee_small']== True:
                            price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['standee_small'], duration_type=duration_type_dict['campaign_weekly'])
                            price.business_price = stanPrice
                            price.society_price = price.business_price
                            price.save()
                            
                            price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['standee_small'], duration_type=duration_type_dict['unit_weekly'])
                            price.business_price = stanPrice/towercount
                            price.society_price = price.business_price
                            price.save()

                        if request.data['standee_medium']== True:
                            price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['standee_medium'], duration_type=duration_type_dict['campaign_weekly'])
                            price.business_price = stanPrice
                            price.society_price = price.business_price
                            price.save()
                        
                            price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['standee_medium'], duration_type=duration_type_dict['unit_weekly'])
                            price.business_price = stanPrice/towercount
                            price.society_price = price.business_price
                            price.save()

                if request.data['stall_allowed']==True:
                    if request.data['stall_small']== True:
                        if request.data['stall_price_day_small']!=None:
                            stallPrice = request.data['stall_price_day_small']
                            price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['stall_small'], duration_type=duration_type_dict['unit_daily'])
                            price.business_price = stallPrice
                            price.society_price = price.business_price
                            price.save()
                    
                            price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['stall_canopy'], duration_type=duration_type_dict['unit_daily'])
                            price.business_price = stallPrice
                            price.society_price = price.business_price
                            price.save()

                    if request.data['stall_large']== True:
                        if request.data['stall_price_day_large']!=None:
                            stallPrice = request.data['stall_price_day_large']
                            price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['stall_large'], duration_type=duration_type_dict['unit_daily'])
                            price.business_price = stallPrice
                            price.society_price = price.business_price
                            price.save()

                if request.data['car_display_allowed']==True:
                    if request.data['cd_standard']== True:
                        if request.data['cd_price_day_standard']!=None:
                            cdPrice = request.data['cd_price_day_standard']
                            price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['car_display_standard'], duration_type=duration_type_dict['unit_daily'])
                            price.business_price = cdPrice
                            price.society_price = price.business_price
                            price.save()

                    if request.data['cd_premium']== True:
                        if request.data['cd_price_day_premium']!=None:
                            cdPrice = request.data['cd_price_day_premium']
                            price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['car_display_premium'], duration_type=duration_type_dict['unit_daily'])
                            price.business_price = cdPrice
                            price.society_price = price.business_price
                            price.save()

                if request.data['flier_price_day']!=None:
                    flierPrice = request.data['flier_price_day']
                    if request.data['mailbox_allowed']== True:
                        price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['flier_mailbox'], duration_type=duration_type_dict['unit_daily'])
                        price.business_price = flierPrice
                        price.society_price = price.business_price
                        price.save()

                    if request.data['d2d_allowed']== True:
                        price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['flier_door_to_door'], duration_type=duration_type_dict['unit_daily'])
                        price.business_price = flierPrice
                        price.society_price = price.business_price
                        price.save()

                    if request.data['flier_lobby_allowed']== True:
                        print "\n\nInside of flier lobby allowed"
                        try:
                            price = PriceMappingDefault.objects.get(supplier_id=id, adinventory_type=adinventory_dict['flier_lobby'], duration_type=duration_type_dict['unit_daily'])
                            price.business_price = flierPrice
                            price.society_price = price.business_price
                            price.save()
                        except KeyError as e:
                            print "\n\nKey Error happened here\n\n"
                    
                
                try:
                    inventory_obj = InventorySummary.objects.get(supplier=society)
                    serilaizer_new = InventorySummarySerializer(inventory_obj)
                    return Response(serilaizer_new.data, status=200)
                except InventorySummary.DoesNotExist:
                    return Response({'message' : 'Error fetching inventory summary object'},status=406)

                # return Response(serializer.validated_data, status=200)
            print "404 Ist"
            return Response(status=404)
        # except:
        #     print "404 2nd"
        #     return Response(status=404)
        except InventorySummary.DoesNotExist:
            print "404 2nd"
            #   return Response(status=404)


    def adinventory_func(self):
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

    def duration_type_func(self):
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
        


    def save_stall_locations(self, c1, c2, society):
        count = int(c2) + 1
        for i in range(c1+1, count):
            stall_id = society.supplier_id + "CA0000ST" + str(i).zfill(2)
            print stall_id
            stall = StallInventory(adinventory_id=stall_id, supplier_id=society.supplier_id)
            stall.save()

    def delete(self, request, id, format=None):
        try:
            print "hi"
            invId = request.query_params.get('invId', None)
            print invId
            stall = StallInventory.objects.get(pk=invId)
            print stall
            stall.delete()

            return Response(status=204)
        except StallInventory.DoesNotExist:
            return Response(status=404)


class BasicPricingAPIView(APIView):
    # def get(self, request, id, format=None):
    #     response = {}
    #     try:
    #         basic_prices = PriceMappingDefault.objects.select_related().filter(supplier__supplier_id=id).values()

    #         for basic_price in basic_prices:
    #             duration_type = DurationType.objects.filter(id=basic_price['duration_type_id']).values().first()
    #             basic_price['duration_type'] = duration_type
    #             adinventory_type = AdInventoryType.objects.filter(id=basic_price['adinventory_type_id']).values().first()
    #             basic_price['adinventory_type'] = adinventory_type
           

    #         towercount = SupplierTypeSociety.objects.get(pk=id).tower_count
    #         response['tower_count'] = towercount
    #         response['prices'] = basic_prices
            
    #         return Response(response,status=200)

    #     except SupplierTypeSociety.DoesNotExist:
    #         return Response(status=404)
    #     except PriceMappingDefault.DoesNotExist:
    #         return Response(status=404)
            
    


    

    def get(self, request, id, format=None):
        response = {}
        try:
            # basic_prices = PriceMappingDefault.objects.select_related().filter(supplier__supplier_id=id)
            # print "basic prices: ", basic_prices
            basic_prices_select = PriceMappingDefault.objects.select_related('supplier','adinventory_type','duration_type').filter(supplier_id=id)
            basic_prices = PriceMappingDefault.objects.filter(supplier_id=id).values()
            
            for basic_item, basic_select_item in izip(basic_prices, basic_prices_select):
                basic_item['supplier'] = basic_select_item.__dict__['_supplier_cache'].__dict__
                basic_item['supplier'].pop("_state",None)
                basic_item['adinventory_type'] = basic_select_item.__dict__['_adinventory_type_cache'].__dict__
                basic_item['adinventory_type'].pop("_state",None)
                basic_item['duration_type'] =  basic_select_item.__dict__['_duration_type_cache'].__dict__
                basic_item['duration_type'].pop("_state",None)


            towercount = SupplierTypeSociety.objects.get(pk=id).tower_count

            response['tower_count'] = towercount

            print "tower count " , towercount
            response['prices'] = basic_prices
           
            return Response(response, status=200)

        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        except PriceMappingDefault.DoesNotExist:
            return Response(status=404)
       

    def post(self, request, id, format=None):
        print request.data

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
        #print request.data

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



class TowerAPIView(APIView):
    def get(self, request, id, format=None):
        try:
            towers = SupplierTypeSociety.objects.get(pk=id).towers.all()
            serializer_tower = UITowerSerializer(towers, many=True)

            inventory_summary = InventorySummary.objects.get(supplier_id=id)
            serializer_inventory = InventorySummarySerializer(inventory_summary)

            response = {
                'tower' : serializer_tower.data,
                'inventory' : serializer_inventory.data,
            }


            return Response(response, status=200)
        except SupplierTypeSociety.DoesNotExist:
            return Response({'message' : 'Invalid Society ID'},status=404)
        except InventorySummary.DoesNotExist:
            return Response({'message' : 'Please fill Inventory Summary Tab','inventory':'true'},status=404)

    def post(self, request, id, format=None):
        print "\n\n\n Tower API View Post"
        print request.data
        print "\n\n\n"
        society=SupplierTypeSociety.objects.get(pk=id)

        # checking of notice board in tower == inventory summary nb_count
        total_nb_count = 0
        total_lift_count = 0
        total_standee_count = 0
        for tower in request.data['TowerDetails']:
            total_nb_count += tower['notice_board_count_per_tower']
            total_lift_count += tower['lift_count']
            total_standee_count += tower['standee_count']

        print "total_nb_count : ",total_nb_count
        print "total_lift_count: ",total_lift_count
        print "total_standee_count: ",total_standee_count


        try:
            inventory_obj = InventorySummary.objects.get(supplier=society) 
        except InventorySummary.DoesNotExist:
            return Response({'message' : 'Please fill Inventory Summary Tab','inventory':'true'},status=404)

        print "inventory_obj.nb_count : ", inventory_obj.nb_count


        if total_nb_count !=0 and total_nb_count != inventory_obj.nb_count:

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
                    print "Tower does not exist"

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


        total_lift_count = 0
        total_standee_count = 0
        for tower in request.data['TowerDetails']:
            total_nb_count += tower['notice_board_count_per_tower']
            total_lift_count += tower['lift_count']
            total_standee_count += tower['standee_count']

        print "total_nb_count : ",total_nb_count
        print "total_lift_count: ",total_lift_count
        print "total_standee_count: ",total_standee_count


        try:
            inventory_obj = InventorySummary.objects.get(supplier=society) 
        except InventorySummary.DoesNotExist:
            return Response({'message' : 'Please fill Inventory Summary Tab','inventory':'true'},status=404)

        print "inventory_obj.nb_count : ", inventory_obj.nb_count


        if total_nb_count !=0 and total_nb_count != inventory_obj.nb_count:

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
                    print "Tower does not exist"

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
            item = InventorySummary.objects.get(supplier=society)

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
            item = InventorySummary.objects.get(supplier=society)

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
        # response = {}
        standees = []

        towers = SupplierTypeSociety.objects.get(pk=id).towers.all()
        society = SupplierTypeSociety.objects.get(pk=id)

        item = InventorySummary.objects.get(supplier=society)

        for tower in towers:
            tower_standees = tower.standees.all().values()
            for standee in tower_standees:
                standee['tower_name'] = tower.tower_name
            standees.extend(tower_standees)


        response = {"disable_standee": item.standee_allowed}
        response['standee_details'] = standees

        return Response(response, status=200)


    def post(self, request, id, format=None):
        # print request.data
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


        response = {}
        fliers = []
        try:
            society = SupplierTypeSociety.objects.get(pk=id)
            flyers = FlyerInventory.objects.filter(supplier=id)
            response['flat_count'] = society.flat_count

            serializer = FlyerInventorySerializer(flyers, many=True)
            response['flyers_data'] = serializer.data
            towers = SupplierTypeSociety.objects.get(pk=id).towers.all().values()
            
            item = InventorySummary.objects.get(supplier=society)

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
            print "in flyer delete"
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

        item = InventorySummary.objects.get(supplier=society)

        for tower in towers:
            tower_standees = tower.standees.all().values()
            for standee in tower_standees:
                standee['tower_name'] = tower.tower_name
            standees.extend(tower_standees)


        response = {"disable_standee": item.standee_allowed}
        response['standee_details'] = standees

        return Response(response, status=200)


    def post(self, request, id, format=None):
        # print request.data
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

        item = InventorySummary.objects.get(supplier=society)

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
        print "request data: ", stall
        society = SupplierTypeSociety.objects.get(supplier_id=id)

        society.street_furniture_available = True if stall['furniture_available'] == 'Yes' else False
        society.stall_timing = stall['stall_timing']
        print "society stall timing is ", society.stall_timing
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
            print "Valid serializer"
            corporate_serializer.save()
            print "Values Saved"
        else:
            print "Serializer error"
            print corporate_serializer.errors
            error['message'] ='Invalid Corporate Info data'
            error = json.dumps(error)
            return Response(response, status=406)

        # Round 2 Saving List of companies
        
        try:
            corporate_id = request.data['supplier_id']
        except KeyError :
            error['message'] ='Invalid Corporate Id'
            error = json.dumps(error)
            return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)

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

        print "\n\nRound 2 complete"

        # Round 3 - Saving contacts
       
        try:
            print id
            instance = SupplierTypeCorporate.objects.get(supplier_id=id)
        except SupplierTypeCorporate.DoesNotExist:
            print "id does not exist in database"
            return Response({'message': 'This corporate park does not exist'}, status=406)

        content_type = ContentType.objects.get_for_model(SupplierTypeCorporate)
        print request.data
        
        contacts_ids = ContactDetailsGeneric.objects.filter(content_type=content_type, object_id=instance.supplier_id).values_list('id',flat=True)
        contacts_ids = list(contacts_ids)
        print contacts_ids
        print type(contacts_ids)

        for contact in request.data['contacts']:
            if 'id' in contact:
                contact_instance = ContactDetailsGeneric.objects.get(id=contact['id'])
                contacts_ids.remove(contact_instance.id)
                serializer = ContactDetailsGenericSerializer(contact_instance, data=contact)
                if serializer.is_valid():
                    serializer.save()
                else:
                    print serializer.errors
                    return Response(status=404)

            else:
                contact['object_id'] = instance.supplier_id
                serializer = ContactDetailsGenericSerializer(data=contact)
                if serializer.is_valid():
                    serializer.save(content_type=content_type)
                else:
                    print serializer.errors
                    return Response(status=404)

        ContactDetailsGeneric.objects.filter(id__in=contacts_ids).delete()


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
        return Response(status=200)


    def get(self, request, id, format=None):
        try:
            data1 = SupplierTypeCorporate.objects.get(supplier_id=id)
            serializer = SupplierTypeCorporateSerializer(data1)
            data2 = CorporateParkCompanyList.objects.filter(supplier_id=id)
            serializer1 = CorporateParkCompanyListSerializer(data2, many=True)
            data3 = ContactDetailsGeneric.objects.filter(object_id=id)
            serializer2 = ContactDetailsGenericSerializer(data3, many=True)
            print "Hello\n\n"
            print serializer2.data
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
class saveBuildingDetailsAPIView(APIView):

    def get(self,request,id, format=None):
        try:
            corporate = SupplierTypeCorporate.objects.get(supplier_id=id)
        except SupplierTypeCorporate.DoesNotExist:
            return Response({'message' : 'Invalid Corporate ID'}, status=406)

        buildings = corporate.get_buildings()
        building_serializer = CorporateBuildingGetSerializer(buildings, many=True)
        return Response(building_serializer.data, status = 200)


    def post(self,request,id,format=None):

        try:
            corporate_object = SupplierTypeCorporate.objects.get(supplier_id=id)
        except SupplierTypeCorporate.DoesNotExist:
            return Response({'message' : 'Invalid Corporate ID'}, status=404)

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
                print "Invalid serializer"
                print building_serializer.errors
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
                print "1"

        if wing_ids_superset:
            CorporateBuildingWing.objects.filter(id__in=wing_ids_superset).delete()
            print "2"
        if buildings_ids:
            CorporateBuilding.objects.filter(id__in=buildings_ids).delete()
            print "3"            

        return Response(status=200)
    

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

        print "\n\n",companies_serializer.data,"\n\n"
        return Response(companies_serializer.data, status=200)


    def post(self, request, id, format=True):
        print "\n\nData to be saved is \n\n",request.data
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
                print "\n\ncompany_detail : ",company_detail
                print "\n\n\n"
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
            print "Valid serializer"
            salon_serializer.save()
            print "Values Saved"
        else:
            print "Serializer error"
            print salon_serializer.errors
            error['message'] ='Invalid Salon Info data'
            error = json.dumps(error)
            return Response(response, status=406)


        # Now saving contacts
        try:
            instance = SupplierTypeSalon.objects.get(supplier_id=id)
        except SupplierTypeSalon.DoesNotExist:
            print "id does not exist in database"
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
                    print serializer.errors
                    return Response(status=404)

            else:
                contact['object_id'] = instance.supplier_id
                serializer = ContactDetailsGenericSerializer(data=contact)
                if serializer.is_valid():
                    serializer.save(content_type=content_type)
                else:
                    print serializer.errors
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
            print "Valid serializer"
            gym_serializer.save()
            print "Values Saved"
        else:
            print "Serializer error"
            print gym_serializer.errors
            error['message'] ='Invalid Gym Info data'
            error = json.dumps(error)
            return Response(response, status=406)


        # Now saving contacts
        try:
            instance = SupplierTypeGym.objects.get(supplier_id=id)
        except SupplierTypeGym.DoesNotExist:
            print "id does not exist in database"
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
                    print serializer.errors
                    return Response(status=404)

            else:
                contact['object_id'] = instance.supplier_id
                serializer = ContactDetailsGenericSerializer(data=contact)
                if serializer.is_valid():
                    serializer.save(content_type=content_type)
                else:
                    print serializer.errors
                    return Response(status=404)

        ContactDetailsGeneric.objects.filter(id__in=contacts_ids).delete()
        return Response(status=200)

        # End of contact saving