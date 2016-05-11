from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from serializers import UIBusinessSerializer, CampaignListSerializer, CampaignInventorySerializer
from v0.serializers import CampaignSupplierTypesSerializer, SocietyInventoryBookingSerializer, CampaignSerializer, CampaignSocietyMappingSerializer, BusinessSerializer, BusinessContactSerializer, ImageMappingSerializer, InventoryLocationSerializer, AdInventoryLocationMappingSerializer, AdInventoryTypeSerializer, DurationTypeSerializer, PriceMappingDefaultSerializer, PriceMappingSerializer, BannerInventorySerializer, CarDisplayInventorySerializer, CommunityHallInfoSerializer, DoorToDoorInfoSerializer, LiftDetailsSerializer, NoticeBoardDetailsSerializer, PosterInventorySerializer, SocietyFlatSerializer, StandeeInventorySerializer, SwimmingPoolInfoSerializer, WallInventorySerializer, UserInquirySerializer, CommonAreaDetailsSerializer, ContactDetailsSerializer, EventsSerializer, InventoryInfoSerializer, MailboxInfoSerializer, OperationsInfoSerializer, PoleInventorySerializer, PosterInventoryMappingSerializer, RatioDetailsSerializer, SignupSerializer, StallInventorySerializer, StreetFurnitureSerializer, SupplierInfoSerializer, SportsInfraSerializer, SupplierTypeSocietySerializer, SocietyTowerSerializer
from v0.models import CampaignSupplierTypes, SocietyInventoryBooking, CampaignTypeMapping, Campaign, CampaignSocietyMapping, Business, BusinessContact, ImageMapping, InventoryLocation, AdInventoryLocationMapping, AdInventoryType, DurationType, PriceMappingDefault, PriceMapping, BannerInventory, CarDisplayInventory, CommunityHallInfo, DoorToDoorInfo, LiftDetails, NoticeBoardDetails, PosterInventory, SocietyFlat, StandeeInventory, SwimmingPoolInfo, WallInventory, UserInquiry, CommonAreaDetails, ContactDetails, Events, InventoryInfo, MailboxInfo, OperationsInfo, PoleInventory, PosterInventoryMapping, RatioDetails, Signup, StallInventory, StreetFurniture, SupplierInfo, SportsInfra, SupplierTypeSociety, SocietyTower
from django.db.models import Q
from django.db import transaction


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
            with transaction.atomic():
                if 'id' in business_data:
                    business = Business.objects.get(pk=business_data['id'])
                    serializer = BusinessSerializer(business,data=business_data)
                else:
                    #request.data['created_by'] = current_user.id
                    serializer = BusinessSerializer(data=business_data)

                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=400)

                business = Business.objects.get(pk=serializer.data['id'])

                #here we will start storing contacts
                #if 'contact' in business_data and business_data['contact']:
                for contact in business_data['contacts']:
                    if 'id' in contact:
                        item = BusinessContact.objects.get(pk=contact['id'])
                        contact_serializer = BusinessContactSerializer(item, data=contact)
                    else:
                        contact_serializer = BusinessContactSerializer(data=contact)
                    if contact_serializer.is_valid():
                        contact_serializer.save(business=business)
                    else:
                        return Response(contact_serializer.errors, status=400)

                if 'campaign_type' in request.data or 'supplier_type' in request.data:
                    campaign_data = {'booking_status':'Shortlisted'}
                    if 'tentative' in request.data:
                        for key in request.data['tentative']:
                            campaign_data[key] = request.data['tentative'][key]

                    campaign_serializer = CampaignSerializer(data=campaign_data)
                    if campaign_serializer.is_valid():
                        campaign_serializer.save(business=business)
                    else:
                        return Response(campaign_serializer.errors, status=400)

                    campaign = Campaign.objects.get(pk=campaign_serializer.data['id'])


                    if 'campaign_type' in request.data:
                        for key, value in request.data['campaign_type'].iteritems():
                            campaign_type_map = CampaignTypeMapping(campaign=campaign, type=key, sub_type=value)
                            campaign_type_map.save()

                    if 'suplier_type' in request.data:
                        for key, value in request.data['supplier_type'].iteritems():
                            supplier_type_map = CampaignSupplierTypes(campaign=campaign, supplier_type=key, count=value)
                            supplier_type_map.save()

                    return  Response(campaign_serializer.data, status=201)

            return Response(status=200)


