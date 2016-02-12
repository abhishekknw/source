from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from serializers import UISocietySerializer, UITowerSerializer
from v0.serializers import ImageMappingSerializer, InventoryLocationSerializer, AdInventoryLocationMappingSerializer, AdInventoryTypeSerializer, DurationTypeSerializer, PriceMappingDefaultSerializer, PriceMappingSerializer, BannerInventorySerializer, CarDisplayInventorySerializer, CommunityHallInfoSerializer, DoorToDoorInfoSerializer, LiftDetailsSerializer, NoticeBoardDetailsSerializer, PosterInventorySerializer, SocietyFlatSerializer, StandeeInventorySerializer, SwimmingPoolInfoSerializer, WallInventorySerializer, UserInquirySerializer, CommonAreaDetailsSerializer, ContactDetailsSerializer, EventsSerializer, InventoryInfoSerializer, MailboxInfoSerializer, OperationsInfoSerializer, PoleInventorySerializer, PosterInventoryMappingSerializer, RatioDetailsSerializer, SignupSerializer, StallInventorySerializer, StreetFurnitureSerializer, SupplierInfoSerializer, SportsInfraSerializer, SupplierTypeSocietySerializer, SocietyTowerSerializer
from v0.models import ImageMapping, InventoryLocation, AdInventoryLocationMapping, AdInventoryType, DurationType, PriceMappingDefault, PriceMapping, BannerInventory, CarDisplayInventory, CommunityHallInfo, DoorToDoorInfo, LiftDetails, NoticeBoardDetails, PosterInventory, SocietyFlat, StandeeInventory, SwimmingPoolInfo, WallInventory, UserInquiry, CommonAreaDetails, ContactDetails, Events, InventoryInfo, MailboxInfo, OperationsInfo, PoleInventory, PosterInventoryMapping, RatioDetails, Signup, StallInventory, StreetFurniture, SupplierInfo, SportsInfra, SupplierTypeSociety, SocietyTower
from django.db.models import Q


class SocietyAPIView(APIView):
    def get(self, request, id, format=None):
        try:
            item = SupplierTypeSociety.objects.get(pk=id)
            serializer = UISocietySerializer(item)
            return Response(serializer.data)
        except :
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
        print request.data
        current_user = request.user
        if 'supplier_id' in request.data:
            society = SupplierTypeSociety.objects.filter(pk=request.data['supplier_id']).first()
            if society:
                serializer = SupplierTypeSocietySerializer(society,data=request.data)
                flag = False
            else:
                request.data['created_by'] = current_user.id
                serializer = SupplierTypeSocietySerializer(data=request.data)
                flag = True


        if serializer.is_valid():
            serializer.save()
            #populate default pricing table
            if flag:
                set_default_pricing(serializer.data['supplier_id'])
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

        return Response(serializer.data, status=201)




def set_default_pricing(society_id):
    society = SupplierTypeSociety.objects.filter(pk=society_id).first()
    ad_types = AdInventoryType.objects.all()
    duration_types = DurationType.objects.all()
    for type in ad_types:
        for duration in duration_types:
            pmdefault = PriceMappingDefault(supplier= society, adinventory_type=type, duration_type=duration, society_price=0, business_price=0)
            pmdefault.save()

    return



class SocietyAPIListView(APIView):
    def get(self, request, format=None):
        try:
            search_txt = request.query_params.get('search', None)
            if search_txt:
                items = SupplierTypeSociety.objects.filter(Q(supplier_id__icontains=search_txt) | Q(society_name__icontains=search_txt)| Q(society_address1__icontains=search_txt)| Q(society_city__icontains=search_txt)| Q(society_state__icontains=search_txt))
            else:
                items = SupplierTypeSociety.objects.all()
            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(items, request)
            serializer = UISocietySerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)




