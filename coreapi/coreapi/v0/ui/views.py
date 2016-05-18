from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from v0.permissions import IsOwnerOrManager
from rest_framework import filters
from serializers import UISocietySerializer, UITowerSerializer
from v0.serializers import ImageMappingSerializer, InventoryLocationSerializer, AdInventoryLocationMappingSerializer, AdInventoryTypeSerializer, DurationTypeSerializer, PriceMappingDefaultSerializer, PriceMappingSerializer, BannerInventorySerializer, CommunityHallInfoSerializer, DoorToDoorInfoSerializer, LiftDetailsSerializer, NoticeBoardDetailsSerializer, PosterInventorySerializer, SocietyFlatSerializer, StandeeInventorySerializer, SwimmingPoolInfoSerializer, WallInventorySerializer, UserInquirySerializer, CommonAreaDetailsSerializer, ContactDetailsSerializer, EventsSerializer, InventoryInfoSerializer, MailboxInfoSerializer, OperationsInfoSerializer, PoleInventorySerializer, PosterInventoryMappingSerializer, RatioDetailsSerializer, SignupSerializer, StallInventorySerializer, StreetFurnitureSerializer, SupplierInfoSerializer, SportsInfraSerializer, SupplierTypeSocietySerializer, SocietyTowerSerializer, FlatTypeSerializer
from v0.models import ImageMapping, InventoryLocation, AdInventoryLocationMapping, AdInventoryType, DurationType, PriceMappingDefault, PriceMapping, BannerInventory, CommunityHallInfo, DoorToDoorInfo, LiftDetails, NoticeBoardDetails, PosterInventory, SocietyFlat, StandeeInventory, SwimmingPoolInfo, WallInventory, UserInquiry, CommonAreaDetails, ContactDetails, Events, InventoryInfo, MailboxInfo, OperationsInfo, PoleInventory, PosterInventoryMapping, RatioDetails, Signup, StallInventory, StreetFurniture, SupplierInfo, SportsInfra, SupplierTypeSociety, SocietyTower, FlatType
from v0.models import City, CityArea, CitySubArea,SupplierTypeCode, InventorySummary, SocietyMajorEvents
from v0.serializers import CitySerializer, CityAreaSerializer, CitySubAreaSerializer, SupplierTypeCodeSerializer, InventorySummarySerializer, SocietyMajorEventsSerializer
from django.db.models import Q



class getInitialDataAPIView(APIView):
    def get(self, request, format=None):
        try:
            cities = City.objects.all()
            serializer = CitySerializer(cities, many=True)
            items = SupplierTypeCode.objects.all()
            serializer1 = SupplierTypeCodeSerializer(items, many=True)
            result = {'cities':serializer.data, 'supplier_types':serializer1.data}
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
            except:
                print "No such society"
            current_user = request.user
            supplier_id = city.city_code + area.area_code + sub_area.subarea_code + request.data['supplier_type'] + request.data['supplier_code']
            supplier = {'supplier_id':supplier_id,
                        'society_name':request.data['supplier_name'],
                        'society_city':city.city_name,
                        'society_locality':area.label,
                        'society_state' : city.state_code.state_name,
                        'created_by': current_user.id
                        }
            serializer = SupplierTypeSocietySerializer(data=supplier)
            if serializer.is_valid():
                serializer.save()
                #populate default pricing table
                set_default_pricing(serializer.data['supplier_id'])
                return Response(serializer.data, status=200)
            else:
                return Response(serializer.errors, status=400)
        #except :
         #   return Response(status=404)


class SocietyAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrManager,)

    def get(self, request, id, format=None):
        #try:
            item = SupplierTypeSociety.objects.get(pk=id)
            #self.check_object_permissions(self.request, item)
            serializer = UISocietySerializer(item)
            return Response(serializer.data)
        #except :
         #   return Response(status=404)

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


