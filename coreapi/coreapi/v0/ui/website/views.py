import math
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from serializers import UIBusinessInfoSerializer, CampaignListSerializer, CampaignInventorySerializer, UIAccountInfoSerializer
from v0.serializers import CampaignSupplierTypesSerializer, SocietyInventoryBookingSerializer, CampaignSerializer, CampaignSocietyMappingSerializer, BusinessInfoSerializer, BusinessAccountContactSerializer, ImageMappingSerializer, InventoryLocationSerializer, AdInventoryLocationMappingSerializer, AdInventoryTypeSerializer, DurationTypeSerializer, PriceMappingDefaultSerializer, PriceMappingSerializer, BannerInventorySerializer, CommunityHallInfoSerializer, DoorToDoorInfoSerializer, LiftDetailsSerializer, NoticeBoardDetailsSerializer, PosterInventorySerializer, SocietyFlatSerializer, StandeeInventorySerializer, SwimmingPoolInfoSerializer, WallInventorySerializer, UserInquirySerializer, CommonAreaDetailsSerializer, ContactDetailsSerializer, EventsSerializer, InventoryInfoSerializer, MailboxInfoSerializer, OperationsInfoSerializer, PoleInventorySerializer, PosterInventoryMappingSerializer, RatioDetailsSerializer, SignupSerializer, StallInventorySerializer, StreetFurnitureSerializer, SupplierInfoSerializer, SportsInfraSerializer, SupplierTypeSocietySerializer, SocietyTowerSerializer, BusinessTypesSerializer, BusinessSubTypesSerializer, AccountInfoSerializer,  CampaignTypeMappingSerializer
from v0.models import CampaignSupplierTypes, SocietyInventoryBooking, CampaignTypeMapping, Campaign, CampaignSocietyMapping, BusinessInfo, BusinessAccountContact, ImageMapping, InventoryLocation, AdInventoryLocationMapping, AdInventoryType, DurationType, PriceMappingDefault, PriceMapping, BannerInventory, CommunityHallInfo, DoorToDoorInfo, LiftDetails, NoticeBoardDetails, PosterInventory, SocietyFlat, StandeeInventory, SwimmingPoolInfo, WallInventory, UserInquiry, CommonAreaDetails, ContactDetails, Events, InventoryInfo, MailboxInfo, OperationsInfo, PoleInventory, PosterInventoryMapping, RatioDetails, Signup, StallInventory, StreetFurniture, SupplierInfo, SportsInfra, SupplierTypeSociety, SocietyTower, BusinessTypes, BusinessSubTypes, AccountInfo, InventorySummary
from django.db.models import Q
from django.db import transaction
from rest_framework import status
import json
from django.contrib.contenttypes.models import ContentType
from v0.models import SupplierTypeCorporate, ProposalInfo, ProposalCenterMapping,SpaceMapping , InventoryType, ShortlistedSpaces
from v0.ui.website.serializers import ProposalInfoSerializer, ProposalCenterMappingSerializer, SpaceMappingSerializer , \
        InventoryTypeSerializer, ShortlistedSpacesSerializer, ProposalSocietySerializer, ProposalCorporateSerializer



class getBusinessTypesAPIView(APIView):
    def get(self, request, format=None):
        print "inside get"
        try:
            busTypes = BusinessTypes.objects.all()

            serializer = BusinessTypesSerializer(busTypes, many=True)
            return Response(serializer.data, status=200)
        except :
            return Response(status=404)


class BusinessAPIListView(APIView):
    def get(self, request, format=None):
        try:
            items = BusinessInfo.objects.all()
            serializer = BusinessInfoSerializer(items, many=True)
            return Response(serializer.data, status=200)
        except :
            return Response(status=404)

    #the delete api is not being used
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


class getBusinessSubTypesAPIView(APIView):
    def get(self, request, id, format=None):
        try:
            items = BusinessSubTypes.objects.filter(business_type_id=id)
            serializer = BusinessSubTypesSerializer(items, many=True)

            return Response(serializer.data)
        except :
            return Response(status=404)


class BusinessAPIView(APIView):
    def get(self, request, id, format=None):
        try:
            item = BusinessInfo.objects.get(pk=id)
            serializer = UIBusinessInfoSerializer(item)
            return Response(serializer.data)
        except :
            return Response(status=404)

    # the delete api is not being used
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



class AccountAPIListView(APIView):
    def get(self, request, format=None):
        try:
            items = AccountInfo.objects.all()
            serializer = AccountInfoSerializer(items, many=True)
            return Response(serializer.data, status=200)
        except :
            return Response(status=404)


