import math, random, string, operator
#import tablib
import csv
import json
import datetime
import os

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.urlresolvers import reverse
from django.db.models import Q, Sum,F
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings
from django.utils import timezone
from django.forms.models import model_to_dict
from django.db.models import get_model
from django.utils.dateparse import parse_datetime

from pygeocoder import Geocoder, GeocoderError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from openpyxl import Workbook
from openpyxl.compat import range
import requests
from rest_framework.parsers import JSONParser, FormParser
from bulk_update.helper import bulk_update

from rest_framework import permissions
import openpyxl

# from import_export import resources

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

from v0.models import City, CityArea, CitySubArea
from coreapi.settings import BASE_URL, BASE_DIR
from v0.ui.utils import get_supplier_id
import utils as website_utils
import v0.ui.utils as ui_utils
import v0.models as models
import serializers as website_serializers
import constants as website_constants
import renderers as website_renderers
import v0.ui.constants as ui_constants
import v0.serializers as v0_serializers
import v0.permissions as v0_permissions
import v0.utils as v0_utils
from v0 import errors
import v0.constants as v0_constants


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
    # permission_classes = (v0_permissions.IsGeneralBdUser, )

    def get(self, request):
        """
        Fetches al businesses belonging to a particular group to which a user belongs.
        Args:
            request: The Request object

        Returns: All businesses.
        """
        class_name = self.__class__.__name__
        try:
            items = BusinessInfo.objects.filter_user_related_objects(user=request.user)
            serializer = BusinessInfoSerializer(items, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

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


class BusinessAccounts(APIView):
    """
    Fetches one buissiness data
    """
    # permission_classes = (v0_permissions.IsGeneralBdUser, )

    def get(self, request, id):
        class_name = self.__class__.__name__
        try:
            item = BusinessInfo.objects.get_user_related_object(user=request.user, pk=id)
            business_serializer = UIBusinessInfoSerializer(item)
            accounts = AccountInfo.objects.filter_user_related_objects(user=request.user, business=item)
            accounts_serializer = UIAccountInfoSerializer(accounts, many=True)
            response = {
                'business': business_serializer.data,
                'accounts': accounts_serializer.data
            }
            return Response(response, status=200)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class Accounts(APIView):

    # permission_classes = (v0_permissions.IsGeneralBdUser, )

    def get(self, request, format=None):
        class_name = self.__class__.__name__
        try:
            items = AccountInfo.objects.filter_user_related_objects(user=request.user)
            serializer = AccountInfoSerializer(items, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class AccountAPIView(APIView):

    # permission_classes = (v0_permissions.IsGeneralBdUser, )

    def get(self, request, id, format=None):

        class_name = self.__class__.__name__

        try:
            account = AccountInfo.objects.get_user_related_object(user=request.user, pk=id)
            account_serializer = UIAccountInfoSerializer(account)
            business = BusinessInfo.objects.get(pk=account.business_id)
            business_serializer = BusinessInfoSerializer(business)
            '''contacts = AccountContact.objects.filter(account=account)
            serializer3 = AccountContactSerializer(contacts, many=True)'''

            data = {'account': account_serializer.data, 'business': business_serializer.data}
            return Response(data, status=200)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class BusinessContacts(APIView):

    # permission_classes = (v0_permissions.IsGeneralBdUser,)

    def post(self, request):
        class_name = self.__class__.__name__
        """

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

        business_data['type_name'] = business_data['business_type_id']
        business_data['sub_type'] = business_data['sub_type_id']

        type_name = BusinessTypes.objects.get(id=int(business_data['business_type_id']))
        sub_type = BusinessSubTypes.objects.get(id=int(business_data['sub_type_id']))

        business_data['user'] = current_user.id
        try:
            with transaction.atomic():

                business_serializer_data = {}

                if 'business_id' in business_data:
                    business = BusinessInfo.objects.get_user_related_object(user=request.user, pk=business_data['business_id'])
                    serializer = BusinessInfoSerializer(business, data=business_data)
                else:
                    business_data['business_id'] = self.generate_business_id(business_name=business_data['name'], \
                                                                             sub_type=sub_type, type_name=type_name)
                    if business_data['business_id'] is None:
                        # if business_id is None --> after 12 attempts couldn't get unique id so return first id in lowercase
                        business_data['business_id'] = self.generate_business_id(business_data['name'], \
                                                                                 sub_type=sub_type, type_name=type_name,
                                                                                 lower=True)
                    serializer = BusinessInfoSerializer(data=business_data)

                if serializer.is_valid():
                     serializer.save()
                     business_serializer_data = serializer.data
                     business_serializer_data['business_sub_type'] = sub_type.business_sub_type
                     business_serializer_data['business_type'] = type_name.business_type

                business = BusinessInfo.objects.get_user_related_object(user=current_user, pk=business_data['business_id'])
                content_type_business = ContentType.objects.get_for_model(BusinessInfo)
                contact_ids = list(business.contacts.all().values_list('id', flat=True))
                contact_list = []

                for contact in business_data['contacts']:

                    contact['object_id'] = business.business_id
                    contact['content_type'] = content_type_business.id
                    contact['user'] = current_user.id

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

                    if contact_serializer.is_valid():
                        contact = contact_serializer.save()
                        contact_list.append(contact)
                    else:
                        return ui_utils.handle_response(class_name, data=contact_serializer.errors)

                # deleting all contacts whose id not received from the frontend
                BusinessAccountContact.objects.filter(id__in=contact_ids).delete()

                contacts_serializer = BusinessAccountContactSerializer(contact_list, many=True)
                business_serializer = UIBusinessInfoSerializer(business)

                response = {
                    'business': business_serializer.data,
                    'contacts': contacts_serializer.data,
                }
                return Response(response, status=200)
        except Exception as e:
                return Response(data={'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)

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


class AccountContacts(APIView):
    """
    API creates Account for a business
    """
    def post(self, request):
        class_name = self.__class__.__name__
        try:
            response = {}
            current_user = request.user

            account_data = request.data['account']

            with transaction.atomic():

                business_id = account_data['business_id']
                # checking a valid business

                business = BusinessInfo.objects.get_user_related_object(user=current_user, business_id=business_id)

                if 'account_id' in account_data:
                    account = AccountInfo.objects.get_user_related_object(user=current_user, pk=account_data['account_id'])
                    serializer = AccountInfoSerializer(account,data=account_data)
                else:
                    account_data['account_id']= self.generate_account_id(account_name=account_data['name'],business_id=business_id)
                    if account_data['account_id'] is None:
                        # if account_id is None --> after 12 attempts couldn't get unique id so return first id in lowercase
                        account_data['account_id'] = self.generate_account_id(account_name=account_data['name'],business_id=business_id, lower=True)
                    serializer = AccountInfoSerializer(data=account_data)

                if serializer.is_valid():
                    account = serializer.save(business=business, user=current_user)
                else:
                    return Response(serializer.errors, status=400)

                content_type_account = ContentType.objects.get_for_model(AccountInfo)

                # #here we will start storing contacts
                contact_ids = list(account.contacts.all().values_list('id',flat=True))
                contact_list = []

                for contact in account_data['contacts']:
                    contact['object_id'] = account.account_id
                    contact['content_type'] = content_type_account.id
                    contact['user'] = current_user.id

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
                account_serializer = AccountInfoSerializer(account)
                contacts_serializer = BusinessAccountContactSerializer(contact_list, many=True)
                response['account'] = account_serializer.data
                response['contacts'] = contacts_serializer.data
            return Response(response, status=200)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

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
            while True:
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
                inv_details = InventorySummary.objects.get_supplier_type_specific_object(request.data.copy(), id)
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
                        society_inventory_obj = InventorySummary.objects.get_supplier_type_specific_object(request.data.copy(),
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
                        corporate_inventory_obj = InventorySummary.objects.get_supplier_type_specific_object(request.data.copy(), corporate['supplier_id'])
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
                    society_inventory_obj = InventorySummary.objects.get_supplier_type_specific_object(request.data.copy(),
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
          'common_filters': { 'latitude': 12, 'longitude': 11, 'radius': 2, 'quality': [ 'UH', 'H' ],'quantity': ['VL'] }
          'inventory_filters': ['PO', 'ST'],
          'amenities': [ ... ]
          'specific_filters': { 'real_estate_allowed': True, 'employees_count': {min: 10, max: 100},}
          'center_id': '23',
          'proposal_id': 'abc'
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

            common_filters = request.data.get('common_filters')  # maps to BaseSupplier Model or a few other models.
            inventory_filters = request.data.get('inventory_filters')  # maps to InventorySummary model
            specific_filters = request.data.get('specific_filters')  # maps to specific supplier table
            proposal_id = request.data.get('proposal_id')
            center_id = request.data.get('center_id')
            amenities = request.data.get('amenities')
            is_standalone_society = request.data.get('is_standalone_society')
            ratio_of_tenants_to_flats = request.data.get('ratio_of_tenants_to_flats')  # cannot be handled  under specific society filters because it involves operation of two columns in database which cannot be generalized to a query.
            # To get business name
            proposal = models.ProposalInfo.objects.get(proposal_id=proposal_id)
            business_name = proposal.account.business.name

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

            master_suppliers_list = set(list(supplier_model.objects.filter(common_filters_query).values_list('supplier_id', flat=True)))

            # now fetch all inventory_related suppliers
            # handle inventory related filters. it involves quite an involved logic hence it is in another function.
            response = website_utils.handle_inventory_filters(inventory_filters)
            if not response.data['status']:
                return response
            inventory_type_query = response.data['data']

            if inventory_type_query.__len__():
                inventory_type_query &= Q(content_type=content_type)
                inventory_type_query_suppliers = set(list(models.InventorySummary.objects.filter(inventory_type_query).values_list('object_id', flat=True)))

            # fetch specific_filters suppliers
            response = website_utils.handle_specific_filters(specific_filters, supplier_type_code)
            if not response.data['status']:
                return response
            specific_filters_query = response.data['data']
            # if indeed there was something in the query

            if specific_filters_query.__len__():
                specific_filters_suppliers = set(list(supplier_model.objects.filter(specific_filters_query).values_list('supplier_id', flat=True)))

            # if both available, find the intersection. basically it's another way of doing AND query.
            # the following conditions are use case dependent. The checking is done on the basis of 
            # query length. an empty query length means that query didn't contain any thing in it.
            if inventory_type_query.__len__() and specific_filters_query.__len__():
                final_suppliers_list = specific_filters_suppliers.intersection(inventory_type_query_suppliers)
            # if only inventory suppliers available, set it. Take the UNION in this case.
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

            # check for amenities here
            if amenities:
                response = website_utils.get_amenities_suppliers(supplier_type_code, amenities)
                if not response.data['status']:
                    return response
                amenities_suppliers = response.data['data']
                final_suppliers_list = final_suppliers_list.intersection(amenities_suppliers)

            # check for society ratio of tenants to flats
            if supplier_type_code == website_constants.society and ratio_of_tenants_to_flats:
                response = website_utils.get_societies_within_tenants_flat_ratio(float(ratio_of_tenants_to_flats['min']), float(ratio_of_tenants_to_flats['max']))
                if not response.data['status']:
                    return response
                final_suppliers_list = final_suppliers_list.intersection(response.data['data'])

            # check for standalone societies
            if supplier_type_code == website_constants.society and is_standalone_society:
                response = website_utils.get_standalone_societies()
                if not response.data['status']:
                    return response
                final_suppliers_list = final_suppliers_list.intersection(response.data['data'])

            result = {}

            # query now for real objects for supplier_id in the list
            suppliers = supplier_model.objects.filter(supplier_id__in=final_suppliers_list)
            supplier_serializer = ui_utils.get_serializer(supplier_type_code)
            serializer = supplier_serializer(suppliers, many=True)

            # to include only those suppliers that lie within radius, we need to send coordinates
            coordinates = {
                'radius': common_filters['radius'],
                'latitude': common_filters['latitude'],
                'longitude': common_filters['longitude']
            }
            # the following function sets the pricing as before and it's temprorary.
            response = website_utils.set_pricing_temproray(serializer.data, final_suppliers_list, supplier_type_code, coordinates)
            if not response.data['status']:
                return response
            suppliers = response.data['data']

            # because some suppliers can be outside the given radius, we need to recalculate list of 
            # supplier_id's. 
            final_suppliers_list = [supplier['supplier_id'] for supplier in suppliers]

            # calculate total aggregate count

            suppliers_inventory_count = InventorySummary.objects.filter(object_id__in=final_suppliers_list, content_type=content_type).aggregate(posters=Sum('total_poster_count'), \
                                                                                                    standees=Sum('total_standee_count'),
                                                                                                    stalls=Sum('total_stall_count'),
                                                                                                    fliers=Sum('flier_frequency'))

            # adding earlier saved shortlisted suppliers in the results.
            if proposal_id and center_id:
                response = website_utils.get_shortlisted_suppliers(proposal_id, request.user)
                if not response.data['status']:
                    return response
                shortlisted_supplier_result = response.data['data']
                if shortlisted_supplier_result.get(center_id):
                    shortlisted_suppliers = shortlisted_supplier_result[center_id].get(supplier_type_code)
                    response = website_utils.union_suppliers(suppliers, shortlisted_suppliers)
                    if not response.data['status']:
                        return response
                    suppliers = response.data['data'].values()

            # construct the response and return
            result['business_name'] = business_name
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
                    supplier_inventory_obj = InventorySummary.objects.get_supplier_type_specific_object(request.data.copy(),
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

            suppliers_inventory_count = InventorySummary.objects.get_supplier_type_specific_objects({'supplier_type_code': supplier_code},
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
                        society_inventory_obj = InventorySummary.objects.get_supplier_type_specific_object(request.data.copy(),
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
                    society_inventory_obj = InventorySummary.objects.get_supplier_type_specific_object(request.data.copy(),
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
                    society_inventory_obj = InventorySummary.objects.get_supplier_type_specific_object(request.data.copy(),
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
                            society_inventory_obj = InventorySummary.objects.get_supplier_type_specific_object(request.data.copy(),
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
                            society_inventory_obj = InventorySummary.objects.get_supplier_type_specific_object(request.data.copy(),
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


class ImportSocietyData(APIView):
    """
    This API reads a csv file and  makes supplier id's for each row. then it adds the data along with
    supplier id in the  supplier_society table. it also populates society_tower table.

    """
    def get(self, request):
        """
        :param request: request object
        :return: success response in case it succeeds else failure message.
        """
        class_name = self.__class__.__name__
        try:
            source_file = open(BASE_DIR + '/files/modified_new_tab.csv', 'rb')
            response = ui_utils.get_content_type(website_constants.society)
            if not response.data['status']:
                return response
            content_type = response.data['data']

            with transaction.atomic():
                reader = csv.reader(source_file)
                for num, row in enumerate(reader):
                    data = {}
                    if num == 0:
                        continue
                    else:
                        # todo: city is not being saved in society.
                        if len(row) != len(website_constants.supplier_keys):
                            return ui_utils.handle_response(class_name, data=errors.LENGTH_MISMATCH_ERROR.format(len(row), len(website_constants.supplier_keys)))

                        for index, key in enumerate(website_constants.supplier_keys):
                            if row[index] == '':
                                data[key] = None
                            else:
                                data[key] = row[index]

                        state_name = ui_constants.state_name
                        state_code = ui_constants.state_code
                        state_object = models.State.objects.get(state_name=state_name, state_code=state_code)
                        city_object = models.City.objects.get(city_code=data['city_code'], state_code=state_object)
                        area_object = models.CityArea.objects.get(area_code=data['area_code'], city_code=city_object)
                        subarea_object = models.CitySubArea.objects.get(subarea_code=data['subarea_code'],area_code=area_object)
                        # make the data needed to make supplier_id
                        supplier_id_data = {
                            'city_code': data['city_code'],
                            'area_code': data['area_code'],
                            'subarea_code': data['subarea_code'],
                            'supplier_type': data['supplier_type'],
                            'supplier_code': data['supplier_code']
                        }

                        response = get_supplier_id(request, supplier_id_data)
                        # this method of handing error code will  change in future
                        if response.status_code == status.HTTP_200_OK:
                            data['supplier_id'] = response.data['data']
                        else:
                            return response

                        (society_object, value) = SupplierTypeSociety.objects.get_or_create(supplier_id=data['supplier_id'])
                        data['society_location_type'] = subarea_object.locality_rating
                        #data['society_state'] = 'Maharashtra'Uttar Pradesh
                        data['society_state'] = 'Haryana'
                        supplier_id = data['supplier_id']
                        society_object.__dict__.update(data)
                        society_object.save()

                        # make entry into PMD here.
                        response = ui_utils.set_default_pricing(supplier_id, data['supplier_type'])
                        if not response.data['status']:
                            return response

                        towercount = SocietyTower.objects.filter(supplier=society_object).count()

                        # what to do if tower are less
                        tower_count_given = int(data['tower_count'])
                        if tower_count_given > towercount:
                            abc = tower_count_given - towercount
                            for i in range(abc):
                                tower = SocietyTower(supplier=society_object, object_id=supplier_id, content_type=content_type)
                                tower.save()
                        print "{0} done \n".format(data['supplier_id'])
            source_file.close()
            return Response(data="success", status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return ui_utils.handle_response(class_name, data=e.args, exception_object=e)
        except KeyError as e:
            return ui_utils.handle_response(class_name, data=e.args, exception_object=e)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


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
    renderer_classes = (website_renderers.XlsxRenderer, )
    # permission_classes = (v0_permissions.IsGeneralBdUser, )

    def post(self, request, proposal_id=None):
        class_name = self.__class__.__name__
        try:
            return website_utils.setup_generic_export(request.data, request.user, proposal_id)
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

            result = {}

            # iterate over multiple sheets
            for sheet in all_sheets:

                # fetch supplier_type_code from sheet name
                supplier_type_code = website_constants.sheet_names_to_codes.get(sheet)
                if not supplier_type_code:
                    continue

                # fetch the worksheet object to work with
                ws = wb.get_sheet_by_name(sheet)

                # fetch all the center id's
                center_id_list_response = website_utils.get_center_id_list(ws, website_constants.index_of_center_id)

                if not center_id_list_response.data['status']:
                    return center_id_list_response

                center_id_list = center_id_list_response.data['data']

                # normalize the center id's or map the actual center id's with indexes starting from zero
                center_id_to_index_mapping = {}

                for index, center_id in enumerate(center_id_list):
                    if not result.get(center_id):
                        result[center_id] = {}

                # iterate through all rows and populate result array
                for index, row in enumerate(ws.iter_rows()):

                    if index == 0 or website_utils.is_empty_row(row):
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

                    # # get the center index mapped for this center_id
                    # center_index = center_id_to_index_mapping[int(row['center_id'])]

                    # # get the actual center_object from result list to process further
                    # center_object = result[center_index]

                    center_id = int(row['center_id'])

                    center_object = result[center_id]

                    # initialize the center_object  with necessary keys if not already                    
                    response = website_utils.initialize_keys(center_object, supplier_type_code)
                    if not response.data['status']:
                        return response
                    center_object = response.data['data']

                    # add 1 supplier that represents this row to the list of suppliers this object has already
                    response = website_utils.make_suppliers(center_object, row, supplier_type_code, proposal_id, center_id)
                    if not response.data['status']:
                        return response
                    center_object = response.data['data']

                    # add the 'center' data  in center_object
                    response = website_utils.make_center(center_object, row)
                    if not response.data['status']:
                        return response
                    center_object = response.data['data']

                    # update the center dict in result with modified center_object
                    result[center_id] = center_object

            # time to hit the url to create-final-proposal that saves shortlisted suppliers and filters data
            # once data is prepared for all sheets,  we hit the url. if it creates problems in future, me might change
            # it.
            url = reverse('create-final-proposal', kwargs={'proposal_id': proposal_id})
            url = BASE_URL + url[1:]

            data = result.values()

            headers={
                'Content-Type': 'application/json',
                'Authorization': request.META.get('HTTP_AUTHORIZATION', '')
             }

            response = requests.post(url, json.dumps(data), headers=headers)

            if response.status_code != status.HTTP_200_OK:
                return Response({'status': False, 'error in final proposal api ': response.text}, status=status.HTTP_400_BAD_REQUEST)

            # data for this supplier is made. populate the shortlisted_inventory_details table before hitting the urls
            response = website_utils.populate_shortlisted_inventory_pricing_details(result, proposal_id, request.user)
            if not response.data['status']:
                return response

            # hit metric url to save metric data. current m sending the entire file, though only first sheet sending
            # is required.

            url = reverse('import-metric-data', kwargs={'proposal_id': proposal_id})
            url = BASE_URL + url[1:]

            # set the pointer to zero to be read again in next api
            my_file.seek(0)
            files = {
                'file': my_file
            }
            headers = {
                'Authorization': request.META.get('HTTP_AUTHORIZATION', '')
            }
            response = requests.post(url, files=files, headers=headers)

            if response.status_code != status.HTTP_200_OK:
                return Response({'status': False, 'error in import-metric-data api ': response.text}, status=status.HTTP_400_BAD_REQUEST)

            # prepare a new name for this file and save it in the required table
            response = website_utils.get_file_name(request.user, proposal_id, is_exported=False)
            if not response.data['status']:
                return response
            file_name = response.data['data']

            return Response({'status': True, 'data': file_name}, status=status.HTTP_200_OK)
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
    # permission_classes = (v0_permissions.IsGeneralBdUser,)

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
                user = request.user

                business_id = proposal_data.get('business_id')
                account_id = account_id

                # create a unique proposal id
                response = website_utils.create_proposal_id(business_id, account_id)
                if not response.data['status']:
                    return response
                proposal_data['proposal_id'] = response.data['data']

                # get the account object. required for creating the proposal
                account = AccountInfo.objects.get_user_related_object(user=user, account_id=account_id)
                proposal_data['account'] = account.account_id
                proposal_data['user'] = user.id

                # query for parent. if available set it. if it's available, then this is an EDIT request.
                parent = request.data.get('parent')
                parent = parent if parent != '0' else None
                proposal_data['parent'] = parent
                # set parent if available
                if parent:
                    proposal_data['parent'] = ProposalInfo.objects.get_user_related_object(user=user, proposal_id=parent).proposal_id

                # call the function that saves basic proposal information
                response = website_utils.create_basic_proposal(proposal_data)
                if not response.data['status']:
                    return response

                # time to save all the centers data
                response = website_utils.save_center_data(proposal_data, user)
                if not response.data['status']:
                    return response

                # return the proposal_id of the new proposal created
                proposal_id = proposal_data['proposal_id']
                return ui_utils.handle_response(class_name, data=proposal_id, success=True)
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
    # permission_classes = (v0_permissions.IsGeneralBdUser, )

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
            return website_utils.setup_create_final_proposal_post(request.data, request.user, proposal_id)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    def put(self, request, proposal_id):
        """
        Args:
            request: The request object
            proposal_id: The proposal id

        Returns: updates ShortlistedSpaces table with new data
        """
        class_name = self.__class__.__name__
        try:
            supplier_type_code = request.data['supplier_type_code']

            content_type_response = ui_utils.get_content_type(supplier_type_code)
            if not content_type_response.data['status']:
                return content_type_response
            content_type = content_type_response.data['data']

            data = {
                'user': request.user,
                'center_id': request.data['center_id'],
                'proposal_id': proposal_id,
                'object_id': request.data['supplier_id'],
                'content_type': content_type,
                'supplier_code': supplier_type_code
            }
            status = request.data['status']
            obj, is_created = models.ShortlistedSpaces.objects.get_or_create(**data)
            obj.status = status
            obj.save()
            return ui_utils.handle_response(class_name, data='success', success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class ProposalViewSet(viewsets.ViewSet):
    """
    A ViewSet handling various operations related to ProposalModel.
    This viewset was made instead of creating separate ApiView's because all the api's in this viewset
    are related to Proposal domain. so keeping them at one place makes sense.
    """
    parser_classes = (JSONParser, FormParser)
    # permission_classes = (v0_permissions.IsGeneralBdUser,)

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

    def update(self, request, pk=None):
        """
        Args:
            request: The request body
            pk: primary key

        Returns: Updated proposal object
        """
        class_name = self.__class__.__name__
        try:
            # prepare the data to be updated
            data = request.data.copy()
            data['proposal_id'] = pk

            proposal = ProposalInfo.objects.get(proposal_id=pk)
            serializer = ProposalInfoSerializer(proposal, data=data)
            if serializer.is_valid():
                serializer.save()
                return ui_utils.handle_response(class_name, data=serializer.data, success=True)
            return ui_utils.handle_response(class_name, data=serializer.errors)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    @detail_route(methods=['GET'])
    def proposal_centers(self, request, pk=None):
        """
        Fetches all centers associated with this proposal
        Args:
            request: request parameter
            pk: primary key of proposal

        Returns: Fetches all centers associated with this proposal. in each center object we have 'codes' array
        which contains which suppliers are allowed. Response is like this
        {
            "status": true,
            "data": [
                {
                  "id": 44,
                  "created_at": "2016-12-01T00:00:00Z",
                  "updated_at": "2016-12-01T00:00:00Z",
                  "center_name": "powai",
                  "address": "powai",
                  "latitude": 19.1153798,
                  "longitude": 72.9091436,
                  "radius": 1,
                  "subarea": "Hiranandani Gardens",
                  "area": "Powai",
                  "city": "Mumbai",
                  "pincode": 400076,
                  "user": 1,
                  "proposal": "BVIDBHBH157a5",
                  "codes": [
                    "RS"
                  ]
                }
              ]
        }
        """
        class_name = self.__class__.__name__
        try:
            response = website_utils.construct_proposal_response(pk, request.user)
            if not response.data['status']:
                return response
            return ui_utils.handle_response(class_name, data=response.data['data'], success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    @list_route()
    def invoice_proposals(self, request):
        """
        Args:
            request: request body
        Returns: All the proposal features  which have invoice_number not null
        """
        class_name = self.__class__.__name__
        try:
            # can't use distinct() to return only unique proposal_id's because .distinct('proposal') is not supported
            # for MySql
            file_objects = models.GenericExportFileName.objects.select_related('proposal', 'user').filter(proposal__invoice_number__isnull=False, is_exported=False).order_by('-proposal__created_on')

            # we need to make a unique list where proposal_id do not repeat.
            seen = set()
            final_file_objects = []
            for file_object in file_objects:
                proposal_id = file_object.proposal_id
                if proposal_id not in seen:
                    seen.add(proposal_id)
                    final_file_objects.append(file_object)

            file_serializer = website_serializers.GenericExportFileSerializerReadOnly(final_file_objects, many=True)
            return ui_utils.handle_response(class_name, data=file_serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    @detail_route(methods=['POST'])
    def get_spaces(self, request, pk=None):
        """
        The API  fetches all the data required to display on the grid view page.
        response looks like :
        {
           'status': true,
           'data' : {
              "business_name": '',
              "suppliers":
                    [
                        {
                           suppliers: { RS: [], CP: [] } ,
                           center: { ...   codes: [] }
                           suppliers_meta: {
                                             'RS': { 'inventory_type_selected' : [ 'PO', 'POST', 'ST' ]  },
                                             'CP': { 'inventory_type_selected':  ['ST']
                            }
                        }
                        ,
                        { }
                    ]
              }

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
        - name: latitude
        - name: longitude
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
                'longitude': longitude,
                'user': request.user
            }
            response = website_utils.suppliers_within_radius(data)
            if not response.data['status']:
                return response

            response = website_utils.add_shortlisted_suppliers_get_spaces(pk, request.user, response.data['data'])
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
            account_id = request.query_params.get('account_id')
            account_id = account_id if account_id!= '0' else None
            data = {
                'parent': pk if pk != '0' else None,
                'user': request.user,
                'account_id': account_id
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
                'proposal_id': pk,
                'user': request.user
            }
            response = website_utils.proposal_shortlisted_spaces(data)
            if not response.data['status']:
                return response
            return ui_utils.handle_response(class_name, data=response.data['data'], success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    @detail_route(methods=['PUT'])
    def shortlisted_suppliers_status(self, request, pk=None):
        """
        Update shortlisted suppliers based on their status value.
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
            center_id = request.data['center']['id']
            proposal = request.data['proposal']
            user = request.user
            
            fixed_data = {
                'center': center_id,
                'proposal': proposal,
            }
            unique_supplier_codes = request.data['suppliers'].keys()
            for code in unique_supplier_codes:
                # get the right model and content_type
                response = ui_utils.get_content_type(code)
                if not response:
                    return response
                content_type = response.data.get('data')
                fixed_data['content_type'] = content_type
                fixed_data['supplier_code'] = code

                response = website_utils.save_shortlisted_suppliers(request.data['suppliers'][code], fixed_data, user)
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
        class_name = self.__class__.__name__
        with transaction.atomic():

            file = open(BASE_DIR + '/files/contacts.csv', 'rb')
            try:
                reader = csv.reader(file)
                file.seek(0)
                for num, row in enumerate(reader):
                    if num == 0:
                        continue
                    else:
                        data = {}

                        length_of_row = len(row)
                        length_of_predefined_keys = len(website_constants.contact_keys)
                        if length_of_row != length_of_predefined_keys:
                            return ui_utils.handle_response(class_name, data=errors.LENGTH_MISMATCH_ERROR.format(length_of_row, length_of_predefined_keys))

                        # make the data
                        for index, key in enumerate(website_constants.contact_keys):
                            if row[index] == '':
                                data[key] = None
                            else:
                                data[key] = row[index]

                        if data.get('landline'):
                            landline_number = data['landline'].split('-')
                            data['landline'] = landline_number[1]
                            data['std_code'] = landline_number[0]

                        data['country_code'] = website_constants.COUNTRY_CODE

                        try:
                            response = get_supplier_id(request, data)
                            # this method of handing error code will  change in future
                            if response.status_code == status.HTTP_200_OK:
                                data['supplier_id'] = response.data['data']
                            else:
                                return response

                            society_object = SupplierTypeSociety.objects.get(supplier_id=data['supplier_id'])
                            data['spoc'] = False
                            data['supplier'] = society_object
                            contact_object = ContactDetails()
                            contact_object.__dict__.update(data)
                            contact_object.save()

                            # print it for universe satisfaction that something is going on !
                            print '{0} supplier contact done'.format(data['supplier_id'])
                        except ObjectDoesNotExist as e:
                            return ui_utils.handle_response(class_name, exception_object=e)
                        except Exception as e:
                            return ui_utils.handle_response(class_name, exception_object=e)

            finally:
                file.close()
            return ui_utils.handle_response(class_name, data='success', success=True)


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

            response = website_utils.manipulate_object_key_values(serializer.data, supplier_type_code=supplier_type_code,  **{'status': website_constants.status})
            if not response.data['status']:
                return response
            suppliers = response.data['data']

            return ui_utils.handle_response(class_name, data=suppliers, success=True)
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


class SendMail(APIView):
    """
    API sends mail. The API sends a file called 'sample_mail_file.xlsx' located in files directory.
    API  is for testing purpose only.

    """
    def post(self, request):
        class_name = self.__class__.__name__
        try:
            # file name
            file_name = 'sample_mail_file.xlsx'

            file_path = BASE_DIR + '/files/sample_mail_file.xlsx'
            with open(file_path, 'rb') as content_file:
                my_file = content_file.read()

            # get the predefined template for the body
            template_body = website_constants.email['body']

            # define a body_mapping.
            body_mapping = {
                 'file': file_name
            }
            # call the function to perform the magic
            response = website_utils.process_template(template_body, body_mapping)
            if not response.data['status']:
                return response

            # get the modified body
            modified_body = response.data['data']

            email_data = {
                'subject': str(request.data['subject']),
                'to': [str(request.data['to']), ],
                'body': modified_body
            }
            attachment = None
            if my_file:
                attachment = {
                    'file_name': file_name,
                    'file_data':  my_file,
                    'mime_type': website_constants.mime['xlsx']
                }
            response = website_utils.send_email(email_data, attachment)
            if not response.data['status']:
                return response
            return ui_utils.handle_response(class_name, data='Ok.Mail sent {0}'.format(response.data['data']), success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class Mail(APIView):
    """
    API sends mail. The API sends a simple mail to a single person
    """
    def post(self, request):
        class_name = self.__class__.__name__
        try:
            # takes these params from request
            subject = request.data['subject']
            to = request.data['to']
            body = request.data['body']

            email_data = {
                'subject': subject,
                'to': [to, ],
                'body': body
            }
            attachment = None
            response = website_utils.send_email(email_data, attachment)
            if not response.data['status']:
                return response
            return ui_utils.handle_response(class_name, data='Ok.Mail sent {0}'.format(response.data['data']), success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class Business(APIView):
    """
    Test api. will be deleted later on.
    """
    def get(self, request):
        class_name = self.__class__.__name__
        try:
            master_user = models.BaseUser.objects.get(id=8)
            result = AccountInfo.objects.get_user_related_object(user=master_user)
            # result = AccountInfo.objects.filter_user_related_objects(user=master_user)
            serializer = v0_serializers.AccountSerializer(result)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class ProposalVersion(APIView):
    """
    The API does following tasks:
    1. creates a new proposal_id and saves all the proposal info in it if user comes from edit proposal.
    2. set's parent to proposal_id received if user comes from edit proposal
    3. saves shortlisted suppliers against the new proposal_id if user comes from edit proposal
    4. saves filter data against the new proposal_id if user comes from edit proposal
    5. sends mail to logged in user
    6. sends mail to BD head.
    7. Generates excel sheet and send's it as attachment in the mail to BD head.
    """
    def post(self, request, proposal_id):
        """
        Args:
            request: The request object
            proposal_id: The proposal_id. ( This is proposal_id for which new version is to be created if is_proposal_version_created is True

        Returns: success if everything succeeds.

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

        """
        class_name = self.__class__.__name__
        try:
            user = request.user
            proposal = models.ProposalInfo.objects.get(proposal_id=proposal_id)
            account = models.AccountInfo.objects.get(account_id=proposal.account.account_id)
            business = models.BusinessInfo.objects.get(business_id=account.business.business_id)

            # if you don't provide this value, No proposal version is created.
            is_proposal_version_created = request.data['is_proposal_version_created'] if request.data.get('is_proposal_version_created') else False
            data = request.data['centers']

            # if this variable is true, we will have to create a new proposal version.
            if is_proposal_version_created:
                # create a unique proposal id
                response = website_utils.create_proposal_id(business.business_id, account.account_id)
                if not response.data['status']:
                    return response
                new_proposal_id = response.data['data']

                # create new ProposalInfo object for this new proposal_id
                proposal.pk = new_proposal_id
                proposal.save()

                # change the parent and save again
                proposal.parent = proposal
                proposal.save()
                # change the proposal_id variable here
                proposal_id = new_proposal_id

            response = website_utils.setup_create_final_proposal_post(data, request.user, proposal_id)
            if not response.data['status']:
                return response

            # call create Final Proposal first
            response = website_utils.setup_generic_export(data, request.user, proposal_id)
            if not response.data['status']:
                return response

            file_name = response.data['data']['name']
            my_file = response.data['data']['file']

            # send mail to logged in user without attachment
            email_data = {
             'subject': website_constants.subjects['agency'],
             'body': website_constants.bodys['agency'],
             'to': [user.email]
             }

            response = website_utils.send_email(email_data)
            if not response.data['status']:
                return response

            bd_body = {
                'user_name': request.user.first_name,
                'business': business.name,
                'account': account.name,
                'proposal_id': proposal_id,
                'file_name': file_name
            }

            response = website_utils.process_template(website_constants.bodys['bd_head'], bd_body)
            if not response.data['status']:
                return response
            bd_body = response.data['data']

            email_data = {
                'subject': website_constants.subjects['bd_head'],
                'body': bd_body,
                'to': [website_constants.emails['bd_head']]
            }

            attachment = {
                'file_data': my_file,
                'file_name': file_name,
                'mime_type': website_constants.mime['xlsx']
            }

            # send mail to Bd Head with attachment
            response = website_utils.send_email(email_data, attachment=attachment)
            if not response.data['status']:
                return response

            # upload this shit to amazon
            response = website_utils.upload_to_amazon(file_name)
            if not response.data['status']:
                return response

            # remove the file name
            os.remove(file_name)
            return ui_utils.handle_response(class_name, data='success', success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class AssignCampaign(APIView):
    """
    This API assigns a campaign to a user by a user
    """
    def post(self, request):
        """
        Args:
            request: The request object
            campaign_id: Assigns campaign_id to a user by a user.
        Returns: Success in case campaign is successfully assigned to the user.
        """
        class_name = self.__class__.__name__
        try:
            assigned_by = request.user

            campaign_id = request.data['campaign_id']

            if assigned_by.is_anonymous():
                return ui_utils.handle_response(class_name, data='A campaign cannot be assigned by an Anonymous user')

            if not request.data['to']:
                return ui_utils.handle_response(class_name, data='You must provide a user to which this campaign will be assigned')

            # fetch BaseUser object.
            assigned_to = models.BaseUser.objects.get(id=request.data['to'])

            # fetch ProposalInfo object.
            proposal = ProposalInfo.objects.get(proposal_id=campaign_id)

            response = website_utils.is_campaign(proposal)
            if not response.data['status']:
                return response

            # todo: check for dates also. you should not assign a past campaign to any user. left for later

            # create the object
            models.CampaignAssignment.objects.get_or_create(assigned_by=assigned_by, assigned_to=assigned_to, campaign=proposal)

            return ui_utils.handle_response(class_name, data='success', success=True)

        except ObjectDoesNotExist as e:
            return ui_utils.handle_response(class_name, exception_object=e)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    def get(self, request):
        """
        Args:
            request: Request object

        Returns: AssignedCampaign objects.
        {
          "status": true,
          "data": [
            {
              "id": 1,
              "assigned_by": {
                "id": 1,
                "first_name": "Nikhil",
                "last_name": "Kumar",
              },
              "assigned_to": {
                "id": 9,
                "first_name": "kamlesh",
                "last_name": "sabziwale"
              },
              "campaign": {
                "proposal_id": "zUkqLPYR",
                "created_at": "2016-12-01T00:00:00Z",
                "updated_at": "2016-12-15T10:18:04.514008Z",
              },
            }
          ]
        }
        Handles three cases :
        Fetches campaigns assigned by a user only
        Fetches campaigns assigned to a particular user only
        Fetches campaigns assigned by a user to a particular user.
        """
        class_name = self.__class__.__name__

        try:
            assigned_by = request.user

            if assigned_by.is_anonymous():
                return ui_utils.handle_response(class_name, data='Anonymous users can\'t have any campaigns assigned')

            query = {}
            # this field determined weather to include 'assigned_by' in query or not
            is_assigned_by = int(request.query_params['include_assigned_by'])

            # to field  must be present  if is_assigned_by is False.
            if not is_assigned_by:
                # 'to' must be present. There should be something to query !
                to = request.query_params['to']
            else:
                # if is_assigned_by is False, try to get to, but assigned_by field must be set to request.user
                to = request.query_params.get('to')
                query['assigned_by'] = request.user

            # if you found to field, fetch the object from BaseUser table.
            if to:
                query['assigned_to'] = models.BaseUser.objects.get(id=to)

            assigned_objects = models.CampaignAssignment.objects.filter(**query)

            # check each one of them weather they are campaign or not
            for assign_object in assigned_objects:
                response = website_utils.is_campaign(assign_object.campaign)
                if not response.data['status']:
                    return response
                    # assign statuses to each of the campaigns.

            serializer = website_serializers.CampaignAssignmentSerializerReadOnly(assigned_objects, many=True)

            for data in serializer.data:
                proposal_start_date = parse_datetime(data['campaign']['tentative_start_date'])
                proposal_end_date = parse_datetime(data['campaign']['tentative_end_date'])
                response = website_utils.get_campaign_status(proposal_start_date, proposal_end_date)
                if not response.data['status']:
                    return response
                data['campaign']['status'] = response.data['data']

            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except ObjectDoesNotExist as e:
            return ui_utils.handle_response(class_name, exception_object=e)
        except KeyError as e:
            return ui_utils.handle_response(class_name, data='key Error', exception_object=e)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class CampaignInventory(APIView):
    """

    """
    def get(self, request, campaign_id):
        """
        The API fetches campaign data + SS  + SID
        Args:
            request: request data
            campaign_id: The proposal_id which has been converted into campaign.

        Returns:

        """
        class_name = self.__class__.__name__
        # todo: reduce the time taken for this API. currently it takes 15ms to fetch data which is too much.
        try:
            proposal = models.ProposalInfo.objects.get(proposal_id=campaign_id)

            response = website_utils.is_campaign(proposal)
            if not response.data['status']:
                return response

            response = website_utils.prepare_shortlisted_spaces_and_inventories(campaign_id)
            if not response.data['status']:
                return response

            return ui_utils.handle_response(class_name, data=response.data['data'], success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    def put(self, request, campaign_id):
        """
        The api updates data against this campaign_id.
        Args:
            request:
            campaign_id: The campaign id to which we want to update

        Returns:

        """
        class_name = self.__class__.__name__
        try:
            proposal = models.ProposalInfo.objects.get(proposal_id=campaign_id)

            response = website_utils.is_campaign(proposal)
            if not response.data['status']:
                return response

            data = request.data

            response = website_utils.handle_update_campaign_inventories(request.user, data)
            if not response.data['status']:
                return response

            return ui_utils.handle_response(class_name, data='successfully updated', success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class CampaignSuppliersInventoryList(APIView):
    """
    works as @Android API and as website API.

    List all valid shortlisted suppliers and there respective shortlisted inventories belonging to any campaign in which
    shortlisted inventories have release, closure, or audit dates within delta d days from current date

    """
    def get(self, request):
        """
        Args:
            request: The request object
        Returns:
        """
        class_name = self.__class__.__name__

        try:
            result = {}
            # both are optional. generally the 'assigned_to' query is given by android, and 'proposal_id' query is given
            # by website
            assigned_to = request.query_params.get('assigned_to')
            proposal_id = request.query_params.get('proposal_id')

            # constructs a Q object based on current date and delta d days defined in constants
            assigned_date_range_query = website_utils.construct_date_range_query('activity_date')

            proposal_query = Q()
            if proposal_id:
                proposal_query = Q(inventory_activity__shortlisted_inventory_details__shortlisted_spaces__proposal_id=proposal_id)

            assigned_to_query = Q()
            if assigned_to:
                assigned_to_query = Q(assigned_to_id=long(assigned_to))

            # we do a huge query to fetch everything we need at once.
            inv_act_assignment_objects = models.InventoryActivityAssignment.objects.\
                select_related('inventory_activity', 'inventory_activity__shortlisted_inventory_details',
                               'inventory_activity__shortlisted_inventory_details__shortlisted_spaces').\
                filter(assigned_date_range_query, proposal_query, assigned_to_query).values(

                'id', 'activity_date', 'reassigned_activity_date', 'inventory_activity', 'inventory_activity__activity_type',
                'inventory_activity__shortlisted_inventory_details__ad_inventory_type__adinventory_name',
                'inventory_activity__shortlisted_inventory_details__ad_inventory_duration__duration_name',
                'inventory_activity__shortlisted_inventory_details',
                'inventory_activity__shortlisted_inventory_details__inventory_id',
                'inventory_activity__shortlisted_inventory_details__inventory_content_type',
                'inventory_activity__shortlisted_inventory_details__comment',
                'inventory_activity__shortlisted_inventory_details__shortlisted_spaces',
                'inventory_activity__shortlisted_inventory_details__shortlisted_spaces__object_id',
                'inventory_activity__shortlisted_inventory_details__shortlisted_spaces__proposal_id',
                'inventory_activity__shortlisted_inventory_details__shortlisted_spaces__content_type',
            )

            total_shortlisted_spaces_list = []  # this is required to fetch supplier details later
            inv_act_assignment_ids = set()  # this is required to fetch images data later
            # the idea of this loop is to separate different table data in different keys.
            for content in inv_act_assignment_objects:
                if not result.get('shortlisted_suppliers'):
                    result['shortlisted_suppliers'] = {}

                # fetch data fro shortlisted_suppliers key
                shortlisted_space_id = content['inventory_activity__shortlisted_inventory_details__shortlisted_spaces']
                proposal_id = content['inventory_activity__shortlisted_inventory_details__shortlisted_spaces__proposal_id']
                supplier_id = content['inventory_activity__shortlisted_inventory_details__shortlisted_spaces__object_id']
                supplier_content_type_id = content['inventory_activity__shortlisted_inventory_details__shortlisted_spaces__content_type']

                result['shortlisted_suppliers'][shortlisted_space_id] = {
                    'proposal_id': proposal_id,
                    'supplier_id': supplier_id,
                    'content_type_id': supplier_content_type_id
                }

                total_shortlisted_spaces_list.append(
                    {
                        'content_type_id': supplier_content_type_id,
                        'supplier_id': supplier_id
                    }
                )

                if not result.get('shortlisted_inventories'):
                    result['shortlisted_inventories'] = {}
                # fetch data for shortlisted_inventories key
                shortlisted_inventory_id = content['inventory_activity__shortlisted_inventory_details']
                inventory_id = content['inventory_activity__shortlisted_inventory_details__inventory_id']
                inventory_content_type_id = content['inventory_activity__shortlisted_inventory_details__inventory_content_type']
                comment = content['inventory_activity__shortlisted_inventory_details__comment']
                inventory_name = content['inventory_activity__shortlisted_inventory_details__ad_inventory_type__adinventory_name']
                inventory_duration = content['inventory_activity__shortlisted_inventory_details__ad_inventory_duration__duration_name']

                result['shortlisted_inventories'][shortlisted_inventory_id] = {
                    'shortlisted_spaces_id': shortlisted_space_id,
                    'inventory_id': inventory_id,
                    'inventory_content_type_id': inventory_content_type_id,
                    'comment': comment,
                    'inventory_name': inventory_name,
                    'inventory_duration': inventory_duration
                }

                if not result.get('inventory_activities'):
                    result['inventory_activities'] = {}
                # fetch data for inventory activity key
                inventory_activity_id = content['inventory_activity']
                activity_type = content['inventory_activity__activity_type']

                result['inventory_activities'][inventory_activity_id] = {
                    'shortlisted_inventory_id': shortlisted_inventory_id,
                    'activity_type': activity_type
                }

                if not result.get('inventory_activity_assignment'):
                    result['inventory_activity_assignment'] = {}
                # fetch data for inventory activity assignment
                inventory_activity_assignment_id = content['id']
                activity_date = content['activity_date']
                reassigned_activity_date = content['reassigned_activity_date']
                inv_act_assignment_ids.add(inventory_activity_assignment_id)

                result['inventory_activity_assignment'][inventory_activity_assignment_id] = {
                    'activity_date': activity_date.date() if activity_date else None,
                    'reassigned_activity_date': reassigned_activity_date.date() if reassigned_activity_date else None,
                    'inventory_activity_id': inventory_activity_id
                }

            # after the result is prepared, here we collect images data
            inventory_activity_images = models.InventoryActivityImage.objects.filter(inventory_activity_assignment_id__in=inv_act_assignment_ids)
            images = {}
            for inv_act_image in inventory_activity_images:
                image_id = inv_act_image.id

                if not images.get(image_id):
                    images[image_id] = {}

                images[image_id] = {
                    'image_path': inv_act_image.image_path,
                    'comment': inv_act_image.comment,
                    'actual_activity_date': inv_act_image.actual_activity_date.date() if inv_act_image.actual_activity_date else None,
                    'inventory_activity_assignment_id': inv_act_image.inventory_activity_assignment_id
                }

            # # set the shortlisted spaces data. it maps various supplier ids to their respective content_types
            response = website_utils.get_objects_per_content_type(total_shortlisted_spaces_list)
            if not response.data['status']:
                return response
            content_type_supplier_id_map, content_type_set, supplier_id_set = response.data['data']

            # converts the ids store in previous step to actual objects and adds additional information which is
            #  supplier specific  like area, name, subarea etc.
            response = website_utils.map_objects_ids_to_objects(content_type_supplier_id_map)
            if not response.data['status']:
                return response

            # the returned response is a dict in which key is (content_type, supplier_id) and value is a dict of extra
            # information for that supplier
            supplier_detail = response.data['data']

            # add the key 'supplier_detail' which holds all sorts of information for that supplier to final result.
            if result:
                for shortlisted_space_id, detail in result['shortlisted_suppliers'].iteritems():
                    try:
                        detail['supplier_detail'] = supplier_detail[detail['content_type_id'], detail['supplier_id']]
                    except KeyError:
                        # ideally every supplier in ss table must also be in the corresponding supplier table. But
                        # because current data is corrupt as i have manually added suppliers, i have to set this to
                        # empty when KeyError occurres. #todo change this later.
                        detail['supplier_detail'] = {}
                        # set images data to final result
                result['images'] = images
            return ui_utils.handle_response(class_name, data=result, success=True)

        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class ProposalToCampaign(APIView):
    """
    tries to  book the assigned inventories to this proposal. if successfull, sets the campaign state to right state that
    marks this proposal a campaign.
    """
    def post(self, request, proposal_id):
        """
        Args:
            request:
            proposal_id:

        Returns:

        """
        class_name = self.__class__.__name__
        try:
            proposal = models.ProposalInfo.objects.get(proposal_id=proposal_id)

            if not proposal.invoice_number:
                return ui_utils.handle_response(class_name, data=errors.CAMPAIGN_NO_INVOICE_ERROR)

            proposal_start_date = proposal.tentative_start_date
            proposal_end_date = proposal.tentative_end_date

            if not proposal_start_date or not proposal_end_date:
                return ui_utils.handle_response(class_name, data=errors.NO_DATES_ERROR.format(proposal_id))

            response = website_utils.is_campaign(proposal)
            if response.data['status']:
                return ui_utils.handle_response(class_name, data=errors.ALREADY_A_CAMPAIGN_ERROR.format(proposal.proposal_id))

            current_assigned_inventories = models.ShortlistedInventoryPricingDetails.objects.select_related('shortlisted_spaces').filter(shortlisted_spaces__proposal_id=proposal_id)

            if not current_assigned_inventories:
                return ui_utils.handle_response(class_name, data=errors.NO_INVENTORIES_ASSIGNED_ERROR.format(proposal_id))

            current_assigned_inventories_map = {}

            for inv in current_assigned_inventories:
                inv_tuple = (inv.inventory_content_type, inv.inventory_id)
                current_assigned_inventories_map[inv_tuple] = (proposal_start_date, proposal_end_date, inv)

            # get all the proposals which are campaign and which overlap with the current campaign
            response = website_utils.get_overlapping_campaigns(proposal)
            if not response.data['status']:
                return response
            overlapping_campaigns = response.data['data']

            if not overlapping_campaigns:
                # currently we have no choice but to book all inventories the same proposal_start and end date
                # this can be made smarter when we know for how many days a particular inventory  is allowed in a
                # supplier this will help in automatically determining R.D and C.D.
                inventory_release_closure_list = [(inv, proposal_start_date, proposal_end_date) for inv in current_assigned_inventories]
                response = website_utils.insert_release_closure_dates(inventory_release_closure_list)
                if not response.data['status']:
                    return response
                proposal.campaign_state = website_constants.proposal_converted_to_campaign
                proposal.save()
                return ui_utils.handle_response(class_name,data=errors.PROPOSAL_CONVERTED_TO_CAMPAIGN.format(proposal_id), success=True)

            already_booked_inventories = models.ShortlistedInventoryPricingDetails.objects.filter(shortlisted_spaces__proposal__in=overlapping_campaigns)
            already_booked_inventories_map = {}

            for inv in already_booked_inventories:
                inv_tuple = (inv.inventory_content_type, inv.inventory_id)
                target_tuple = (inv.release_date, inv.closure_date, inv.shortlisted_spaces.proposal_id)
                try:
                    reference = already_booked_inventories_map[inv_tuple]
                except KeyError:
                    already_booked_inventories_map[inv_tuple] = []
                    reference = already_booked_inventories_map[inv_tuple]
                reference.append(target_tuple)

            response = website_utils.book_inventories(current_assigned_inventories_map, already_booked_inventories_map)
            if not response.data['status']:
                return response
            booked_inventories, inventory_release_closure_list, inv_error_list = response.data['data']

            # if there is something in error list then one or more inventories overlapped with already running campaigns
            # we do not convert a proposal into campaign in this case
            if inv_error_list:
                return ui_utils.handle_response(class_name, data=errors.CANNOT_CONVERT_TO_CAMPAIGN_ERROR.format(proposal_id, inv_error_list))

            # insert the RD and CD dates for each inventory
            response = website_utils.insert_release_closure_dates(inventory_release_closure_list)
            if not response.data['status']:
                return response

            bulk_update(booked_inventories)
            proposal.campaign_state = website_constants.proposal_converted_to_campaign
            proposal.save()

            return ui_utils.handle_response(class_name, data=errors.PROPOSAL_CONVERTED_TO_CAMPAIGN.format(proposal_id), success=True)

        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class CampaignToProposal(APIView):
    """
    Releases the inventories booked under a campaign and the sets the campaign state back to proposal state.
    """
    def post(self, request, campaign_id):
        """
        Args:
            request:
            campaign_id: The campaign_id

        Returns:
        """
        class_name = self.__class__.__name__
        try:
            proposal = models.ProposalInfo.objects.get(proposal_id=campaign_id)

            response = website_utils.is_campaign(proposal)
            if not response.data['status']:
                return response

            proposal.campaign_state = website_constants.proposal_not_converted_to_campaign
            proposal.save()

            current_assigned_inventories = models.ShortlistedInventoryPricingDetails.objects.select_related('shortlisted_spaces').filter(shortlisted_spaces__proposal_id=campaign_id)
            models.InventoryActivityAssignment.objects.filter(inventory_activity__shortlisted_inventory_details__in=current_assigned_inventories).delete()

            return ui_utils.handle_response(class_name, data=errors.REVERT_CAMPAIGN_TO_PROPOSAL.format(campaign_id, website_constants.proposal_not_converted_to_campaign), success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class ImportCorporateData(APIView):
    """
    This API reads a csv file and  makes supplier id's for each row. then it adds the data along with
    supplier id in the  supplier_society table. it also populates society_tower table.
    """

    def get(self, request):
        """
        :param request: request object
        :return: success response in case it succeeds else failure message.
        """
        class_name = self.__class__.__name__
        try:
            source_file = open(BASE_DIR + '/files/corporate.csv', 'rb')
            with transaction.atomic():
                reader = csv.reader(source_file)
                for num, row in enumerate(reader):
                    data = {}
                    if num == 0:
                        continue
                    else:
                        if len(row) != len(website_constants.corporate_keys):
                            return ui_utils.handle_response(class_name, data=errors.LENGTH_MISMATCH_ERROR.format(len(row), len(website_constants.corporate_keys)))

                        for index, key in enumerate(website_constants.corporate_keys):
                            if row[index] == '':
                                data[key] = None
                            else:
                                data[key] = row[index]
                        state_name = ui_constants.state_name
                        state_code = ui_constants.state_code
                        state_object = models.State.objects.get(state_name=state_name, state_code=state_code)
                        city_object = models.City.objects.get(city_code=data['city_code'], state_code=state_object)
                        area_object = models.CityArea.objects.get(area_code=data['area_code'], city_code=city_object)
                        subarea_object = models.CitySubArea.objects.get(subarea_code=data['subarea_code'],area_code=area_object)
                        # make the data needed to make supplier_id
                        supplier_id_data = {
                            'city_code': data['city_code'],
                            'area_code': data['area_code'],
                            'subarea_code': data['subarea_code'],
                            'supplier_type': data['supplier_type'],
                            'supplier_code': data['supplier_code']
                        }

                        response = get_supplier_id(request, supplier_id_data)
                        # this method of handing error code will  change in future
                        if response.status_code == status.HTTP_200_OK:
                            data['supplier_id'] = response.data['data']
                        else:
                            return response

                        (corporate_object, value) = SupplierTypeCorporate.objects.get_or_create(supplier_id=data['supplier_id'])

                        data['society_state'] = 'Maharashtra'
                        corporate_object.__dict__.update(data)
                        corporate_object.save()

                        # make entry into PMD here.
                        response = ui_utils.set_default_pricing(data['supplier_id'], data['supplier_type'])
                        if not response.data['status']:
                            return response

                        url = reverse('inventory-summary', kwargs={'id': data['supplier_id']})
                        url = BASE_URL + url[1:]
                        headers = {
                            'Content-Type': 'application/json',
                            'Authorization': request.META.get('HTTP_AUTHORIZATION', '')
                        }
                        response = requests.post(url, json.dumps(data), headers=headers)
                        print "{0} done \n".format(data['supplier_id'])

            source_file.close()
            return Response(data="success", status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return ui_utils.handle_response(class_name, data=e.args, exception_object=e)
        except KeyError as e:
            return ui_utils.handle_response(class_name, data=e.args, exception_object=e)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class InventoryActivityImage(APIView):
    """
     @Android API. used to insert image paths from Android.
     makes an entry into InventoryActivityImage table.
    """
    def post(self, request):
        """
        stores image_path against an inventory_id.
        Args:
            request: The request data

        Returns: success in case the object is created.
        """
        class_name = self.__class__.__name__
        try:

            shortlisted_inventory_detail_instance = models.ShortlistedInventoryPricingDetails.objects.get(id=request.data['shortlisted_inventory_detail_id'])
            activity_date = request.data['activity_date']
            activity_type = request.data['activity_type']
            activity_by = long(request.data['activity_by'])
            actual_activity_date = request.data['actual_activity_date']
            use_assigned_date = int(request.data['use_assigned_date'])

            if use_assigned_date:
                date_query = Q(activity_date=ui_utils.get_aware_datetime_from_string(activity_date))
            else:
                date_query = Q(reassigned_activity_date=ui_utils.get_aware_datetime_from_string(activity_date))

            user = models.BaseUser.objects.get(id=activity_by)

            # they can send all the garbage in activity_type. we need to check if it's valid.
            valid_activity_types = [ac_type[0] for ac_type in models.INVENTORY_ACTIVITY_TYPES]

            if activity_type not in valid_activity_types:
                return ui_utils.handle_response(class_name, data=errors.INVALID_ACTIVITY_TYPE_ERROR.format(activity_type))

            inventory_activity_assignment_instance = models.InventoryActivityAssignment.objects.get(
                date_query,
                inventory_activity__shortlisted_inventory_details=shortlisted_inventory_detail_instance,
                inventory_activity__activity_type=activity_type,
            )
            # if it's not superuser and it's not assigned to take the image
            if (not user.is_superuser) and (not inventory_activity_assignment_instance.assigned_to_id == activity_by):
                return ui_utils.handle_response(class_name, data=errors.NO_INVENTORY_ACTIVITY_ASSIGNMENT_ERROR)

            # image path shall be unique
            instance, is_created = models.InventoryActivityImage.objects.get_or_create(image_path=request.data['image_path'])
            instance.inventory_activity_assignment = inventory_activity_assignment_instance
            instance.comment = request.data['comment']
            instance.actual_activity_date = actual_activity_date
            instance.activity_by = models.BaseUser.objects.get(id=activity_by)
            instance.save()

            return ui_utils.handle_response(class_name, data=model_to_dict(instance), success=True)

        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    def delete(self, request):
        """
        Deletes an instance of inventory activity image

        Args:
            request:

        Returns:

        """
        class_name = self.__class__.__name__
        try:
            pk = request.data['id']
            models.InventoryActivityImage.objects.get(pk=pk).delete()
            return ui_utils.handle_response(class_name, data=pk, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class SupplierDetails(APIView):
    """
    Detail of individual supplier
    """
    def get(self, request):
        """
        Args:
            self:
            request:
        Returns: matching supplier object from supplier type model

        """
        class_name = self.__class__.__name__

        try:
            supplier_id = request.query_params['supplier_id']
            supplier_type_code = request.query_params['supplier_type_code']

            response = ui_utils.get_content_type(supplier_type_code)
            if not response.data['status']:
                return response
            content_type = response.data['data']
     
            supplier_model = ContentType.objects.get(pk=content_type.id).model
            model = get_model(settings.APP_NAME,supplier_model)

            supplier_object = model.objects.get(supplier_id=supplier_id)

            data = model_to_dict(supplier_object)

            response = website_utils.manipulate_object_key_values([data])
            if not response.data['status']:
                return response
            data = response.data['data'][0]

            return ui_utils.handle_response(class_name, data=data, success=True)

        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    def put(self, request):
        """
        updates a particular supplier
        Args:
            request:
        Returns: returns updated supplier object

        """
        class_name = self.__class__.__name__
        try:
            supplier_id = request.data['supplier_id']
            supplier_type_code = request.data['supplier_type_code']

            data = request.data.copy()

            data.pop('supplier_id')
            data.pop('supplier_type_code')

            response = ui_utils.get_content_type(supplier_type_code)
            if not response.data['status']:
                return response
            content_type = response.data['data']
            supplier_model = content_type.model

            model = get_model(settings.APP_NAME, supplier_model)

            model.objects.filter(supplier_id=supplier_id).update(**data)

            supplier_object = model.objects.get(pk=supplier_id)
            return ui_utils.handle_response(class_name, data=model_to_dict(supplier_object), success=True)

        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class GenerateInventoryActivitySummary(APIView):
    """
    Generates inventory summary in which we show how much of the total inventories were release, audited, and closed
    on particular date
    """
    def get(self, request):
        """
        Args:
            request: The request param

        Returns:
        """
        class_name = self.__class__.__name__
        try:
            proposal_id = request.query_params['proposal_id']
            proposal = models.ProposalInfo.objects.get(proposal_id=proposal_id)

            data = {}

            response = website_utils.is_campaign(proposal)
            if not response.data['status']:
                return response

            response = website_utils.get_possible_activity_count(proposal_id)
            if not response.data['status']:
                return response
            data['Total'] = response.data['data']

            response = website_utils.get_actual_activity_count(proposal_id)
            if not response.data['status']:
                return response
            data['Actual'] = response.data['data']

            return ui_utils.handle_response(class_name, data=data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class Amenity(APIView):
    """
    API to create an Amenity
    """
    def post(self, request):
        """
        create a single amenity
        Args:
            request:

        Returns:

        """
        class_name = self.__class__.__name__
        try:
            name = request.data['name']
            code = request.data['code']

            if code not in v0_constants.valid_amenities.keys():
                return ui_utils.handle_response(class_name, data=errors.INVALID_AMENITY_CODE_ERROR.format(code))

            amenity, is_created = models.Amenity.objects.get_or_create(code=code)
            amenity.name = name
            amenity.save()

            return ui_utils.handle_response(class_name, data=model_to_dict(amenity), success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class GetAllAmenities(APIView):
    """
    Fetches all amenities
    """
    def get(self, request):
        """
        fetches all amenities
        Args:
            request:

        Returns:

        """
        class_name = self.__class__.__name__
        try:
            amenities = models.Amenity.objects.all()
            serializer = website_serializers.AmenitySerializer(amenities, many=True)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class SupplierAmenity(APIView):
    """
    Returns all amenities per supplier
    """
    def get(self, request):
        """
        Args:
            request:

        Returns:
        """
        class_name = self.__class__.__name__
        try:
            supplier_type_code = request.query_params['supplier_type_code']

            response = ui_utils.get_content_type(supplier_type_code)
            if not response.data['status']:
                return response
            content_type = response.data['data']

            amenities = models.SupplierAmenitiesMap.objects.filter(object_id=request.query_params['supplier_id'], content_type=content_type)
            serializer = website_serializers.SupplierAmenitiesMapSerializer(amenities, many=True)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    # def post(self, request):
    #     """
    #     Args:
    #         request:
    #     Returns:
    #     """
    #     class_name = self.__class__.__name__
    #     try:
    #         supplier_id = request.data['supplier_id']
    #         supplier_type_code = request.data['supplier_type_code']
    #         amenity_id = request.data['amenity_id']

    #         response = ui_utils.get_content_type(supplier_type_code)
    #         if not response.data['status']:
    #             return response
    #         content_type = response.data['data']

    #         models.SupplierAmenitiesMap.objects.get_or_create(object_id=supplier_id, content_type=content_type, amenity_id=amenity_id)
    #         return ui_utils.handle_response(class_name, data='success', success=True)
    #     except Exception as e:
    #         return ui_utils.handle_response(class_name, exception_object=e)

    def post(self, request):
        """
        Args:
            request:
        Returns:
        """
        class_name = self.__class__.__name__
        try:
            supplier_type_code = request.data['supplier_type_code']
            supplier_id = request.data['supplier_id']
            response = website_utils.save_amenities_for_supplier(supplier_type_code, supplier_id, request.data['amenities'])

            if not response.data['status']:
                return response

            return ui_utils.handle_response(class_name, data='success', success=True)

        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class BulkInsertInventoryActivityImage(APIView):
    """
    @Android API

    used by android app to bulk upload image's paths when internet is switched on and there are images yet to
    to be synced to django backend
    """

    def post(self, request):
        """
        Bulk inserts data into inv image table.

        Args:
            request: request data that holds info to be updated

        Returns: 

        """
        class_name = self.__class__.__name__
        try:
            shortlisted_inv_ids = set()  # to store shortlisted inv ids
            act_dates = set()  # to store all act dates
            act_types = set() # to store all act types
            inv_act_assignment_to_image_data_map = {}  # map from tuple to inv act image data
            inv_image_objects = []  # inv act image objects will be stored here for bulk create

            # they can send all the garbage in activity_type. we need to check if it's valid.
            valid_activity_types = [ac_type[0] for ac_type in models.INVENTORY_ACTIVITY_TYPES]

            # this loop makes inv_act_assignment_to_image_data_map which maps a tuple of sid, act_date, act_type to
            # image data this is required later for creation of inv act image objects.
            image_taken_by = request.user
            inv_image_data = request.data

            # pull out all image paths for these assignment objects
            database_image_paths = models.InventoryActivityImage.objects.all().values_list('image_path', flat=True)

            # to reduce checking of certain image_path in the list above, instead create a dict and map image_paths to some
            # value like True. it's faster to check for this image_path in the dict rather in the list
            image_path_dict = {}
            for image_path in database_image_paths:
                image_path_dict[image_path] = True

            for data in inv_image_data:

                image_path = data['image_path']
                if image_path_dict.get(image_path):
                    # move to next path buddy, we have already stored this path
                    continue

                shortlisted_inv_id = int(data['shortlisted_inventory_detail_id'])
                shortlisted_inv_ids.add(shortlisted_inv_id)

                act_dates.add(ui_utils.get_aware_datetime_from_string(data['activity_date']))
                act_types.add(data['activity_type'])

                if data['activity_type'] not in valid_activity_types:
                    return ui_utils.handle_response(class_name,data=errors.INVALID_ACTIVITY_TYPE_ERROR.format(data['activity_type']))

                image_data = {
                    'image_path': data['image_path'],
                    'comment': data['comment'],
                    'activity_by': image_taken_by,
                    'actual_activity_date': data['activity_date'],
                }

                try:
                    # these three keys determine unique inventory assignment object for an image object
                    reference = inv_act_assignment_to_image_data_map[shortlisted_inv_id, data['activity_date'], data['activity_type']]
                    reference.append(image_data)
                except KeyError:
                    reference = [image_data]
                    inv_act_assignment_to_image_data_map[shortlisted_inv_id, data['activity_date'], data['activity_type']] = reference

            # i can determine weather all images synced up or not by checking this dict because we are not proceeding further in the
            # above loop if the path is already stored.
            if not inv_act_assignment_to_image_data_map:
                return  ui_utils.handle_response(class_name, data=errors.ALL_IMAGES_SYNCED_UP_MESSAGE, success=True)

            # fetch only those objects which have these fields in the list and assigned to the incoming user
            inv_act_assignment_objects = models.InventoryActivityAssignment.objects. \
                filter(
                inventory_activity__shortlisted_inventory_details__id__in=shortlisted_inv_ids,
                inventory_activity__activity_type__in=act_types,
                activity_date__in=act_dates,
                assigned_to=image_taken_by
            )

            if not inv_act_assignment_objects:
                return ui_utils.handle_response(class_name, data=errors.NO_INVENTORY_ACTIVITY_ASSIGNMENT_ERROR)

            # this loop creates actual inv act image objects
            for inv_act_assign in inv_act_assignment_objects:

                image_data_list = inv_act_assignment_to_image_data_map[

                        inv_act_assign.inventory_activity.shortlisted_inventory_details.id,
                        ui_utils.get_date_string_from_datetime(inv_act_assign.activity_date),
                        inv_act_assign.inventory_activity.activity_type
                ]
                for image_data in image_data_list:

                    # add two more fields to complete image_data dict
                    image_data['inventory_activity_assignment'] = inv_act_assign
                    image_data['activity_by'] = image_taken_by
                    inv_image_objects.append(models.InventoryActivityImage(**image_data))

            models.InventoryActivityImage.objects.bulk_create(inv_image_objects)
            return ui_utils.handle_response(class_name, data='success. {0} objects created'.format(len(inv_image_objects)), success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class InventoryActivityAssignment(APIView):
    """
    Handles assignment of inventory activities to a user
    """

    def post(self, request):
        """
        Assigns inv act dates to a user

        Args:
            request: contains shortlisted_spaces_id, inventory_content_type_id, and assigned_activities

        Returns: success in case assignment is complete.
        """
        class_name = self.__class__.__name__
        try:
            inv_assign_data = request.data

            # to store shortlisted inventory pricing details ID and ids of users assigned to
            shortlisted_inv_ids = []
            assigned_to_users_ids = []

            # collect these ids
            for data in inv_assign_data:
                shortlisted_inv_ids.append(int(data['shortlisted_inventory_id']))
                assigned_to_users_ids.append(int(data['assigned_to']))

            # form a map from id --> object. it's helps in fetching objects on basis of ids.
            shortlisted_inv_objects_map = models.ShortlistedInventoryPricingDetails.objects.in_bulk(shortlisted_inv_ids)
            assigned_to_users_objects_map = models.BaseUser.objects.in_bulk(assigned_to_users_ids)

            # inv_act_assign objects container
            inv_assignment_objects = []

            for data in inv_assign_data:
                shortlisted_inv_id = int(data['shortlisted_inventory_id'])
                assigned_to_user_id = int(data['assigned_to'])

                instance, is_created = models.InventoryActivityAssignment.objects.get_or_create(
                    shortlisted_inventory_details=shortlisted_inv_objects_map[shortlisted_inv_id],
                    activity_type=data['activity_type'],
                    activity_date=data['activity_date']
                )
                instance.assigned_to = assigned_to_users_objects_map[assigned_to_user_id]
                instance.assigned_by = request.user

                instance.save()
                inv_assignment_objects.append(instance)

            serializer = website_serializers.InventoryActivityAssignmentSerializer(inv_assignment_objects, many=True)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    def put(self, request):
        """
        updates a single object of inventory activity assignment table
        Args:
            request: contains id of inventory activity assignment model

        Returns: updated object
        """
        class_name = self.__class__.__name__
        try:
            inv_act_assignment_id = request.data['inventory_activity_assignment_id']
            data = request.data.copy()
            data.pop('inventory_activity_assignment_id')
            models.InventoryActivityAssignment.objects.filter(id=inv_act_assignment_id).update(**data)
            instance = models.InventoryActivityAssignment.objects.get(id=inv_act_assignment_id)
            return ui_utils.handle_response(class_name, data=model_to_dict(instance), success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    def get(self, request):
        """
        Args:
            request:
        Returns: fetches inv act assignment  object along with the images that are associated
        """
        class_name = self.__class__.__name__
        try:
            inv_act_assignment_id = request.query_params['inventory_activity_assignment_id']
            inventory_activity_assignment_object = models.InventoryActivityAssignment.objects.get(id=inv_act_assignment_id)
            serializer = website_serializers.InventoryActivityAssignmentSerializerReadOnly(inventory_activity_assignment_object)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class AssignInventoryActivityDateUsers(APIView):
    """
    Assign inventory dates and users for each of the inventories in the list
    """
    def post(self, request):
        """
        request data contains

        Args:
            request:

        Returns: success in case dates and users are assigned to all the inventories in the request

        """
        class_name = self.__class__.__name__
        try:

            shortlisted_inventory_detail_ids = [long(sipd) for sipd in request.data['shortlisted_inventory_id_detail']]
            assignment_detail = request.data['assignment_detail']

            shortlisted_inventory_detail_map = models.ShortlistedInventoryPricingDetails.objects.in_bulk(shortlisted_inventory_detail_ids)
            # they can send all the garbage in activity_type. we need to check if it's valid.
            valid_activity_types = [ac_type[0] for ac_type in models.INVENTORY_ACTIVITY_TYPES]

            inventory_activity_objects = models.InventoryActivity.objects.filter(shortlisted_inventory_details__id__in=shortlisted_inventory_detail_ids)
            # to reduce db hits, a map is created for InventoryActivity model where (shortlisted_inventory_detail_id, activity_type)
            # is keyed for inventoryActivity instance
            inventory_activity_objects_map = {}
            for inv_act_instance in inventory_activity_objects:
                try:
                    inventory_activity_objects_map[inv_act_instance.shortlisted_inventory_details_id, inv_act_instance.activity_type]
                except KeyError:
                    inventory_activity_objects_map[inv_act_instance.shortlisted_inventory_details_id, inv_act_instance.activity_type] = inv_act_instance

            # to reduce db hits, all users are stored and queried beforehand.
            users = set()
            for assignment_data in assignment_detail:
                for date, user in assignment_data['date_user_assignments'].iteritems():
                    users.add(long(user))
            user_map = models.BaseUser.objects.in_bulk(users)

            # now assign for each shortlisted inventory detail id
            for shortlisted_inv_detail_id in shortlisted_inventory_detail_ids:
                for assignment_data in assignment_detail:

                    activity_type = assignment_data['activity_type']

                    if activity_type not in valid_activity_types:
                        return ui_utils.handle_response(class_name, data=errors.INVALID_ACTIVITY_TYPE_ERROR.format(activity_type))
                    try:
                        inventory_activity_instance = inventory_activity_objects_map[shortlisted_inv_detail_id, activity_type]
                    except KeyError:
                        # only create when above combo is not found
                        inventory_activity_instance, is_created = models.InventoryActivity.objects.get_or_create(
                            shortlisted_inventory_details = shortlisted_inventory_detail_map[shortlisted_inv_detail_id],
                            activity_type=activity_type
                        )

                    for date, user in assignment_data['date_user_assignments'].iteritems():
                        inv_act_assignment, is_created = models.InventoryActivityAssignment.objects.get_or_create(inventory_activity=inventory_activity_instance, activity_date=ui_utils.get_aware_datetime_from_string(date))
                        inv_act_assignment.assigned_to = user_map[long(user)]
                        inv_act_assignment.save()

            return ui_utils.handle_response(class_name, data='successfully assigned', success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class ReassignInventoryActivityDateUsers(APIView):
    """
    handles Reassignment of dates on images page.
    """
    def post(self, request):
        """
        updates inventory activity assignment table with new dates which goes in reassigned_activity_date and user
        which goes in assigned_to field.
        Args:
            request:

        Returns: success in case update is successfull

        """
        class_name = self.__class__.__name__
        try:
            data = request.data.copy()
            inventory_activity_assignment_ids = [long(obj_id) for obj_id in data.keys()]
            user_ids = [long(detail['assigned_to']) for detail in data.values()]
            inventory_activity_assignment_map = models.InventoryActivityAssignment.objects.in_bulk(inventory_activity_assignment_ids)
            user_map = models.BaseUser.objects.in_bulk(user_ids)
            inventory_activity_assignment_objects = []
            for inventory_activity_assignment_id, detail in data.iteritems():
                instance = inventory_activity_assignment_map[long(inventory_activity_assignment_id)]
                instance.reassigned_activity_date = ui_utils.get_aware_datetime_from_string(detail['reassigned_activity_date'])
                instance.assigned_to = user_map[long(detail['assigned_to'])]
                inventory_activity_assignment_objects.append(instance)
            bulk_update(inventory_activity_assignment_objects)
            return ui_utils.handle_response(class_name, data='successfully reassigned', success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class UserList(APIView):
    """
        returns all users
    """

    def get(self, request):
        """
        Args:
            request:
        Returns: returns all users
        """
        class_name = self.__class__.__name__
        try:
            users = models.BaseUser.objects.all()
            user_serializer = website_serializers.BaseUserSerializer(users, many=True)
            return ui_utils.handle_response(class_name, data=user_serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)