def set_default_pricing(society_id):
    society = SupplierTypeSociety.objects.get(pk=society_id)
    ad_types = AdInventoryType.objects.all()
    duration_types = DurationType.objects.all()
    for type in ad_types:
        for duration in duration_types:
            if (type.adinventory_name=='POSTER'):
                if((duration.duration_name=='Unit Daily')):
                    pmdefault = PriceMappingDefault(supplier= society, adinventory_type=type, duration_type=duration, society_price=-1, business_price=-1)
                    pmdefault.save()
                if((duration.duration_name=='Campaign Weekly')|(duration.duration_name=='Campaign Monthly')|(duration.duration_name=='Unit Monthly')|(duration.duration_name=='Unit Weekly')):
                    pmdefault = PriceMappingDefault(supplier= society, adinventory_type=type, duration_type=duration, society_price=0, business_price=0)
                    pmdefault.save()
            if (type.adinventory_name=='STANDEE'):
                if((duration.duration_name=='Campaign Weekly')|(duration.duration_name=='Unit Weekly')):
                    if(type.adinventory_type=='Large'):
                        pmdefault = PriceMappingDefault(supplier= society, adinventory_type=type, duration_type=duration, society_price=-1, business_price=-1)
                        pmdefault.save()
                    else:
                        pmdefault = PriceMappingDefault(supplier= society, adinventory_type=type, duration_type=duration, society_price=0, business_price=0)
                        pmdefault.save()
            if (type.adinventory_name=='STALL'):
                if(duration.duration_name=='Unit Daily'):
                    if ((type.adinventory_type=='Canopy')|(type.adinventory_type=='Small')|(type.adinventory_type=='Large')):
                        pmdefault = PriceMappingDefault(supplier= society, adinventory_type=type, duration_type=duration, society_price=0, business_price=0)
                        pmdefault.save()
                    if(type.adinventory_type=='Customize'):
                        pmdefault = PriceMappingDefault(supplier= society, adinventory_type=type, duration_type=duration, society_price=-1, business_price=-1)
                        pmdefault.save()
            if ((type.adinventory_name=='CAR DISPLAY')&(duration.duration_name=='Unit Daily')):
                if ((type.adinventory_type=='Standard')|(type.adinventory_type=='Premium')):
                    pmdefault = PriceMappingDefault(supplier= society, adinventory_type=type, duration_type=duration, society_price=0, business_price=0)
                    pmdefault.save()
            if ((type.adinventory_name=='FLIER')&(duration.duration_name=='Unit Daily')):
                if ((type.adinventory_type=='Door-to-Door')|(type.adinventory_type=='Mailbox')):
                    pmdefault = PriceMappingDefault(supplier= society, adinventory_type=type, duration_type=duration, society_price=0, business_price=0)
                    pmdefault.save()


    return


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
                else:
                    items = SupplierTypeSociety.objects.filter(created_by=user.id)

            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(items, request)
            serializer = UISocietySerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)

class SocietyAPIFiltersListView(APIView):
    def post(self, request, format=None):
        try:
            cityArea = []
            societytype = []
            flatquantity = []
            inventorytype = []
            filter_present = False

            if 'locationValueModel' in request.data:
                for key in request.data['locationValueModel']:
                    cityArea.append(key['label'])
                    filter_present = True

            if 'typeValuemodel' in request.data:
                for key in request.data['typeValuemodel']:
                    societytype.append(key['label'])
                    filter_present = True

            if 'checkboxes' in request.data:
                for key in request.data['checkboxes']:
                    if key['checked']:
                     flatquantity.append(key['name'])
                     filter_present = True

            if 'types' in request.data:
                for key in request.data['types']:
                    if key['checked']:
                     inventorytype.append(key['inventoryname'])
                     filter_present = True
                print inventorytype

            if filter_present:
                    items = SupplierTypeSociety.objects.filter(Q(society_locality__in = cityArea) | Q(society_type_quality__in = societytype) | Q(society_type_quantity__in = flatquantity))
                    serializer = UISocietySerializer(items, many= True)
            else:
                    items = SupplierTypeSociety.objects.all()
                    serializer = UISocietySerializer(items, many= True)

            return Response(serializer.data, status = 200)

        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)


class FlatTypeAPIView(APIView):
    def get(self, request, id, format=None):
        try:
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
            else:
                return Response(serializer.errors, status=400)

        return Response(status=201)