class AccountAPIView(APIView):
    def get(self, request, id, format=None):
        try:
            account = AccountInfo.objects.get(pk=id)
            serializer1 = UIAccountInfoSerializer(account)
            business = BusinessInfo.objects.get(pk=account.business_id)
            serializer2 = BusinessInfoSerializer(business)
            '''contacts = AccountContact.objects.filter(account=account)
            serializer3 = AccountContactSerializer(contacts, many=True)'''

            serializer = {'account':serializer1.data, 'business':serializer2.data}
            return Response(serializer, status=200)
        except :
            return Response(status=404)


class NewCampaignAPIView(APIView):
     def post(self, request, format=None):

            # print "\n\n\n  Request Data : "
            # print request.data
            # print "\n\n\n"

            current_user = request.user
            business_data = request.data['business']
            error = {}

            # checking if the business with the same name already exists in the database
            try:
                if 'id' not in business_data :
                    business = BusinessInfo.objects.get(name=business_data['name'])
                    error['message'] = 'Business with this name already exists'
                    error = json.dumps(error)
                    return Response(error, status = status.HTTP_406_NOT_ACCEPTABLE)
                # else:
                #     print "\n\nYeyyyy! found id in the business \n\n"
            except BusinessInfo.DoesNotExist:
                pass


            with transaction.atomic():
                if 'id' in business_data:
                    # print "\nInside if 1\n"
                    business = BusinessInfo.objects.get(pk=business_data['id'])
                    serializer = BusinessInfoSerializer(business,data=business_data)
                else:
                    # print "\nInside else 1\n"
                    #request.data['created_by'] = current_user.id
                    serializer = BusinessInfoSerializer(data=business_data)

                if serializer.is_valid():
                    # print "\n\n\n Business Serializer Validated Data"
                    # print serializer.validated_data
                    # print "\n\n\n"
                    try:
                        type_name = BusinessTypes.objects.get(id=int(business_data['type_name_id']))
                        sub_type = BusinessSubTypes.objects.get(id=int(business_data['sub_type_id']))
                        serializer.save(type_name=type_name, sub_type=sub_type)

                    except ValueError:
                        error['message'] = "Business Type/SubType Invalid"
                        error = json.dumps(error)
                        return Response(error, status=status.HTTP_406_NOT_ACCEPTABLE)

                else:
                    return Response(serializer.errors, status=400)


                business = BusinessInfo.objects.get(pk=serializer.data['id'])
                # print "\n\n\n***************************************"
                # print "Business Contacts : ", business_data['contacts'] 
                # print "***************************************\n\n\n"


                #here we will start storing contacts
                #if 'contact' in business_data and business_data['contact']:
                content_type_business = ContentType.objects.get_for_model(BusinessInfo)
                contact_ids = list(business.contacts.all().values_list('id',flat=True))
                for contact in business_data['contacts']:
                    
                    contact['object_id'] = business.id
                    contact['content_type'] = content_type_business.id

                    if 'id' in contact:
                        # print "\nInside if 2\n"
                        item = BusinessAccountContact.objects.get(pk=contact['id'])
                        if contact['spoc'] == '':
                            contact['spoc'] = item.spoc
                        contact_ids.remove(item.id)
                        contact_serializer = BusinessAccountContactSerializer(item, data=contact)
                    else:
                        if contact['spoc'] == '':
                            contact['spoc'] = 'false'
                        # print "\nInside else 2\n"
                        contact_serializer = BusinessAccountContactSerializer(data=contact)

                    contact_serializer.is_valid(raise_exception=True)

                    contact_serializer.save()
                
                # deleting all contacts whose id not received from the frontend
                BusinessAccountContact.objects.filter(id__in=contact_ids).delete()

                business_serializer = BusinessInfoSerializer(business)
                contacts = business.contacts.all()
                contacts_serializer = BusinessAccountContactSerializer(contacts, many=True)

                response = json.dumps({
                        'business' : business_serializer.data,
                        'contacts' : contacts_serializer.data,
                    })
            return Response(response,status=200)