class CampaignAPIView(APIView):

    def get(self, request, format=None):
        try:
            status = request.query_params.get('status', None)
            if status:
                items = Campaign.objects.filter(booking_status=status)
            else:
                items = Campaign.objects.all()
            serializer = CampaignListSerializer(items, many=True)
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



class CampaignInventoryAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            campaign = Campaign.objects.get(pk=id)
            campaign_serializer = CampaignListSerializer(campaign)
            items = campaign.societies.all().filter(booking_status__in=['Shortlisted','Requested', 'Finalized', 'Removed'])
            serializer = CampaignInventorySerializer(items, many=True)
            response={'inventories':serializer.data, 'campaign':campaign_serializer.data}
            return Response(response, status=200)
        except :
            return Response(status=404)

    def post(self, request, id, format=None):

        try:
            for society in request.data['inventory']:
                if 'id' in society:
                    campaign_society = CampaignSocietyMapping.objects.get(pk=society['id'])
                    serializer = CampaignSocietyMappingSerializer(campaign_society,data=society)
                else:
                    #request.data['created_by'] = current_user.id
                    serializer = CampaignSocietyMappingSerializer(data=society)

                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=400)

                for inv in society['inventories']:
                    if 'id' in inv:
                        society_inv = SocietyInventoryBooking.objects.get(pk=inv['id'])
                        serializer = SocietyInventoryBookingSerializer(society_inv,data=inv)
                    else:
                        serializer = SocietyInventoryBookingSerializer(data=inv)

                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return Response(serializer.errors, status=400)

            save_type = request.data['type']
            print save_type
            if save_type and save_type=='submit':
                campaign = Campaign.objects.get(pk=id)
                campaign.booking_status = 'Finalized'
                campaign.save()

            return Response(status=200)
        except:
            return Response(status=404)


    def delete(self, request, id, format=None):
        try:
            type = request.query_params.get('type', None)
            item = CampaignSocietyMapping.objects.get(pk=id)
        except CampaignSocietyMapping.DoesNotExist:
            return Response({'message':'Requested Inventory Does not Exist'}, status=404)

        if type and (type=='Permanent'):
            inventories = SocietyInventoryBooking.objects.filter(campaign=item.campaign, society=item.society)
            for key in inventories:
                key.delete()
            item.delete()
        elif type and (type=='Temporary'):
            item.booking_status = 'Removed'
            item.save()
        else:
            return Response({'message':'Specify a correct type/mode of deletion'}, status=400)

        return Response(status=200)


class ShortlistSocietyAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            campaign = Campaign.objects.get(pk=id)
            items = campaign.societies.all().filter(booking_status='Requested')
            serializer = FinalizeInventorySerializer(items, many=True)
            return Response(serializer.data, status=200)
        except :
            return Response(status=404)

    def post(self, request, format=None):

        print request.data
        if 'campaign_id' in request.data:
            try:
                campaign = Campaign.objects.get(pk=request.data['campaign_id'])
            except Campaign.DoesNotExist:
                return Response(status=404)
        else:
            return Response(status=400)

        if 'society_id' in request.data:
            try:
                society_id = request.data['society_id']
                society = SupplierTypeSociety.objects.get(pk=request.data['society_id'])
            except SupplierTypeSociety.DoesNotExist:
                return Response(status=404)
        else:
            return Response(status=400)

        campaign_society = CampaignSocietyMapping(campaign=campaign, society=society, booking_status='Shortlisted')
        campaign_society.save()

        for key in campaign.get_types():
            inventory = SocietyInventoryBooking(campaign=campaign, society=society, adinventory_type=key)
            inventory.save()

        return Response({"message": "Society Shortlisted", "id": society_id}, status=200)


class BookCampaignAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            status = request.query_params.get('status', None)
            if status:
                campaign = Campaign.objects.get(pk=id)
                campaign.booking_status = status
                campaign.save()

            return Response(status=200)
        except :
            return Response(status=404)


class FinalCampaignBookingAPIView(APIView):

    def get(self, request, id, format=None):

        try:
            campaign = Campaign.objects.get(pk=id)
            serializer = CampaignSerializer(campaign)
            return Response(serializer.data)
        except :
            return Response(status=404)

