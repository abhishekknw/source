from rest_framework.views import APIView
from rest_framework import viewsets, status
from django.db.models import Count, Sum
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from pygeocoder import Geocoder, GeocoderError
from openpyxl import load_workbook
from requests.exceptions import ConnectionError
from celery.result import GroupResult
import shutil
import os
import pytz
import v0.permissions as v0_permissions
from django.conf import settings
from models import ProposalInfo, ProposalCenterMapping
from serializers import (ProposalInfoSerializer, ProposalCenterMappingSerializer, ProposalCenterMappingSpaceSerializer,
                         ProposalCenterMappingVersionSpaceSerializer)
from rest_framework.decorators import detail_route, list_route
from v0.ui.account.models import AccountInfo
import v0.ui.website.utils as website_utils
import v0.ui.utils as ui_utils
from v0.ui.organisation.models import Organisation
from django.db import transaction
from v0.ui.location.models import City, CityArea
from v0.ui.campaign.models import GenericExportFileName
from v0.ui.website.views import GenericExportFileSerializerReadOnly
from rest_framework.response import Response
from v0.ui.proposal.serializers import (ProposalInfoSerializer, ProposalCenterMappingSerializer,
                                        ProposalCenterMappingVersionSerializer, ProposalInfoVersionSerializer,
                                        SpaceMappingSerializer, ProposalCenterMappingSpaceSerializer,
                                        ProposalCenterMappingVersionSpaceSerializer, SpaceMappingVersionSerializer,
                                        ProposalSocietySerializer, ProposalCorporateSerializer, HashtagImagesSerializer)
from v0.ui.inventory.models import (SupplierTypeSociety, AdInventoryType, InventorySummary)
from models import (ProposalInfo, ProposalCenterMapping, ProposalCenterMappingVersion, SpaceMappingVersion,
                    SpaceMapping, ShortlistedSpacesVersion, ShortlistedSpaces, SupplierPhase)
from serializers import (SupplierPhaseSerializer)
from v0.ui.inventory.models import (AdInventoryType,InventoryActivityAssignment,InventorySummary,InventoryTypeVersion,
                                    InventoryType,InventoryActivity)
from v0.ui.inventory.serializers import (InventoryTypeSerializer, InventoryTypeVersionSerializer)
from v0.ui.finances.models import (ShortlistedInventoryPricingDetails, PriceMappingDefault, getPriceDict)
from v0.ui.campaign.models import Campaign
from v0.ui.website.utils import return_price
import v0.constants as v0_constants
import v0.ui.website.tasks as tasks
from v0.ui.supplier.models import SupplierTypeCorporate
from v0.ui.base.models import DurationType
from v0 import errors
from rest_framework import viewsets
from models import SupplierPhase, ProposalInfo
from serializers import SupplierPhaseSerializer
from v0.ui.utils import handle_response



def create_proposal_object(organisation_id, account_id, user, tentative_cost, name):
    account = AccountInfo.objects.get_permission(user=user, account_id=account_id)
    return {
        'organisation_id': organisation_id,
        'account_id': account_id,
        'proposal_id': website_utils.get_generic_id(
            [Organisation.objects.get(pk=organisation_id).name, AccountInfo.objects.get(pk=account_id).name]),
        'account': account.account_id,
        'user': user.id,
        'created_by': user.id,
        'tentative_cost': tentative_cost,
        'name': name
        # 'campaign_state': 'PTC'
    }


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
                organisation_id = proposal_data['organisation_id']
                account_id = account_id

                # create a unique proposal id
                proposal_data['proposal_id'] = website_utils.get_generic_id(
                    [Organisation.objects.get(pk=organisation_id).name, AccountInfo.objects.get(pk=account_id).name])

                # get the account object. required for creating the proposal
                account = AccountInfo.objects.get_permission(user=user, account_id=account_id)
                proposal_data['account'] = account.account_id
                proposal_data['user'] = user.id

                # query for parent. if available set it. if it's available, then this is an EDIT request.
                parent = request.data.get('parent')
                parent = parent if parent != '0' else None
                proposal_data['parent'] = parent
                # set parent if available
                if parent:
                    proposal_data['parent'] = ProposalInfo.objects.get_permission(user=user,
                                                                                  proposal_id=parent).proposal_id

                # call the function that saves basic proposal information
                proposal_data['created_by'] = user.username
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
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