class BasicPricingAPIView(APIView):
    def get(self, request, id, format=None):
        try:
            basic_prices = PriceMappingDefault.objects.select_related().filter(supplier__supplier_id=id)
            #basic_prices = SupplierTypeSociety.objects.get(pk=id).default_prices.all()
            serializer = PriceMappingDefaultSerializer(basic_prices, many=True)
            return Response(serializer.data)
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
            #basic_prices = SupplierTypeSociety.objects.get(pk=id).default_prices.all()
            serializer = PriceMappingSerializer(inv_prices, many=True)
            return Response(serializer.data)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        except PriceMapping.DoesNotExist:
            return Response(status=404)


    def post(self, request, id, format=None):
        print request.data


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
        print request.data
        society=SupplierTypeSociety.objects.get(pk=id)
        for key in request.data['TowerDetails']:
            if 'tower_id' in key:
                item = SocietyTower.objects.get(pk=key['tower_id'])
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

            tag_initial = society.society_name[:3] + tower_data.tower_name[:3]

            if key['notice_board_details_available']:
                for index, notice_board in enumerate(key['notice_board_details'], start=1):
                    if 'id' in notice_board:
                        notice_item = NoticeBoardDetails.objects.get(pk=notice_board['id'])
                        notice_serializer = NoticeBoardDetailsSerializer(notice_item, data=notice_board)
                    else:
                        notice_serializer = NoticeBoardDetailsSerializer(data=notice_board)

                        #populate location and ad inventory table
                        notice_tag = generate_location_tag(tag_initial, 'noticeboard', index)
                        nb_location = InventoryLocation(location_id = notice_tag, location_type='Notice Board')
                        nb_location.save()
                        for i in range(notice_board['total_poster_per_notice_board']):
                            ad_inv = AdInventoryLocationMapping(adinventory_id = notice_tag+'PO'+str(i), adinventory_name = 'POSTER', location = nb_location)
                            ad_inv.save("Poster", society)

                    if notice_serializer.is_valid():
                        notice_serializer.save(tower=tower_data)

                    else:
                        #transaction.rollback()
                        return Response(notice_serializer.errors, status=400)

            if key['lift_details_available']:
                for index, lift in enumerate(key['lift_details'], start=1):
                    if 'id' in lift:
                        lift_item = LiftDetails.objects.get(pk=lift['id'])
                        lift_serializer = LiftDetailsSerializer(lift_item,data=lift)
                    else:
                        lift_serializer = LiftDetailsSerializer(data=lift)
                        #populate location and ad inventory table
                        lift_tag = generate_location_tag(tag_initial, 'lift', index)
                        lift_location = InventoryLocation(location_id = lift_tag, location_type='Lift')
                        lift_location.save()
                        ad_inv = AdInventoryLocationMapping(adinventory_id = lift_tag+'PO', adinventory_name = 'POSTER', location = lift_location)
                        ad_inv.save("Poster", society)

                    if lift_serializer.is_valid():
                        lift_serializer.save(tower=tower_data)


                    else:
                        return Response(lift_serializer.errors, status=400)

            if key['flat_details_available']:
                for index, flat in enumerate(key['flat_details'], start=1):
                    if 'id' in flat:
                        flat_item = SocietyFlat.objects.get(pk=flat['id'])
                        flat_serializer=SocietyFlatSerializer(flat_item,data=flat)
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
            item = SocietyTower.objects.get(pk=id)
        except SocietyTower.DoesNotExist:
            return Response(status=404)
        for key in ['lift', 'notice_board', 'flat']:
            fn_name = "get_" + key + "_list"
            func = getattr(item,fn_name)
            objects = func()
            for obj in objects:
                obj.delete()
        item.delete()
        return Response(status=204)