class CreateCampaignAPIView(APIView):
    def post(self, request, format=None):
            response = {}
            current_user = request.user
            errro = {}

            # checking if the data received contains name of the account
            try : 
                account_data = request.data['account']
                account_name = account_data['name']
            except KeyError :
                # print "account object not found"
                error['message'] = 'Appropriate data not provided',
                error = json.dumps(error)
                return Response(error, status = status.HTTP_406_NOT_ACCEPTABLE)

            with transaction.atomic():
                
                # checking if the account with the same name already exists or not
                if 'id' not in account_data:
                    try:
                        acc = AccountInfo.objects.get(name=account_data['name'])
                        error['message'] =  'Business with this name already exists',
                        error = json.dumps(error)
                        return Response(error, status = status.HTTP_406_NOT_ACCEPTABLE)
                    except AccountInfo.DoesNotExist:
                        pass

                # checking if business id is integer
                try:
                    business_id = int(account_data['business_id'])
                except ValueError: 
                    error['message'] = "Imporper Business Type Id"
                    error = json.dumps(error)
                    return Response(error, status = status.HTTP_406_NOT_ACCEPTABLE)

                
                # checking a valid business
                try:
                    business = BusinessInfo.objects.get(id=business_id)
                except BusinessInfo.DoesNotExist:
                    error['message'] =  "Business Does Not Exist"
                    error = json.dumps(error)
                    return Response(error, status = status.HTTP_406_NOT_ACCEPTABLE)

                if 'id' in account_data:
                    account = AccountInfo.objects.get(pk=account_data['id'])
                    serializer = AccountInfoSerializer(account,data=account_data)
                else:
                    serializer = AccountInfoSerializer(data=account_data)

                if serializer.is_valid():
                    serializer.save(business=business)
                else:
                    return Response(serializer.errors, status=400)

                account_id = serializer.data['id']
                account = AccountInfo.objects.get(id=account_id)
            
                content_type_account = ContentType.objects.get_for_model(AccountInfo)

                # #here we will start storing contacts
                contact_ids = list(account.contacts.all().values_list('id',flat=True))

                
                for contact in account_data['contacts']:
                    contact['object_id'] = account.id
                    contact['content_type'] = content_type_account.id

                    if 'id' in contact:
                        item = BusinessAccountContact.objects.get(pk=contact['id'])
                        contact_ids.remove(item.id)
                        if contact['spoc'] == '':
                            contact['spoc'] = item.spoc
                        contact_serializer = BusinessAccountContactSerializer(item, data=contact)
                    else:
                        if contact['spoc'] == '':
                            contact['spoc'] = 'false'
                        contact_serializer = BusinessAccountContactSerializer(data=contact)
                    
                    if contact_serializer.is_valid():
                        contact_serializer.save()
                    else:
                        return Response(contact_serializer.errors, status=400)

                BusinessAccountContact.objects.filter(id__in=contact_ids).delete()

                # if 'campaign_type' in request.data or 'supplier_type' in request.data:
                #     campaign_data = {'booking_status':'Shortlisted'}
                #     if 'tentative' in request.data:
                #         for key in request.data['tentative']:
                #             campaign_data[key] = request.data['tentative'][key]

                #     campaign_serializer = CampaignSerializer(data=campaign_data)

                #     campaign_serializer.is_valid(raise_exception=True)
                #     campaign_serializer.save(account=account)
                    
                #     campaign = Campaign.objects.get(pk=campaign_serializer.data['id'])

                #     if 'campaign_type' in request.data:
                #         for key, value in request.data['campaign_type'].iteritems():
                #             campaign_type_map = CampaignTypeMapping(campaign=campaign, type=key, sub_type=value)

                #             campaign_type_map.save()

                #     if 'supplier_type' in request.data:
                #         for key, value in request.data['supplier_type'].iteritems():
                #             supplier_type_map = CampaignSupplierTypes(campaign=campaign, supplier_type=key, count=value)
                #             supplier_type_map.save()
                #             response['campaign'] = campaign_serializer.data

                #     # redirecting to societylist page if the campaign info received
                #     return  Response(campaign_serializer.data, status=201)

                
                # sending accounts and related contacts fields to allow updating 
                account = AccountInfo.objects.get(id=account_id)
                account_serializer = AccountInfoSerializer(account)
                contacts = account.contacts.all()
                contacts_serializer = BusinessAccountContactSerializer(contacts, many=True)
                response['account'] = account_serializer.data
                response['contacts'] = contacts_serializer.data
            return Response(response, status=200)






class CampaignAPIView(APIView):

    def get(self, request, format=None):
        try:
            status = request.query_params.get('status', None)
            if status:
                print status
                items = Campaign.objects.filter(booking_status=status)
            else:
                items = Campaign.objects.all()
            serializer = CampaignListSerializer(items, many=True)
            return Response(serializer.data)
        except :
            return Response(status=404)

    # the delete api is not being used
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


class ShortlistSocietyCountAPIView(APIView):
    # to get the number of shortlisted socities on societyDetailPage
    def get(self, request, id=None, format=None):
        try:
            campaign = Campaign.objects.get(pk=id)
            societies_count = CampaignSocietyMapping.objects.filter(campaign=campaign).count()
            return Response({'count': societies_count}, status=200)
        except Campaign.DoesNotExist:
            return Response({'error':'No such campaign id exists'},status=406)
        



