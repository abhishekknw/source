from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from serializers import UISocietySerializer, UITowerSerializer
from v0.serializers import BannerInventorySerializer, CarDisplayInventorySerializer, CommunityHallInfoSerializer, DoorToDoorInfoSerializer, LiftDetailsSerializer, NoticeBoardDetailsSerializer, PosterInventorySerializer, SocietyFlatSerializer, StandeeInventorySerializer, SwimmingPoolInfoSerializer, WallInventorySerializer, UserInquirySerializer, CommonAreaDetailsSerializer, ContactDetailsSerializer, EventsSerializer, InventoryInfoSerializer, MailboxInfoSerializer, OperationsInfoSerializer, PoleInventorySerializer, PosterInventoryMappingSerializer, RatioDetailsSerializer, SignupSerializer, StallInventorySerializer, StreetFurnitureSerializer, SupplierInfoSerializer, SupplierTypeSocietySerializer, SocietyTowerSerializer
from v0.models import BannerInventory, CarDisplayInventory, CommunityHallInfo, DoorToDoorInfo, LiftDetails, NoticeBoardDetails, PosterInventory, SocietyFlat, StandeeInventory, SwimmingPoolInfo, WallInventory, UserInquiry, CommonAreaDetails, ContactDetails, Events, InventoryInfo, MailboxInfo, OperationsInfo, PoleInventory, PosterInventoryMapping, RatioDetails, Signup, StallInventory, StreetFurniture, SupplierInfo, SupplierTypeSociety, SocietyTower



class SocietyAPIView(APIView):
    def get(self, request, id, format=None):
        try:
            item = SupplierTypeSociety.objects.get(pk=id)
            serializer = UISocietySerializer(item)
            return Response(serializer.data)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)


class SocietyAPIListView(APIView):
    def post(self, request, format=None):
        print request.data
        item = SupplierTypeSociety.objects.filter(pk=request.data['supplier_id']).first()
        if item:
            serializer = SupplierTypeSocietySerializer(item,data=request.data)
        else:
            serializer = SupplierTypeSocietySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=400)
        #here we will start storing contacts
        if request.data and request.data['basic_contact_available']:
            for contact in request.data['basic_contacts']:
                contact_serializer = ContactDetailsSerializer(data=contact)
                if contact_serializer.is_valid():
                    contact_serializer.save(supplier_id=request.data['supplier_id'])

        if request.data and request.data['basic_reference_available']:
            for contact in request.data['basic_reference_contacts']:
                contact_serializer = ContactDetailsSerializer(data=contact)
                if contact_serializer.is_valid():
                    contact_serializer.save(supplier_id=request.data['supplier_id'])

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
        serializer={}
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

            print "testing tower"
            print tower_data


            if key['notice_board_details_available']:
                for notice_board in key['notice_board_details']:
                    if 'id' in notice_board:
                        notice_item = NoticeBoardDetails.objects.get(pk=notice_board['id'])
                        notice_serializer = NoticeBoardDetailsSerializer(notice_item, data=notice_board)
                    else:
                        notice_serializer = NoticeBoardDetailsSerializer(data=notice_board)

                    if notice_serializer.is_valid():
                        notice_serializer.save(tower=tower_data)
                    else:
                        #transaction.rollback()
                        return Response(notice_serializer.errors, status=400)

            if key['lift_details_available']:
                for lift in key['lift_details']:
                    if 'id' in lift:
                        lift_item = LiftDetails.objects.get(pk=lift['id'])
                        lift_serializer = LiftDetailsSerializer(lift_item,data=lift)
                    else:
                        lift_serializer = LiftDetailsSerializer(data=lift)

                    if lift_serializer.is_valid():
                        lift_serializer.save(tower=tower_data)
                    else:
                        return Response(lift_serializer.errors, status=400)

            if key['flat_details_available']:
                for flat in key['flat_details']:
                    if 'id' in flat:
                        flat_item = SocietyFlat.objects.get(pk=flat['id'])
                        flat_serializer=SocietyFlatSerializer(flat_item,data=flat)
                    else:
                        flat_serializer = SocietyFlatSerializer(data=flat)

                    if flat_serializer.is_valid():
                        flat_serializer.save(tower=tower_data)
                    else:
                        return Response(flat_serializer.errors, status=400)

        return Response(status=201)

        #here we will start storing contacts



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
        serializer={}
        society=SupplierTypeSociety.objects.get(pk=id)

        if request.data['event_details_available']:
            if request.data['events_count_per_year'] != len(request.data['event_details']):
                return Response({'message':'No of Events entered does not match event count'},status=400)

        for key in request.data['event_details']:
            if 'event_id' in key:
                print "test loop"
                item = Events.objects.get(pk=key['event_id'])
                serializer = EventsSerializer(item, data=key)
            else:
                serializer = EventsSerializer(data=key)
            try:
                if serializer.is_valid():
                    serializer.save(supplier=society)
            except:
                return Response(serializer.errors, status=400)




        return Response(serializer.data, status=201)
        #here we will start storing contacts