class InventorySummaryAPIView(APIView):
    def get(self, request, id, format=None):
        try:
            inv_summary = InventorySummary.objects.select_related().filter(supplier__supplier_id=id).first()
            serializer = InventorySummarySerializer(inv_summary)
            return Response(serializer.data)
        except InventorySummary.DoesNotExist:
            return Response(status=404)


    def post(self, request, id, format=None):
        #try:
            society = SupplierTypeSociety.objects.get(pk=id)
            towercount = society.tower_count

            poster_campaign = 0
            standee_campaign = 0
            stall_campaign = 0
            flier_campaign = 0
            total_campaign = 0

            if request.data['poster_allowed_nb']:
                if request.data['nb_count']!=None and request.data['nb_count'] > 0:
                    poster_campaign = request.data['nb_count']
                    request.data['poster_campaign'] = poster_campaign
            if request.data['lift_count']!=None and request.data['poster_allowed_lift']:
                if request.data['lift_count'] > 0:
                    poster_campaign = poster_campaign + request.data['lift_count']
                    request.data['poster_campaign'] = poster_campaign
            if request.data['standee_allowed']:
                if request.data['total_standee_count']!=None and request.data['total_standee_count'] > 0:
                    standee_campaign = request.data['total_standee_count']
                    request.data['standee_campaign'] = standee_campaign
            if request.data['stall_allowed'] or request.data['car_display_allowed']:
                if request.data['total_stall_count']!=None and request.data['total_stall_count'] > 0:
                    stall_campaign = request.data['total_stall_count']
                    request.data['stall_or_cd_campaign'] = stall_campaign
            if request.data['flier_allowed']:
                if request.data['flier_frequency']!=None and request.data['flier_frequency'] > 0:
                    flier_campaign = request.data['flier_frequency']
                    request.data['flier_campaign'] = flier_campaign

            #society = SupplierTypeSociety.objects.get(pk=id)
            society.total_campaign = poster_campaign+standee_campaign+stall_campaign+flier_campaign
            society.save()



            flag = True
            if 'id' in request.data:
                flag = False
                item = InventorySummary.objects.get(supplier=society)
                if request.data['stall_allowed']==True:
                    if request.data['total_stall_count']!=None and item.total_stall_count < request.data['total_stall_count']:
                        self.save_stall_locations(item.total_stall_count, request.data['total_stall_count'], society)
                    serializer = InventorySummarySerializer(item, data=request.data)

            else:
                if flag and request.data['total_stall_count']!=None:
                    self.save_stall_locations(0, request.data['total_stall_count'], society)
                serializer = InventorySummarySerializer(data=request.data)


            if serializer.is_valid():
                serializer.save(supplier=society)

            if request.data['poster_price_week_nb']!=None:
                posPrice = request.data['poster_price_week_nb']
                #change_price(id, 'POSTER', 'A3','Campaign Weekly', posPrice)
                if request.data['poster_allowed_nb']==True:
                    if request.data['nb_A3_allowed']== True:
                        price = PriceMappingDefault.objects.get(supplier__supplier_id=id, adinventory_type__adinventory_name='POSTER',adinventory_type__adinventory_type='A3', duration_type__duration_name='Campaign Weekly')
                        price.business_price = posPrice
                        price.save()
                        price = PriceMappingDefault.objects.get(supplier__supplier_id=id, adinventory_type__adinventory_name='POSTER',adinventory_type__adinventory_type='A3', duration_type__duration_name='Unit Weekly')
                        price.business_price = posPrice/towercount
                        price.save()

                    if request.data['nb_A4_allowed']== True:
                        price = PriceMappingDefault.objects.get(supplier__supplier_id=id, adinventory_type__adinventory_name='POSTER',adinventory_type__adinventory_type='A4', duration_type__duration_name='Campaign Weekly')
                        price.business_price = posPrice
                        price.save()
                        price = PriceMappingDefault.objects.get(supplier__supplier_id=id, adinventory_type__adinventory_name='POSTER',adinventory_type__adinventory_type='A4', duration_type__duration_name='Unit Weekly')
                        price.business_price = posPrice/towercount
                        price.save()

                    if request.data['standee_price_week']!=None:
                        stanPrice = request.data['standee_price_week']
                        if request.data['standee_allowed']==True:
                            if request.data['standee_small']== True:
                                price = PriceMappingDefault.objects.get(supplier__supplier_id=id, adinventory_type__adinventory_name='STANDEE',adinventory_type__adinventory_type='Small', duration_type__duration_name='Campaign Weekly')
                                price.business_price = stanPrice
                                price.save()
                                price = PriceMappingDefault.objects.get(supplier__supplier_id=id, adinventory_type__adinventory_name='STANDEE',adinventory_type__adinventory_type='Small', duration_type__duration_name='Unit Weekly')
                                price.business_price = stanPrice/towercount
                                price.save()

                            if request.data['standee_medium']== True:
                                price = PriceMappingDefault.objects.get(supplier__supplier_id=id, adinventory_type__adinventory_name='STANDEE',adinventory_type__adinventory_type='Medium', duration_type__duration_name='Campaign Weekly')
                                price.business_price = stanPrice
                                price.save()
                                price = PriceMappingDefault.objects.get(supplier__supplier_id=id, adinventory_type__adinventory_name='STANDEE',adinventory_type__adinventory_type='Medium', duration_type__duration_name='Unit Weekly')
                                price.business_price = stanPrice/towercount
                                price.save()

                    if request.data['stall_allowed']==True:
                        if request.data['stall_small']== True:
                            if request.data['stall_price_day_small']!=None:
                                stallPrice = request.data['stall_price_day_small']
                                price = PriceMappingDefault.objects.get(supplier__supplier_id=id, adinventory_type__adinventory_name='STALL',adinventory_type__adinventory_type='Small', duration_type__duration_name='Unit Daily')
                                price.business_price = stallPrice
                                price.save()
                                price = PriceMappingDefault.objects.get(supplier__supplier_id=id, adinventory_type__adinventory_name='STALL',adinventory_type__adinventory_type='Canopy', duration_type__duration_name='Unit Daily')
                                price.business_price = stallPrice
                                price.save()

                        if request.data['stall_large']== True:
                            if request.data['stall_price_day_large']!=None:
                                stallPrice = request.data['stall_price_day_large']
                                price = PriceMappingDefault.objects.get(supplier__supplier_id=id, adinventory_type__adinventory_name='STALL',adinventory_type__adinventory_type='Large', duration_type__duration_name='Unit Daily')
                                price.business_price = stallPrice
                                price.save()

                    if request.data['car_display_allowed']==True:
                        if request.data['cd_standard']== True:
                            if request.data['cd_price_day_standard']!=None:
                                cdPrice = request.data['cd_price_day_standard']
                                price = PriceMappingDefault.objects.get(supplier__supplier_id=id, adinventory_type__adinventory_name='CAR DISPLAY',adinventory_type__adinventory_type='Standard', duration_type__duration_name='Unit Daily')
                                price.business_price = cdPrice
                                price.save()

                        if request.data['cd_premium']== True:
                            if request.data['cd_price_day_premium']!=None:
                                cdPrice = request.data['cd_price_day_premium']
                                price = PriceMappingDefault.objects.get(supplier__supplier_id=id, adinventory_type__adinventory_name='CAR DISPLAY',adinventory_type__adinventory_type='Premium', duration_type__duration_name='Unit Daily')
                                price.business_price = cdPrice
                                price.save()

                if request.data['flier_price_day']!=None:
                    flierPrice = request.data['flier_price_day']
                    if request.data['mailbox_allowed']== True:
                        price = PriceMappingDefault.objects.get(supplier__supplier_id=id, adinventory_type__adinventory_name='FLIER',adinventory_type__adinventory_type='Mailbox', duration_type__duration_name='Unit Daily')
                        price.business_price = flierPrice
                        price.save()

                    if request.data['d2d_allowed']== True:
                        price = PriceMappingDefault.objects.get(supplier__supplier_id=id, adinventory_type__adinventory_name='FLIER',adinventory_type__adinventory_type='Door-to-Door', duration_type__duration_name='Unit Daily')
                        price.business_price = flierPrice
                        price.save()

                return Response(serializer.data, status=200)

            else:
                return Response(serializer.errors, status=400)

            return Response(serializer.data, status=200)


        #except:
        #    return Response(status=404)


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
    def get(self, request, id, format=None):
        response = {}
        try:
            basic_prices = PriceMappingDefault.objects.select_related().filter(supplier__supplier_id=id)
            towercount = SupplierTypeSociety.objects.get(pk=id).tower_count
            serializer = PriceMappingDefaultSerializer(basic_prices, many=True)
            response['tower_count'] = towercount
            response['prices'] = serializer.data
            return Response(response)

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
            serializer = UITowerSerializer(towers, many=True)
            return Response(serializer.data)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        except SocietyTower.DoesNotExist:
            return Response(status=404)

    def post(self, request, id, format=None):
        #print request.data
        flag = True
        society=SupplierTypeSociety.objects.get(pk=id)

        for key in request.data['TowerDetails']:
            if 'tower_id' in key:
                flag = False
                item = SocietyTower.objects.get(pk=key['tower_id'])
                if item.lift_count < key['lift_count']:
                    self.save_lift_locations(item.lift_count, key['lift_count'], item, society)
                if item.notice_board_count_per_tower < key['notice_board_count_per_tower']:
                    self.save_nb_locations(item.notice_board_count_per_tower, key['notice_board_count_per_tower'], item, society)
                if item.standee_count < key['standee_count']:
                    self.save_standee_locations(item.standee_count, key['standee_count'], item, society)
                serializer = SocietyTowerSerializer(item, data=key)
            else:
                serializer = SocietyTowerSerializer(data=key)

            try:
                if serializer.is_valid():
                    serializer.save(supplier=society)
                  #  tower_data=serializer.data
            except:
                return Response(serializer.errors, status=400)

            try:
                tower_data = SocietyTower.objects.get(pk=serializer.data['tower_id'])
            except SocietyTower.DoesNotExist:
                return Response(status=404)

            #create automated IDs for lift, notice boards, standees
            if flag:
                self.save_lift_locations(0, key['lift_count'], tower_data, society)
                self.save_nb_locations(0, key['notice_board_count_per_tower'], tower_data, society)
                self.save_standee_locations(0, key['standee_count'], tower_data, society)

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

            towerId = 9 #request.query_params.get('towId', None)
            item = SocietyTower.objects.get(pk=towerId)
            item.delete()

            return Response(status=204)
        except SocietyTower.DoesNotExist:
            return Response(status=404)


    def save_lift_locations(self, c1, c2, tower, society):
        i = c1 + 1
        tow_name = tower.tower_name
        while i <= c2:
            lift_tag = tower.tower_tag + "00L" + str(i).zfill(2)
            adId = society.supplier_id + lift_tag + "PO01"
            lift = LiftDetails(adinventory_id=adId, lift_tag=lift_tag, tower=tower)
            lift_inv = PosterInventory(adinventory_id=adId, poster_location=lift_tag, tower_name=tow_name, supplier=society)
            lift.save()
            lift_inv.save()
            i += 1

    def save_nb_locations(self, c1, c2, tower, society):
        i = c1 + 1
        while i <= c2:
            nb_tag = tower.tower_tag + "00N" + str(i).zfill(2)
            nb = NoticeBoardDetails(notice_board_tag=nb_tag, tower=tower)
            nb.save()

            i += 1

    def save_standee_locations(self, c1, c2, tower, society):
        i = c1 + 1
        while i <= c2:
            sd_tag = society.supplier_id + tower.tower_tag + "0000SD" + str(i).zfill(2)
            sd = StandeeInventory(adinventory_id=sd_tag, tower=tower)
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
        response = {}
        try:
            mail_boxes = SupplierTypeSociety.objects.get(pk=id).mail_boxes.all()
            serializer = MailboxInfoSerializer(mail_boxes, many=True)
            mail_box_available = get_availability(serializer.data)
            response['mail_box_available'] = mail_box_available
            response['mail_box_details'] = serializer.data


            door_to_doors = SupplierTypeSociety.objects.get(pk=id).door_to_doors.all()
            serializer = DoorToDoorInfoSerializer(door_to_doors, many=True)
            door_to_door_allowed = get_availability(serializer.data)
            response['door_to_door_allowed'] = door_to_door_allowed
            response['door_to_door_details'] = serializer.data

            return Response(response, status=200)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        except MailboxInfo.DoesNotExist:
            return Response(status=404)
        except DoorToDoorInfo.DoesNotExist:
            return Response(status=404)

    def post(self, request, id, format=None):
            #print request.data
            society = SupplierTypeSociety.objects.get(pk=id)
            if request.data['mail_box_available']:
                response = post_data(MailboxInfo, MailboxInfoSerializer, request.data['mail_box_details'], society)
                if response == False:
                    return Response(status=400)

            if request.data['door_to_door_allowed']:
                response = post_data(DoorToDoorInfo, DoorToDoorInfoSerializer, request.data['door_to_door_details'], society)
                if response == False:
                    return Response(status=400)

            return Response(status=201)



class StandeeBannerAPIView(APIView):
    def get(self, request, id, format=None):
        response = {}
        standees = []

        towers = SupplierTypeSociety.objects.get(pk=id).towers.all()
        society = SupplierTypeSociety.objects.get(pk=id)
        for tower in towers:
            standees.extend(tower.standees.all())

        item = InventorySummary.objects.get(supplier=society)

        serializer1 = InventorySummarySerializer(item, many=True)
        response = {"disable_standee": item.standee_allowed}
        serializer = StandeeInventorySerializer(standees, many=True)
        response['standee_details'] = serializer.data

        return Response(response, status=200)


    def post(self, request, id, format=None):
        for standee in request.data['standee_details']:
            if 'id' in standee:
                standee_item = StandeeInventory.objects.get(pk=lift['id'])
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

        return Response(response, status=200)


    def post(self, request, id, format=None):
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