class ShortlistSocietyAPIView(APIView):

    # discuss use of this get function no id in url
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

        try:
            print "Inside try"
            campaign_society = CampaignSocietyMapping.objects.get(campaign=campaign, society=society)
            total_societies = CampaignSocietyMapping.objects.filter(campaign=campaign).count()
            error = {"message" : "Already Shortlisted", 'count':total_societies}
            return Response(error, status=200)
        except CampaignSocietyMapping.DoesNotExist:
            campaign_society = CampaignSocietyMapping(campaign=campaign, society=society, booking_status='Shortlisted')
            campaign_society.save()
        # except CampaignSocietyMapping.MultipleObjectsReturned:
        #     total_societies = CampaignSocietyMapping.objects.filter(campaign=campaign).count() 
        #     error = {"message" : "Already Shortlisted", 'count':total_societies}
        #     return Response(error, status=200)

        for key in campaign.get_types():
            inventory = SocietyInventoryBooking(campaign=campaign, society=society, adinventory_type=key)
            inventory.save()

        total_societies = CampaignSocietyMapping.objects.filter(campaign=campaign).count() 
        return Response({"message": "Society Shortlisted", "id": society_id, 'count':total_societies}, status=200)


class CreateProposalAPIView(APIView):
    def get(self, request, id, format=None):
        try:
            campaign = Campaign.objects.get(pk=id)
            items = campaign.societies.filter(booking_status='Shortlisted')
            inv_types = campaign.types.all()

            response = []
            allowed = '_allowed'
            total = 'total_'
            count = '_count'
            price_dict = self.getPriceDict()
            for item in items:
                society_detail = {}     #List of society-related details required to be displayed
                society_id = item.society.supplier_id
                society_name = item.society.society_name
                society_detail['id'] = society_id
                society_detail['society_name'] = society_name
                society_detail['flat_count'] = item.society.flat_count
                society_detail['tower_count'] = item.society.tower_count
                society_detail['inventory'] = []
                inv_details = InventorySummary.objects.get(supplier_id=society_id)
                for inv in inv_types:
                    inv_name = inv.type
                    inv_size = inv.sub_type
                    #print inv_details.flier_allowed
                    #print inv_name.lower() + allowed
                    if (hasattr(inv_details, inv_name.lower() + allowed) and getattr(inv_details, inv_name.lower() + allowed)):
                        #print "has attribute"
                        if(inv_name == 'Flier'):
                            inv_count = 1
                        else:
                            inv_count = getattr(inv_details, total+inv_name.lower()+ count)
                        inv_info = {}       #List of inventory and its count details

                        # adinventory_type = models.ForeignKey('AdInventoryType', db_column='ADINVENTORY_TYPE_ID', blank=True, null=True, on_delete=models.CASCADE)
                        # supplier = models.ForeignKey('SupplierTypeSociety', db_column='SUPPLIER_ID', related_name='default_prices', blank=True, null=True, on_delete=models.CASCADE)
                        # duration_type = models.ForeignKey('DurationType', db_column='DURATION_ID', blank=True, null=True, on_delete=models.CASCADE)
                        duration_type = DurationType.objects.get(id=int(price_dict[inv_name]['duration']))
                        adinventory_type = AdInventoryType.objects.get(id=int(price_dict[inv_name]['types'][inv_size]))
                        price_obj = PriceMappingDefault.objects.get(supplier=item.society,duration_type=duration_type, adinventory_type=adinventory_type)
                        #print "price obj price is : " , price_obj.id
                        inv_price = price_obj.business_price
                        inv_info['count'] = str(inv_count)
                        inv_info['price'] = str(inv_price)
                        inv_info['type'] = inv_name
                        society_detail['inventory'].append(inv_info)

                response.append(society_detail)

            response = json.dumps(response)
            return Response(response, status=200)

        except :
            return Response(status=404)

    def getPriceDict(self):
        price_dict = {
            'Standee' : {
                            'duration': '1',
                            'types' : {
                                            'Small' : '3',
                                            'Medium' : '4',
                                            # 'Large'  : '5'
                                       }
                        },

            'Flier' : {
                            'duration' : '5',
                            'types' : {
                                        'Door-to-Door' : '12',
                                        'Mailbox' : '13',
                                      }
            },

            'Stall' : {
                            'duration': '5',
                            'types' : {
                                            'Canopy' : '6',
                                            'Small' : '7',
                                            'Large'  : '8',
                                            # 'Customize' : '9'
                                       }
            },
        }

        return price_dict

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

        return Response({"message": "Campaign Booked Successfully"}, status=200)




class CreateInitialProposalAPIView(APIView):
    '''This API creates initial proposal when the user enters the center(address, name etc.) and basic proposal 
    fields are stored in the database
    ProposalInfo and ProposalCenterMapping models are used only'''

    def post(self, request, id, format=None):
        proposal_data = request.data
        proposal_data['proposal_id'] = self.create_proposal_id()
        proposal_serializer = ProposalInfoSerializer(data=proposal_data)

        if proposal_serializer.is_valid():
            proposal_object = proposal_serializer.save()
        else:
            return Response({'message' : 'Invalid Proposal Data', 'errors' : proposal_serializer.errors}, status=406)


        for center in proposal_data['centers']:
            center['proposal'] = proposal_object.proposal_id
            center_serializer = ProposalCenterMappingSerializer(data=center)

            if serializer.is_valid():
                center_serializer.save()
            else:
                return Response({'message':'Invalid Center Info', 'errors' : center_serializer.errors}, status=406)



    def create_proposal_id(self):
        return "Proposal1"


