import math, random, string, operator
#import tablib
import csv
import json
import datetime

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.urlresolvers import reverse
from django.db.models import Q, Sum
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from pygeocoder import Geocoder, GeocoderError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route,list_route
from openpyxl import Workbook
from openpyxl.compat import range
import requests
from rest_framework.parsers import JSONParser, FormParser
#from import_export import resources

import openpyxl
from serializers import UIBusinessInfoSerializer, CampaignListSerializer, CampaignInventorySerializer, UIAccountInfoSerializer
from v0.serializers import CampaignSupplierTypesSerializer, SocietyInventoryBookingSerializer, CampaignSerializer, CampaignSocietyMappingSerializer, BusinessInfoSerializer, BusinessAccountContactSerializer, ImageMappingSerializer, InventoryLocationSerializer, AdInventoryLocationMappingSerializer, AdInventoryTypeSerializer, DurationTypeSerializer, PriceMappingDefaultSerializer, PriceMappingSerializer, BannerInventorySerializer, CommunityHallInfoSerializer, DoorToDoorInfoSerializer, LiftDetailsSerializer, NoticeBoardDetailsSerializer, PosterInventorySerializer, SocietyFlatSerializer, StandeeInventorySerializer, SwimmingPoolInfoSerializer, WallInventorySerializer, UserInquirySerializer, CommonAreaDetailsSerializer, ContactDetailsSerializer, EventsSerializer, InventoryInfoSerializer, MailboxInfoSerializer, OperationsInfoSerializer, PoleInventorySerializer, PosterInventoryMappingSerializer, RatioDetailsSerializer, SignupSerializer, StallInventorySerializer, StreetFurnitureSerializer, SupplierInfoSerializer, SportsInfraSerializer, SupplierTypeSocietySerializer, SocietyTowerSerializer, BusinessTypesSerializer, BusinessSubTypesSerializer, AccountInfoSerializer,  CampaignTypeMappingSerializer
from v0.models import CampaignSupplierTypes, SocietyInventoryBooking, CampaignTypeMapping, Campaign, CampaignSocietyMapping, BusinessInfo, \
                    BusinessAccountContact, ImageMapping, InventoryLocation, AdInventoryLocationMapping, AdInventoryType, DurationType, PriceMappingDefault, \
                    PriceMapping, BannerInventory, CommunityHallInfo, DoorToDoorInfo, LiftDetails, NoticeBoardDetails, PosterInventory, SocietyFlat, StandeeInventory, \
                    SwimmingPoolInfo, WallInventory, UserInquiry, CommonAreaDetails, ContactDetails, Events, InventoryInfo, MailboxInfo, OperationsInfo, PoleInventory, \
                    PosterInventoryMapping, RatioDetails, Signup, StallInventory, StreetFurniture, SupplierInfo, SportsInfra, SupplierTypeSociety, SocietyTower, BusinessTypes, \
                    BusinessSubTypes, AccountInfo, InventorySummary, FlatType, ProposalInfoVersion, ProposalCenterMappingVersion, \
                    SpaceMappingVersion, InventoryTypeVersion, ShortlistedSpacesVersion
from v0.ui.views import InventorySummaryAPIView
from v0.models import SupplierTypeCorporate, ProposalInfo, ProposalCenterMapping,SpaceMapping , InventoryType, ShortlistedSpaces
from v0.ui.website.serializers import ProposalInfoSerializer, ProposalCenterMappingSerializer, SpaceMappingSerializer , \
        InventoryTypeSerializer, ShortlistedSpacesSerializer, ProposalSocietySerializer, ProposalCorporateSerializer, ProposalCenterMappingSpaceSerializer,\
        ProposalInfoVersionSerializer, ProposalCenterMappingVersionSerializer, SpaceMappingVersionSerializer, InventoryTypeVersionSerializer,\
        ShortlistedSpacesVersionSerializer, ProposalCenterMappingVersionSpaceSerializer


from constants import supplier_keys, contact_keys, STD_CODE, COUNTRY_CODE, proposal_header_keys, sample_data, export_keys, center_keys,\
                      inventorylist, society_keys, flat_type_dict, index_of_center_id, offline_pricing_data
from constants import *

from v0.models import City, CityArea, CitySubArea
from coreapi.settings import BASE_URL, BASE_DIR
from v0.ui.utils import get_supplier_id
import utils as website_utils
import v0.ui.utils as ui_utils
import v0.models as models
import serializers as website_serializers
import constants as website_constants


# codes for supplier Types  Society -> RS   Corporate -> CP  Gym -> GY   salon -> SA


class GetBusinessTypesAPIView(APIView):
    """
    fetches all types of businesses.
    """
    def get(self, request, format=None):
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