class StandeeBannerAPIView(APIView):
    def get(self, request, id, format=None):
        response = {}
        try:
            standees = SupplierTypeSociety.objects.get(pk=id).standees.all()
            serializer = StandeeInventorySerializer(standees, many=True)
            standee_available = get_availability(serializer.data)
            response['standee_available'] = standee_available
            response['standee_details'] = serializer.data

            banners = SupplierTypeSociety.objects.get(pk=id).banners.all()
            serializer = BannerInventorySerializer(banners, many=True)
            banner_available = get_availability(serializer.data)
            response['banner_available'] = banner_available
            response['banner_details'] = serializer.data

            return Response(response, status=200)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        except StandeeInventory.DoesNotExist:
            return Response(status=404)
        except BannerInventory.DoesNotExist:
            return  Response(status=404)

    def post(self, request, id, format=None):
        society=SupplierTypeSociety.objects.get(pk=id)

        if request.data['standee_available']:
            response = post_data(StandeeInventory, StandeeInventorySerializer, request.data['standee_details'], society)
            if response == False:
                return Response(status=400)

            for index, key in enumerate(request.data['standee_details'], start=1):
                if 'id' not in key:
                    #populate ad inventory tablelift_tag = generate_location_tag(tag_initial, 'lift', index)
                    #loc_tag = society.society_name.upper()[:3] + key['standee_location'].upper()[:3] +'SD' + str(index)
                    loc_tag = key['adinventory_id'].upper()[:18]
                    sd_location = InventoryLocation(location_id = loc_tag, location_type='Standee')
                    sd_location.save()

                    ad_inv = AdInventoryLocationMapping(adinventory_id = key['adinventory_id'], adinventory_name = 'STANDEE', location = sd_location)
                    ad_inv.save(key['type'], society)

        if request.data['banner_available']:
            response = post_data(BannerInventory, BannerInventorySerializer, request.data['banner_details'], society)
            if response == False:
                return Response(status=400)

            for index, key in enumerate(request.data['banner_details'], start=1):
                if 'id' not in key:
                    #populate ad inventory table
                    loc_tag = society.society_name.upper()[:3] + key['banner_location'].upper()[:3] +'BA' + str(index)
                    ba_location = InventoryLocation(location_id = loc_tag, location_type='Banner')
                    ba_location.save()
                    ad_inv = AdInventoryLocationMapping(adinventory_id = loc_tag, adinventory_name = 'BANNER', location = ba_location)
                    ad_inv.save(key['type'], society)

        return Response(status=201)


class StallAPIView(APIView):
    def get(self, request, id, format=None):
        response = {}
        try:
            stalls = SupplierTypeSociety.objects.get(pk=id).stalls.all()
            serializer = StallInventorySerializer(stalls, many=True)
            stalls_available = get_availability(serializer.data)
            response['stalls_available'] = stalls_available
            response['stall_details'] = serializer.data

            return Response(response, status=200)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        except StallInventory.DoesNotExist:
            return Response(status=404)


    def post(self, request, id, format=None):
        print request.data
        society=SupplierTypeSociety.objects.get(pk=id)

        if request.data['stalls_available']:
            response = post_data(StallInventory, StallInventorySerializer, request.data['stall_details'], society)
            if response == False:
                return Response(status=400)

            for index, key in enumerate(request.data['stall_details'], start=1):
                if 'id' not in key:
                    #populate ad inventory tablelift_tag = generate_location_tag(tag_initial, 'lift', index)
                    #loc_tag = society.society_name.upper()[:3] + key['stall_location'].upper()[:3] +'ST' + str(index)
                    loc_tag = key['adinventory_id'].upper()[:18]
                    st_location = InventoryLocation(location_id = loc_tag, location_type='Stall')
                    st_location.save()
                    ad_inv = AdInventoryLocationMapping(adinventory_id = key['adinventory_id'], adinventory_name = 'STALL', location = st_location)
                    ad_inv.save(key['type'], society)

        return Response(status=201)

class CarDisplayAPIView(APIView):
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
        print request.data
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

        return Response(serializer.data, status=201)



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

            response = {}
            response['events_count_per_year'] = count
            response['event_details_available'] = event_details_available
            response['event_details'] = serializer.data

            return Response(response, status=200)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        except Events.DoesNotExist:
            return Response(status=404)

    def post(self, request, id, format=None):
        print request.data
        society=SupplierTypeSociety.objects.get(pk=id)
        if request.data['event_details_available']:
            if request.data['events_count_per_year'] != len(request.data['event_details']):
                return Response({'message':'No of Events entered does not match event count'},status=400)

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
        print request.data
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

        if request.data['mail_box_available']:
            response = post_data(MailboxInfo, MailboxInfoSerializer, request.data['mail_box_details'], society)
            if response == False:
                return Response(status=400)

        if request.data['door_to_door_allowed']:
            response = post_data(DoorToDoorInfo, DoorToDoorInfoSerializer, request.data['door_to_door_details'], society)
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
        print request.data
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
            print serializer.errors
            return False
    return True



def get_availability(data):
     if len(data) > 0:
        return True
     else:
         return False