class SpacesOnCenterAPIView(APIView):
    def get(self,request,id=None, format=None):
        ''' This function filters all the spaces(Societies, Corporates etc.) based on the center and
        radius provided currently considering radius as the half of side of square
        This API is called before map view page is loaded'''

        # try:
        #     proposal = ProposalInfo.objects.get(proposal_id=id)
        # except ProposalInfo.DoesNotExist:
        #     return Response({'message' : 'Invalid Proposal ID sent'}, status=406)

        # proposal_centers = ProposalCenterMapping.objects.filter(proposal=proposal)
        # centers_data_list = []

        # for proposal_center in proposal_centers:

        #     delta_latitude = proposal_center.radius/ 110.574
        #     min_latitude = proposal_center.latitude - delta_latitude
        #     max_latitude = proposal_center.latitude + delta_latitude

        #     delta_longitude = proposal_center.radius/(111.320 * cos(math.radians(latitude)))
        #     min_longitude = proposal_center.longitude - delta_longitude
        #     max_longitude = proposal_center.longitude + delta_longitude

        #     societies = SupplierTypeSociety.objects.filter(Q(latitude__lt=max_latitude) & Q(latitude__gt=min_latitude) & Q(longitude__lt=max_longitude) & Q(longitude__gt=min_longitude))
        #     corporates = SupplierTypeCorporate.objects.filter(Q(latitude__lt=max_latitude) & Q(latitude__gt=min_latitude) & Q(longitude__lt=max_longitude) & Q(longitude__gt=min_longitude))

        #     societies_count = societies.count()
        #     corporates_count = corporates.count()

        #     proposal_center_serializer = ProposalCenterMappingSerializer(proposal_center)
        #     societies_serializer =  ProposalSocietySerializer(societies, many=True)
        #     corporates_serializer = ProposalCorporateSerializer(corporates, many=True)  
        #     centers_data_list.append({
        #         'center' : proposal_center_serializer.data,
        #         'societies' : societies_serializer.data,
        #         'corporates' : corporates_serializer.data,
        #         'societies_count' : societies_count,
        #         'corporates_count' : corporates_count,
        #     })

        # return Response(centers_data_list, status=200)

        min_latitude = 19.12
        max_latitude = 19.34

        min_longitude = 73.45
        max_longitude = 73.65

        societies = SupplierTypeSociety.objects.filter(Q(latitude__lt=max_latitude) & Q(latitude__gt=min_latitude) & Q(longitude__lt=max_longitude) & Q(longitude__gt=min_longitude))
        corporates = SupplierTypeCorporate.objects.filter(Q(latitude__lt=max_latitude) & Q(latitude__gt=min_latitude) & Q(longitude__lt=max_longitude) & Q(longitude__gt=min_longitude))

        societies_count = societies.count()
        corporates_count = corporates.count()

        societies_serializer =  ProposalSocietySerializer(societies, many=True)
        corporates_serializer = ProposalCorporateSerializer(corporates, many=True)  

        response = {
            'societies' : societies_serializer.data,
            'corporates' : corporates_serializer.data,
            'societies_count' : societies_count,
            'corporates_count' : corporates_count,
        }

        return Response(response, status=200)


    def post(self,request,id=None,format=None):
        societies = SupplierTypeSociety.objects.all()
        society_serializer = SupplierTypeSocietySerializer(societies,many=True)
        societies_count = societies.count()
        response = {
            'societies' : society_serializer.data,
            'societies_count' : societies_count
        }

        return Response(response,status=200)



class GetSpaceInfoAPIView(APIView):
    ''' This API is to fetch the space(society,corporate, gym) etc. using its supplier Code
    e.g. RS for residential Society 

    Currently only working for societies '''
    def get(self, request, id , format=None):
        try:
            '''  On introducing new spaces we have to use if conditions to check the supplier code 
            like RS for society and the fetch society object
            e.g. if supplier_code == 'RS':
                      society = SupplierTypeSociety.objects.get(supplier_id=id)'''

            society = SupplierTypeSociety.objects.get(supplier_id=id)
            serializer = SupplierTypeSocietySerializer(society)
            return Response(serializer.data, status=200)
        except SupplierTypeSociety.DoesNotExist:
            return Response({'message' : 'No society Exists'}, status=406)


