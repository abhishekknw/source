from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from serializers import UISocietySerializer
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
