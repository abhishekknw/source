from v0.ui.proposal.models import ProposalInfo, ShortlistedSpaces, SupplierPhase
from v0.ui.utils import handle_response
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from v0.ui.proposal.models import (ProposalInfo)
import v0.ui.utils as ui_utils
import v0.constants as v0_constants
from v0.ui.supplier.models import (SupplierTypeSociety)
import v0.ui.website.utils as website_utils
from django.db.models import Q
from django.db.models import Count
from models import (CampaignSocietyMapping, Campaign)
from serializers import (CampaignListSerializer, CampaignSerializer)
from v0.ui.proposal.models import ShortlistedSpaces
from v0.ui.supplier.serializers import SupplierTypeSocietySerializer, SupplierTypeSocietySerializer2
from v0.ui.inventory.models import InventoryActivityImage
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework import status
import gpxpy.geo
from v0.ui.leads.models import Leads, LeadsForm, LeadsFormItems, LeadsFormData
from v0.ui.leads.serializers import LeadsFormItemsSerializer
import json, datetime

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


class ShortlistSocietyCountAPIView(APIView):
    # to get the number of shortlisted socities on societyDetailPage
    def get(self, request, id=None, format=None):
        try:
            campaign = Campaign.objects.get(pk=id)
            societies_count = CampaignSocietyMapping.objects.filter(campaign=campaign).count()
            return Response({'count': societies_count}, status=200)
        except Campaign.DoesNotExist:
            return Response({'error':'No such campaign id exists'},status=406)


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