class GetFilteredSocietiesAPIView(APIView):

    def get(self, request, id, format=None):
        ''' This API gives societies based on different filters from mapView and gridView Page
        Currently implemented filters are locality and location (Standard, Medium High etc.)
        flat_count (100 - 250 etc.) flat_type(1BHK, 2BHK etc.) '''

        location_params = request.query_params.get('loc',None)
        locality_params = request.query_params.get('qlt',None)
        flat_count = request.query_params.get('flc',None)
        flat_type_params = reqeust.query_params.get('room',None)
        latitude_params = request.query_params.get('lat', None)
        longitude_params = request.query_params.get('lng',None)
        inventory_params = request.query_params.get('inv',None)

        q = Q()
        quality_dict = get_related_dict()
        flat_type_dict = {
            '1R' : '1 RK',      '1B' : '1 BHK',     '1-5B' : '1.5 BHK',     '2B' : '2 BHK',
            '2-5B' : '2.5 BHK',    '3B' : '3 BHK',  '3-5B' : '3.5 BHK',     '4B' : '4 BHK',
            '5B' : '5 BHK',         'PH' : 'PENT HOUSE',    'RH' : 'ROW HOUSE',  'DP' : 'DUPLEX' 
        }


        if not latitude_params and not longitude_params:
            return Response({'message' : 'Please Provide longitude and latitude values as well'}, status=406)

        if latitude_params:
            latitude_params = latitude_params.split()
            if len(latitude_params) == 2:
                min_latitude = latitude_params[0]
                max_latitude = latitude_params[1]

                q &= Q(latitude__lt=max_latitude) & Q(latitude__gt=min_latitude)
            else : 
                return Response({'message' : 'Please Provide proper latitude values'}, status=406)

        if longitude_params:
            longitude_params = longitude_params.split()
            if len(longitude_params) == 2 :
                min_longitude = longitude_params[0]
                max_longitude = longitude_params[1]

                q &= Q(longitude__lt=max_longitude) & Q(longitude__gt=min_longitude)
            else :
                return Response({'message' : 'Please Provide proper longitude values'}, status=406)

        if flat_type_params:
            flat_types = []
            flat_type_params = flat_type_params.split()
            for param in flat_type_params:
                try:
                    flat_types.append(quality_dict[param])
                except KeyError:
                    pass

            if flat_types:
                ''' We can improve performance here  by appending .distinct('society_id') when using postgresql ''' 
                society_ids = set(FlatType.objects.filter(flat_type__in=flat_types).values_list('society_id',flat=True))
                q &= Q(supplier_id__in=society_ids)

        if location_params:
            location_ratings = []
            location_params = location_params.split()
            for param in location_params:
                try:
                    location_ratings.append(quality_dict[param])
                except KeyError:
                    pass
            if locality_params:
                q &= Q(location_type__in=location_ratings)

        if locality_params:
            locality_ratings = []
            locality_params = locality_params.split()
            for param in locality_params:
                try:
                    locality_ratings.append(quality_dict[param])
                except KeyError:
                    pass

            if locality_ratings:
                q &= Q(locality__in=locality_ratings)

        if flat_count:
            flat_count = flat_count.split()
            if len(flat_count) == 2:
                flat_min = flat_count[0]
                flat_max = flat_count[1]

                q &= Q(flat_count__gte=flat_min) & Q(flat_count__lte=flat_max)


        if inventory_params:
            inventory_parmas = inventory_parmas.split()
            for param in inventory_parmas:
                if param == 'PO': # PO --> Poster
                    q &= Q(poster_allowed=True)
                elif param == 'ST': # ST --> Standee
                    q &= Q(standee_allowed=True)
                elif param == 'SL': # SL --> Stall 
                    q &= Q(stall_allowed=True)
                elif param == 'FL': # FL --> Flier
                    q &= Q(flier_allowed = True) 
                elif parma == 'CD': # CD --> Car Display
                    q &= Q(car_display_allowed=True)
                elif param == 'BA': # BA --> Banner
                    # Banner is currently not tracked in the website
                    # when tracked replace pass by --> q &= Q(banner_allowed=True)
                    pass 
        

        societies = SupplierTypeSociety.objects.filter(q)
        society_serializer = ProposalSocietySerializer(societies, many=True)

        return Response(society_serializer.data, status=200)


    def post(self, request, format=None):
        ''' This API is for deep filtering 
        Basic Idea is that if filter is chosen on the left of the map view page get request is fired
        But if he clicks on deep filters he can choose on almost anything like cars_count, luxury_cars_count,
        avg_pg_occupancy, women_occupants, etc. whatever required. This is the approach most commonly found on
        other websites '''
        pass



def get_related_dict():
    # inv_dict = {
    #     'PO' : 'Poster',    'ST' : 'Standee',   'SL' : 'Stall',
    #     'FL' : 'Flier'
    # }
    quality_dict = {
        'UH' : 'Ultra High',    'HH' : 'High',
        'MH' : 'Medium High',   'ST' : 'Standard'    
    }

    return quality_dict