class GetBusinessSubTypesAPIView(APIView):
    def get(self, request, id, format=None):
        try:
            items = BusinessSubTypes.objects.filter(business_type_id=id)
            serializer = BusinessSubTypesSerializer(items, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


class BusinessAPIView(APIView):
    """
    Fetches one buisiness data
    """

    def get(self, request, id, format=None):
        try:
            item = BusinessInfo.objects.get(pk=id)
            business_serializer = UIBusinessInfoSerializer(item)
            accounts = AccountInfo.objects.filter(business=item)
            accounts_serializer = UIAccountInfoSerializer(accounts, many=True)
            response = {
                'business': business_serializer.data,
                'accounts': accounts_serializer.data
            }
            return Response(response, status=200)
        except BusinessInfo.DoesNotExist:
            return Response(data={'status': False, 'error': "No Buisness data found"},
                            status=status.HTTP_400_BAD_REQUEST)


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
        """
        creates new campaign
        ---
        parameters:
        - name: business
          description: a dict having keys buisiness_id, business_type_id, sub_type_id, name, contacts.
          paramType: body

        """

        current_user = request.user

        business_data = request.data.get('business')
        if not business_data:
            return Response(data={'status': False, 'error': 'No business data supplied'},
                            status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():

            try:
                if 'business_id' in business_data:

                    business = BusinessInfo.objects.get(pk=business_data['business_id'])
                    serializer = BusinessInfoSerializer(business, data=business_data)
                else:
                    # creating business ID

                    type_name = BusinessTypes.objects.get(id=int(business_data['business_type_id']))
                    sub_type = BusinessSubTypes.objects.get(id=int(business_data['sub_type_id']))
                    business_data['business_id'] = self.generate_business_id(business_name=business_data['name'], \
                                                                             sub_type=sub_type, type_name=type_name)
                    if business_data['business_id'] is None:
                        # if business_id is None --> after 12 attempts couldn't get unique id so return first id in lowercase
                        business_data['business_id'] = self.generate_business_id(business_data['name'], \
                                                                                 sub_type=sub_type, type_name=type_name,
                                                                                 lower=True)

                    serializer = BusinessInfoSerializer(data=business_data)

                if serializer.is_valid():
                    try:
                        # This will not hit database again cache will be used if else is executed
                        type_name = BusinessTypes.objects.get(id=int(business_data['business_type_id']))
                        sub_type = BusinessSubTypes.objects.get(id=int(business_data['sub_type_id']))
                        business = serializer.save(type_name=type_name, sub_type=sub_type)

                    except ValueError:
                        return Response({'message': 'Business Type/SubType Invalid'}, \
                                        status=status.HTTP_406_NOT_ACCEPTABLE)

                else:
                    return Response(serializer.errors, status=400)

                content_type_business = ContentType.objects.get_for_model(BusinessInfo)
                contact_ids = list(business.contacts.all().values_list('id', flat=True))
                contact_list = []

                for contact in business_data['contacts']:

                    contact['object_id'] = business.business_id
                    contact['content_type'] = content_type_business.id

                    if 'id' in contact:
                        item = BusinessAccountContact.objects.get(pk=contact['id'])
                        if contact['spoc'] == '':
                            contact['spoc'] = item.spoc
                        contact_ids.remove(item.id)
                        contact_serializer = BusinessAccountContactSerializer(item, data=contact)
                    else:
                        if contact['spoc'] == '':
                            contact['spoc'] = 'false'
                        contact_serializer = BusinessAccountContactSerializer(data=contact)

                    contact_serializer.is_valid(raise_exception=True)

                    contact = contact_serializer.save()
                    # contact object is returned on saving serializer so appending that inside list to send back to the page
                    contact_list.append(contact)

                # deleting all contacts whose id not received from the frontend
                BusinessAccountContact.objects.filter(id__in=contact_ids).delete()

                business_serializer = BusinessInfoSerializer(business)
                contacts_serializer = BusinessAccountContactSerializer(contact_list, many=True)

                response = {
                    'business': business_serializer.data,
                    'contacts': contacts_serializer.data,
                }
            except Exception as e:
                return Response(data={'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)

        return Response(response, status=200)

    def generate_business_id(self, business_name, sub_type, type_name, lower=False):
        business_code = create_code(name=business_name)
        business_front = type_name.business_type_code + sub_type.business_sub_type_code
        business_id = business_front + business_code
        if lower:
            return business_id.lower()

        try:
            business = BusinessInfo.objects.get(business_id=business_id)
            # if exception does not occur means conflict
            business_code = create_code(name=business_name, conflict=True)
            business_id = type_name.business_type_code + sub_type.business_sub_type_code + business_code
            business = BusinessInfo.objects.get(business_id=business_id)

            # still conflict ---> Generate random 4 uppercase character string
            i = 0  # i keeps track of infinite loop tune it according to the needs
            while (True):
                if i > 10:
                    return None
                business_code = ''.join(random.choice(string.ascii_uppercase) for _ in range(4))
                business_id = business_front + business_code
                business = BusinessInfo.objects.get(business_id=business_id)
                i += 1

        except BusinessInfo.DoesNotExist:
            return business_id.upper()


def create_code(name, conflict=False):
    name = name.split()

    if len(name) >= 4:
        code = name[0][0] + name[1][0] + name[2][0] + name[3][0]
    if len(name) == 3:
        if len(name[0]) >= 2:
            code = name[0][:2] + name[1][0] + name[2][0]
        else :
            code = get_extra_character() + name[0] + name[1][0] + name[2][0]
    elif len(name) == 2:
        if len(name[0]) >= 2 and len(name[1]) >= 2:
            code = name[0][:2] + name[1][:2]
        elif len(name[0]) >= 3:
            code = name[0][:3] + name[1]
        elif len(name[1]) >= 3:
            code = name[0] + name[1][:3]
        elif len(name[0]) >= 2 or len(name[0]) >=2:
            code = get_extra_character() + name[0] + name[1]
        else :
            code = get_extra_character(size=2) + name[0] + name[1]
    else:
        if len(name[0]) >= 4:
            code = name[0][:4]
        else :
            size = 4 - len(name[0])
            extra_characters = get_extra_character(size)
            code = extra_characters + name[0]

    # conflict means previous code already present in database
    # so append a extra char in front of existing code and remove last char from it
    if conflict:
        code = get_extra_character() + code[:3]


    return code.upper()


def get_extra_character(size=1):
    return ''.join(random.choice(string.ascii_uppercase ) for _ in range(size))



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
                return Response({'message' : 'Appropriate data not provided'} , \
                        status = status.HTTP_406_NOT_ACCEPTABLE)

            with transaction.atomic():

                try:
                    business_id = account_data['business_id']
                except KeyError:
                    return Response({'message' : 'Imporper Business Type Id'}, status = status.HTTP_406_NOT_ACCEPTABLE)


                # checking a valid business
                try:
                    business = BusinessInfo.objects.get(business_id=business_id)
                except BusinessInfo.DoesNotExist:
                    return Response({'message' : 'Business Does Not Exist'}, status = status.HTTP_406_NOT_ACCEPTABLE)

                if 'account_id' in account_data:
                    account = AccountInfo.objects.get(pk=account_data['account_id'])
                    serializer = AccountInfoSerializer(account,data=account_data)
                else:
                    account_data['account_id']= self.generate_account_id(account_name=account_data['name'],business_id=business_id)
                    if account_data['account_id'] is None:
                        # if account_id is None --> after 12 attempts couldn't get unique id so return first id in lowercase
                        account_data['account_id'] = self.generate_account_id(account_name=account_data['name'],business_id=business_id, lower=True)
                    serializer = AccountInfoSerializer(data=account_data)

                if serializer.is_valid():
                    account = serializer.save(business=business)
                else:
                    return Response(serializer.errors, status=400)

                content_type_account = ContentType.objects.get_for_model(AccountInfo)

                # #here we will start storing contacts
                contact_ids = list(account.contacts.all().values_list('id',flat=True))
                contact_list = []

                for contact in account_data['contacts']:
                    contact['object_id'] = account.account_id
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
                        contact = contact_serializer.save()
                        contact_list.append(contact)
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
                # account = AccountInfo.objects.get(id=account_id)
                account_serializer = AccountInfoSerializer(account)
                # contacts = account.contacts.all()
                contacts_serializer = BusinessAccountContactSerializer(contact_list, many=True)
                response['account'] = account_serializer.data
                response['contacts'] = contacts_serializer.data
            return Response(response, status=200)


    def generate_account_id(self, account_name, business_id, lower=False):
        business_code = business_id[-4:]
        account_code = create_code(name = account_name)
        account_id = business_code + account_code

        try:
            account = AccountInfo.objects.get(account_id=account_id)
            # if exception does not occur means confict
            account_code = create_code(name = account_name, conflict=True)
            account_id = business_code + account_code
            account = AccountInfo.objects.get(account_id=account_id)

            # still conflict ---> Generate random 4 uppercase character string
            i = 0  # i keeps track of infinite loop tune it according to the needs
            while(True):
                if i > 10:
                    return None
                account_code = ''.join(random.choice(string.ascii_uppercase ) for _ in range(4))
                account_id = business_code + account_code
                account = AccountInfo.objects.get(account_id=account_id)
                i += 1

        except AccountInfo.DoesNotExist:
            return account_id.upper()


class GetAccountProposalsAPIView(APIView):
    """
    fetches proposals for a given account_id
    """

    def get(self, request, account_id, format=None):

        try:
            account = AccountInfo.objects.get(account_id=account_id)


            proposals = ProposalInfo.objects.filter(account=account)
            proposal_serializer = ProposalInfoSerializer(proposals, many=True)
        
            return Response(proposal_serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


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
        """
        ---
        parameters:
        - name: request.data
          description: dict having keys 'inventory', 'type'.
          paramType: body

        """

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
                inv_details = InventorySummary.objects.get_object(request.data.copy(), id)
                if not inv_details:
                    return Response({'status': False, 'error': 'Inventory object not found for {0} id'.format(id)},
                                    status=status.HTTP_400_BAD_REQUEST)

                #inv_details = InventorySummary.objects.get(supplier_id=society_id)
                for inv in inv_types:
                    inv_name = inv.type
                    inv_size = inv.sub_type
                    if (hasattr(inv_details, inv_name.lower() + allowed) and getattr(inv_details, inv_name.lower() + allowed)):
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
                        inv_price = price_obj.business_price
                        inv_info['count'] = str(inv_count)
                        inv_info['price'] = str(inv_price)
                        inv_info['type'] = inv_name
                        society_detail['inventory'].append(inv_info)


                response.append(society_detail)

            # response = (response)
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


# Beta API below this point. Be Careful. Danger Below

def return_price(adinventory_type_dict, duration_type_dict, inv_type, dur_type):
    price_mapping = PriceMappingDefault.objects.filter(adinventory_type=adinventory_type_dict[inv_type], duration_type=duration_type_dict[dur_type])
    if price_mapping:
        return price_mapping[0].business_price
    return 0


class SpacesOnCenterAPIView(APIView):
    def get(self,request,proposal_id=None, format=None):
        ''' This function filters all the spaces(Societies, Corporates etc.) based on the center and
        radius provided currently considering radius
        This API is called before map view page is loaded
        center -- center id for which to filter societies and corporates.

        '''

        ''' !IMPORTANT --> you have to manually add all the type of spaces that are being added apart from
        Corporate and Society '''
        response = {}
        center_id = request.query_params.get('center',None)
        try:
            proposal = ProposalInfo.objects.get(proposal_id=proposal_id)
            response['business_name'] = proposal.account.business.name
        except ProposalInfo.DoesNotExist:
            return Response({'message' : 'Invalid Proposal ID sent'}, status=406)

        # if center comes in get request then just return the result for that center
        # this is to implement the reset center functionality
        if center_id:
            try:
                center_id = int(center_id)
            except ValueError:
                return Response({'message' : 'Invalid Center ID provided'}, status=406)
            # fetch center object
            proposal_centers = ProposalCenterMapping.objects.filter(id=center_id)
            if not proposal_centers:
                return Response({'message' : 'Invalid Center ID provided'}, status=406)
        else :
            # fetch all centers for this proposal id
            proposal_centers = ProposalCenterMapping.objects.filter(proposal=proposal)

        centers_data_list = []
        # iterate all centers one by one
        for proposal_center in proposal_centers:
            try:
                space_mapping_object = SpaceMapping.objects.get(center=proposal_center)
            except SpaceMapping.DoesNotExist:
                return Response({'message' : 'Space Mapping Does Not Exist'}, status=406)

            space_info_dict = {}

            # calculate the max, min lat long
            delta_dict = website_utils.get_delta_latitude_longitude(float(proposal_center.radius), float(proposal_center.latitude))

            delta_latitude = delta_dict['delta_latitude']
            min_latitude = proposal_center.latitude - delta_latitude
            max_latitude = proposal_center.latitude + delta_latitude

            delta_longitude = delta_dict['delta_longitude']
            min_longitude = proposal_center.longitude - delta_longitude
            max_longitude = proposal_center.longitude + delta_longitude
            # for society
            if space_mapping_object.society_allowed:
                q = Q(society_latitude__lt=max_latitude) & Q(society_latitude__gt=min_latitude) & Q(society_longitude__lt=max_longitude) & Q(society_longitude__gt=min_longitude)
                
                societies_inventory = space_mapping_object.get_society_inventories()
                societies_inventory_serializer = InventoryTypeSerializer(societies_inventory)
                # applying filter on basis of inventory
                for param in ['poster_allowed', 'standee_allowed', 'flier_allowed', 'stall_allowed', 'banner_allowed']:
                    try:
                        if param == 'poster_allowed' and societies_inventory.__dict__[param]:
                            q &= (Q(poster_allowed_nb=True) | Q(poster_allowed_lift=True))
                        elif societies_inventory.__dict__[param]:
                            q |= Q(**{param : True})
                            
                    except KeyError:
                        pass

                # get all societies based on the query q
                societies_temp = SupplierTypeSociety.objects.filter(q).values('supplier_id','society_latitude','society_longitude','society_name','society_address1', 'society_address2', 'society_subarea', 'society_locality', 'society_location_type', 'flat_count', 'average_rent', 'machadalo_index', 'society_type_quality','tower_count','flat_count')

                # to maintain list of shortlisted societies
                societies = []

                # to maintain list of society_ids
                society_ids = []

                # to maintain total count of societies
                societies_count = 0

                # for each society within defined lat long, process the society
                for society in societies_temp:
                    if website_utils.space_on_circle(proposal_center.latitude, proposal_center.longitude, proposal_center.radius, \
                        society['society_latitude'], society['society_longitude']):
                        society_inventory_obj = InventorySummary.objects.get_object(request.data.copy(),
                                                                                    society['supplier_id'])
                        adinventory_type_dict = ui_utils.adinventory_func()
                        duration_type_dict = ui_utils.duration_type_func()

                        if society_inventory_obj:
                            society['shortlisted'] = True
                            society['buffer_status'] = False

                            # not required
                            if society_inventory_obj.poster_allowed_nb or society_inventory_obj.poster_allowed_lift:
                                society['total_poster_count'] = society_inventory_obj.total_poster_count
                                society['poster_price'] = return_price(adinventory_type_dict, duration_type_dict, 'poster_a4', 'campaign_weekly')
                            # not required
                            if society_inventory_obj.standee_allowed:
                                society['total_standee_count'] = society_inventory_obj.total_standee_count
                                society['standee_price'] = return_price(adinventory_type_dict, duration_type_dict, 'standee_small', 'campaign_weekly')

                            if society_inventory_obj.stall_allowed:
                                society['total_stall_count'] = society_inventory_obj.total_stall_count
                                society['stall_price'] = return_price(adinventory_type_dict, duration_type_dict, 'stall_small', 'unit_daily')
                                society['car_display_price'] = return_price(adinventory_type_dict, duration_type_dict, 'car_display_standard', 'unit_daily')

                            if society_inventory_obj.flier_allowed:
                                society['flier_frequency'] = society_inventory_obj.flier_frequency
                                society['filer_price'] = return_price(adinventory_type_dict, duration_type_dict, 'flier_door_to_door', 'unit_daily')

                        # append the society id
                        society_ids.append(society['supplier_id'])

                        # append the society object to list
                        societies.append(society)

                        # increment the societies count
                        societies_count += 1
                # aggregate information over counts of standee, flier, poster etc is required.
                societies_inventory_count =  InventorySummary.objects.filter(supplier_id__in=society_ids).aggregate(posters=Sum('total_poster_count'),\
                    standees=Sum('total_standee_count'), stalls=Sum('total_stall_count'), fliers=Sum('flier_frequency'))

                # add all societies shortlisted
                space_info_dict['societies'] = societies

                space_info_dict['societies_inventory_count'] = societies_inventory_count
                space_info_dict['societies_inventory'] = societies_inventory_serializer.data
                space_info_dict['societies_count'] = societies_count

            
            if space_mapping_object.corporate_allowed:
                q = Q(latitude__lt=max_latitude) & Q(latitude__gt=min_latitude) & Q(longitude__lt=max_longitude) & Q(longitude__gt=min_longitude)

                # ADDNEW --> uncomment this line when corporate inventory implemented
                corporates_inventory = space_mapping_object.get_corporate_inventories()
                corporates_inventory_serializer = InventoryTypeSerializer(corporates_inventory)
                # then run for loop almost same as above for applying filter on inventory_allowed
                # make a query for different inventory count (e.g. poster_count )

                corporates_temp = SupplierTypeCorporate.objects.filter(q).values('supplier_id','latitude','longitude')
                corporates = []
                corporate_ids = []
                corporates_count = 0
                for corporate in corporates_temp:
                    if website_utils.space_on_circle(proposal_center.latitude, proposal_center.longitude, proposal_center.radius, \
                        corporate['latitude'], corporate['longitude']):
                        corporate_inventory_obj = InventorySummary.objects.get_object(request.data.copy(),corporate['supplier_id'])
                        adinventory_type_dict = ui_utils.adinventory_func()
                        duration_type_dict = ui_utils.duration_type_func()
                        if corporate_inventory_obj:
                            corporate['shortlisted'] = True
                            corporate['buffer_status'] = False

                            if corporate_inventory_obj.poster_allowed_nb or corporate_inventory_obj.poster_allowed_lift:
                                corporate['total_poster_count'] = corporate_inventory_obj.total_poster_count
                                corporate['poster_price'] = return_price(adinventory_type_dict, duration_type_dict, 'poster_a4', 'campaign_weekly')
                            if corporate_inventory_obj.standee_allowed:
                                corporate['total_standee_count'] = corporate_inventory_obj.total_standee_count
                                corporate['standee_price'] = return_price(adinventory_type_dict, duration_type_dict, 'standee_small', 'campaign_weekly')
                            if corporate_inventory_obj.stall_allowed:
                                corporate['total_stall_count'] = corporate_inventory_obj.total_stall_count
                                corporate['stall_price'] = return_price(adinventory_type_dict, duration_type_dict, 'stall_small', 'unit_daily')
                                corporate['car_display_price'] = return_price(adinventory_type_dict, duration_type_dict, 'car_display_standard', 'unit_daily')
                            if corporate_inventory_obj.flier_allowed:     
                                corporate['flier_frequency'] = corporate_inventory_obj.flier_frequency
                                corporate['filer_price'] = return_price(adinventory_type_dict, duration_type_dict, 'flier_door_to_door', 'unit_daily')



                        corporate_ids.append(corporate['supplier_id'])
                        corporates.append(corporate)
                        corporates_count += 1

                # corporates_serializer = ProposalCorporateSerializer(corporates, many=True)

                carporates_inventory_count =  InventorySummary.objects.filter(supplier_id__in=corporate_ids).aggregate(posters=Sum('total_poster_count'),\
                    standees=Sum('total_standee_count'), stalls=Sum('total_stall_count'), fliers=Sum('flier_frequency'))

                space_info_dict['corporates'] = corporates
                space_info_dict['corporates_count'] = corporates_count
                space_info_dict['corporates_inventory_count'] = carporates_inventory_count  #implement this first
                space_info_dict['corporates_inventory'] = corporates_inventory_serializer.data

                # add inventory count information
                space_info_dict['societies_inventory_count'] = societies_inventory_count

                # add InventoryType details
                space_info_dict['societies_inventory'] = societies_inventory_serializer.data

                # add the total count of shortlisted societies
                space_info_dict['societies_count'] = societies_count

            # add center information
            proposal_center_serializer = ProposalCenterMappingSpaceSerializer(proposal_center)
            space_info_dict['center'] = proposal_center_serializer.data

            # append the structure obtained into the list for centers
            centers_data_list.append(space_info_dict)

        # return the result
        response['centers'] = centers_data_list

        return Response(response, status=200)



    def post(self, request,proposal_id=None, format=None):
        '''This API returns the spaces info when center or radius is changed
        API ONLY PRODUCE RESULTS FOR SOCIETIES ONLY
        Code to be written for other spaces
        ---


        '''
        response = {}
        center_info = request.data
        try:
            center = center_info['center']
            space_mappings = center['space_mappings']
        except KeyError:
            return Response({'message':'Improper center or space_mappings data'}, status=406)

        response['center'] = center
        latitude = float(center['latitude'])
        longitude = float(center['longitude'])
        radius = float(center['radius'])
        # area= "Andheri(E)"
        delta_dict = website_utils.get_delta_latitude_longitude(radius, latitude)

        delta_latitude = delta_dict['delta_latitude']
        min_latitude = center['latitude'] - delta_latitude
        max_latitude = center['latitude'] + delta_latitude

        delta_longitude = delta_dict['delta_longitude']
        min_longitude = center['longitude'] - delta_longitude
        max_longitude = center['longitude'] + delta_longitude
        q = Q()
        if space_mappings['society_allowed']:
            q &= Q(society_latitude__lt=max_latitude) & Q(society_latitude__gt=min_latitude) & Q(society_longitude__lt=max_longitude) & Q(society_longitude__gt=min_longitude)
            # p = Q(society_locality=area)
            try:
                societies_inventory = center_info['societies_inventory']
            except KeyError:
                return Response({'message' : 'Provide society_inventory when society selected'}, status=406)

            for param in ['poster_allowed', 'standee_allowed', 'flier_allowed', 'stall_allowed', 'banner_allowed']:
                try:
                    if param == 'poster_allowed' and societies_inventory[param]:
                        q &= (Q(poster_allowed_nb=True) | Q(poster_allowed_lift=True))
                    elif societies_inventory[param]:
                        q &= Q(**{param : True})
                except KeyError:
                    pass
            # societies_temp1 = SupplierTypeSociety.objects.filter(p).values('supplier_id','society_latitude','society_longitude','society_zip')    
            societies_temp = SupplierTypeSociety.objects.filter(q).values('supplier_id','society_latitude','society_longitude','society_name','society_address1','society_subarea','society_location_type','tower_count','flat_count','society_type_quality')
            societies = []
            society_ids = []
            societies_count = 0
            for society in societies_temp:
                if website_utils.space_on_circle(latitude, longitude, radius, society['society_latitude'], society['society_longitude']):
                    society_inventory_obj = InventorySummary.objects.get_object(request.data.copy(),
                                                                                society['supplier_id'])
                    if society_inventory_obj:
                    #society_inventory_obj = InventorySummary.objects.get(supplier_id=society['supplier_id'])
                        society['shortlisted'] = True
                        society['buffer_status'] = False
                        # obj = InventorySummaryAPIView()
                        adinventory_type_dict = ui_utils.adinventory_func()
                        duration_type_dict = ui_utils.duration_type_func()
                        if society_inventory_obj.poster_allowed_nb or society_inventory_obj.poster_allowed_lift:
                            society['total_poster_count'] = society_inventory_obj.total_poster_count
                            society['poster_price'] = return_price(adinventory_type_dict, duration_type_dict, 'poster_a4', 'campaign_weekly')

                        if society_inventory_obj.standee_allowed:
                            society['total_standee_count'] = society_inventory_obj.total_standee_count
                            society['standee_price'] = return_price(adinventory_type_dict, duration_type_dict, 'standee_small', 'campaign_weekly')

                        if society_inventory_obj.stall_allowed:
                            society['total_stall_count'] = society_inventory_obj.total_stall_count
                            society['stall_price'] = return_price(adinventory_type_dict, duration_type_dict, 'stall_small', 'unit_daily')
                            society['car_display_price'] = return_price(adinventory_type_dict, duration_type_dict, 'car_display_standard', 'unit_daily')

                        if society_inventory_obj.flier_allowed:
                            society['flier_frequency'] = society_inventory_obj.flier_frequency
                            society['filer_price'] = return_price(adinventory_type_dict, duration_type_dict, 'flier_door_to_door', 'unit_daily')

                    # ADDNEW -->
                    society_ids.append(society['supplier_id'])
                    societies.append(society)
                    societies_count += 1

            # societies_serializer =  ProposalSocietySerializer(societies, many=True)

            # following query find sum of all the variables specified in a dictionary
            # this finds sum of all inventories, if you don't need some of some inventory make it 0 in front end
            societies_inventory_count =  InventorySummary.objects.filter(supplier_id__in=society_ids).aggregate(posters=Sum('total_poster_count'),\
                standees=Sum('total_standee_count'), stalls=Sum('total_stall_count'), fliers=Sum('flier_frequency'))

            response['suppliers'] = societies
            response['supplier_inventory_count'] = societies_inventory_count
            response['supplier_inventory'] = societies_inventory
            response['supplier_count'] = societies_count
            # response['area_societies'] = societies_temp1 

        if space_mappings['corporate_allowed']:
            pass
            # q = Q(latitude__lt=max_latitude) & Q(latitude__gt=min_latitude) & Q(longitude__lt=max_longitude) & Q(longitude__gt=min_longitude)

            # ADDNEW --> uncomment when implemented properly
            # try:
            #     corporates_inventory = center_info['corporate_inventory']
            # except KeyError:
            #     return Response({'message' : 'Provide corporates_inventory when corporates selected'}, status=406)

            # filter on basis of corporates_inventory (poster_allowed etc.) like in society_filter


            # corporates_temp = SupplierTypeCorporate.objects.filter(q)
            # corporates = []
            # corporates_count = 0
            # for corporate in corporates_temp:
            #     if space_on_circle(center['latitude'], center['longitude'], center['radius'], \
            #         corporate.latitude, corporate.longitude):
            #         corporates.append(corporate)
            #         corporates_count += 1

            # corporates_serializer = ProposalCorporateSerializer(corporates, many=True)

            # response['corporates'] = corporates_serializer.data
            # response['corporates_count'] = corporates_count
            # response['corporates_inventory'] = corporates_inventory


        if space_mappings['gym_allowed']:
            # ADDNEW --> write code for gym
            pass

        if space_mappings['salon_allowed']:
            # ADDNEW --> write code for salon
            pass

        return Response(response, status=200)


class FilteredSuppliers(APIView):
    """
    This API gives suppliers based on different filters from mapView and gridView Page.
    Very expensive API. Use carefully.
    """

    def post(self, request):
        """
        The request looks like :
        {
          'supplier_type_code': 'CP',
          'common_filters': { 'latitude': 12, 'longitude': 11, 'radius': 2, 'quality': [ 'UH', 'H' ],
           'quantity': ['VL'],
           },
           'inventory_filters': ['PO', 'ST'],
          'specific_filters': { 'real_estate_allowed': True, 'employees_count': {min: 10, max: 100},}
        }
        and the response looks like.:
        {
            "status": true,
            "data": {
                "suppliers": {
                    "RS": []
                },
                "suppliers_meta": {
                    "RS": {
                        "count": 0,
                        "inventory_count": {
                            "posters": null,
                            "stalls": null,
                            "standees": null,
                            "fliers": null
                        }
                    },
                }
            }
        }

        """
        class_name = self.__class__.__name__
        try:
            # if not supplier type code, return
            supplier_type_code = request.data.get('supplier_type_code')
            if not supplier_type_code:
                return ui_utils.handle_response(class_name, data='provide supplier type code')

            common_filters = request.data.get('common_filters')  # maps to BaseSupplier Model
            inventory_filters = request.data.get('inventory_filters')  # maps to InventorySummary model
            specific_filters = request.data.get('specific_filters')  # maps to specific supplier table

            # get the right model and content_type
            supplier_model = ui_utils.get_model(supplier_type_code)
            response = ui_utils.get_content_type(supplier_type_code)
            if not response:
                return response
            content_type = response.data.get('data')
            # first fetch common query which is applicable to all suppliers. The results of this query will form
            # our master supplier list.
            response = website_utils.handle_common_filters(common_filters, supplier_type_code)
            if not response.data['status']:
                return response
            common_filters_query = response.data['data']

            # container to store specific_filters type of suppliers
            specific_filters_suppliers = []
            # container to store inventory filters type of suppliers
            inventory_type_query_suppliers = []
            # this is the main list. if no filter is selected this is what is returned by default

            master_suppliers_list = supplier_model.objects.filter(common_filters_query).values_list('supplier_id')

            # now fetch all inventory_related suppliers
            # handle inventory related filters. it involves quite an involved logic hence it is in another function.
            response = website_utils.handle_inventory_filters(inventory_filters)
            if not response.data['status']:
                return response
            inventory_type_query = response.data['data']

            if inventory_type_query.__len__():
                inventory_type_query &= Q(content_type=content_type)
                inventory_type_query_suppliers = list(models.InventorySummary.objects.filter(inventory_type_query).values_list('object_id'))

            # fetch specific_filters suppliers
            response = website_utils.handle_specific_filters(specific_filters, supplier_type_code)
            if not response.data['status']:
                return response
            specific_filters_query = response.data['data']
            # if indeed there was something in the query
           
            if specific_filters_query.__len__():
                specific_filters_suppliers = list(supplier_model.objects.filter(specific_filters_query).values_list('supplier_id'))

            # pull only the ID's, not the tuples !
            inventory_type_query_suppliers = set([supplier_tuple[0] for supplier_tuple in inventory_type_query_suppliers])
            specific_filters_suppliers = set([supplier_tuple[0] for supplier_tuple in specific_filters_suppliers])
            master_suppliers_list = set([supplier_tuple[0] for supplier_tuple in master_suppliers_list])
            
            # if both available, find the intersection. basically it's another way of doing AND query.
            # the following conditions are use case dependent. The checking is done on the basis of 
            # query length. an empty query lenth means that query didn't contain any thing in it. 
            if inventory_type_query.__len__() and specific_filters_query.__len__():
                final_suppliers_list = specific_filters_suppliers.intersection(inventory_type_query_suppliers)
            # if only inventory suppliers available, set it. Take the UNION in this case
            elif inventory_type_query.__len__():
                final_suppliers_list = inventory_type_query_suppliers
            # if only specific suppliers available, set it. Take the UNION in this case.
            elif specific_filters_query.__len__():
                final_suppliers_list = specific_filters_suppliers
            # if nobody is available, set it to master supplier list
            else:
                final_suppliers_list = master_suppliers_list

            # when the final supplier list is prepared. we need to take intersection with master list. 
            final_suppliers_list = final_suppliers_list.intersection(master_suppliers_list)
        
            result = {}

            # query now for real objects for supplier_id in the list
            suppliers = supplier_model.objects.filter(supplier_id__in=final_suppliers_list)
            supplier_serializer = ui_utils.get_serializer(supplier_type_code)
            serializer = supplier_serializer(suppliers, many=True)

            # to incllude only those suppliers that lie within radius, we need to send coordinates
            coordinates = {
                'radius': common_filters['radius'],
                'latitude': common_filters['latitude'],
                'longitude': common_filters['longitude']
            }
            # the following function sets the pricing as before and it's temproaray.
            response = website_utils.set_pricing_temproray(serializer.data, final_suppliers_list, supplier_type_code, coordinates)
            if not response.data['status']:
                return response
            suppliers = response.data['data']
            # response = website_utils.set_supplier_extra_attributes(serializer.data, supplier_type_code, inventory_filters)
            # if not response.data['status']:
            #     return response
            # serializer.data = response.data['data']

            # calculate total aggregate count
            suppliers_inventory_count = InventorySummary.objects.filter(object_id__in=final_suppliers_list, content_type=content_type).aggregate(posters=Sum('total_poster_count'), \
                                                                                                        standees=Sum('total_standee_count'),
                                                                                                        stalls=Sum('total_stall_count'),

                                                                                                        fliers=Sum('flier_frequency'))

            # construct the response and return
            result['suppliers'] = {}
            result['suppliers_meta'] = {}

            result['suppliers'][supplier_type_code] = suppliers

            result['suppliers_meta'][supplier_type_code] = {}

            result['suppliers_meta'][supplier_type_code]['count'] = 0
            result['suppliers_meta'][supplier_type_code]['inventory_count'] = suppliers_inventory_count

            return ui_utils.handle_response(class_name, data=result, success=True)

        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class FilteredSuppliersAPIView(APIView):
    """
    This API gives suppliers based on different filters from mapView and gridView Page
    Currently implemented filters are locality and location (Standard, Medium High etc.)
    flat_count (100 - 250 etc.) flat_type(1BHK, 2BHK etc.)
    """

    def get(self, request, format=None):
        '''
        Response is in form
        {
            "status": true,
            "data": {
                "suppliers": {
                    "RS": []
                },
                "suppliers_meta": {
                    "RS": {
                        "count": 0,
                        "inventory_count": {
                            "posters": null,
                            "stalls": null,
                            "standees": null,
                            "fliers": null
                        }
                    }
                }
            }
        }

        lat -- latitude
        lng -- longitude
        r -- radius
        loc -- location params
        qlt -- supplier quality params example UH, HH, MH
        qnt -- supplier quantity params example LA, MD
        flc -- flat count
        inv -- inventory params example PO, ST, SL
        supplier_type_code -- RS, CP etc
        '''
        class_name = self.__class__.__name__
        try:

            response = {}

            latitude = request.query_params.get('lat', None)
            longitude = request.query_params.get('lng', None)
            radius = request.query_params.get('r', None)  # radius change
            location_params = request.query_params.get('loc', None)
            supplier_quality_params = request.query_params.get('qlt', None)
            supplier_quantity_params = request.query_params.get('qnt', None)
            flat_count = request.query_params.get('flc', None)
            flat_type_params = request.query_params.get('flt', None)
            inventory_params = request.query_params.get('inv', None)
            supplier_code = request.query_params.get('supplier_type_code')
            filter_query = Q()

            supplier_code = 'RS'

            if not supplier_code:
                return Response({'status': False, 'error': 'Provide supplier type code'},
                                status=status.HTTP_400_BAD_REQUEST)

            if not latitude or not longitude or not radius:
                return Response({'message': 'Please Provide longitude and latitude and radius as well'}, status=406)

            latitude = float(latitude)
            longitude = float(longitude)
            radius = float(radius)


            if flat_type_params:
                flat_types = []
                flat_type_params = flat_type_params.split()
                for param in flat_type_params:
                    try:
                        flat_types.append(flat_type_dict[param])
                    except KeyError:
                        pass
                if flat_types:
                    ''' We can improve performance here  by appending .distinct('supplier_id') when using postgresql '''
                    supplier_ids = set(FlatType.objects.filter(flat_type__in=flat_types).values_list('object_id', flat=True))
                    filter_query &= Q(supplier_id__in=supplier_ids)
                    # here to include those suppliers which don't have this info nothing can be done
                    # It is simply all the suppliers -> filter becomes useless
            delta_dict = website_utils.get_delta_latitude_longitude(radius, latitude)

            # add data to get min,max lat-long
            delta_dict['latitude'] = float(latitude)
            delta_dict['longitude'] = float(longitude)
            delta_dict['supplier_type_code'] = supplier_code

            # call the function to get min,max, lat,long data
            min_max_lat_long_response = website_utils.get_min_max_lat_long(delta_dict)
            if not min_max_lat_long_response.data['status']:
                return min_max_lat_long_response

            # make right params to call make_filter_query function
            filter_query_params = min_max_lat_long_response.data['data']
            filter_query_params['location_params'] = location_params
            filter_query_params['supplier_quality_params'] = supplier_quality_params
            filter_query_params['supplier_quantity_params'] = supplier_quantity_params
            filter_query_params['flat_count'] = flat_count
            filter_query_params['inventory_params'] = inventory_params
            filter_query_params['supplier_type_code'] = supplier_code

            # call function to make filter
            #todo: make filter function specific to supplier
            filter_query_response = website_utils.make_filter_query(filter_query_params)
            if not filter_query_response.data['status']:
                return filter_query_response
            filter_query &= filter_query_response.data['data']

            # get all suppliers  with all columns for the filter we constructed.
            suppliers = ui_utils.get_model(supplier_code).objects.filter(filter_query)

            serializer = ui_utils.get_serializer(supplier_code)(suppliers, many=True)

            suppliers = serializer.data
            supplier_ids = []
            suppliers_count = 0
            suppliers_data = []

            # iterate over all suppliers to  generate the final response
            for supplier in suppliers:

                supplier['supplier_latitude'] = supplier['society_latitude'] if supplier['society_latitude'] else supplier['latitude']
                supplier['supplier_longitude'] = supplier['society_longitude'] if supplier['society_longitude'] else supplier['longitude']

                if website_utils.space_on_circle(latitude, longitude, radius, supplier['supplier_latitude'],supplier['supplier_longitude']):
                    supplier_inventory_obj = InventorySummary.objects.get_object(request.data.copy(),
                                                                                 supplier['supplier_id'])
                    if supplier_inventory_obj:

                        supplier['shortlisted'] = True
                        supplier['buffer_status'] = False
                        adinventory_type_dict = ui_utils.adinventory_func()
                        duration_type_dict = ui_utils.duration_type_func()

                        if supplier_inventory_obj.poster_allowed_nb or supplier_inventory_obj.poster_allowed_lift:
                            supplier['total_poster_count'] = supplier_inventory_obj.total_poster_count
                            supplier['poster_price'] = return_price(adinventory_type_dict, duration_type_dict, 'poster_a4',
                                                                    'campaign_weekly')

                        if supplier_inventory_obj.standee_allowed:
                            supplier['total_standee_count'] = supplier_inventory_obj.total_standee_count
                            supplier['standee_price'] = return_price(adinventory_type_dict, duration_type_dict,
                                                                     'standee_small', 'campaign_weekly')

                        if supplier_inventory_obj.stall_allowed:
                            supplier['total_stall_count'] = supplier_inventory_obj.total_stall_count
                            supplier['stall_price'] = return_price(adinventory_type_dict, duration_type_dict, 'stall_small',
                                                                   'unit_daily')
                            supplier['car_display_price'] = return_price(adinventory_type_dict, duration_type_dict,
                                                                         'car_display_standard', 'unit_daily')

                        if supplier_inventory_obj.flier_allowed:
                            supplier['flier_frequency'] = supplier_inventory_obj.flier_frequency
                            supplier['filer_price'] = return_price(adinventory_type_dict, duration_type_dict,
                                                                   'flier_door_to_door', 'unit_daily')

                        # ADDNEW -->
                supplier_ids.append(supplier['supplier_id'])
                suppliers_data.append(supplier)
                suppliers_count += 1

                for society_key, actual_key in website_constants.society_common_keys.iteritems():
                    if society_key in supplier.keys():
                        value = supplier[society_key]
                        del supplier[society_key]
                        supplier[actual_key] = value

            suppliers_inventory_count = InventorySummary.objects.filter_objects({'supplier_type_code': supplier_code},
                                                                                supplier_ids).aggregate(posters=Sum('total_poster_count'), \
                                                                                                        standees=Sum('total_standee_count'),
                                                                                                        stalls=Sum('total_stall_count'),
                                                                                                        fliers=Sum('flier_frequency'))

            result = {}

            result['suppliers'] = {}
            result['suppliers_meta'] = {}

            result['suppliers']['RS'] = suppliers_data

            result['suppliers_meta']['RS'] = {}

            result['suppliers_meta']['RS']['count'] = suppliers_count
            result['suppliers_meta']['RS']['inventory_count'] = suppliers_inventory_count

            return ui_utils.handle_response(class_name, data=result, success=True)

            # response['suppliers'] = suppliers_data
            # response['supplier_inventory_count'] = suppliers_inventory_count
            # response['supplier_count'] = suppliers_count
            # response['supplier_type_code'] = supplier_code
            # return Response(response, status=200)
        except Exception as e:
            return Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


class FinalProposalAPIView(APIView):

    def get(self, request, proposal_id=None, format=None):
        ''' This API sends the data to frontend based on the centers of that proposal and applying
        space filter(society_allowed, corporate_allowed) and there inventories as well
        e.g. (Society --> poster, standee ) will give societies that have both poster and standee allowed
        '''
        try:
            # if proposal_id is None:
            #     proposal_id = 'AlntOlJi';
            proposal_object = ProposalInfo.objects.get(proposal_id=proposal_id)
        except ProposalInfo.DoesNotExist:
            return Response({'message' : 'Invalid Proposal ID sent'}, status=406)

        space_dict , supplier_code_dict = self.get_space_code_dict()
        # ADDNEW -->
        space_model_dict = {
            'society' : SupplierTypeSociety,    'corporate' : SupplierTypeCorporate,
            # 'gym' : SupplierTypeGym,          'salon' : SupplierTypesalon
        }

        space_serializer_dict = {
            'society' : ProposalSocietySerializer,  'corporate' : ProposalCorporateSerializer,
            # 'gym' : ProposalGymSerializer,        'salon' : ProposalsalonSerializer
        }

        centers_objects = proposal_object.get_centers()
        centers_list = []

        for center_object in centers_objects:
            space_info_dict = {}
            center_serializer   = ProposalCenterMappingSpaceSerializer(center_object)
            space_info_dict['center'] = center_serializer.data

            space_mapping_object = center_object.get_space_mappings()

            # for space_name in ['society','corporate','gym','salon']:
            #     if space_mapping_object.__dict__[space_name + '_allowed']:
            #         space_inventory_object = InventoryTypes.objects.get(space_mapping=space_mapping_object, supplier_code=supplier_code_dict[space_name])
            #         space_info_dict[space_dict[space_name] + '_inventory'] = InventoryTypeSerializer(space_inventory_object)

            #         space_ids = ShortlistedSpaces.objects.filter(space_mapping=space_mapping_object, supplier_code=supplier_code_dict[space_name]).values_list('object_id',flat=True)
            #         spaces = space_model_dict[space_name].objects.filter(supplier_id__in=space_ids)
            #         spaces_serializer = space_serializer_dict[space_name](spaces)
            #         space_info_dict[space_dict[space_name]] = spaces_serializer.data

            #         # still have to put inventory count and then done

            #         centers_list.append(space_info_dict)

            if space_mapping_object.society_allowed:
                societies_inventory = space_mapping_object.get_society_inventories()
                societies_inventory_serializer = InventoryTypeSerializer(societies_inventory)

                society_ids = ShortlistedSpaces.objects.filter(space_mapping=space_mapping_object, supplier_code='RS').values_list('object_id',flat=True)
                societies_temp = SupplierTypeSociety.objects.filter(supplier_id__in=society_ids).values('supplier_id','society_latitude','society_longitude','society_name','society_address1','society_subarea','society_location_type')
                societies = []
                society_ids = []
                societies_count = 0
                for society in societies_temp:
                    if website_utils.space_on_circle(center_object.latitude, center_object.longitude, center_object.radius, \
                        society['society_latitude'], society['society_longitude']):
                        society_inventory_obj = InventorySummary.objects.get_object(request.data.copy(),
                                                                                    society['supplier_id'])
                        #society_inventory_obj = InventorySummary.objects.get(supplier_id=society['supplier_id'])
                        society['shortlisted'] = True
                        society['buffer_status'] = False
                        # obj = InventorySummaryAPIView()
                        adinventory_type_dict = ui_utils.adinventory_func()
                        duration_type_dict = ui_utils.duration_type_func()
                        if society_inventory_obj.poster_allowed_nb or society_inventory_obj.poster_allowed_lift:
                            society['total_poster_count'] = society_inventory_obj.total_poster_count
                            society['poster_price'] = return_price(adinventory_type_dict, duration_type_dict, 'poster_a4', 'campaign_weekly')

                        if society_inventory_obj.standee_allowed:
                            society['total_standee_count'] = society_inventory_obj.total_standee_count
                            society['standee_price'] = return_price(adinventory_type_dict, duration_type_dict, 'standee_small', 'campaign_weekly')

                        if society_inventory_obj.stall_allowed:
                            society['total_stall_count'] = society_inventory_obj.total_stall_count
                            society['stall_price'] = return_price(adinventory_type_dict, duration_type_dict, 'stall_small', 'unit_daily')
                            society['car_display_price'] = return_price(adinventory_type_dict, duration_type_dict, 'car_display_standard', 'unit_daily')

                        if society_inventory_obj.flier_allowed:
                            society['flier_frequency'] = society_inventory_obj.flier_frequency
                            society['filer_price'] = return_price(adinventory_type_dict, duration_type_dict, 'flier_door_to_door', 'unit_daily')

                        # ADDNEW --> Banner etc.
                        society_ids.append(society['supplier_id'])
                        societies.append(society)
                        societies_count += 1

                # societies_serializer =  ProposalSocietySerializer(societies, many=True)

                # following query find sum of all the variables specified in a dictionary
                # this finds sum of all inventories, if you don't need some of some inventory make it 0 in front end
                societies_inventory_count =  InventorySummary.objects.filter(supplier_id__in=society_ids).aggregate(posters=Sum('total_poster_count'),\
                    standees=Sum('total_standee_count'), stalls=Sum('total_stall_count'), fliers=Sum('flier_frequency'))

                space_info_dict['societies'] = societies
                space_info_dict['societies_inventory_count'] = societies_inventory_count
                space_info_dict['societies_inventory'] = societies_inventory_serializer.data
                space_info_dict['societies_count'] = societies_count

            if space_mapping_object.corporate_allowed:
                # ADDNEW -->
                pass

            if space_mapping_object.gym_allowed:
                # ADDNEW -->
                pass


            centers_list.append(space_info_dict)

        proposal_serializer = ProposalInfoSerializer(proposal_object)
        response = {
            'proposal' : proposal_serializer.data,
            'centers'  : centers_list,
        }

        return Response(response, status=200)

    def post(self, request, proposal_id=None, format=None):
        ''' Saving the proposal from the map view. Every time mapview page is loaded and grid view is submitted from there
        This makes a new version of proposal. And also updates all the required table as well
        This expects id of both center and space mapping from the frontend as they are saved on basic proposal page (InitialProposalAPIView)
        '''

        centers = request.data
        space_dict, supplier_code_dict = self.get_space_code_dict()

        with transaction.atomic():
            try:
                shortlisted_space_list = []
                shortlisted_space_version_list = []
                for center_info in centers:
                    center = center_info['center']
                    center_id = center['id']

                    proposal_version_object_response = website_utils.save_proposal_version(center_id)
                    if not proposal_version_object_response.data['status']:
                        return proposal_version_object_response
                    proposal_version_object = proposal_version_object_response.data['data']

                    center_object = ProposalCenterMapping.objects.select_related('proposal').get(id=center_id)
                    proposal_object = center_object.proposal

                    center_serializer = ProposalCenterMappingSerializer(center_object, data=center)
                    if center_serializer.is_valid():
                        center_object = center_serializer.save()
                    else:
                        return Response({'message': 'Invalid Center Data', 'errors': center_serializer.errors}, status=406)

                    # version save
                    center['proposal_version'] = proposal_version_object.id
                    del center['id']
                    center_version_serailizer = ProposalCenterMappingVersionSerializer(data=center)

                    if center_version_serailizer.is_valid():
                        center_version_object = center_version_serailizer.save()
                    else:
                        return Response(
                            {'message': 'Invalid Center Version Data', 'errors': center_version_serailizer.errors}, \
                            status=406)

                    space_mappings = center['space_mappings']
                    space_mapping_id = space_mappings['id']
                    space_mapping_object = SpaceMapping.objects.get(id=space_mapping_id)

                    space_mapping_serializer = SpaceMappingSerializer(space_mapping_object, data=space_mappings)
                    if space_mapping_serializer.is_valid():
                        space_mapping_object = space_mapping_serializer.save()
                    else:
                        return Response(
                            {'message': 'Invalid Space Mapping Data', 'errors': space_mapping_serializer.errors}, \
                            status=406)

                    # version save
                    space_mappings['center_version'] = center_version_object.id
                    space_mappings['proposal_version'] = proposal_version_object.id
                    del space_mappings['id']
                    space_mapping_version_serializer = SpaceMappingVersionSerializer(data=space_mappings)
                    if space_mapping_version_serializer.is_valid():
                        space_mapping_version_object = space_mapping_version_serializer.save()
                    else:
                        return Response({'message': 'Invalid Space Mapping Version Data',
                                         'errors': space_mapping_version_serializer.errors}, \
                                        status=406)

                    for space_name in ['society', 'corporate', 'gym', 'salon']:

                        if space_mapping_object.__dict__[space_name + "_allowed"]:
                            content_type = ContentType.objects.get(model='SupplierType' + space_name.title())
                            supplier_code = supplier_code_dict[space_name]

                            try:
                                space_inventory_type = center_info[space_dict[space_name] + '_inventory']
                            except KeyError:
                                # Just ignoring because for corporate inventory is not made
                                continue

                            try:
                                inventory_type_object = InventoryType.objects.get(id=space_inventory_type['id'])
                                inventory_type_serializer = InventoryTypeSerializer(inventory_type_object,
                                                                                    data=space_inventory_type)
                                del space_inventory_type['id']
                            except KeyError:
                                space_inventory_type['space_mapping'] = space_mapping_object.id
                                inventory_type_serializer = InventoryTypeSerializer(data=space_inventory_type)

                            if inventory_type_serializer.is_valid():
                                inventory_type_serializer.save()
                            else:
                                return Response({'message': 'Invalid Inventory Details for ' + space_name, 'errors': \
                                    inventory_type_serializer.errors}, status=406)

                            # version save
                            space_inventory_type['space_mapping_version'] = space_mapping_version_object.id
                            inventory_type_version_serializer = InventoryTypeVersionSerializer(data=space_inventory_type)
                            if inventory_type_version_serializer.is_valid():
                                inventory_type_version_serializer.save()
                            else:
                                return Response(
                                    {'message': 'Invalid Inventory Details Version for ' + space_name, ' errors': \
                                        inventory_type_version_serializer.errors}, status=406)

                            space_mapping_object.get_all_spaces().delete()

                            for space in center_info[space_dict[space_name]]:
                                if space.get('shortlisted'):
                                    object_id = space['supplier_id']
                                    shortlisted_space = ShortlistedSpaces(space_mapping=space_mapping_object,
                                                                          content_type=content_type, \
                                                                          supplier_code=supplier_code, object_id=object_id,
                                                                          buffer_status=space['buffer_status'])

                                    shortlisted_space_list.append(shortlisted_space)

                                    # version save
                                    shortlisted_version_space = ShortlistedSpacesVersion(
                                        space_mapping_version=space_mapping_version_object, \
                                        content_type=content_type, supplier_code=supplier_code, object_id=object_id,
                                        buffer_status=space['buffer_status'])
                                    shortlisted_space_version_list.append(shortlisted_version_space)

                ShortlistedSpaces.objects.bulk_create(shortlisted_space_list)
                # version save
                ShortlistedSpacesVersion.objects.bulk_create(shortlisted_space_version_list)
            except Exception as e:
                return Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message':'Successfully Saved'}, status=200)


    # def put(self, request, format=None):
    #     centers = request.data
    #     for center in centers:


    def get_space_code_dict(self):
        space_dict = { # singular space as key and its plural as value
            'society' : 'societies',    'corporate' : 'corporates',
            'gym' : 'gyms',             'salon'    : 'salons',
        }

        supplier_code_dict = {
            'society' : 'RS',   'corporate' : 'CP',
            'gym' : 'GY',       'salon' : 'SA',
        }

        return space_dict, supplier_code_dict


class FinalProposalSubmit(APIView):
    """
    Saves final proposal
    """

    def post(self, request):
        for center in request.data:
            # create an entry of this proposal in  proposal_info_version table
            pass


class CurrentProposalAPIView(APIView):

    def get(self, request, proposal_id, format=None):
        ''' This returns the proposal info of the proposal id
        '''

        try:
            proposal_object = ProposalInfo.objects.get(proposal_id=proposal_id)
        except ProposalInfo.DoesNotExist:
            return Response({'message' : 'Invalid Proposal ID'}, status=406)

        proposal_serializer = ProposalInfoSerializer(proposal_object)
        centers = proposal_object.get_centers()
        centers_list = []

        for center in centers:
            space_info_dict = {}
            space_mapping_object = center.get_space_mappings()
            center_serializer = ProposalCenterMappingSpaceSerializer(center)
            space_info_dict['center'] = center_serializer.data


            if space_mapping_object.society_allowed:
                societies_shortlisted_ids = ShortlistedSpaces.objects.filter(space_mapping=space_mapping_object, supplier_code='RS',\
                    buffer_status=False).values_list('object_id', flat=True)

                societies_shortlisted_temp = SupplierTypeSociety.objects.filter(supplier_id__in=societies_shortlisted_ids).values('supplier_id','society_latitude','society_longitude','society_name','society_address1','society_subarea','society_location_type')

                societies_shortlisted = []
                societies_shortlisted_count = 0

                for society in societies_shortlisted_temp:
                    society_inventory_obj = InventorySummary.objects.get_object(request.data.copy(),
                                                                                society['supplier_id'])
                    #society_inventory_obj = InventorySummary.objects.get(supplier_id=society['supplier_id'])
                    society['shortlisted'] = True
                    society['buffer_status'] = False
                    # obj = InventorySummaryAPIView()
                    adinventory_type_dict = ui_utils.adinventory_func()
                    duration_type_dict = ui_utils.duration_type_func()


                    if society_inventory_obj.poster_allowed_nb or society_inventory_obj.poster_allowed_lift:
                        society['total_poster_count'] = society_inventory_obj.poster_count_per_tower
                        society['poster_price'] = return_price(adinventory_type_dict, duration_type_dict, 'poster_a4', 'campaign_weekly')

                    if society_inventory_obj.standee_allowed:
                        society['total_standee_count'] = society_inventory_obj.total_standee_count
                        society['standee_price'] = return_price(adinventory_type_dict, duration_type_dict, 'standee_small', 'campaign_weekly')

                    if society_inventory_obj.stall_allowed:
                        society['total_stall_count'] = society_inventory_obj.total_stall_count
                        society['stall_price'] = return_price(adinventory_type_dict, duration_type_dict, 'stall_small', 'unit_daily')
                        society['car_display_price'] = return_price(adinventory_type_dict, duration_type_dict, 'car_display_standard', 'unit_daily')

                    if society_inventory_obj.flier_allowed:
                        society['flier_frequency'] = society_inventory_obj.flier_frequency
                        society['filer_price'] = return_price(adinventory_type_dict, duration_type_dict, 'flier_door_to_door', 'unit_daily')

                    societies_shortlisted.append(society)
                    societies_shortlisted_count += 1


                space_info_dict['societies_shortlisted'] = societies_shortlisted
                space_info_dict['societies_shortlisted_count'] = societies_shortlisted_count


                societies_buffered_ids = ShortlistedSpaces.objects.filter(space_mapping=space_mapping_object, supplier_code='RS',\
                    buffer_status=True).values_list('object_id', flat=True)
                societies_buffered_temp = SupplierTypeSociety.objects.filter(supplier_id__in=societies_buffered_ids).values('supplier_id','society_latitude','society_longitude','society_name','society_address1','society_subarea','society_location_type')
                societies_buffered = []
                societies_buffered_count = 0
                for society in societies_buffered_temp:
                    society_inventory_obj = InventorySummary.objects.get_object(request.data.copy(),
                                                                                society['supplier_id'])

                    #society_inventory_obj = InventorySummary.objects.get(supplier_id=society['supplier_id'])
                    society['shortlisted'] = True
                    society['buffer_status'] = False
                    # obj = InventorySummaryAPIView()
                    adinventory_type_dict = ui_utils.adinventory_func()
                    duration_type_dict = ui_utils.duration_type_func()

                    if society_inventory_obj.poster_allowed_nb or society_inventory_obj.poster_allowed_lift:
                        society['total_poster_count'] = society_inventory_obj.poster_count_per_tower
                        society['poster_price'] = return_price(adinventory_type_dict, duration_type_dict, 'poster_a4', 'campaign_weekly')

                    if society_inventory_obj.standee_allowed:
                        society['total_standee_count'] = society_inventory_obj.total_standee_count
                        society['standee_price'] = return_price(adinventory_type_dict, duration_type_dict, 'standee_small', 'campaign_weekly')

                    if society_inventory_obj.stall_allowed:
                        society['total_stall_count'] = society_inventory_obj.total_stall_count
                        society['stall_price'] = return_price(adinventory_type_dict, duration_type_dict, 'stall_small', 'unit_daily')
                        society['car_display_price'] = return_price(adinventory_type_dict, duration_type_dict, 'car_display_standard', 'unit_daily')

                    if society_inventory_obj.flier_allowed:
                        society['flier_frequency'] = society_inventory_obj.flier_frequency
                        society['filer_price'] = return_price(adinventory_type_dict, duration_type_dict, 'flier_door_to_door', 'unit_daily')

                    societies_buffered.append(society)
                    societies_buffered_count += 1


                space_info_dict['societies_buffered'] = societies_buffered
                space_info_dict['societies_buffered_count'] = societies_buffered_count

                societies_inventory = InventoryType.objects.get(supplier_code='RS', space_mapping=space_mapping_object)
                societies_inventory_serializer = InventoryTypeSerializer(societies_inventory)
                # inventory count only for shortlisted ones
                # to add buffered societies as well uncomment following line
                # societies_shortlisted_ids.extend(societies_buffered_ids)
                societies_inventory_count = InventorySummary.objects.filter(supplier_id__in=societies_shortlisted_ids).aggregate(posters=Sum('poster_count_per_tower'),\
                standees=Sum('total_standee_count'), stalls=Sum('total_stall_count'), fliers=Sum('flier_frequency'))

                # Count only for society_shortlisted
                space_info_dict['societies_inventory_count'] = societies_inventory_count
                space_info_dict['societies_inventory'] = societies_inventory_serializer.data


            if space_mapping_object.corporate_allowed:
                # ADDNEW -->
                pass

            if space_mapping_object.salon_allowed:
                # ADDNEW -->
                pass

            if space_mapping_object.gym_allowed:
                # ADDNEW -->
                pass

            centers_list.append(space_info_dict)

        response = {
            'proposal' : proposal_serializer.data,
            'centers'  : centers_list,
        }


        return Response(response, status=200)


    def post(self, request, proposal_id, format=None):
        ''' Updates the buffer and shortlisted spaces. This API allows user to delete
        move buffer to shortlisted and vice versa. No addition allowed using this API
        '''
        try:
            proposal_object = ProposalInfo.objects.get(proposal_id=proposal_id)
        except ProposalInfo.DoesNotExist:
            return Response({'message' : 'Invalid Proposal ID'}, status=406)

        # version save
        # proposal_version_object = ProposalInfoVersion(proposal=proposal_object, name=proposal_object.name, payment_status=proposal_object.payment_status,\
        #     created_on=proposal_object.created_on, created_by=proposal_object.created_by, tentative_cost=proposal_object.tentative_cost,\
        #     tentative_start_date=proposal_object.tentative_start_date, tentative_end_date=proposal_object.tentative_end_date)
        # proposal_version_object.save()

        shortlisted_space_list = []
        centers = request.data
        for center_info in centers:
            space_mappings = center_info['center']['space_mappings']
            space_mapping_id = space_mappings['id']

            ShortlistedSpaces.objects.filter(space_mapping_id=space_mapping_id).delete()

            if space_mappings['society_allowed']:
                supplier_code = 'RS'
                content_type = ContentType.objects.get_for_model(SupplierTypeSociety)
                for society in center_info['societies_shortlisted']:
                    if society['shortlisted']:
                        object_id = society['supplier_id']
                        shortlisted_society = ShortlistedSpaces(space_mapping_id = space_mapping_id,content_type=content_type, \
                            supplier_code=supplier_code, object_id=object_id, buffer_status = society['buffer_status'])

                        shortlisted_space_list.append(shortlisted_society)

                for society in center_info['societies_buffered']:
                    if society['shortlisted']:
                        object_id = society['supplier_id']
                        shortlisted_society = ShortlistedSpaces(space_mapping_id = space_mapping_id,content_type=content_type, \
                            supplier_code=supplier_code, object_id=object_id, buffer_status = society['buffer_status'])

                        shortlisted_space_list.append(shortlisted_society)



            if space_mappings['corporate_allowed']:
                # ADDNEW -->
                pass

            if space_mappings['salon_allowed']:
                # ADDNEW -->
                pass

            if space_mappings['gym_allowed']:
                # ADDNEW -->
                pass

        ShortlistedSpaces.objects.bulk_create(shortlisted_space_list)
        return Response(status=200)


class ProposalHistoryAPIView(APIView):
    def get(self, request, proposal_id, format=None):
        ''' Sends the proposal versions for the particular proposal id
        Currently if no proposal_id  set to a default one
        sends socities shortlisted and buffered differently
        '''

        try:
            proposal_object = ProposalInfo.objects.get(proposal_id=proposal_id)
        except ProposalInfo.DoesNotExist:
            return Response({'message' : 'Invalid Proposal ID'}, status=406)

        proposal_versions = proposal_object.get_proposal_versions()
        proposal_versions_list = []

        try:
            for proposal_version_object in proposal_versions:
                proposal_info_dict = {}
                proposal_version_serializer = ProposalInfoVersionSerializer(proposal_version_object)
                proposal_info_dict['proposal'] = proposal_version_serializer.data
                proposal_center_versions = ProposalCenterMappingVersion.objects.filter(proposal_version=proposal_version_object)
                center_versions_list = []
                for center_version_object in proposal_center_versions:
                    space_info_dict = {}
                    center_version_serailizer = ProposalCenterMappingVersionSpaceSerializer(center_version_object)
                    space_info_dict['center'] = center_version_serailizer.data

                    space_mapping_version_object = SpaceMappingVersion.objects.get(center_version=center_version_object)

                    if space_mapping_version_object.society_allowed:
                        societies_shortlisted_ids = ShortlistedSpacesVersion.objects.filter(space_mapping_version=space_mapping_version_object,\
                                supplier_code = 'RS', buffer_status=False).values_list('object_id',flat=True)
                        societies_shortlisted_temp = SupplierTypeSociety.objects.filter(supplier_id__in=societies_shortlisted_ids).values('supplier_id','society_latitude','society_longitude','society_name','society_address1','society_subarea','society_location_type')
                        societies_shortlisted = []
                        societies_shortlisted_count = 0
                        # societies_shortlisted_serializer = ProposalSocietySerializer(societies_shortlisted, many=True)
                        for society in societies_shortlisted_temp:
                            society_inventory_obj = InventorySummary.objects.get_object(request.data.copy(),
                                                                                        society['supplier_id'])

                            #society_inventory_obj = InventorySummary.objects.get(supplier_id=society['supplier_id'])
                            society['shortlisted'] = True
                            society['buffer_status'] = False
                            # obj = InventorySummaryAPIView()
                            adinventory_type_dict = ui_utils.adinventory_func()
                            duration_type_dict = ui_utils.duration_type_func()

                            if society_inventory_obj.poster_allowed_nb or society_inventory_obj.poster_allowed_lift:
                                society['total_poster_count'] = society_inventory_obj.total_poster_count
                                society['poster_price'] = return_price(adinventory_type_dict, duration_type_dict, 'poster_a4', 'campaign_weekly')

                            if society_inventory_obj.standee_allowed:
                                society['total_standee_count'] = society_inventory_obj.total_standee_count
                                society['standee_price'] = return_price(adinventory_type_dict, duration_type_dict, 'standee_small', 'campaign_weekly')

                            if society_inventory_obj.stall_allowed:
                                society['total_stall_count'] = society_inventory_obj.total_stall_count
                                society['stall_price'] = return_price(adinventory_type_dict, duration_type_dict, 'stall_small', 'unit_daily')
                                society['car_display_price'] = return_price(adinventory_type_dict, duration_type_dict, 'car_display_standard', 'unit_daily')

                            if society_inventory_obj.flier_allowed:
                                society['flier_frequency'] = society_inventory_obj.flier_frequency
                                society['filer_price'] = return_price(adinventory_type_dict, duration_type_dict, 'flier_door_to_door', 'unit_daily')

                            societies_shortlisted.append(society)
                            societies_shortlisted_count += 1

                        space_info_dict['societies_shortlisted'] = societies_shortlisted
                        space_info_dict['societies_shortlisted_count'] = societies_shortlisted_count


                        societies_buffered_ids = ShortlistedSpacesVersion.objects.filter(space_mapping_version=space_mapping_version_object,\
                                supplier_code = 'RS', buffer_status=True).values_list('object_id',flat=True)
                        societies_buffered_temp = SupplierTypeSociety.objects.filter(supplier_id__in=societies_buffered_ids).values('supplier_id','society_latitude','society_longitude','society_name','society_address1','society_subarea','society_location_type')
                        # societies_buffered_serializer = ProposalSocietySerializer(societies_buffered, many=True)
                        societies_buffered = []
                        societies_buffered_count = 0
                        for society in societies_buffered_temp:
                            society_inventory_obj = InventorySummary.objects.get_object(request.data.copy(),
                                                                                        society['supplier_id'])

                            #society_inventory_obj = InventorySummary.objects.get(supplier_id=society['supplier_id'])
                            society['shortlisted'] = True
                            society['buffer_status'] = False
                            # obj = InventorySummaryAPIView()
                            adinventory_type_dict = ui_utils.adinventory_func()
                            duration_type_dict = ui_utils.duration_type_func()

                            if society_inventory_obj.poster_allowed_nb or society_inventory_obj.poster_allowed_lift:
                                society['total_poster_count'] = society_inventory_obj.total_poster_count
                                society['poster_price'] = return_price(adinventory_type_dict, duration_type_dict, 'poster_a4', 'campaign_weekly')

                            if society_inventory_obj.standee_allowed:
                                society['total_standee_count'] = society_inventory_obj.total_standee_count
                                society['standee_price'] = return_price(adinventory_type_dict, duration_type_dict, 'standee_small', 'campaign_weekly')

                            if society_inventory_obj.stall_allowed:
                                society['total_stall_count'] = society_inventory_obj.total_stall_count
                                society['stall_price'] = return_price(adinventory_type_dict, duration_type_dict, 'stall_small', 'unit_daily')
                                society['car_display_price'] = return_price(adinventory_type_dict, duration_type_dict, 'car_display_standard', 'unit_daily')

                            if society_inventory_obj.flier_allowed:
                                society['flier_freqency'] = society_inventory_obj.flier_frequency
                                society['filer_price'] = return_price(adinventory_type_dict, duration_type_dict, 'flier_door_to_door', 'unit_daily')

                            societies_buffered.append(society)
                            societies_buffered_count += 1


                        space_info_dict['societies_buffered'] = societies_buffered
                        space_info_dict['societies_buffered_count'] = societies_buffered_count

                        societies_inventory = InventoryTypeVersion.objects.get(supplier_code='RS', \
                                space_mapping_version=space_mapping_version_object)
                        societies_inventory_serializer = InventoryTypeVersionSerializer(societies_inventory)
                        societies_inventory_count = InventorySummary.objects.filter(supplier_id__in=societies_shortlisted_ids).aggregate(posters=Sum('total_poster_count'),\
                        standees=Sum('total_standee_count'), stalls=Sum('total_stall_count'), fliers=Sum('flier_frequency'))

                        # Count only for society_shortlisted
                        space_info_dict['societies_inventory_count'] = societies_inventory_count
                        space_info_dict['societies_inventory'] = societies_inventory_serializer.data

                    if space_mapping_version_object.corporate_allowed:
                        # ADDNEW -->
                        pass

                    if space_mapping_version_object.gym_allowed:
                        # ADDNEW -->
                        pass

                    if space_mapping_version_object.salon_allowed:
                        # ADDNEW -->
                        pass

                    center_versions_list.append(space_info_dict)

                proposal_info_dict['centers'] = center_versions_list
                proposal_versions_list.append(proposal_info_dict)

            return Response(proposal_versions_list, status=200)
        except ObjectDoesNotExist as e:
            Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)



class SaveSocietyData(APIView):
    """
    This API reads a csv file and  makes supplier id's for each row. then it adds the data along with
    supplier id in the  supplier_society table. it also populates society_tower table.
    """

    def get(self, request):
        """
        :param request: request object
        :return: success response in case it succeeds else failure message.
        """

        with transaction.atomic():

            source_file = open(BASE_DIR + '/modified_new_tab.csv', 'rb')
            file_errros = open(BASE_DIR + '/errors.txt', 'w')
            try:
                reader = csv.reader(source_file)

                for num, row in enumerate(reader):
                    d = {}
                    if num == 0:
                        continue
                    else:
                        for index, key in enumerate(supplier_keys):
                            if row[index] == '':
                                d[key] = None
                            else:
                                d[key] = row[index]

                        try:
                            area_object = CityArea.objects.get(label=d['area'])
                            subarea_object = CitySubArea.objects.get(subarea_name=d['sub_area'],
                                                                     area_code=area_object)
                            response = get_supplier_id(request, d)
                            # this method of handing error code will  change in future
                            if response.status_code == status.HTTP_200_OK:
                                d['supplier_id'] = response.data['supplier_id']
                            else:
                                file_errros.write("Error in generating supplier id {0} ". format(response.data['error']))
                                continue

                            (society_object, value) = SupplierTypeSociety.objects.get_or_create(
                                supplier_id=d['supplier_id'])
                            d['society_location_type'] = subarea_object.locality_rating
                            d['society_state'] = 'Maharashtra'
                            society_object.__dict__.update(d)
                            society_object.save()

                            towercount = SocietyTower.objects.filter(supplier=society_object).count()

                            # what to do if tower are less
                            tower_count_given = int(d['tower_count'])
                            if tower_count_given > towercount:
                                abc = tower_count_given - towercount
                                for i in range(abc):
                                    tower = SocietyTower(supplier=society_object)
                                    tower.save()

                        except ObjectDoesNotExist as e:
                            file_errros.write(str(e.message) + "," + str(e.args) + ' for ' + str(d['sub_area']) + ' and ' + str(area_object.area_code)
                                              )
                            continue
                        except KeyError as e:
                            return Response(data=str(e.message), status=status.HTTP_400_BAD_REQUEST)
                        except Exception as e:
                            # severe error if reached here, must be returned
                            return Response(data=str(e.message), status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response(data=str(e.message), status=status.HTTP_400_BAD_REQUEST)

            finally:
                source_file.close()
                file_errros.close()
        return Response(data="success", status=status.HTTP_200_OK)


class ExportData(APIView):
    """
     The request is in form:
     [
          {
               center : { id : 1 , center_name: c1, ...   } ,
               suppliers: [  'RS' : [ { 'supplier_type_code': 'RS', 'status': 'R', 'supplier_id' : '1'}, {...}, {...} ]
               suppliers_meta: {
                                  'RS': { 'inventory_type_selected' : [ 'PO', 'POST', 'ST' ]  },
                                  'CP': { 'inventory_type_selected':  ['ST']
               }
          }
     ]
     Exports supplier data on grid view page.
     The API is divided into two phases :
     1. extension of Headers and DATA keys. This is because one or more inventory type selected map to more HEADER
     and hence more DATA keys
     2. Making of individual rows. Number of rows in the sheet is equal to total number of societies in all centers combined
    """

    def post(self, request, proposal_id=None, format=None):
        try:
            wb = Workbook()

            # ws = wb.active
            ws = wb.create_sheet(index=0, title='Shortlisted Spaces Details')

            # iterating through centers in request.data array
            for center in request.data:

                supplier_codes = center['supplier_codes']

                inventory_array = center['inventory_type_selected']

                # get the unique codes by combining all the codes
                response = website_utils.get_unique_inventory_codes(inventory_array)

                if not response.data['status']:
                    return response
                unique_inventory_codes = response.data['data']

                # get the union of HEADERS
                response = website_utils.get_union_keys_inventory_code('HEADER', unique_inventory_codes)
                if not response.data['status']:
                    return response
                extra_header_keys = response.data['data']

                # get the union of DATA
                response = website_utils.get_union_keys_inventory_code('DATA', unique_inventory_codes)
                if not response.data['status']:
                    return response
                extra_supplier_keys = response.data['data']

                # extend the society_keys
                society_keys.extend(extra_supplier_keys)

                # extend the proposal_header_keys
                proposal_header_keys.extend(extra_header_keys)

            # remove duplicates if any
            proposal_header_keys = website_utils.remove_duplicates_preserver_order(proposal_header_keys)
            society_keys = website_utils.remove_duplicates_preserver_order(society_keys)

            # set the final headers in the sheet
            for col in range(1):
                ws.append(proposal_header_keys)

            # populate sheet row by row. Number of rows will be equal to number of societies. 1 society = 1 row
            master_list = []
            # for all centers in request.data

            for center in request.data:
                # get the inventory_array containg all the codes selected for this center
                inventory_array = center['inventory_type_selected']

                # get the unique codes by combining all the codes
                response = website_utils.get_unique_inventory_codes(inventory_array)
                if not response.data['status']:
                    return response
                unique_inventory_codes = response.data['data']

                # for all societies in societies array
                for index, item in enumerate(center['suppliers']):

                    # iterate over center_keys and make a partial row with data from center object
                    center_list = []
                    for key in center_keys:
                        center_list.append(center['center'][key])

                    # add space mapping id
                    # center_list.append(center['center']['space_mappings']['id'])

                    # add inventory type id
                    # center_list.append(center['societies_inventory']['id'])

                    # calculates inventory price per flat and  store the result in dict itself
                    local_list = []

                    # modify the dict with extra keys for pricing
                    response = website_utils.get_union_inventory_price_per_flat(item, unique_inventory_codes, index)
                    if not response.data['status']:
                        return response
                    item = response.data['data']

                    # use the modified dict in the getList function that makes a list out of keys present in society_keys
                    temp = website_utils.getList(item, society_keys)
                    local_list.extend(temp)

                    # append this list to center_list to make final row.
                    center_list.extend(local_list)

                    # add row to the sheet
                    ws.append(center_list)

            file_name = 'machadalo_{0}.xlsx'.format(str(datetime.datetime.now()))
            wb.save(file_name)

            return Response(data={"successs"})
        except Exception as e:
            return Response(data={'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)


class GenericExportData(APIView):
    """
        The request is in form:
        [
             {
                  center : { id : 1 , center_name: c1, ...   } ,
                  suppliers: { 'RS' : [ { 'supplier_type_code': 'RS', 'status': 'R', 'supplier_id' : '1'}, {...}, {...} }
                  suppliers_meta: {
                                     'RS': { 'inventory_type_selected' : [ 'PO', 'POST', 'ST' ]  },
                                     'CP': { 'inventory_type_selected':  ['ST']
                  }
             }
        ]
        Exports supplier data on grid view page.
        The API is divided into two phases :
        1. extension of Headers and DATA keys. This is because one or more inventory type selected map to more HEADER
        and hence more DATA keys
        2. Making of individual rows. Number of rows in the sheet is equal to total number of societies in all centers combined
    """
    def post(self, request, proposal_id=None):
        class_name = self.__class__.__name__
        try:
            workbook = Workbook()

            # ws = wb.active
            # ws = wb.create_sheet(index=0, title='Shortlisted Spaces Details')
            # iterating through centers in request.data array

            data = request.data

            # get the supplier type codes available in the request
            response = website_utils.unique_supplier_type_codes(data)
            if not response.data['status']:
                return response
            unique_supplier_codes = response.data['data']

            result = {}

            # initialize the result = {} dict which will be used in inserting into sheet
            response = website_utils.initialize_export_final_response(unique_supplier_codes, result)
            if not response.data['status']:
                return response
            result = response.data['data']

            # collect all the extra header and database keys for all the supplier type codes and all inv codes in them
            response = website_utils.extra_header_database_keys(unique_supplier_codes, data, result)
            if not response.data['status']:
                return response
            result = response.data['data']

            # make the call to generate data in the result
            response = website_utils.make_export_final_response(result, data)
            if not response.data['status']:
                return response
            result = response.data['data']

            # print result
            response = website_utils.insert_supplier_sheet(workbook, result)
            if not response.data['status']:
                return response
            workbook = response.data['data']

            # make a file name for this file
            response = website_utils.get_file_name(request.user, proposal_id)
            if not response.data['status']:
                return response
            file_name = response.data['data']
            workbook.save(file_name)

            return website_utils.send_excel_file(file_name)

            #return ui_utils.handle_response(class_name, data=workbook, success=True)

        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class ImportSupplierData(APIView):
    """
    This API basically takes an excel sheet , process the data and saves it in the database.

    The request by which the sheet is made  is in form:
    [
         {
              center : { id : 1 , center_name: c1, ...   } ,
              suppliers: { 'RS' : [ { 'supplier_type_code': 'RS', 'status': 'R', 'supplier_id' : '1'}, {...}, {...} }
              suppliers_meta: {
                                 'RS': { 'inventory_type_selected' : [ 'PO', 'POST', 'ST' ]  },
                                 'CP': { 'inventory_type_selected':  ['ST']
              }
         }
    ]
    """
    def post(self, request, proposal_id=None):
        """
        Args:
            request: request param
            proposal_id: proposal_id

        Returns: Saves the  data in db
        """
        class_name = self.__class__.__name__
        try:

            if not request.FILES:
                return ui_utils.handle_response(class_name, data='No File Found')
            my_file = request.FILES['file']
            wb = openpyxl.load_workbook(my_file)

            # fetch all sheets
            all_sheets = wb.get_sheet_names()

            # iterate over multiple sheets
            for sheet in all_sheets:

                # fetch supplier_type_code from sheet name
                supplier_type_code = website_constants.sheet_names_to_codes.get(sheet)
                if not supplier_type_code:
                    continue

                # fetch the worksheet object to work with
                ws = wb.get_sheet_by_name(sheet)

                # fetch all the center id's
                center_id_list_response = website_utils.get_center_id_list(ws, index_of_center_id)

                if not center_id_list_response.data['status']:
                    return center_id_list_response

                center_id_list = center_id_list_response.data['data']

                # normalize the center id's or map the actual center id's with indexes starting from zero
                center_id_to_index_mapping = {}
                result = []
                for index, center_id in enumerate(center_id_list):
                    result.append({})
                    center_id_to_index_mapping[center_id] = index

                # iterate through all rows and populate result array
                for index, row in enumerate(ws.iter_rows()):
                    if index == 0:
                        continue

                    """
                      Number of rows in 'result' is number of distinct centers. each center has a center_id which is mapped
                      to an index in the 'result' list. each element of result list is a center_object.
                      Goal is to populate the right center_object with data of it's 3 keys:
                     'societies_inventory', 'societies', 'center'

                    """
                    # in order to proceed further we need a dict in which keys are header names with spaces
                    # removed and values are value of the row which we are processing

                    row_response = website_utils.get_mapped_row(ws, row)
                    if not row_response.data['status']:
                        return row_response
                    row = row_response.data['data']

                    # get the center index mapped for this center_id
                    center_index = center_id_to_index_mapping[int(row['center_id'])]

                    # get the actual center_object from result list to process further
                    center_object = result[center_index]

                    # initialize the center_object  with necessary keys if not already
                    if not center_object:
                        response = website_utils.initialize_keys(center_object, supplier_type_code)
                        if not response.data['status']:
                            return response
                        center_object = response.data['data']

                    # add 1 society that represents this row to the list of societies this object has already
                    response = website_utils.make_suppliers(center_object, row, supplier_type_code)
                    if not response.data['status']:
                        return response
                    center_object = response.data['data']

                    # add the 'center' data  in center_object
                    response = website_utils.make_center(center_object, row)
                    if not response.data['status']:
                        return response
                    center_object = response.data['data']

                    # update the center dict in result with modified center_object
                    result[center_index] = center_object

                # populate the shortlisted_inventory_details table before hiting the url
                response = website_utils.populate_shortlisted_inventory_details(result)
                if not response.data['status']:
                    return response

                # time to hit the url to create-final-proposal that saves shortlisted suppliers and filters data
                # once data is prepared for one sheet, we hit the url. if it creates problems in future, me might change
                # it.
                url = reverse('create-final-proposal', kwargs={'proposal_id': proposal_id})
                url = BASE_URL + url[1:]

                data = result
                headers={
                    'Content-Type': 'application/json'
                }
                response = requests.post(url, json.dumps(data), headers=headers)

                if response.status_code != status.HTTP_200_OK:
                    return Response({'status': False, 'error in final proposal api ': response.text}, status=status.HTTP_400_BAD_REQUEST)

            # hit metric url to save metric data. current m sending the entire file, though only first sheet sending
            # is required.
            url = reverse('import-metric-data', kwargs={'proposal_id': proposal_id})
            url = BASE_URL + url[1:]

            # set the pointer to zero to be read again in next api
            my_file.seek(0)
            files = {
                'file': my_file
            }
            response = requests.post(url, files=files)

            if response.status_code != status.HTTP_200_OK:
                return Response({'status': False, 'error in import-metric-data api ': response.text},
                                status=status.HTTP_400_BAD_REQUEST)

            return Response({'status': True, 'data': 'successfully imported'}, status=status.HTTP_200_OK)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class ImportProposalCostData(APIView):
    """
    The class is responsible for importing proposal cost data from an excel sheet.
    All the import api's heavily depend upon the structure of the sheet which it's importing.
    so if you are trying to understand what this api does, understand the structure of the sheet first.

    two phases: data collection and data insertion.
    """
    def post(self, request, proposal_id):

        class_name = self.__class__.__name__

        if not request.FILES:
            return ui_utils.handle_response(class_name, data='No files found')

        file = request.FILES['file']
        # load the workbook
        wb = openpyxl.load_workbook(file)
        # read the sheet
        ws = wb.get_sheet_by_name(website_constants.metric_sheet_name)

        # before inserting delete all previous data as we don't want to duplicate things.
        response = website_utils.delete_proposal_cost_data(proposal_id)
        if not response.data['status']:
            return response

        with transaction.atomic():
            try:
                count = 0
                master_data = {}
                # DATA COLLECTION  in order to  collect data in master_data, initialize with proper data structures
                master_data = website_utils.initialize_master_data(master_data)
                for index, row in enumerate(ws.iter_rows()):

                    # ignore empty rows
                    if website_utils.is_empty_row(row):
                        continue
                    # send one row for processing
                    response = website_utils.handle_offline_pricing_row(row, master_data)
                    if not response.data['status']:
                        return response
                    # update master_data with response
                    master_data = response.data['data']
                    count += 1

                # DATA INSERTION time to save the data
                master_data['proposal_master_cost']['proposal'] = proposal_id
                response = website_utils.save_master_data(master_data)
                if not response.data['status']:
                    return response
                return ui_utils.handle_response(class_name, data='successfully imported.Saved {0} rows'.format(count),
                                                success=
                                                True)
            except Exception as e:
                return ui_utils.handle_response(class_name, exception_object=e)


class CreateInitialProposal(APIView):
    """
    This is first step in creating proposal. Basic data get's stored here.
    because we have reduced number of models in which Proposal
    data is stored hence we have created new classes CreateInitialProposal and CreateFinalProposal API.
    author: nikhil
    """

    def post(self, request, account_id):
        """
        Args:
            request: request param
            proposal_id:  proposal_id for which data is to be saved


        Returns: success or failure depending an initial proposal is created or not.

        """
        class_name = self.__class__.__name__
        try:

            with transaction.atomic():
                proposal_data = request.data

                # create a unique proposal id
                proposal_data['proposal_id'] = website_utils.create_proposal_id()

                # get the account object. required for creating the proposal
                account = AccountInfo.objects.get(account_id=account_id)
                proposal_data['account'] = account.account_id

                # query for parent. if available set it. if it's available, then this is an EDIT request.
                parent = request.data.get('parent')

                # set parent if available
                if parent:
                    parent_proposal = ProposalInfo.objects.get(proposal_id=parent)
                    proposal_data['parent'] = parent_proposal.proposal_id

                # call the function that saves basic proposal information
                response = website_utils.create_basic_proposal(proposal_data)
                if not response.data['status']:
                    return response

                # time to save all the centers data
                response = website_utils.save_center_data(proposal_data)
                if not response.data['status']:
                    return response

                # return the proposal_id of the new proposal created
                return ui_utils.handle_response(class_name, data=proposal_data['proposal_id'], success=True)
        except Exception as e:
             return ui_utils.handle_response(class_name, exception_object=e)


class CreateFinalProposal(APIView):
    """
    The request is in form:
        [
             {
                  center : { id : 1 , center_name: c1, ...   } ,
                  suppliers:  { 'RS' : [ { 'supplier_type_code': 'RS', 'status': 'R', 'supplier_id' : '1'}, {...}, {...}  }
                  suppliers_meta: {
                                     'RS': { 'inventory_type_selected' : [ 'PO', 'POST', 'ST' ]  },
                                     'CP': { 'inventory_type_selected':  ['ST']
                  }
             }
        ]
    This is second step for creating proposal.
    The proposal_id in the request is always a brand new proposal_id wether you hit this API from an EDIT form of
    the proposal or you are creating an entirely new proposal.

    structure of request.data is  a list. item of the list is the one center information. inside center
    information we have all the suppliers shortlisted, all the Filters and all.

    """

    def post(self, request, proposal_id):
        """
        Args:
            request: request data
            proposal_id: proposal_id to be updated
            author: nikhil

        Returns: success if data is saved successfully.
        """
        class_name = self.__class__.__name__
        try:
            # simple dict to count new objects created each time the API is hit. a valuable information.

            # to keep count of new objects created
            objects_created = {
                'SHORTLISTED_SUPPLIERS': 0,
                'FILTER_OBJECTS': 0
            }
            # get the supplier type codes available in the request
            response = website_utils.unique_supplier_type_codes(request.data)
            if not response.data['status']:
                return response
            unique_supplier_codes = response.data['data']

            with transaction.atomic():
                for proposal_data in request.data:

                    proposal_data['proposal_id'] = proposal_id
                    response = website_utils.save_final_proposal(proposal_data, unique_supplier_codes)
                    if not response.data['status']:
                        return response
                    objects_created['SHORTLISTED_SUPPLIERS'] += response.data['data']['SHORTLISTED_SUPPLIERS']
                    objects_created['FILTER_OBJECTS'] += response.data['data']['FILTER_OBJECTS']

                return ui_utils.handle_response(class_name, data=objects_created, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class ProposalViewSet(viewsets.ViewSet):
    """
     A ViewSet handling various operations related to ProposalModel.
     This viewset was made instead of creating separate ApiView's because all the api's in this viewset
     are related to Proposal domain. so keeping them at one place makes sense.
    """
    parser_classes = (JSONParser, FormParser)

    def retrieve(self, request, pk=None):
        """
        Fetches one Proposal object
        Args:
            request: request parameter
            pk: primary key of proposal

        Returns: one proposal object

        """
        class_name = self.__class__.__name__
        try:
            proposal = ProposalInfo.objects.get(proposal_id=pk)
            serializer = ProposalInfoSerializer(proposal)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    @detail_route(methods=['POST'])
    def get_spaces(self, request, pk=None):
        """
        The API  fetches all the data required to display on the grid view page.
        response looks like :
        {
           'status': true,
           'data' : [
                {
                   suppliers: { RS: [], CP: [] } ,
                   center: { ...   codes: [] }
                }
           ]

        }
        Args:
            request:  request param
            pk: proposal_id
        Returns: collects data for all shortlisted suppliers and filters and send them.
        ---
        parameters:
        - name: center_id
          description:  center_id
        - name: radius
          description: radius
        - name: supplier_codes
          description:  array of codes like RS, CP, etc
        """
        class_name = self.__class__.__name__
        try:
            center_id = request.data.get('center_id')
            radius = request.data.get('radius')
            latitude = request.data.get('latitude')
            longitude = request.data.get('longitude')

            data = {
                'proposal_id': pk,
                'center_id': center_id,
                'radius': radius,
                'latitude': latitude,
                'longitude': longitude
            }
            response = website_utils.suppliers_within_radius(data)
            if not response.data['status']:
                return response

            return ui_utils.handle_response(class_name, data=response.data['data'], success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    @detail_route(methods=['GET'])
    def child_proposals(self, request, pk=None):
        """
        Fetches all proposals who have parent = pk
        Args:
            request: request param
            pk: parent pk value. if pk == '0',this means we need to fetch all proposals whose parent is NULL.

        Returns:

        """
        class_name = self.__class__.__name__
        try:
            data = {
                'parent': pk if pk != '0' else None
            }
            response = website_utils.child_proposals(data)
            if not response:
                return response
            return ui_utils.handle_response(class_name, data=response.data['data'], success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    @detail_route(methods=['GET'])
    def shortlisted_suppliers(self, request, pk=None):
        """
        Fetches all shortlisted suppliers for this proposal.
        Response looks like :
        {
           'status': true,
           'data' : [
                {
                   suppliers: { RS: [], CP: [] } ,
                   center: { ...   codes: [] }
                }
           ]
        }

        Args:
            request: request
            pk: pk

        Returns:

        """
        class_name = self.__class__.__name__
        try:
            data = {
                'proposal_id': pk
            }
            response = website_utils.proposal_shortlisted_spaces(data)
            if not response.data['status']:
                return response
            return ui_utils.handle_response(class_name, data=response.data['data'], success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class InitialProposalAPIView(APIView):
    '''This API creates initial proposal when the user enters the center(address, name etc.) and basic proposal
    fields are stored in the database
    ProposalInfo and ProposalCenterMapping models are used only'''

    def post(self, request, account_id=None, format=None):
        '''In this centers contain format like
        centers : [
            center : [
                space_mapping : []
            ]
            society_inventory : []  // these will be made if in center[space_mapping][society_allowed] is true
            corporate_inventory : []
        ]
        This is done to be in sync with the format on map view page as serializers.data dont allow to append
        any new (key,value) pair to its existing data
        '''

        supplier_codes = {
            'society' : 'RS',   'corporate' : 'CP',
            'gym' : 'GY',       'salon' : 'SA'
        }

        with transaction.atomic():
            proposal_data = request.data
            proposal_data['proposal_id'] = self.create_proposal_id()
            try:
                account = AccountInfo.objects.get(account_id=account_id)
            except AccountInfo.DoesNotExist:
                return Response({'message':'Invalid Account ID'}, status=406)
            proposal_data['account'] = account.account_id
            try:
                proposal_object = ProposalInfo.objects.get(proposal_id=proposal_data['proposal_id'])
                # id already exists --> Do something
                return Response(status=404)
            except ProposalInfo.DoesNotExist:
                proposal_serializer = ProposalInfoSerializer(data=proposal_data)

                if proposal_serializer.is_valid():
                    proposal_object = proposal_serializer.save()
                else:
                    return Response({'message' : 'Invalid Proposal Info', 'errors' : \
                        proposal_serializer.errors}, status=406)

                for center_info in proposal_data['centers']:
                    center = center_info['center']
                    space_mapping = center['space_mapping']
                    center['proposal'] = proposal_object.proposal_id
                    address = center['address'] + "," + center['subarea'] + ',' + center['area'] + ',' + center['city'] + ' ' + center['pincode']
                    geocoder = Geocoder(api_key='AIzaSyCy_uR_SVnzgxCQTw1TS6CYbBTQEbf6jOY')
                    try:
                        geo_object = geocoder.geocode(address)
                    except GeocoderError:
                        ProposalInfo.objects.get(proposal_id=proposal_object.proposal_id).delete()
                        return Response({'message' : 'Latitude Longitude Not found for address : ' + address}, status=406)
                    except ConnectionError:
                        ProposalInfo.objects.get(proposal_id=proposal_object.proposal_id).delete()
                        return Response({'message' : 'Unable to connect to google Maps'}, status=406)

                    center['latitude'] = geo_object.latitude
                    center['longitude'] = geo_object.longitude

                    center_serializer = ProposalCenterMappingSerializer(data=center)

                    if center_serializer.is_valid():
                        center_object = center_serializer.save()
                    else:
                        ProposalInfo.objects.get(proposal_id=proposal_object.proposal_id).delete()
                        return Response({'message' : 'Invalid Center Data', 'errors' : center_serializer.errors},\
                            status=406)

                    space_mapping['center'] = center_object.id
                    space_mapping['proposal'] = proposal_object.proposal_id
                    space_mapping_serializer = SpaceMappingSerializer(data=space_mapping)
                    if space_mapping_serializer.is_valid():
                        space_mapping_object = space_mapping_serializer.save()
                    else:
                        ProposalInfo.objects.get(proposal_id=proposal_object.proposal_id).delete()
                        return Response({
                                'message' : 'Invalid Space Mapping Data',
                                'errors' : space_mapping_serializer.errors
                            }, status=406)


                    # ADDNEW --> extend the list in for loop when new spaces added. Keep the variables names accordingly
                    for space in ['society','corporate','gym','salon']:
                        ''' This loops checks if the space is allowed and if it is allowed save the
                        inventory types chosen by the user in the inventory_type table '''
                        try:
                            space_allowed = space + '_allowed'
                            if space_mapping[space_allowed]:
                                space_inventory = space + '_inventory'
                                center_info[space_inventory]['supplier_code'] = supplier_codes[space]
                                center_info[space_inventory]['space_mapping'] = space_mapping_object.id
                                inventory_type_serializer = InventoryTypeSerializer(data=center_info[space_inventory])
                                if inventory_type_serializer.is_valid():
                                    inventory_type_serializer.save()
                                else:
                                    ProposalInfo.objects.get(proposal_id=proposal_object.proposal_id).delete()
                                    return Response({
                                            'message' : 'Invalid Inventory Type Info',
                                            'errors' : inventory_type_serializer.errors
                                        })
                        except KeyError:
                            pass


        return Response(proposal_object.proposal_id,status=200)

    def create_proposal_id(self):
        import random, string
        return ''.join(random.choice(string.ascii_letters) for _ in range(8))


class ImportContactDetails(APIView):
    """
    Saves contact details in db for each supplier.
    The API expects source file to be named as contacts.csv and should be placed in a folder called 'file'.
    """

    def get(self, request):

        with transaction.atomic():

            file = open(BASE_DIR + '/files/contacts.csv', 'rb')
            file_errros = open(BASE_DIR + '/files/contacts_errors.txt', 'w')

            try:
                reader = csv.reader(file)
                total_count = sum(1 for row in reader) - 1
                failure_count = 0
                file.seek(0)
                for num, row in enumerate(reader):
                    if num == 0:
                        continue
                    else:
                        data = {}
                        for index, key in enumerate(contact_keys):
                            if row[index] == '':
                                data[key] = None
                            else:
                                data[key] = row[index]

                        landline_number = data['landline'].split('-')
                        data['landline'] = landline_number[1]
                        data['std_code'] = landline_number[0]
                        data['country_code'] = COUNTRY_CODE
                        try:
                            response = get_supplier_id(request, data)
                            # this method of handing error code will  change in future
                            if response.status_code == status.HTTP_200_OK:
                                data['supplier_id'] = response.data['supplier_id']
                            else:
                                file_errros.write("Error in generating supplier id {0} ".format(response.data['error']))
                                failure_count += 1
                                continue
                            society_object = SupplierTypeSociety.objects.get(supplier_id=data['supplier_id'])
                            data['spoc'] = False
                            data['supplier'] = society_object
                            contact_object = ContactDetails()
                            contact_object.__dict__.update(data)
                            contact_object.save()

                        except ObjectDoesNotExist as e:
                            file_errros.write("Supplier object not found for {0}".format(data['supplier_id']))
                            failure_count += 1
                            continue
                        except Exception as e:
                            return Response(data={str(e.message)}, status=status.HTTP_400_BAD_REQUEST)

            finally:
                file.close()
                file_errros.close()
        return Response(
            data="Information: out of {0} rows, {1} successfully inserted and {2} failed ".format(total_count,
                                                                                                  total_count - failure_count,
                                                                                                  failure_count),
            status=status.HTTP_200_OK)


class ImportCampaignLeads(APIView):
    """
    The api to import campaign leads data
    """

    def post(self, request):
        class_name = self.__class__.__name__
        if not request.FILES:
            return ui_utils.handle_response(class_name, data='No File Found')
        my_file = request.FILES['file']
        wb = openpyxl.load_workbook(my_file)

        ws = wb.get_sheet_by_name('campaign_leads')

        result = []

        try:
            # iterate through all rows and populate result array
            for index, row in enumerate(ws.iter_rows()):
                if index == 0:
                    continue

                # make a dict of the row
                row_response = website_utils.get_mapped_row(ws, row)
                if not row_response.data['status']:
                    return row_response
                row = row_response.data['data']

                # handle it
                response = website_utils.handle_campaign_leads(row)
                if not response.data['status']:
                    return response

                result.append(response.data['data'])
            return ui_utils.handle_response(class_name, data=result, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class SupplierSearch(APIView):
    """
    Generic API to perform simple search on predefined fields. The API will be slow because search uses
    basic icontains query. It can be made faster by making  FULLTEXT indexes on the db columns
    todo: attach user level permissions later
    """

    def get(self, request):

        class_name = self.__class__.__name__
        try:
            search_txt = request.query_params.get('search')
            supplier_type_code = request.query_params.get('supplier_type_code')
            if not supplier_type_code:
                return ui_utils.handle_response(class_name, data='provide supplier type code')

            if not search_txt:
                return ui_utils.handle_response(class_name, data=[], success=True)

            model = ui_utils.get_model(supplier_type_code)
            search_query = Q()
            for search_field in website_constants.search_fields[supplier_type_code]:
                if search_query:
                    search_query |= Q(**{search_field: search_txt})
                else:
                    search_query = Q(**{search_field: search_txt})

            suppliers = model.objects.filter(search_query)
            serializer_class = ui_utils.get_serializer(supplier_type_code)
            serializer = serializer_class(suppliers, many=True)
            if supplier_type_code == 'RS':
                for supplier in serializer.data:
                    for society_key, common_key in website_constants.society_common_keys.iteritems():
                        supplier_key_value = supplier[society_key]
                        del supplier[society_key]
                        supplier[common_key] = supplier_key_value

            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except ObjectDoesNotExist as e:
            return ui_utils.handle_response(class_name, exception_object=e)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class ImportAreaSubArea(APIView):
    """
    This API populates AREA and SUBAREA tables from an excel sheet.
    """
    def post(self, request):
        """
        Args:
            request: request data
            The data structure it makes is to create a list of form
             [
                { 'state': {}, 'city': {}, 'area': {}, 'subarea': {} },
                { 'state': {}, 'city': {}, 'area': {}, 'subarea': {} },
             ]
             The structure of this data structure does not follows FK relationships in the table. This is because
             constructing this data structure is far more easier than constructing the one which follows FK relationships
             which will add more complexity.
        Returns:

        """
        class_name = self.__class__.__name__
        try:
            # fetch the file from files dir
            my_file = open(BASE_DIR + '/files/new_area_subarea.xlsx', 'rb')
            wb = openpyxl.load_workbook(my_file)
            ws = wb.get_sheet_by_name('new_area_sheet')

            result = []
            result_index = 0

            # iterate through all rows and populate result array
            for index, row in enumerate(ws.iter_rows()):

                if index == 0 or website_utils.is_empty_row(row):
                    continue

                result.extend([None])
                # in order to proceed further we need a dict in which keys are header names with spaces
                # removed and values are value of the row which we are processing
                row_response = website_utils.get_mapped_row(ws, row)
                if not row_response.data['status']:
                    return row_response
                row = row_response.data['data']

                response = website_utils.initialize_area_subarea(result, result_index)
                if not response.data['status']:
                    return response
                result = response.data['data']

                response = website_utils.handle_states(result, result_index, row)
                if not response.data['status']:
                    return response
                result = response.data['data']

                response = website_utils.handle_city(result, result_index, row)
                if not response.data['status']:
                    return response
                result = response.data['data']

                response = website_utils.handle_area(result, result_index, row)
                if not response.data['status']:
                    return response
                result = response.data['data']

                response = website_utils.handle_subarea(result, result_index, row)
                if not response.data['status']:
                    return response
                result = response.data['data']

                result_index += 1

            # once the data is collected, time to save it
            response = website_utils.save_area_subarea(result)
            if not response.data['status']:
                return response

            return ui_utils.handle_response(class_name, data=response.data['data'], success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