class CreateInitialProposalBulkBasic(APIView):
    def post(self, request):
        class_name = self.__class__.__name__
        source_file = request.data['file']
        wb = load_workbook(source_file)
        ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
        proposal_list = []
        campaign_list = []
        proposal_data = {}
        organisation_id = request.data['organisation_id']
        account_id = request.data['account_id']
        user = request.user
        tentative_cost = request.data['tentative_cost']
        name = request.data['name']
        proposal_data = create_proposal_object(organisation_id, account_id, user, tentative_cost, name)
        response = website_utils.create_basic_proposal(proposal_data)
        if not response.data['status']:
            return response
        center_name = request.data['center_name']
        city = request.data['city']
        area = request.data['area']
        subarea = request.data['subarea']
        pincode = request.data['pincode']
        radius = request.data['radius']
        address = request.data['address']
        supplier_codes = request.data['codes'].split(',')
        supplier_codes = [x.strip(' ') for x in supplier_codes]
        city_id = City.objects.get(city_name=city).id
        area_id = CityArea.objects.get(label=area).id
        all_suppliers = {'RS': 'Societies', 'CP': 'Corporate Parks', 'BS': 'Bus Shelter', 'GY': 'Gym', 'SA': 'Saloon',
                         'RE': 'Retail Shop'}
        suppliers = []
        for supplier in all_suppliers:
            selected_status = False
            if supplier in supplier_codes:
                selected_status = True
            suppliers.append({
                'selected': selected_status,
                'code': supplier,
                'name': all_suppliers[supplier]
            })
        centers = [{
            'isEditProposal': False,
            'city': city_id,
            'area': area_id,
            'suppliers': suppliers,
            'center': {
                'city': city,
                'area': area,
                'codes': supplier_codes,
                'center_name': center_name,
                'subarea': subarea,
                'pincode': pincode,
                'radius': radius,
                'address': address
            }}]
        proposal_data['centers'] = centers
        center_response = website_utils.save_center_data(proposal_data, user)
        center_id = center_response.data['data']['center_id']
        if not center_response.data['status']:
            return response
        for index, row in enumerate(ws.iter_rows()):
            if index > 0:
                start_date = row[0].value if row[0].value else None
                end_date = row[1].value if row[1].value else None
                invoice_no = int(row[2].value) if row[2].value else None
                poster_filter = True if int(row[3].value) == 1 else False
                standee_filter = True if int(row[4].value) == 1 else False
                flier_filter = True if int(row[5].value) == 1 else False
                stall_filter = True if int(row[6].value) == 1 else False
                gatewayarch_filter = True if int(row[7].value) == 1 else False
                supplier_id = row[8].value if row[8].value else None
                total_negotiated_price = int(row[9].value) if row[9].value else None
                start_date = start_date.replace(tzinfo=pytz.UTC) if start_date else None
                end_date = end_date.replace(tzinfo=pytz.UTC) if end_date else None
                proposal_data['tentative_start_date'] = start_date
                proposal_data['tentative_end_date'] = end_date
                proposal_data['center_id'] = center_id
                proposal_data['invoice_number'] = invoice_no
                proposal_data['total_negotiated_price'] = total_negotiated_price
                center = ProposalCenterMapping.objects.get(pk=center_id)
                filter_codes = []
                if poster_filter:
                    filter_codes.append({'id': 'PO'})
                if stall_filter:
                    filter_codes.append({'id': 'SL'})
                if standee_filter:
                    filter_codes.append({'id': 'ST'})
                if flier_filter:
                    filter_codes.append({'id': 'FL'})
                if gatewayarch_filter:
                    filter_codes.append({'id': 'GA'})
                supplier_data = [{
                    'status': 'F',
                    'id': supplier_id,
                    'total_negotiated_price': total_negotiated_price
                }]
                center_data = {
                    'RS': {
                        'filter_codes': filter_codes,
                        'supplier_data': supplier_data
                    }
                }
                proposal_data['center_data'] = center_data
                proposal = ProposalInfo.objects.get(pk=proposal_data['proposal_id'])
                for supplier_code in proposal_data['center_data']:
                    response = website_utils.save_filters(center, supplier_code, proposal_data, proposal)
                    if not response.data['status']:
                        return response
                    response = website_utils.save_shortlisted_suppliers_data(center, supplier_code, proposal_data,
                                                                             proposal)
                    if not response.data['status']:
                        return response
                    response = website_utils.save_shortlisted_inventory_pricing_details_data(center, supplier_code,
                                                                                             proposal_data, proposal)
                    if not response.data['status']:
                        return response
                response = website_utils.update_proposal_invoice_and_state(proposal_data, proposal)
                if not response.data['status']:
                    return response
                response = website_utils.create_generic_export_file_data(proposal)
                if not response.data['status']:
                    return response
        return ui_utils.handle_response({}, data='success', success=True)