class CreateProposalAPIView(APIView):

    def get(self,request, format=None):
        ''' This API creates/update the proposal related to a particular account
        Currently Versioning of Proposals is not done
        Tables for versioning are still to be made'''
        from datetime import datetime
        proposal = {
            'proposal_id' : 'BUSACCP01',
            'account_id' : '2',
            'name' : 'Sample Proposal',
            'tentative_cost' : '50000',
            'tentative_start_date' : datetime.now(),
            'tentative_end_date' : datetime.now(),
            'centers' : [{
                'center_name' : 'Oxford Chambers',
                'Address' : '',
                'latitude' : 19.119128, 
                'longitude' : 72.890795,
                'radius' : 3.5,
                'area' : 'Powai',
                'subarea' : 'Hiranandani Gardens',
                'city'    : 'Mumbai',
                'pincode' : '400072',

                'space_mappings' : [
                    {
                        'space_name' : 'society',
                        'space_count' : '10',
                        'buffer_space_count' : '5',
                        'spaces' : [
                            {  'object_id' : 'S1'},
                            {  'object_id' : 'S2'},
                            {  'object_id' : 'S3'},
                            {  'object_id' : 'S4'},
                        ],

                        'inventories' : [
                            {
                                'inventory_name' : 'POSTER',
                                'inventory_type' : 'A3',
                            },
                            {
                                'inventory_name' : 'POSTER LIFT',
                                'inventory_type' : 'A3',
                            },
                            {
                                'inventory_name' : 'STANDEE',
                                'inventory_type' : 'MEDIUM',
                            },
                        ],
                    },

                    {
                        'space_name' : 'Corporate',
                        'space_count' : '14',
                        'buffer_space_count' : '4',
                        'spaces' : [
                            {'object_id' : 'CP1'},
                            {'object_id' : 'CP2'},
                            {'object_id' : 'CP3'},
                        ],

                        'inventories' : [
                            {
                                'inventory_name' : 'POSTER',
                                'inventory_type' : 'A3',
                            },
                            {
                                'inventory_name' : 'POSTER LIFT',
                                'inventory_type' : 'A3',
                            },
                            {
                                'inventory_name' : 'STANDEE',
                                'inventory_type' : 'MEDIUM',
                            },
                        ],
                    },
                ],

            }],
        }

        with transaction.atomic():
            proposal['account'] = proposal['account_id']

            try:
                proposal_object = ProposalInfo.objects.get(proposal_id = proposal['proposal_id'])
                proposal_serializer = ProposalInfoSerializer(proposal_object,data=proposal)
            except ProposalInfo.DoesNotExist:
                proposal_serializer = ProposalInfoSerializer(data=proposal)

            if proposal_serializer.is_valid():
                proposal_object = proposal_serializer.save()
            else: 
                return Response({'message' : 'Proposal Serializer Invalid', \
                    'errors' : proposal_serializer.errors}, status=406)
            

            centers = proposal['centers']

            space_mappings_superset = set()
            inventory_type_superset = set()
            spaces_superset = set()
            centers_superset  = set(proposal_object.get_centers().values_list('id',flat=True))
            
            for center in centers:
                center['proposal'] = proposal_object.proposal_id

                if 'id' in center:
                    center_object = ProposalCenterMapping.objects.get(id=center['id'])
                    centers_superset.remove(center_object.id)
                    center_serializer = ProposalCenterMappingSerializer(center_object ,data=center)
                else:
                    center_serializer = ProposalCenterMappingSerializer(data=center)

                if center_serializer.is_valid():
                    center_object = center_serializer.save()
                else:
                    return Response({'message' : 'Center Serializer Invalid',\
                        'errors' : center_serializer.errors}, status=406)

                

                space_mappings = center['space_mappings']
                space_mappings_set = set(SpaceMapping.objects.filter(center=center_object).values_list('id',flat=True))

                for space_mapping in space_mappings:

                    content_model = "SupplierType" + space_mapping['space_name'].title() 
                    content_type = ContentType.objects.get(model=content_model)


                    space_mapping['proposal'] = proposal_object.proposal_id
                    space_mapping['center'] = center_object.id
                    space_mapping['inventory_type_count'] = len(space_mapping['inventories'])

                    if 'id' in space_mapping:
                        space_mapping_object = SpaceMapping.objects.get(id=space_mapping['id'])
                        space_mappings_set.remove(space_mapping_object.id)
                        space_mapping_serializer = SpaceMappingSerializer(space_mapping_object,data=space_mapping)
                    else:    
                        space_mapping_serializer = SpaceMappingSerializer(data=space_mapping)

                    if space_mapping_serializer.is_valid():
                        space_mapping_object = space_mapping_serializer.save()
                    else :
                        return Response({'message' : 'Invalid Space Mapping Received',\
                            'errors' : space_mapping_serializer.errors}, status=406)


                    
                    inventories = space_mapping['inventories']
                    inventory_type_set = set(InventoryType.objects.filter(space_mapping=space_mapping_object).values_list('id',flat=True))
                    for inventory in inventories:
                        inventory['space_mapping'] = space_mapping_object.id

                        if 'id' in inventory:
                            inventory_type_object = InventoryType.objects.get(id=inventory['id'])
                            inventory_type_set.remove(inventory_type_object.id)
                            inventory_serializer = InventoryTypeSerializer(inventory_type_object, data=inventory)
                        else:
                            inventory_serializer = InventoryTypeSerializer(data=inventory)

                        if inventory_serializer.is_valid():
                            inventory_serializer.save()
                        else:
                            return Response({'message' : 'Invalid Inventory Received',\
                                'errors' : inventory_serializer.errors} , status=406 )

                    inventory_type_superset = inventory_type_superset.union(inventory_type_set)

                    
                    spaces = space_mapping['spaces']
                    spaces_set = set(ShortlistedSpaces.objects.filter(space_mapping=space_mapping_object).values_list('id',flat=True))
                    
                    for space in spaces:
                        if not 'buffer_status' in space:
                            space['buffer_status'] = 'false' 
                        print space

                        space['content_type'] = content_type.id
                        space['space_mapping'] = space_mapping_object.id

                        if 'id' in space:
                            space_object = ShortlistedSpaces.objects.get(id=space['id'])
                            spaces_set.remove(space_object.id)
                            space_serializer = ShortlistedSpacesSerializer(space_object, data=space)
                        else:
                            space_serializer = ShortlistedSpacesSerializer(data=space)

                        if space_serializer.is_valid():
                            space_serializer.save()
                        else:
                            return Response({'message' : 'Invalid Space Received',\
                                'errros' : space_serializer.errors}, status=406)
            
                    spaces_superset = spaces_superset.union(spaces_set)

                space_mappings_superset = space_mappings_superset.union(space_mappings_set)
            

            ProposalCenterMapping.objects.filter(id__in=centers_superset).delete()            
            SpaceMapping.objects.filter(id__in=space_mappings_superset).delete()
            InventoryType.objects.filter(id__in=inventory_type_superset).delete()
            ShortlistedSpaces.objects.filter(id__in=spaces_superset).delete()

        return Response(status=200)