class campaignListAPIVIew(APIView):
    """
    API around campaign list
    """

    def get(self, request, organisation_id):
        """

        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            user = request.user
            date = request.query_params['date']
            result = []
            category = request.query_params['category']
            if user.is_superuser:
                result = website_utils.get_campaigns_with_status(category, user)
            else:
                result = website_utils.get_campaigns_with_status(category, user)
            return ui_utils.handle_response(class_name, data=result, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


class DashBoardViewSet(viewsets.ViewSet):
    """
    viewset around dashboard activities
    This will return all the required data to display on dashboard
    """

    @list_route()
    def suppliers_booking_status(self, request, pk=None):
        """

        :param request:
        :param pk:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            campaign_id = request.query_params.get('campaign_id', None)
            query_value = request.query_params.get('query', None)
            if v0_constants.query_status['supplier_code'] == query_value:
                result = ShortlistedSpaces.objects.filter(proposal_id=campaign_id). \
                    values('supplier_code').annotate(total=Count('object_id'))
            if v0_constants.query_status['booking_status'] == query_value:
                result = ShortlistedSpaces.objects.filter(proposal_id=campaign_id). \
                    values('booking_status').annotate(total=Count('object_id'))
            if v0_constants.query_status['phase'] == query_value:
                result = ShortlistedSpaces.objects.filter(proposal_id=campaign_id). \
                    values('supplier_code', 'phase', 'booking_status').annotate(total=Count('object_id'))
            return ui_utils.handle_response(class_name, data=result, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    @list_route()
    def get_count_of_supplier_types_by_campaign_status(self, request):
        """

        :param request:
        :param pk:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            user = request.user
            campaign_status = request.query_params.get('status', None)
            perm_query = Q()
            if not request.user.is_superuser:
                category = user.profile.organisation.category
                organisation_id = user.profile.organisation.organisation_id
                if category.upper() == v0_constants.category['business']:
                    perm_query = Q(proposal__account__organisation__organisation_id=organisation_id)
                if category.upper() == v0_constants.category['business_agency']:
                    perm_query = Q(proposal__user=user)
                if category.upper() == v0_constants.category['supplier_agency']:
                    perm_query = Q(proposal__campaignassignemnt__assigned_to=user)
            current_date = timezone.now()

            if campaign_status == v0_constants.campaign_status['ongoing_campaigns']:
                query = Q(proposal__tentative_start_date__lte=current_date) & Q(
                    proposal__tentative_end_date__gte=current_date) & Q(proposal__campaign_state='PTC')

                proposal_data = ShortlistedSpaces.objects.filter(perm_query, query).values('supplier_code',
                                                                                           'proposal__name',
                                                                                           'proposal_id',
                                                                                           'center__latitude',
                                                                                           'center__longitude'). \
                    annotate(total=Count('object_id'))
                proposal_data = website_utils.get_leads_count_by_campaign(proposal_data)

            if campaign_status == v0_constants.campaign_status['completed_campaigns']:
                query = Q(proposal__tentative_start_date__lt=current_date) & Q(proposal__campaign_state='PTC')

                proposal_data = ShortlistedSpaces.objects.filter(query, perm_query).values('supplier_code',
                                                                                           'proposal__name',
                                                                                           'proposal_id',
                                                                                           'center__latitude',
                                                                                           'center__longitude'). \
                    annotate(total=Count('object_id'))
                proposal_data = website_utils.get_leads_count_by_campaign(proposal_data)

            if campaign_status == v0_constants.campaign_status['upcoming_campaigns']:
                query = Q(proposal__tentative_start_date__gt=current_date) & Q(proposal__campaign_state='PTC')

                proposal_data = ShortlistedSpaces.objects.filter(query, perm_query).values('supplier_code',
                                                                                           'proposal__name',
                                                                                           'proposal_id',
                                                                                           'center__latitude',
                                                                                           'center__longitude'). \
                    annotate(total=Count('object_id'))
                proposal_data = website_utils.get_leads_count_by_campaign(proposal_data)

            data = {}
            for proposal in proposal_data:
                if proposal['supplier_code'] not in data:
                    data[proposal['supplier_code']] = []
                data[proposal['supplier_code']].append(proposal)

            return ui_utils.handle_response(class_name, data=data, success=True)

        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    @list_route()
    def get_suppliers_current_status(self, request):
        """
        This function gives supplier's current status like - ongoing,upcoming,completed

        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            campaign_id = request.query_params.get('campaign_id', None)
            current_date = timezone.now()
            object_id_alias = 'inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__shortlisted_spaces__object_id'

            shortlisted_suppliers = ShortlistedSpaces.objects.filter(proposal__proposal_id=campaign_id)
            shortlisted_suppliers_id_list = [supplier.object_id for supplier in shortlisted_suppliers]

            suppliers_instances = SupplierTypeSociety.objects.filter(supplier_id__in=shortlisted_suppliers_id_list)
            supplier_serializer = SupplierTypeSocietySerializer(suppliers_instances, many=True)
            suppliers = supplier_serializer.data

            supplier_objects_id_list = {supplier['supplier_id']: supplier for supplier in suppliers}

            leads = website_utils.get_campaign_leads(campaign_id)
            inv_data_objects_list = website_utils.get_campaign_inv_data(campaign_id)
            # inv_data_objects_list = {inv['object_id']:inv for inv in inv_data}
            ongoing_suppliers = InventoryActivityImage.objects.select_related('inventory_activity_assignment',
                                                                              'inventory_activity_assignment__inventory_activity',
                                                                              'inventory_activity_assignment__inventory_activity',
                                                                              'inventory_activity_assignment__inventory_activity__shortlisted_inventory_details',
                                                                              'inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__shortlisted_spaces'). \
                filter(
                inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__shortlisted_spaces__proposal=campaign_id,
                inventory_activity_assignment__inventory_activity__activity_type='RELEASE',
                inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__shortlisted_spaces__is_completed=False). \
                values(object_id_alias). \
                distinct()

            ongoing_supplier_id_list = [supplier[object_id_alias] for supplier in ongoing_suppliers]

            completed_suppliers = ShortlistedSpaces.objects.filter(proposal__proposal_id=campaign_id,
                                                                   is_completed=True).values('object_id')

            completed_supplier_id_list = [supplier['object_id'] for supplier in completed_suppliers]

            upcoming_supplier_id_list = set(shortlisted_suppliers_id_list) - set(
                ongoing_supplier_id_list + completed_supplier_id_list)

            ongoing_suppliers_list = []
            for id in ongoing_supplier_id_list:
                data = {
                    'supplier': supplier_objects_id_list[id],
                    'leads_data': []
                }
                if leads and (id in leads):
                    data['leads_data'] = leads[id]
                if id in inv_data_objects_list:
                    data['supplier']['inv_data'] = inv_data_objects_list[id]

                ongoing_suppliers_list.append(data)

            completed_suppliers_list = []
            for id in completed_supplier_id_list:
                data = {
                    'supplier': supplier_objects_id_list[id],
                    'leads_data': []
                }
                if leads and (id in leads):
                    data['leads_data'] = leads[id]
                if id in inv_data_objects_list:
                    data['supplier']['inv_data'] = inv_data_objects_list[id]
                completed_suppliers_list.append(data)

            upcoming_suppliers_list = []
            for id in upcoming_supplier_id_list:
                data = {
                    'supplier': supplier_objects_id_list[id],
                    'leads_data': []
                }
                if leads and (id in leads):
                    data['leads_data'] = leads[id]
                if id in inv_data_objects_list:
                    data['supplier']['inv_data'] = inv_data_objects_list[id]
                upcoming_suppliers_list.append(data)

            data = {
                'ongoing': ongoing_suppliers_list,
                'completed': completed_suppliers_list,
                'upcoming': upcoming_suppliers_list
            }

            return ui_utils.handle_response(class_name, data=data, success=True)

        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    @list_route()
    def get_campaign_filters(self, request):
        """

        :param self:
        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            campaign_id = request.query_params.get('campaign_id', None)
            filters = website_utils.get_filters_by_campaign(campaign_id)
            return ui_utils.handle_response(class_name, data=filters, success=True)

        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    @list_route()
    def get_performance_metrics_data(self, request):
        """

        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            campaign_id = request.query_params.get('campaign_id', None)
            if not campaign_id:
                return Response("Campaign Id is Not Provided", status=status.HTTP_200_OK)
            type = request.query_params.get('type', None)
            result = {}
            if type == v0_constants.perf_metrics_types['inv_type']:
                result = website_utils.get_performance_metrics_data_for_inventory(campaign_id, request)
            return ui_utils.handle_response(class_name, data=result, success=True)

        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    @list_route()
    def get_location_difference_of_inventory(self, request):
        """

        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            campaign_id = request.query_params.get('campaign_id', None)
            inv_code = request.query_params.get('inv', None)
            content_type = ui_utils.fetch_content_type(inv_code)
            content_type_id = content_type.id

            result = website_utils.get_activity_data_by_values(campaign_id, content_type_id)

            supplier_ids = {supplier['object_id'] for supplier in result}
            supplier_objects = SupplierTypeSociety.objects.filter(supplier_id__in=supplier_ids)
            serializer = SupplierTypeSocietySerializer(supplier_objects, many=True)
            suppliers = serializer.data
            supplier_objects_id_map = {supplier['supplier_id']: supplier for supplier in suppliers}

            inv_assignemnt_objects = {}
            for item in result:
                lat1 = item['latitude']
                lon1 = item['longitude']
                # need to be changed for other suppliers
                lat2 = supplier_objects_id_map[item['object_id']]['society_latitude']
                lon2 = supplier_objects_id_map[item['object_id']]['society_longitude']

                if lat1 and lon1 and lat2 and lon2:
                    distance = gpxpy.geo.haversine_distance(lat1, lon1, lat2, lon2)
                    item['distance'] = distance
                if not (item['activity'] in inv_assignemnt_objects):
                    inv_assignemnt_objects[item['activity']] = {}
                if not (item['inventory_activity_assignment_id'] in inv_assignemnt_objects[item['activity']]):
                    inv_assignemnt_objects[item['activity']][item['inventory_activity_assignment_id']] = []
                inv_assignemnt_objects[item['activity']][item['inventory_activity_assignment_id']].append(item)

            return ui_utils.handle_response(class_name, data=inv_assignemnt_objects, success=True)

        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    @list_route()
    def get_supplier_data_by_campaign(self, request):
        """
        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            campaign_id = request.query_params.get('campaign_id', None)
            supplier_id_list = ShortlistedSpaces.objects.filter(proposal=campaign_id).values_list('object_id')
            suppliers = SupplierTypeSociety.objects.filter(supplier_id__in=supplier_id_list)
            serializer = SupplierTypeSocietySerializer(suppliers, many=True)
            filters = website_utils.get_filters_by_campaign(campaign_id)
            data = {
                'supplier_data': serializer.data,
                'filters': filters
            }
            return ui_utils.handle_response(class_name, data=data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    @list_route()
    def get_campaign_inventory_activity_details(self, request):
        """

        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            campaign_id = request.query_params.get('campaign_id', None)
            result = website_utils.get_campaign_inventory_activity_data(campaign_id)
            return ui_utils.handle_response(class_name, data=result, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    @list_route()
    def get_leads_by_campaign(self, request):
        """

        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            campaign_id = request.query_params.get('campaign_id', None)

            leads = Leads.objects.filter(campaign__proposal_id=campaign_id). \
                values('object_id', 'campaign', 'is_interested'). \
                annotate(total=Count('object_id'))
            leads_by_date = Leads.objects.filter(campaign__proposal_id=campaign_id). \
                values('is_interested', 'created_at'). \
                annotate(total=Count('created_at'))
            supplier_ids_list = Leads.objects.filter(campaign__proposal_id=campaign_id).values('object_id').distinct()
            supplier_objects = SupplierTypeSociety.objects.filter(supplier_id__in=supplier_ids_list).values()

            supplier_id_object_list = {supplier['supplier_id']: supplier for supplier in supplier_objects}
            supplier_data = {}
            for supplier in leads:
                if supplier['object_id'] not in supplier_data:
                    supplier_data[supplier['object_id']] = supplier
                    supplier_data[supplier['object_id']]['interested'] = 0
                    supplier_data[supplier['object_id']]['data'] = supplier_id_object_list[supplier['object_id']]
                else:
                    supplier_data[supplier['object_id']]['total'] += supplier['total']

                if supplier['is_interested']:
                    supplier_data[supplier['object_id']]['interested'] += supplier['total']

            date_data = {}
            for supplier in leads_by_date:
                if str(supplier['created_at'].date()) not in date_data:
                    date_data[str(supplier['created_at'].date())] = supplier
                    date_data[str(supplier['created_at'].date())]['interested'] = 0
                else:
                    date_data[str(supplier['created_at'].date())]['total'] += supplier['total']
                if supplier['is_interested']:
                    date_data[str(supplier['created_at'].date())]['interested'] += supplier['total']

            data = {
                'supplier_data': supplier_data,
                'date_data': date_data
            }

            return ui_utils.handle_response(class_name, data=data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    @list_route()
    def get_leads_by_campaign_new(self, request):
        class_name = self.__class__.__name__
        campaign_id = request.query_params.get('campaign_id', None)
        leads_form_objects = LeadsForm.objects.filter(campaign_id=campaign_id).exclude(status='inactive')
        leads_form_data = LeadsFormData.objects.filter(campaign_id=campaign_id).exclude(status='inactive')
        supplier_ids = leads_form_data.values('supplier_id').distinct()

        all_suppliers_list = {}
        hot_leads_global = 0
        all_leads_global = 0

        for supplier_id in supplier_ids:
            supplier = supplier_id['supplier_id']
            lead_form_items_list = LeadsFormItems.objects.filter(campaign_id = campaign_id, supplier_id = supplier).\
                exclude(status='inactive')
            lead_form_data = LeadsFormData.objects.filter(campaign_id = campaign_id, supplier_id = supplier).\
                exclude(status='inactive')
            form_id = lead_form_items_list[0].leads_form_id
            leads_form_details = LeadsForm.objects.get(id=form_id)
            total_leads = leads_form_details.last_entry_id
            hot_leads = 0

            # counting hot leads for current supplier
            for x in range(total_leads):
                entry_id = x+1
                current_entry = lead_form_data.filter(entry_id= entry_id)
                hot_lead=False
                for item_data in current_entry:
                    item_value = item_data.item_value
                    item_id = item_data.item_id
                    hot_lead_criteria = lead_form_items_list.get(item_id=item_id).hot_lead_criteria
                    if item_value == hot_lead_criteria:
                        if hot_lead==False:
                            hot_leads = hot_leads+1
                        hot_lead = True
                        continue
            # getting society information
            society_data_1 = SupplierTypeSociety.objects.get(supplier_id=supplier)
            society_data = SupplierTypeSocietySerializer2(society_data_1).data
            now = datetime.datetime.now()
            current_supplier_data = {
                "is_interested": False,
                "campaign": campaign_id,
                "object_id": supplier,
                "interested": hot_leads,
                "total": total_leads,
                "data": society_data,
                }
            all_suppliers_list.update({supplier: current_supplier_data})
            hot_leads_global = hot_leads_global+hot_leads
            all_leads_global = all_leads_global+total_leads

        time = now
        date = now.strftime("%Y-%m-%d")
        date_data = {str(date):
                         {
                             "total": all_leads_global,
                             "created_at": str(time),
                             "is_interested": False,
                             "interested": hot_leads_global
                         }}
        all_suppliers_list.update({"date_data": date_data})

        return ui_utils.handle_response({}, data={'supplier_data': all_suppliers_list}, success=True)

    @detail_route(methods=['POST'])
    def get_leads_by_multiple_campaigns(self, request, pk=None):
        """

        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            campaign_list = request.data
            leads = Leads.objects.filter(campaign__proposal_id__in=campaign_list). \
                values('campaign', 'is_interested'). \
                annotate(total=Count('campaign'))
            campaign_objects = ProposalInfo.objects.filter(proposal_id__in=campaign_list).values()
            campaign_objects_list = {campaign['proposal_id']: campaign for campaign in campaign_objects}
            data = {}
            for campaign in leads:
                if campaign['campaign'] not in data:
                    data[campaign['campaign']] = campaign
                    data[campaign['campaign']]['interested'] = 0
                    data[campaign['campaign']]['data'] = campaign_objects_list[campaign['campaign']]
                if campaign['is_interested']:
                    data[campaign['campaign']]['interested'] += campaign['total']

            return ui_utils.handle_response(class_name, data=data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    @list_route()
    def get_activity_images_by_suppliers(self, request):
        """
        It will retrieve the images of suppliers
        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            supplier_id = request.query_params.get('supplier_id', None)
            inv_code = request.query_params.get('inv_code', None)
            act_type = request.query_params.get('act_type', None)

            content_type = ui_utils.fetch_content_type(inv_code)
            content_type_id = content_type.id

            result = InventoryActivityImage.objects. \
                filter(
                inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__shortlisted_spaces__object_id=supplier_id,
                inventory_activity_assignment__inventory_activity__activity_type=act_type,
                inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__inventory_content_type_id=content_type_id). \
                values()

            for imageInstance in result:
                imageInstance['object_id'] = supplier_id

            supplier = SupplierTypeSociety.objects.filter(supplier_id=supplier_id).values()

            inv_act_image_objects_with_distance = website_utils.calculate_location_difference_between_inventory_and_supplier(
                result, supplier)
            return ui_utils.handle_response(class_name, data=inv_act_image_objects_with_distance, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    # @list_route()
    # def get_all_inventory_details_of_supplier(self, request):
    #     """
    #     This function returns the total, assigned, completed inv and image details for Release, Audit & Closure of supplier
    #     :param request:
    #     :return:
    #     """
    #     class_name = self.__class__.__name__
    #     try:
    #         pass
    #         supplier_id = request.query_params.get('supplier_id',None)
    #         inv_code = request.query_params.get('inv_code', None)
    #         if not supplier_id or not inv_code:
    #             return Response(data={'status': False, 'error': 'No Supplier Id or Inv Code provided'},
    #                             status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         return ui_utils.handle_response(class_name, exception_object=e, request=request)

class CreateSupplierPhaseData(APIView):

    def post(self, request):
        class_name = self.__class__.__name__
        try:
            phase_data = []
            campaigns = ProposalInfo.objects.all()
            # serializer = ProposalInfoSerializer(campaigns, many=True)
            for campaign in campaigns:
                phases = ShortlistedSpaces.objects.filter(proposal=campaign).values('phase').distinct()
                for item in phases:
                    if item['phase']:
                        data = {
                            'phase_no' : item['phase'],
                            'campaign' : campaign
                        }
                        phase_data.append(SupplierPhase(**data))
            SupplierPhase.objects.all().delete()
            SupplierPhase.objects.bulk_create(phase_data)

            for campaign in campaigns:
                phases = SupplierPhase.objects.filter(campaign=campaign)
                for phase in phases:
                    suppliers = ShortlistedSpaces.objects.filter(proposal=campaign)
                    for supplier in suppliers:
                        if supplier.phase == phase.phase_no:
                            supplier.phase_no = phase
                            supplier.save()

            return handle_response(class_name, data={}, success=True)
        except Exception as e:
            return handle_response(class_name, exception_object=e, request=request)


