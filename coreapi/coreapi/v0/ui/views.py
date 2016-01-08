from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from serializers import UISocietySerializer, UITowerSerializer
from v0.serializers import MasterBannerInventorySerializer, MasterCarDisplayInventorySerializer, MasterCommunityHallInfoSerializer, MasterDoorToDoorInfoSerializer, MasterLiftDetailsSerializer, MasterNoticeBoardDetailsSerializer, MasterPosterInventorySerializer, MasterSocietyFlatSerializer, MasterStandeeInventorySerializer, MasterSwimmingPoolInfoSerializer, MasterWallInventorySerializer, UserInquirySerializer, CommonAreaDetailsSerializer, MasterContactDetailsSerializer, MasterEventsSerializer, MasterInventoryInfoSerializer, MasterMailboxInfoSerializer, MasterOperationsInfoSerializer, MasterPoleInventorySerializer, MasterPosterInventoryMappingSerializer, MasterRatioDetailsSerializer, MasterSignupSerializer, MasterStallInventorySerializer, MasterStreetFurnitureSerializer, MasterSupplierInfoSerializer, MasterSupplierTypeSocietySerializer, MasterSupplierTypeSocietyTowerSerializer
from v0.models import MasterBannerInventory, MasterCarDisplayInventory, MasterCommunityHallInfo, MasterDoorToDoorInfo, MasterLiftDetails, MasterNoticeBoardDetails, MasterPosterInventory, MasterSocietyFlat, MasterStandeeInventory, MasterSwimmingPoolInfo, MasterWallInventory, UserInquiry, CommonAreaDetails, MasterContactDetails, MasterEvents, MasterInventoryInfo, MasterMailboxInfo, MasterOperationsInfo, MasterPoleInventory, MasterPosterInventoryMapping, MasterRatioDetails, MasterSignup, MasterStallInventory, MasterStreetFurniture, MasterSupplierInfo, MasterSupplierTypeSociety, MasterSupplierTypeSocietyTower



class SocietyAPIView(APIView):
    def get(self, request, id, format=None):
        try:
            item = MasterSupplierTypeSociety.objects.get(pk=id)
            serializer = UISocietySerializer(item)
            return Response(serializer.data)
        except MasterSupplierTypeSociety.DoesNotExist:
            return Response(status=404)


class SocietyAPIListView(APIView):
    def post(self, request, format=None):
        print request.data
        item = MasterSupplierTypeSociety.objects.filter(pk=request.data['supplier_id']).first()
        if item:
            serializer = MasterSupplierTypeSocietySerializer(item,data=request.data)
        else:
            serializer = MasterSupplierTypeSocietySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=400)
        #here we will start storing contacts
        if request.data and request.data['basic_contact_available']:
            for contact in request.data['basic_contacts']:
                contact_serializer = MasterContactDetailsSerializer(data=contact)
                if contact_serializer.is_valid():
                    contact_serializer.save(supplier_id=request.data['supplier_id'])

        if request.data and request.data['basic_reference_available']:
            for contact in request.data['basic_reference_contacts']:
                contact_serializer = MasterContactDetailsSerializer(data=contact)
                if contact_serializer.is_valid():
                    contact_serializer.save(supplier_id=request.data['supplier_id'])

        return Response(serializer.data, status=201)


class TowerAPIView(APIView):
    def get(self, request, id, format=None):
        try:
            towers = MasterSupplierTypeSociety.objects.get(pk=id).towers.all()
            serializer = UITowerSerializer(towers, many=True)
            return Response(serializer.data)
        except MasterSupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        except MasterSupplierTypeSocietyTower.DoesNotExist:
            return Response(status=404)

    def post(self, request, id, format=None):
        print request.data
        serializer={}
        society=MasterSupplierTypeSociety.objects.get(pk=id)
        for key in request.data['TowerDetails']:
            if 'tower_id' in key:
                item = MasterSupplierTypeSocietyTower.objects.get(pk=key['tower_id'])
                serializer = MasterSupplierTypeSocietyTowerSerializer(item, data=key)
            else:
                serializer = MasterSupplierTypeSocietyTowerSerializer(data=key)
            try:
                if serializer.is_valid():
                    serializer.save(supplier=society)
                    print serializer.data
                    tower_data=serializer.data
            except:
                return Response(serializer.errors, status=400)

            try:
                tower = MasterSupplierTypeSocietyTower.objects.get(pk=tower_data['tower_id'])
            except MasterSupplierTypeSocietyTower.DoesNotExist:
                return Response(status=404)


            if key['notice_board_details_available']:
                for notice_board in key['notice_board_details']:
                    notice_serializer = MasterNoticeBoardDetailsSerializer(data=notice_board)

                    if notice_serializer.is_valid():
                        notice_serializer.save(tower=tower)
                    else:
                        #transaction.rollback()
                        return Response(notice_serializer.errors, status=400)

            if key['lift_details_available']:
                for lift in key['lift_details']:
                    lift_serializer = MasterLiftDetailsSerializer(data=lift)
                    if lift_serializer.is_valid():
                        lift_serializer.save(tower=tower)
                    else:
                        return Response(lift_serializer.errors, status=400)

            if key['flat_details_available']:
                for flat in key['flat_details']:
                    flat_serializer = MasterSocietyFlatSerializer(data=flat)
                    if flat_serializer.is_valid():
                        try:
                            flat_serializer.save(tower=tower)
                        except:
                             return Response(flat_serializer.errors, status=400)

                    else:
                        return Response(flat_serializer.errors, status=400)

        return Response(status=201)
        #here we will start storing contacts



class EventAPIView(APIView):
    def get(self, request, id, format=None):
        try:
            events = MasterSupplierTypeSociety.objects.get(pk=id).events.all()
            serializer = MasterEventsSerializer(events, many=True)
            return Response(serializer.data)
        except MasterSupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        except MasterEvents.DoesNotExist:
            return Response(status=404)

    def post(self, request, id, format=None):
        print request.data
        serializer={}
        society=MasterSupplierTypeSociety.objects.get(pk=id)
        for key in request.data['event_details']:
            if 'event_id' in key:
                print "test loop"
                item = MasterEvents.objects.get(pk=key['event_id'])
                serializer = MasterEventsSerializer(item, data=key)
            else:
                serializer = MasterEventsSerializer(data=key)
            try:
                if serializer.is_valid():
                    serializer.save(supplier=society)
                    print serializer.data
            except:
                return Response(serializer.errors, status=400)




        return Response(serializer.data, status=201)
        #here we will start storing contacts