# 19.119128, 72.890795

# class CorporateCompanyDetails(models.Model):
#    id = models.AutoField(db_column='ID', primary_key=True)
#    company_id = models.ForeignKey('CorporateParkCompanyList', db_column='COMPANY_ID', related_name='companydetails', blank=True, null=True, on_delete=models.CASCADE)
#    building_id = models.ForeignKey('CorporateBuilding', db_column='BUILDING_NAME', related_name='companybuilding', blank=True, null=True, on_delete=models.CASCADE)
#    wing_id = models.ForeignKey('CorporateBuildingWing', db_column='WING_ID', related_name='companybuildingwing', blank=True, null=True, on_delete=models.CASCADE)    

# class CompanyFloor(models.Model):
#    company_details_id = models.ForeignKey('CorporateCompanyDetails',db_column='COMPANY_DETAILS_ID',related_name='wingfloor', blank=True, null=True, on_delete=models.CASCADE)
#    floor_number = models.IntegerField(db_column='FLOOR_NUMBER', blank=True, null=True)

# class CorporateParkCompanyList(models.Model):
#    id = models.AutoField(db_column='ID', primary_key=True)
#    name = models.CharField(db_column='COMPANY_NAME',max_length='50', blank=True, null=True)
#    supplier_id = models.ForeignKey('SupplierTypeCorporate', db_column='CORPORATEPARK_ID', related_name='corporatecompany', blank=True, null=True, on_delete=models.CASCADE)

# def post(self, request,format=None):
#     companies = request.data
#     for company in companies:
#         for builiding_key in comapn['details']:
#             builiding_key['company_id'] = company['company_id']
#             try:    
#                 detail_id = building_key['id']
#                 company_details = CorporateCompanyDetails.objects.get(id=detail_id)
#                 company_detail_serializer = CorporateCompanyDetailsSerializer(company_details, data=building_key)
#             except KeyError:    
#                 company_detail_serializer = CorporateCompanyDetailsSerializer(data=building_key)

#             if company_detail_serializer.is_valid():
#                 company_detail = company_detail_serializer.save()
#             else:
#                 return Response({'message' : 'Invalid Company Details Serializer' \
#                     'errors' : company_detail_serializer.errors}, status=406)



#             corporate = SupplierTypeCorporate.objects.get(supplier_id=id)
#             company_instance = CorporateParkCompanyList.objects.filter(corporate_id=corporate)