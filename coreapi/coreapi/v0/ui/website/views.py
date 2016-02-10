from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from serializers import UIBusinessSerializer
from v0.serializers import CampaignSerializer, BusinessSerializer, BusinessContactSerializer, ImageMappingSerializer, InventoryLocationSerializer, AdInventoryLocationMappingSerializer, AdInventoryTypeSerializer, DurationTypeSerializer, PriceMappingDefaultSerializer, PriceMappingSerializer, BannerInventorySerializer, CarDisplayInventorySerializer, CommunityHallInfoSerializer, DoorToDoorInfoSerializer, LiftDetailsSerializer, NoticeBoardDetailsSerializer, PosterInventorySerializer, SocietyFlatSerializer, StandeeInventorySerializer, SwimmingPoolInfoSerializer, WallInventorySerializer, UserInquirySerializer, CommonAreaDetailsSerializer, ContactDetailsSerializer, EventsSerializer, InventoryInfoSerializer, MailboxInfoSerializer, OperationsInfoSerializer, PoleInventorySerializer, PosterInventoryMappingSerializer, RatioDetailsSerializer, SignupSerializer, StallInventorySerializer, StreetFurnitureSerializer, SupplierInfoSerializer, SportsInfraSerializer, SupplierTypeSocietySerializer, SocietyTowerSerializer
from v0.models import CampaignTypeMapping, Campaign, Business, BusinessContact, ImageMapping, InventoryLocation, AdInventoryLocationMapping, AdInventoryType, DurationType, PriceMappingDefault, PriceMapping, BannerInventory, CarDisplayInventory, CommunityHallInfo, DoorToDoorInfo, LiftDetails, NoticeBoardDetails, PosterInventory, SocietyFlat, StandeeInventory, SwimmingPoolInfo, WallInventory, UserInquiry, CommonAreaDetails, ContactDetails, Events, InventoryInfo, MailboxInfo, OperationsInfo, PoleInventory, PosterInventoryMapping, RatioDetails, Signup, StallInventory, StreetFurniture, SupplierInfo, SportsInfra, SupplierTypeSociety, SocietyTower
from django.db.models import Q


class BusinessAPIListView(APIView):
    def get(self, request, format=None):
        try:
            items = Business.objects.all()
            serializer = BusinessSerializer(items, many=True)
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



class BusinessAPIView(APIView):
    def get(self, request, id, format=None):
        try:
            item = Business.objects.get(pk=id)
            serializer = UIBusinessSerializer(item)
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


class NewCampaignAPIView(APIView):

    def post(self, request, format=None):

        print request.data
        #current_user = request.user

        business_data = request.data['business']
        if 'id' in business_data:
            business = Business.objects.get(pk=business_data['id'])
            serializer = BusinessSerializer(business,data=request.data)
        else:
            #request.data['created_by'] = current_user.id
            serializer = BusinessSerializer(data=business_data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=400)

        business = Business.objects.get(pk=serializer.data['id'])

        #here we will start storing contacts
        if business_data['contact']:
            if 'id' in business_data['contact']:
                item = BusinessContact.objects.get(pk=business_data['contact']['id'])
                contact_serializer = BusinessContactSerializer(item, data=business_data['contact'])
            else:
                contact_serializer = BusinessContactSerializer(data=business_data['contact'])
            if contact_serializer.is_valid():
                contact_serializer.save(business=business)
            else:
                return Response(contact_serializer.errors, status=400)

        if 'campaign_cost' in request.data:
            campaign = Campaign(booking_status='Shortlisted', business=business, tentative_cost=request.data['campaign_cost'])
        else:
            campaign = Campaign(booking_status='Shortlisted', business=business)
        campaign.save()

        if request.data['campaign_type']:
            for key, value in request.data['campaign_type'].iteritems():
                campaign_type_map = CampaignTypeMapping(campaign=campaign, type=key, sub_type=value)
                campaign_type_map.save()


        return  Response(serializer.data, status=201)