class ChildProposals(APIView):
    """
    Fetches child proposals of a given proposal. if the given proposal is string '0', all the parent proposals are fetched.
    """

    def get(self, request, proposal_id=None):

        """
        Fetches all proposals who have parent = pk
        Args:
            request: request param
            pk: parent pk value. if pk == '0',this means we need to fetch all proposals whose parent is NULL.
            proposal_id: Proposal id
        Returns:
        """
        class_name = self.__class__.__name__
        try:
            account_id = request.query_params.get('account_id')
            account_id = account_id if account_id != '0' else None
            data = {
                'parent': proposal_id if proposal_id != '0' else None,
                'user': request.user,
                'account_id': account_id
            }
            return ui_utils.handle_response(class_name, data=website_utils.child_proposals(data), success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


class ProposalViewSet(viewsets.ViewSet):
    """
    A ViewSet handling various operations related to ProposalModel.
    This viewset was made instead of creating separate ApiView's because all the api's in this viewset
    are related to Proposal domain. so keeping them at one place makes sense.
    """

    # parser_classes = (JSONParser, FormParser)
    # permission_classes = (v0_permissions.IsProposalAuthenticated, )

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
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    def list(self, request):
        class_name = self.__class__.__name__
        try:
            proposal = ProposalInfo.objects.all()
            serializer = ProposalInfoSerializer(proposal, many=True)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

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
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

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
            response = website_utils.construct_proposal_response(pk)
            if not response.data['status']:
                return response
            return ui_utils.handle_response(class_name, data=response.data['data'], success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

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
            file_objects = GenericExportFileName.objects.select_related('proposal', 'user').filter(
                proposal__invoice_number__isnull=False, is_exported=False).order_by('-proposal__created_on')

            # we need to make a unique list where proposal_id do not repeat.
            seen = set()
            final_file_objects = []
            for file_object in file_objects:
                proposal_id = file_object.proposal_id
                if proposal_id not in seen:
                    seen.add(proposal_id)
                    final_file_objects.append(file_object)
            file_serializer = GenericExportFileSerializerReadOnly(final_file_objects, many=True)
            return ui_utils.handle_response(class_name, data=file_serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

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
            }

            # update center's radius here. This is being updated so that when next time get_spaces is called, radius is reflected in front end
            if center_id:
                instance = ProposalCenterMapping.objects.get(id=int(center_id))
                instance.radius = float(radius)
                instance.save()

            response = website_utils.suppliers_within_radius(data)
            if not response.data['status']:
                return response

            response = website_utils.add_shortlisted_suppliers_get_spaces(pk, request.user, response.data['data'])
            if not response.data['status']:
                return response

            return ui_utils.handle_response(class_name, data=response.data['data'], success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

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
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    @detail_route(methods=['PUT'])
    def shortlisted_suppliers_status(self, request, pk=None):
        """
            Update shortlisted suppliers based on their status value.
        Response looks like :def list
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
            shortlisted_suppliers = []

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
                shortlisted_suppliers.append(
                    website_utils.save_shortlisted_suppliers(request.data['suppliers'][code], fixed_data))

            return ui_utils.handle_response(class_name, data=shortlisted_suppliers, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


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
            'society': 'RS', 'corporate': 'CP',
            'gym': 'GY', 'salon': 'SA'
        }

        with transaction.atomic():
            proposal_data = request.data
            proposal_data['proposal_id'] = self.create_proposal_id()
            try:
                account = AccountInfo.objects.get(account_id=account_id)
            except AccountInfo.DoesNotExist:
                return Response({'message': 'Invalid Account ID'}, status=406)
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
                    return Response({'message': 'Invalid Proposal Info', 'errors': \
                        proposal_serializer.errors}, status=406)

                for center_info in proposal_data['centers']:
                    center = center_info['center']
                    space_mapping = center['space_mapping']
                    center['proposal'] = proposal_object.proposal_id
                    address = center['address'] + "," + center['subarea'] + ',' + center['area'] + ',' + center[
                        'city'] + ' ' + center['pincode']
                    geocoder = Geocoder(api_key='AIzaSyCy_uR_SVnzgxCQTw1TS6CYbBTQEbf6jOY')
                    try:
                        geo_object = geocoder.geocode(address)
                    except GeocoderError:
                        ProposalInfo.objects.get(proposal_id=proposal_object.proposal_id).delete()
                        return Response({'message': 'Latitude Longitude Not found for address : ' + address},
                                        status=406)
                    except ConnectionError:
                        ProposalInfo.objects.get(proposal_id=proposal_object.proposal_id).delete()
                        return Response({'message': 'Unable to connect to google Maps'}, status=406)

                    center['latitude'] = geo_object.latitude
                    center['longitude'] = geo_object.longitude

                    center_serializer = ProposalCenterMappingSerializer(data=center)

                    if center_serializer.is_valid():
                        center_object = center_serializer.save()
                    else:
                        ProposalInfo.objects.get(proposal_id=proposal_object.proposal_id).delete()
                        return Response({'message': 'Invalid Center Data', 'errors': center_serializer.errors}, \
                                        status=406)

                    space_mapping['center'] = center_object.id
                    space_mapping['proposal'] = proposal_object.proposal_id
                    space_mapping_serializer = SpaceMappingSerializer(data=space_mapping)
                    if space_mapping_serializer.is_valid():
                        space_mapping_object = space_mapping_serializer.save()
                    else:
                        ProposalInfo.objects.get(proposal_id=proposal_object.proposal_id).delete()
                        return Response({
                            'message': 'Invalid Space Mapping Data',
                            'errors': space_mapping_serializer.errors
                        }, status=406)

                    # ADDNEW --> extend the list in for loop when new spaces added. Keep the variables names accordingly
                    for space in ['society', 'corporate', 'gym', 'salon']:
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
                                        'message': 'Invalid Inventory Type Info',
                                        'errors': inventory_type_serializer.errors
                                    })
                        except KeyError:
                            pass

        return Response(proposal_object.proposal_id, status=200)

    def create_proposal_id(self):
        import random, string
        return ''.join(random.choice(string.ascii_letters) for _ in range(8))


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


class CurrentProposalAPIView(APIView):

    def get(self, request, proposal_id, format=None):
        ''' This returns the proposal info of the proposal id
        '''

        try:
            proposal_object = ProposalInfo.objects.get(proposal_id=proposal_id)
        except ProposalInfo.DoesNotExist:
            return Response({'message': 'Invalid Proposal ID'}, status=406)

        proposal_serializer = ProposalInfoSerializer(proposal_object)
        centers = proposal_object.get_centers()
        centers_list = []

        for center in centers:
            space_info_dict = {}
            space_mapping_object = center.get_space_mappings()
            center_serializer = ProposalCenterMappingSpaceSerializer(center)
            space_info_dict['center'] = center_serializer.data

            if space_mapping_object.society_allowed:
                societies_shortlisted_ids = ShortlistedSpaces.objects.filter(space_mapping=space_mapping_object,
                                                                             supplier_code='RS',
                                                                             buffer_status=False).values_list(
                    'object_id', flat=True)

                societies_shortlisted_temp = SupplierTypeSociety.objects.filter(
                    supplier_id__in=societies_shortlisted_ids).values('supplier_id', 'society_latitude',
                                                                      'society_longitude', 'society_name',
                                                                      'society_address1', 'society_subarea',
                                                                      'society_location_type')

                societies_shortlisted = []
                societies_shortlisted_count = 0

                for society in societies_shortlisted_temp:
                    society_inventory_obj = InventorySummary.objects.get_supplier_type_specific_object(
                        request.data.copy(),
                        society['supplier_id'])
                    # society_inventory_obj = InventorySummary.objects.get(supplier_id=society['supplier_id'])
                    society['shortlisted'] = True
                    society['buffer_status'] = False
                    # obj = InventorySummaryAPIView()
                    adinventory_type_dict = ui_utils.adinventory_func()
                    duration_type_dict = ui_utils.duration_type_func()

                    if society_inventory_obj.poster_allowed_nb or society_inventory_obj.poster_allowed_lift:
                        society['total_poster_count'] = society_inventory_obj.poster_count_per_tower
                        society['poster_price'] = return_price(adinventory_type_dict, duration_type_dict, 'poster_a4',
                                                               'campaign_weekly')

                    if society_inventory_obj.standee_allowed:
                        society['total_standee_count'] = society_inventory_obj.total_standee_count
                        society['standee_price'] = return_price(adinventory_type_dict, duration_type_dict,
                                                                'standee_small', 'campaign_weekly')

                    if society_inventory_obj.stall_allowed:
                        society['total_stall_count'] = society_inventory_obj.total_stall_count
                        society['stall_price'] = return_price(adinventory_type_dict, duration_type_dict, 'stall_small',
                                                              'unit_daily')
                        society['car_display_price'] = return_price(adinventory_type_dict, duration_type_dict,
                                                                    'car_display_standard', 'unit_daily')

                    if society_inventory_obj.flier_allowed:
                        society['flier_frequency'] = society_inventory_obj.flier_frequency
                        society['filer_price'] = return_price(adinventory_type_dict, duration_type_dict,
                                                              'flier_door_to_door', 'unit_daily')

                    societies_shortlisted.append(society)
                    societies_shortlisted_count += 1

                space_info_dict['societies_shortlisted'] = societies_shortlisted
                space_info_dict['societies_shortlisted_count'] = societies_shortlisted_count

                societies_buffered_ids = ShortlistedSpaces.objects.filter(space_mapping=space_mapping_object,
                                                                          supplier_code='RS', \
                                                                          buffer_status=True).values_list('object_id',
                                                                                                          flat=True)
                societies_buffered_temp = SupplierTypeSociety.objects.filter(
                    supplier_id__in=societies_buffered_ids).values('supplier_id', 'society_latitude',
                                                                   'society_longitude', 'society_name',
                                                                   'society_address1', 'society_subarea',
                                                                   'society_location_type')
                societies_buffered = []
                societies_buffered_count = 0
                for society in societies_buffered_temp:
                    society_inventory_obj = InventorySummary.objects.get_supplier_type_specific_object(
                        request.data.copy(),
                        society['supplier_id'])

                    # society_inventory_obj = InventorySummary.objects.get(supplier_id=society['supplier_id'])
                    society['shortlisted'] = True
                    society['buffer_status'] = False
                    # obj = InventorySummaryAPIView()
                    adinventory_type_dict = ui_utils.adinventory_func()
                    duration_type_dict = ui_utils.duration_type_func()

                    if society_inventory_obj.poster_allowed_nb or society_inventory_obj.poster_allowed_lift:
                        society['total_poster_count'] = society_inventory_obj.poster_count_per_tower
                        society['poster_price'] = return_price(adinventory_type_dict, duration_type_dict, 'poster_a4',
                                                               'campaign_weekly')

                    if society_inventory_obj.standee_allowed:
                        society['total_standee_count'] = society_inventory_obj.total_standee_count
                        society['standee_price'] = return_price(adinventory_type_dict, duration_type_dict,
                                                                'standee_small', 'campaign_weekly')

                    if society_inventory_obj.stall_allowed:
                        society['total_stall_count'] = society_inventory_obj.total_stall_count
                        society['stall_price'] = return_price(adinventory_type_dict, duration_type_dict, 'stall_small',
                                                              'unit_daily')
                        society['car_display_price'] = return_price(adinventory_type_dict, duration_type_dict,
                                                                    'car_display_standard', 'unit_daily')

                    if society_inventory_obj.flier_allowed:
                        society['flier_frequency'] = society_inventory_obj.flier_frequency
                        society['filer_price'] = return_price(adinventory_type_dict, duration_type_dict,
                                                              'flier_door_to_door', 'unit_daily')

                    societies_buffered.append(society)
                    societies_buffered_count += 1

                space_info_dict['societies_buffered'] = societies_buffered
                space_info_dict['societies_buffered_count'] = societies_buffered_count

                societies_inventory = InventoryType.objects.get(supplier_code='RS', space_mapping=space_mapping_object)
                societies_inventory_serializer = InventoryTypeSerializer(societies_inventory)
                # inventory count only for shortlisted ones
                # to add buffered societies as well uncomment following line
                # societies_shortlisted_ids.extend(societies_buffered_ids)
                societies_inventory_count = InventorySummary.objects.filter(
                    supplier_id__in=societies_shortlisted_ids).aggregate(posters=Sum('poster_count_per_tower'), \
                                                                         standees=Sum('total_standee_count'),
                                                                         stalls=Sum('total_stall_count'),
                                                                         fliers=Sum('flier_frequency'))

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
            'proposal': proposal_serializer.data,
            'centers': centers_list,
        }

        return Response(response, status=200)

    def post(self, request, proposal_id, format=None):
        ''' Updates the buffer and shortlisted spaces. This API allows user to delete
        move buffer to shortlisted and vice versa. No addition allowed using this API
        '''
        try:
            proposal_object = ProposalInfo.objects.get(proposal_id=proposal_id)
        except ProposalInfo.DoesNotExist:
            return Response({'message': 'Invalid Proposal ID'}, status=406)

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
                        shortlisted_society = ShortlistedSpaces(space_mapping_id=space_mapping_id,
                                                                content_type=content_type, \
                                                                supplier_code=supplier_code, object_id=object_id,
                                                                buffer_status=society['buffer_status'])

                        shortlisted_space_list.append(shortlisted_society)

                for society in center_info['societies_buffered']:
                    if society['shortlisted']:
                        object_id = society['supplier_id']
                        shortlisted_society = ShortlistedSpaces(space_mapping_id=space_mapping_id,
                                                                content_type=content_type,
                                                                supplier_code=supplier_code, object_id=object_id,
                                                                buffer_status=society['buffer_status'])

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
            return Response({'message': 'Invalid Proposal ID'}, status=406)

        proposal_versions = proposal_object.get_proposal_versions()
        proposal_versions_list = []

        try:
            for proposal_version_object in proposal_versions:
                proposal_info_dict = {}
                proposal_version_serializer = ProposalInfoVersionSerializer(proposal_version_object)
                proposal_info_dict['proposal'] = proposal_version_serializer.data
                proposal_center_versions = ProposalCenterMappingVersion.objects.filter(
                    proposal_version=proposal_version_object)
                center_versions_list = []
                for center_version_object in proposal_center_versions:
                    space_info_dict = {}
                    center_version_serailizer = ProposalCenterMappingVersionSpaceSerializer(center_version_object)
                    space_info_dict['center'] = center_version_serailizer.data

                    space_mapping_version_object = SpaceMappingVersion.objects.get(center_version=center_version_object)

                    if space_mapping_version_object.society_allowed:
                        societies_shortlisted_ids = ShortlistedSpacesVersion.objects.filter(
                            space_mapping_version=space_mapping_version_object,
                            supplier_code='RS', buffer_status=False).values_list('object_id', flat=True)
                        societies_shortlisted_temp = SupplierTypeSociety.objects.filter(
                            supplier_id__in=societies_shortlisted_ids).values('supplier_id', 'society_latitude',
                                                                              'society_longitude', 'society_name',
                                                                              'society_address1', 'society_subarea',
                                                                              'society_location_type')
                        societies_shortlisted = []
                        societies_shortlisted_count = 0
                        # societies_shortlisted_serializer = ProposalSocietySerializer(societies_shortlisted, many=True)
                        for society in societies_shortlisted_temp:
                            society_inventory_obj = InventorySummary.objects.get_supplier_type_specific_object(
                                request.data.copy(),
                                society['supplier_id'])

                            # society_inventory_obj = InventorySummary.objects.get(supplier_id=society['supplier_id'])
                            society['shortlisted'] = True
                            society['buffer_status'] = False
                            # obj = InventorySummaryAPIView()
                            adinventory_type_dict = ui_utils.adinventory_func()
                            duration_type_dict = ui_utils.duration_type_func()

                            if society_inventory_obj.poster_allowed_nb or society_inventory_obj.poster_allowed_lift:
                                society['total_poster_count'] = society_inventory_obj.total_poster_count
                                society['poster_price'] = return_price(adinventory_type_dict, duration_type_dict,
                                                                       'poster_a4', 'campaign_weekly')

                            if society_inventory_obj.standee_allowed:
                                society['total_standee_count'] = society_inventory_obj.total_standee_count
                                society['standee_price'] = return_price(adinventory_type_dict, duration_type_dict,
                                                                        'standee_small', 'campaign_weekly')

                            if society_inventory_obj.stall_allowed:
                                society['total_stall_count'] = society_inventory_obj.total_stall_count
                                society['stall_price'] = return_price(adinventory_type_dict, duration_type_dict,
                                                                      'stall_small', 'unit_daily')
                                society['car_display_price'] = return_price(adinventory_type_dict, duration_type_dict,
                                                                            'car_display_standard', 'unit_daily')

                            if society_inventory_obj.flier_allowed:
                                society['flier_frequency'] = society_inventory_obj.flier_frequency
                                society['filer_price'] = return_price(adinventory_type_dict, duration_type_dict,
                                                                      'flier_door_to_door', 'unit_daily')

                            societies_shortlisted.append(society)
                            societies_shortlisted_count += 1

                        space_info_dict['societies_shortlisted'] = societies_shortlisted
                        space_info_dict['societies_shortlisted_count'] = societies_shortlisted_count

                        societies_buffered_ids = ShortlistedSpacesVersion.objects.filter(
                            space_mapping_version=space_mapping_version_object, \
                            supplier_code='RS', buffer_status=True).values_list('object_id', flat=True)
                        societies_buffered_temp = SupplierTypeSociety.objects.filter(
                            supplier_id__in=societies_buffered_ids).values('supplier_id', 'society_latitude',
                                                                           'society_longitude', 'society_name',
                                                                           'society_address1', 'society_subarea',
                                                                           'society_location_type')
                        # societies_buffered_serializer = ProposalSocietySerializer(societies_buffered, many=True)
                        societies_buffered = []
                        societies_buffered_count = 0
                        for society in societies_buffered_temp:
                            society_inventory_obj = InventorySummary.objects.get_supplier_type_specific_object(
                                request.data.copy(),
                                society['supplier_id'])

                            # society_inventory_obj = InventorySummary.objects.get(supplier_id=society['supplier_id'])
                            society['shortlisted'] = True
                            society['buffer_status'] = False
                            # obj = InventorySummaryAPIView()
                            adinventory_type_dict = ui_utils.adinventory_func()
                            duration_type_dict = ui_utils.duration_type_func()

                            if society_inventory_obj.poster_allowed_nb or society_inventory_obj.poster_allowed_lift:
                                society['total_poster_count'] = society_inventory_obj.total_poster_count
                                society['poster_price'] = return_price(adinventory_type_dict, duration_type_dict,
                                                                       'poster_a4', 'campaign_weekly')

                            if society_inventory_obj.standee_allowed:
                                society['total_standee_count'] = society_inventory_obj.total_standee_count
                                society['standee_price'] = return_price(adinventory_type_dict, duration_type_dict,
                                                                        'standee_small', 'campaign_weekly')

                            if society_inventory_obj.stall_allowed:
                                society['total_stall_count'] = society_inventory_obj.total_stall_count
                                society['stall_price'] = return_price(adinventory_type_dict, duration_type_dict,
                                                                      'stall_small', 'unit_daily')
                                society['car_display_price'] = return_price(adinventory_type_dict, duration_type_dict,
                                                                            'car_display_standard', 'unit_daily')

                            if society_inventory_obj.flier_allowed:
                                society['flier_freqency'] = society_inventory_obj.flier_frequency
                                society['filer_price'] = return_price(adinventory_type_dict, duration_type_dict,
                                                                      'flier_door_to_door', 'unit_daily')

                            societies_buffered.append(society)
                            societies_buffered_count += 1

                        space_info_dict['societies_buffered'] = societies_buffered
                        space_info_dict['societies_buffered_count'] = societies_buffered_count

                        societies_inventory = InventoryTypeVersion.objects.get(supplier_code='RS', \
                                                                               space_mapping_version=space_mapping_version_object)
                        societies_inventory_serializer = InventoryTypeVersionSerializer(societies_inventory)
                        societies_inventory_count = InventorySummary.objects.filter(
                            supplier_id__in=societies_shortlisted_ids).aggregate(posters=Sum('total_poster_count'), \
                                                                                 standees=Sum('total_standee_count'),
                                                                                 stalls=Sum('total_stall_count'),
                                                                                 fliers=Sum('flier_frequency'))

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


class HashtagImagesViewSet(viewsets.ViewSet):
    """
    This class is arround hashtagged images by audit app
    """

    def create(self, request):
        """

        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            data = request.data.copy()
            supplier_type_code = request.data.get('supplierTypeCode')
            response = ui_utils.get_content_type(supplier_type_code)
            if not response:
                return response
            content_type = response.data.get('data')
            data['content_type'] = content_type.id
            serializer = HashtagImagesSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return ui_utils.handle_response(class_name, data=serializer.data, success=True)
            return ui_utils.handle_response(class_name, data=serializer.errors)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


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

    permission_classes = (v0_permissions.IsProposalAuthenticated,)

    def post(self, request, proposal_id):
        """
        Args:
            request: request data
            proposal_id: proposal_id to be updated

        Returns: success if data is saved successfully.
        """
        class_name = self.__class__.__name__
        try:
            # when save button is clicked, we have already saved space status before hand on individual API call. Only filters are saved here.
            website_utils.setup_create_final_proposal_post(request.data, proposal_id, delete_and_save_filter_data=True,
                                                           delete_and_save_spaces=False)
            return ui_utils.handle_response(class_name, data='success', success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    def put(self, request, proposal_id):
        """
        Args:
            request: The request object
            proposal_id: The proposal id

        Returns: updates ShortlistedSpaces table with new data or creates the shortlisted space if not already there. PUT does the job of creating data already.
        """
        class_name = self.__class__.__name__
        try:

            supplier_type_code = request.data['supplier_type_code']

            content_type_response = ui_utils.get_content_type(supplier_type_code)
            if not content_type_response.data['status']:
                return content_type_response
            content_type = content_type_response.data['data']

            data = {
                'center_id': request.data['center_id'],
                'proposal_id': proposal_id,
                'object_id': request.data['supplier_id'],
                'content_type': content_type,
                'supplier_code': supplier_type_code
            }
            status = request.data['status']
            obj, is_created = ShortlistedSpaces.objects.get_or_create(**data)
            obj.status = status
            obj.save()
            return ui_utils.handle_response(class_name, data='success', success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


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

    # permission_classes = (v0_permissions.IsProposalAuthenticated, )

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
            proposal = ProposalInfo.objects.get(proposal_id=proposal_id)
            account = AccountInfo.objects.get(account_id=proposal.account.account_id)
            business = Organisation.objects.get(organisation_id=account.organisation.organisation_id)

            # if you don't provide this value, No proposal version is created.
            is_proposal_version_created = request.data['is_proposal_version_created'] if request.data.get(
                'is_proposal_version_created') else False
            data = request.data['centers']

            # if this variable is true, we will have to create a new proposal version.
            if is_proposal_version_created:
                # create a unique proposal id
                new_proposal_id = website_utils.create_proposal_id(business.organisation_id, account.account_id)

                # create new ProposalInfo object for this new proposal_id
                proposal.pk = new_proposal_id
                proposal.save()

                # change the parent and save again
                proposal.parent = proposal
                proposal.save()
                # change the proposal_id variable here
                proposal_id = new_proposal_id

            # call create Final Proposal first. We need to delete and save filter data. We don't save spaces here. The single status of each space has already been done before on Grid View.
            website_utils.setup_create_final_proposal_post(data, proposal_id, delete_and_save_filter_data=True,
                                                           delete_and_save_spaces=False)

            result = website_utils.setup_generic_export(data, request.user, proposal_id)
            file_name = result['name']
            stats = result['stats']
            # todo : either we can check stats and if it's not empty we can throw error here and not allow sheet formation
            # or we can allow sheet formation and let the user know that such errors have occurred. Fix when it's clear

            bd_body = {
                'user_name': request.user.first_name,
                'business': business.name,
                'account': account.name,
                'proposal_id': proposal_id,
                'file_name': file_name
            }

            bd_body = website_utils.process_template(v0_constants.bodys['bd_head'], bd_body)

            email_data = {
                'subject': v0_constants.subjects['bd_head'],
                'body': bd_body,
                'to': [v0_constants.emails['bd_head'], v0_constants.emails['bd_user'], v0_constants.emails['root_user']]
            }

            #  email_data = {
            #     'subject': v0_constants.subjects['bd_head'],
            #     'body': bd_body,
            #     'to': [v0_constants.emails['developer'], ]
            # }

            attachment = {
                'file_name': file_name,
                'mime_type': v0_constants.mime['xlsx']
            }

            # send mail to Bd Head with attachment
            bd_head_async_id = tasks.send_email.delay(email_data, attachment=attachment).id

            # send mail to logged in user without attachment
            email_data = {
                'subject': v0_constants.subjects['agency'],
                'body': v0_constants.bodys['agency'],
                'to': [user.email]
            }

            logged_in_user_async_id = tasks.send_email.delay(email_data).id

            # upload this shit to amazon
            upload_to_amazon_aync_id = tasks.upload_to_amazon.delay(file_name).id

            # prepare to send back async ids
            data = {
                'logged_in_user_async_id': logged_in_user_async_id,
                'bd_head_async_id': bd_head_async_id,
                'upload_to_amazon_async_id': upload_to_amazon_aync_id,
                'file_name': file_name,
                'stats': stats
            }
            # change campaign state
            proposal.campaign_state = v0_constants.proposal_requested
            proposal.save()

            # change the status of the proposal to 'requested' once everything is okay.
            return ui_utils.handle_response(class_name, data=data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


class ProposalToCampaign(APIView):
    """
    sets the campaign state to right state that
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

            proposal = ProposalInfo.objects.get(proposal_id=proposal_id)

            if not proposal.invoice_number:
                return ui_utils.handle_response(class_name, data=errors.CAMPAIGN_NO_INVOICE_ERROR, request=request)

            proposal_start_date = proposal.tentative_start_date
            proposal_end_date = proposal.tentative_end_date

            if not proposal_start_date or not proposal_end_date:
                return ui_utils.handle_response(class_name, data=errors.NO_DATES_ERROR.format(proposal_id),
                                                request=request)

            # todo: disabling this check. Now user can press accept as many times as required.
            #
            # response = website_utils.is_campaign(proposal)
            # if response.data['status']:
            #     return ui_utils.handle_response(class_name, data=errors.ALREADY_A_CAMPAIGN_ERROR.format(proposal.proposal_id), request=request)

            # these are the current inventories assigned. These are inventories assigned to this proposal when sheet was imported.
            # current_assigned_inventories = models.ShortlistedInventoryPricingDetails.objects.select_related('shortlisted_spaces').filter(shortlisted_spaces__proposal_id=proposal_id)

            # assign default dates when you have some inventories assigned
            # if current_assigned_inventories:
            #     current_assigned_inventories_map = {}
            #
            #     for inv in current_assigned_inventories:
            #         inv_tuple = (inv.inventory_content_type, inv.inventory_id)
            #         current_assigned_inventories_map[inv_tuple] = (proposal_start_date, proposal_end_date, inv)
            #
            #     # currently set the R.D and C.D of all inventories to proposal's start and end date.
            #     inventory_release_closure_list = [(inv, proposal_start_date, proposal_end_date) for inv in current_assigned_inventories]
            #     response = website_utils.insert_release_closure_dates(inventory_release_closure_list)
            #     if not response.data['status']:
            #         return response

            # convert to campaign and return
            proposal.campaign_state = v0_constants.proposal_converted_to_campaign
            proposal.save()
            return ui_utils.handle_response(class_name, data=errors.PROPOSAL_CONVERTED_TO_CAMPAIGN.format(proposal_id),
                                            success=True)

            # todo: uncomment this code and modify when date based booking of inventory comes into picture
            # # get all the proposals which are campaign and which overlap with the current campaign
            # response = website_utils.get_overlapping_campaigns(proposal)
            # if not response.data['status']:
            #     return response
            # overlapping_campaigns = response.data['data']
            #
            # if not overlapping_campaigns:
            #     # currently we have no choice but to book all inventories the same proposal_start and end date
            #     # this can be made smarter when we know for how many days a particular inventory  is allowed in a
            #     # supplier this will help in automatically determining R.D and C.D.
            #     inventory_release_closure_list = [(inv, proposal_start_date, proposal_end_date) for inv in current_assigned_inventories]
            #     response = website_utils.insert_release_closure_dates(inventory_release_closure_list)
            #     if not response.data['status']:
            #         return response
            #     proposal.campaign_state = v0_constants.proposal_converted_to_campaign
            #     proposal.save()
            #     return ui_utils.handle_response(class_name,data=errors.PROPOSAL_CONVERTED_TO_CAMPAIGN.format(proposal_id), success=True)
            #
            # already_booked_inventories = models.ShortlistedInventoryPricingDetails.objects.filter(shortlisted_spaces__proposal__in=overlapping_campaigns)
            # already_booked_inventories_map = {}
            #
            # for inv in already_booked_inventories:
            #     inv_tuple = (inv.inventory_content_type, inv.inventory_id)
            #     target_tuple = (inv.release_date, inv.closure_date, inv.shortlisted_spaces.proposal_id)
            #     try:
            #         reference = already_booked_inventories_map[inv_tuple]
            #     except KeyError:
            #         already_booked_inventories_map[inv_tuple] = []
            #         reference = already_booked_inventories_map[inv_tuple]
            #     reference.append(target_tuple)
            #
            # response = website_utils.book_inventories(current_assigned_inventories_map, already_booked_inventories_map)
            # if not response.data['status']:
            #     return response
            # booked_inventories, inventory_release_closure_list, inv_error_list = response.data['data']
            #
            # # if there is something in error list then one or more inventories overlapped with already running campaigns
            # # we do not convert a proposal into campaign in this case
            # if inv_error_list:
            #     return ui_utils.handle_response(class_name, data=errors.CANNOT_CONVERT_TO_CAMPAIGN_ERROR.format(proposal_id, inv_error_list))
            #
            # # insert the RD and CD dates for each inventory
            # response = website_utils.insert_release_closure_dates(inventory_release_closure_list)
            # if not response.data['status']:
            #     return response
            #
            # bulk_update(booked_inventories)
            # proposal.campaign_state = v0_constants.proposal_converted_to_campaign
            # proposal.save()
            #
            # return ui_utils.handle_response(class_name, data=errors.PROPOSAL_CONVERTED_TO_CAMPAIGN.format(proposal_id), success=True)

        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


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
            return Response({'message': 'Invalid Proposal ID sent'}, status=406)

        space_dict, supplier_code_dict = self.get_space_code_dict()
        # ADDNEW -->
        space_model_dict = {
            'society': SupplierTypeSociety, 'corporate': SupplierTypeCorporate,
            # 'gym' : SupplierTypeGym,          'salon' : SupplierTypesalon
        }

        space_serializer_dict = {
            'society': ProposalSocietySerializer, 'corporate': ProposalCorporateSerializer,
            # 'gym' : ProposalGymSerializer,        'salon' : ProposalsalonSerializer
        }

        centers_objects = proposal_object.get_centers()
        centers_list = []

        for center_object in centers_objects:
            space_info_dict = {}
            center_serializer = ProposalCenterMappingSpaceSerializer(center_object)
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

                society_ids = ShortlistedSpaces.objects.filter(space_mapping=space_mapping_object,
                                                               supplier_code='RS').values_list('object_id', flat=True)
                societies_temp = SupplierTypeSociety.objects.filter(supplier_id__in=society_ids).values('supplier_id',
                                                                                                        'society_latitude',
                                                                                                        'society_longitude',
                                                                                                        'society_name',
                                                                                                        'society_address1',
                                                                                                        'society_subarea',
                                                                                                        'society_location_type')
                societies = []
                society_ids = []
                societies_count = 0
                for society in societies_temp:
                    if website_utils.space_on_circle(center_object.latitude, center_object.longitude,
                                                     center_object.radius, \
                                                     society['society_latitude'], society['society_longitude']):
                        society_inventory_obj = InventorySummary.objects.get_supplier_type_specific_object(
                            request.data.copy(),
                            society['supplier_id'])
                        # society_inventory_obj = InventorySummary.objects.get(supplier_id=society['supplier_id'])
                        society['shortlisted'] = True
                        society['buffer_status'] = False
                        # obj = InventorySummaryAPIView()
                        adinventory_type_dict = ui_utils.adinventory_func()
                        duration_type_dict = ui_utils.duration_type_func()
                        if society_inventory_obj.poster_allowed_nb or society_inventory_obj.poster_allowed_lift:
                            society['total_poster_count'] = society_inventory_obj.total_poster_count
                            society['poster_price'] = return_price(adinventory_type_dict, duration_type_dict,
                                                                   'poster_a4', 'campaign_weekly')

                        if society_inventory_obj.standee_allowed:
                            society['total_standee_count'] = society_inventory_obj.total_standee_count
                            society['standee_price'] = return_price(adinventory_type_dict, duration_type_dict,
                                                                    'standee_small', 'campaign_weekly')

                        if society_inventory_obj.stall_allowed:
                            society['total_stall_count'] = society_inventory_obj.total_stall_count
                            society['stall_price'] = return_price(adinventory_type_dict, duration_type_dict,
                                                                  'stall_small', 'unit_daily')
                            society['car_display_price'] = return_price(adinventory_type_dict, duration_type_dict,
                                                                        'car_display_standard', 'unit_daily')

                        if society_inventory_obj.flier_allowed:
                            society['flier_frequency'] = society_inventory_obj.flier_frequency
                            society['filer_price'] = return_price(adinventory_type_dict, duration_type_dict,
                                                                  'flier_door_to_door', 'unit_daily')

                        # ADDNEW --> Banner etc.
                        society_ids.append(society['supplier_id'])
                        societies.append(society)
                        societies_count += 1

                # societies_serializer =  ProposalSocietySerializer(societies, many=True)

                # following query find sum of all the variables specified in a dictionary
                # this finds sum of all inventories, if you don't need some of some inventory make it 0 in front end
                societies_inventory_count = InventorySummary.objects.filter(supplier_id__in=society_ids).aggregate(
                    posters=Sum('total_poster_count'), \
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
            'proposal': proposal_serializer.data,
            'centers': centers_list,
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
                        return Response({'message': 'Invalid Center Data', 'errors': center_serializer.errors},
                                        status=406)

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
                            inventory_type_version_serializer = InventoryTypeVersionSerializer(
                                data=space_inventory_type)
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
                                                                          content_type=content_type,
                                                                          supplier_code=supplier_code,
                                                                          object_id=object_id,
                                                                          buffer_status=space['buffer_status'])

                                    shortlisted_space_list.append(shortlisted_space)

                                    # version save
                                    shortlisted_version_space = ShortlistedSpacesVersion(
                                        space_mapping_version=space_mapping_version_object,
                                        content_type=content_type, supplier_code=supplier_code, object_id=object_id,
                                        buffer_status=space['buffer_status'])
                                    shortlisted_space_version_list.append(shortlisted_version_space)

                ShortlistedSpaces.objects.bulk_create(shortlisted_space_list)
                # version save
                ShortlistedSpacesVersion.objects.bulk_create(shortlisted_space_version_list)
            except Exception as e:
                return Response({'status': False, 'error': e.message}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Successfully Saved'}, status=200)

    # def put(self, request, format=None):
    #     centers = request.data
    #     for center in centers:

    def get_space_code_dict(self):
        space_dict = {  # singular space as key and its plural as value
            'society': 'societies', 'corporate': 'corporates',
            'gym': 'gyms', 'salon': 'salons',
        }

        supplier_code_dict = {
            'society': 'RS', 'corporate': 'CP',
            'gym': 'GY', 'salon': 'SA',
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
            price_dict = getPriceDict()
            for item in items:
                society_detail = {}  # List of society-related details required to be displayed
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

                # inv_details = InventorySummary.objects.get(supplier_id=society_id)
                for inv in inv_types:
                    inv_name = inv.type
                    inv_size = inv.sub_type
                    if (hasattr(inv_details, inv_name.lower() + allowed) and getattr(inv_details,
                                                                                     inv_name.lower() + allowed)):
                        if (inv_name == 'Flier'):
                            inv_count = 1
                        else:
                            inv_count = getattr(inv_details, total + inv_name.lower() + count)
                        inv_info = {}  # List of inventory and its count details

                        # adinventory_type = models.ForeignKey('AdInventoryType', db_column='ADINVENTORY_TYPE_ID', blank=True, null=True, on_delete=models.CASCADE)
                        # supplier = models.ForeignKey('SupplierTypeSociety', db_column='SUPPLIER_ID', related_name='default_prices', blank=True, null=True, on_delete=models.CASCADE)
                        # duration_type = models.ForeignKey('DurationType', db_column='DURATION_ID', blank=True, null=True, on_delete=models.CASCADE)
                        duration_type = DurationType.objects.get(id=int(price_dict[inv_name]['duration']))
                        adinventory_type = AdInventoryType.objects.get(id=int(price_dict[inv_name]['types'][inv_size]))
                        price_obj = PriceMappingDefault.objects.get(supplier=item.society, duration_type=duration_type,
                                                                    adinventory_type=adinventory_type)
                        inv_price = price_obj.business_price
                        inv_info['count'] = str(inv_count)
                        inv_info['price'] = str(inv_price)
                        inv_info['type'] = inv_name
                        society_detail['inventory'].append(inv_info)

                response.append(society_detail)

            # response = (response)
            return Response(response, status=200)

        except:
            return Response(status=404)


class ProposalImagesPath(APIView):
    """
    returns a path to downloaded images in zip format. The zipped file is stored in Media directory
    This API  converts the folder present in 'files' directory into zip file and returns a path to download the file.
    """

    def get(self, request):
        class_name = self.__class__.__name__
        try:
            proposal_id = request.query_params['proposal_id']
            task_id = request.query_params['task_id']
            result = GroupResult.restore(task_id)
            if not result.successful():
                return ui_utils.handle_response(class_name, data=errors.TASK_NOT_DONE_YET_ERROR.format(task_id))

            path_to_master_dir = settings.BASE_DIR + '/files/downloaded_images/' + proposal_id
            output_path = os.path.join(settings.MEDIA_ROOT, proposal_id)

            if not os.path.exists(path_to_master_dir):
                return ui_utils.handle_response(class_name, data=errors.PATH_DOES_NOT_EXIST.format(path_to_master_dir))

            shutil.make_archive(output_path, 'zip', path_to_master_dir)
            file_url = settings.BASE_URL + proposal_id + '.zip'
            # we should remove the original folder as it will consume space.
            shutil.rmtree(path_to_master_dir)
            return ui_utils.handle_response(class_name, data=file_url, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


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
            proposal = ProposalInfo.objects.get(proposal_id=campaign_id)

            response = website_utils.is_campaign(proposal)
            if not response.data['status']:
                return response

            proposal.campaign_state = v0_constants.proposal_not_converted_to_campaign
            proposal.save()

            current_assigned_inventories = ShortlistedInventoryPricingDetails.objects.select_related(
                'shortlisted_spaces').filter(shortlisted_spaces__proposal_id=campaign_id)
            InventoryActivityAssignment.objects.filter(
                inventory_activity__shortlisted_inventory_details__in=current_assigned_inventories).delete()

            return ui_utils.handle_response(class_name, data=errors.REVERT_CAMPAIGN_TO_PROPOSAL.format(campaign_id,
                                                                                                       v0_constants.proposal_not_converted_to_campaign),
                                            success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


class convertDirectProposalToCampaign(APIView):
    """
    This will convert proposal to campaign where supplier id's should be provided in sheet
    """

    def post(self, request):
        """

        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            proposal_data = request.data
            center_id = proposal_data['center_id']
            proposal = ProposalInfo.objects.get(pk=proposal_data['proposal_id'])
            center = ProposalCenterMapping.objects.get(pk=center_id)

            for supplier_code in proposal_data['center_data']:

                response = website_utils.save_filters(center, supplier_code, proposal_data, proposal)
                if not response.data['status']:
                    return response
                response = website_utils.save_shortlisted_suppliers_data(center, supplier_code, proposal_data, proposal)
                if not response.data['status']:
                    return response
                response = website_utils.save_shortlisted_inventory_pricing_details_data(center, supplier_code,
                                                                                         proposal_data, proposal)
                if not response.data['status']:
                    return response
            response = website_utils.update_proposal_invoice_and_state(proposal_data, proposal)
            if not response.data['status']:
                return response
            response = website_utils.create_generic_export_file_data(proposal)
            if not response.data['status']:
                return response

            return ui_utils.handle_response(class_name, data={}, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


def strToList(str):
    elements = str.split(',')
    converted_list = [x.strip(' ') for x in elements]
    return converted_list


def convertDirectProposalToCampaignExcel(proposal_list):
    for proposal_data in proposal_list:
        center_id = proposal_data['center_id']
        proposal = ProposalInfo.objects.get(pk=proposal_data['proposal_id'])
        center = ProposalCenterMapping.objects.get(pk=center_id)

        # data conversion
        center_data = {}


class SupplierPhaseViewSet(viewsets.ViewSet):

    def list(self, request):
        class_name = self.__class__.__name__
        try:
            campaign_id = request.query_params.get('campaign_id')
            phases = SupplierPhase.objects.filter(campaign=campaign_id)
            serializer = SupplierPhaseSerializer(phases, many=True)
            return handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return handle_response(class_name, exception_object=e, request=request)

    def create(self, request):
        class_name = self.__class__.__name__
        try:
            phases = request.data
            campaign_id = request.query_params.get('campaign_id')
            for phase in phases:
                if 'id' in phase:
                    item = SupplierPhase.objects.get(pk=phase['id'],campaign=campaign_id)
                    phase_serializer = SupplierPhaseSerializer(item, data=phase)
                else:
                    phase['campaign'] = campaign_id
                    phase_serializer = SupplierPhaseSerializer(data=phase)
                if phase_serializer.is_valid():
                    phase_serializer.save()
            data = SupplierPhase.objects.filter(campaign=campaign_id)
            serializer = SupplierPhaseSerializer(data, many=True)
            return handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return handle_response(class_name, exception_object=e, request=request)
