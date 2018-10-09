import random
import numpy as np
from datetime import datetime
from datetime import timedelta
from v0.ui.proposal.models import ProposalInfo, ShortlistedSpaces, SupplierPhase, HashTagImages
from v0.ui.utils import handle_response, calculate_percentage
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from v0.ui.proposal.models import (ProposalInfo)
import v0.ui.utils as ui_utils
import v0.constants as v0_constants
from v0.ui.supplier.models import (SupplierTypeSociety)
import v0.ui.website.utils as website_utils
from django.db.models import Q, F
from models import (CampaignSocietyMapping, Campaign, CampaignAssignment, CampaignComments)
from serializers import (CampaignListSerializer, CampaignSerializer, CampaignAssignmentSerializer)
from v0.ui.proposal.models import ShortlistedSpaces
from v0.ui.supplier.serializers import SupplierTypeSocietySerializer, SupplierTypeSocietySerializer2
from v0.ui.inventory.models import InventoryActivityImage, InventoryActivityAssignment, InventoryActivity, AdInventoryType
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework import status
import gpxpy.geo
from v0.ui.leads.models import LeadsForm, LeadsFormItems, LeadsFormData, LeadsFormSummary
from v0.ui.leads.serializers import LeadsFormItemsSerializer, LeadsFormSummarySerializer
from v0.utils import get_values
from v0.ui.base.models import DurationType
from v0.ui.finances.models import ShortlistedInventoryPricingDetails
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from v0.ui.common.models import BaseUser
from operator import itemgetter
import requests
from celery import shared_task
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
from dateutil import tz
from django.db.models import Count, Sum


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


def get_sorted_value_keys(main_dict,sub_key):
    keys_list = main_dict.keys()
    sub_array = []
    for curr_key in keys_list:
        curr_data = dict_array[curr_key]
        curr_value = curr_data[sub_key]
        sub_array.append(
            {'member': curr_key,
             'value': curr_value
             }
        )
    sorted_array = sorted(sub_array,'value')
    return sorted_array


def z_calculator_dict(dict_data, variable):
    z_array = []
    keys = dict_data.keys()
    for key in keys:
        z_array.append(dict_data[key][variable])
    if len(z_array)>0:
        global_mean = np.mean(z_array)
        stdev = np.std(z_array)
    for key in keys:
        curr_mean = dict_data[key][variable]
        z_value = (curr_mean-global_mean)/stdev if not stdev==0 else 0
        dict_data[key]['z_value'] = z_value
        if z_value>1:
            color = 'Green'
        elif z_value<-1:
            color = 'Red'
        else:
            color = 'Yellow'
        dict_data[key]['color'] = color
    return dict_data


def get_distinct_from_dict_array(dict_array, key_name):
    all_values = {x[key_name] for x in dict_array}
    distinct_values = list(set(all_values))
    return distinct_values


def hot_lead_ratio_calculator(data_array):
    for data in data_array:
        total_leads = data_array[data]['total']
        hot_leads = data_array[data]['interested']
        hot_lead_ratio = round(float(hot_leads)/float(total_leads), 5) if total_leads>0 else 0
        data_array[data]['hot_leads_percentage'] = hot_lead_ratio*100
    return data_array


def lead_counter(campaign_id, supplier_id,lead_form_items_list):
    hot_lead_criteria_dict = {}
    for lead in lead_form_items_list:
        if lead.leads_form_id not in hot_lead_criteria_dict:
            hot_lead_criteria_dict[lead.leads_form_id] = {}
        if lead.item_id not in hot_lead_criteria_dict[lead.leads_form_id]:
            hot_lead_criteria_dict[lead.leads_form_id][lead.item_id] = {}
        hot_lead_criteria_dict[lead.leads_form_id][lead.item_id]['hot_lead_criteria'] = lead.hot_lead_criteria
    lead_form_data = LeadsFormData.objects.filter(campaign_id=campaign_id, supplier_id=supplier_id). \
        exclude(status='inactive')
    lead_form_data_array = []
    for curr_object in lead_form_data:
        curr_data = curr_object.__dict__
        lead_form_data_array.append(curr_data)

    total_leads = 0
    hot_leads = 0
    hot_lead_details = []
    leads_form_items_dict = {item.item_id:item.key_name for item in lead_form_items_list}
    # print leads_form_items_dict
    form_id_data = get_distinct_from_dict_array(lead_form_data_array,'leads_form_id')
    for form_id in form_id_data:
        current_leads_data = [x for x in lead_form_data_array if x['leads_form_id'] == form_id]
        current_lead_entries = get_distinct_from_dict_array(current_leads_data,'entry_id')
        current_leads = len(current_lead_entries)
        total_leads = total_leads + current_leads
        for entry_id in current_lead_entries:
            current_entry = [x for x in lead_form_data_array if x['entry_id'] == entry_id]
            hot_lead = False
            for item_data in current_entry:
                item_value = item_data['item_value']
                item_id = item_data['item_id']
                leads_form_id = item_data['leads_form_id']
                hot_lead_criteria = hot_lead_criteria_dict[leads_form_id][item_id]['hot_lead_criteria']
                if item_value:
                    if (hot_lead_criteria and str(item_value) == str(hot_lead_criteria)) or 'counseling' in leads_form_items_dict[item_id].lower():
                        if hot_lead is False:
                            hot_leads = hot_leads + 1
                            hot_lead_details.append({
                                'leads_form_id': leads_form_id,
                                'entry_id': entry_id
                            })
                        hot_lead = True
                        continue
    result = {'total_leads': total_leads, 'hot_leads': hot_leads, 'hot_lead_details':hot_lead_details}
    return result

# def hot_lead(hot_lead_criteria_query):
#

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

            if campaign_status == v0_constants.campaign_status['completed_campaigns']:
                query = Q(proposal__tentative_start_date__lt=current_date) & Q(proposal__campaign_state='PTC')

                proposal_data = ShortlistedSpaces.objects.filter(query, perm_query).values('supplier_code',
                                                                                           'proposal__name',
                                                                                           'proposal_id',
                                                                                           'center__latitude',
                                                                                           'center__longitude'). \
                    annotate(total=Count('object_id'))

            if campaign_status == v0_constants.campaign_status['upcoming_campaigns']:
                query = Q(proposal__tentative_start_date__gt=current_date) & Q(proposal__campaign_state='PTC')

                proposal_data = ShortlistedSpaces.objects.filter(query, perm_query).values('supplier_code',
                                                                                           'proposal__name',
                                                                                           'proposal_id',
                                                                                           'center__latitude',
                                                                                           'center__longitude'). \
                    annotate(total=Count('object_id'))

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
            shortlisted_spaces_id_list = [supplier.id for supplier in shortlisted_suppliers]
            shortlisted_spaces_id_dict = {supplier.id: supplier.object_id for supplier in shortlisted_suppliers}

            suppliers_instances = SupplierTypeSociety.objects.filter(supplier_id__in=shortlisted_suppliers_id_list)
            supplier_serializer = SupplierTypeSocietySerializer(suppliers_instances, many=True)
            suppliers = supplier_serializer.data
            flat_count = 0

            supplier_objects_id_list = {supplier['supplier_id']: supplier for supplier in suppliers}
            all_leads_count = LeadsFormSummary.objects.filter(campaign_id=campaign_id).all()
            supplier_wise_leads_count = {}

            for leads in all_leads_count:
                if 'flat_count' in supplier_objects_id_list[leads.supplier_id] and supplier_objects_id_list[leads.supplier_id]['flat_count']:
                    flat_count = supplier_objects_id_list[leads.supplier_id]['flat_count']
                else:
                    flat_count = 0
                supplier_wise_leads_count[leads.supplier_id] = {
                    'hot_leads_count': leads.hot_leads_count,
                    'total_leads_count': leads.total_leads_count,
                    'hot_leads_percentage': leads.hot_leads_percentage,
                    'hot_leads_percentage_by_flat_count': calculate_percentage(leads.hot_leads_count, flat_count),
                    'flat_count': flat_count,
                    'leads_flat_percentage': calculate_percentage(leads.total_leads_count, flat_count)
                }
            inv_data_objects_list = website_utils.get_campaign_inv_data(campaign_id)
            # inv_data_objects_list = {inv['object_id']:inv for inv in inv_data}
            ongoing_suppliers = InventoryActivityImage.objects.select_related('inventory_activity_assignment',
                                                                              'inventory_activity_assignment__inventory_activity',
                                                                              'inventory_activity_assignment__inventory_activity__shortlisted_inventory_details',
                                                                              'inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__shortlisted_spaces'). \
                filter(
                inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__shortlisted_spaces__proposal=campaign_id,
                inventory_activity_assignment__inventory_activity__activity_type='RELEASE',
                inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__shortlisted_spaces__is_completed=False). \
                values(object_id_alias). \
                distinct()
            all_inventory_activity_images = InventoryActivityImage.objects.filter(
                inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__shortlisted_spaces_id__in=shortlisted_spaces_id_list).all()
            all_images_by_supplier = {}
            for inventory_image in all_inventory_activity_images:
                supplier_id = shortlisted_spaces_id_dict[
                    inventory_image.inventory_activity_assignment.inventory_activity.shortlisted_inventory_details.shortlisted_spaces_id]
                inventory_name = inventory_image.inventory_activity_assignment.inventory_activity.shortlisted_inventory_details.ad_inventory_type.adinventory_name
                if supplier_id not in all_images_by_supplier:
                    all_images_by_supplier[supplier_id] = {}
                if inventory_name not in all_images_by_supplier[supplier_id]:
                    all_images_by_supplier[supplier_id][inventory_name] = {"images": [], "total_count":0}
                all_images_by_supplier[supplier_id][inventory_name]["images"].append({
                    'image_path': inventory_image.image_path,
                    'actual_activity_date': str(inventory_image.actual_activity_date),
                    'latitude': str(inventory_image.latitude),
                    'longitude': str(inventory_image.longitude),
                    'comment': str(inventory_image.comment),
                    'inventory_name': inventory_name
                })

                all_images_by_supplier[supplier_id][inventory_name]["total_count"] += 1

            all_hashtag_images = HashTagImages.objects.filter(campaign_id=campaign_id).all()
            for hashtag_image in all_hashtag_images:
                supplier_id = hashtag_image.object_id
                if supplier_id not in all_images_by_supplier:
                    all_images_by_supplier[supplier_id] = {}
                if hashtag_image.hashtag not in all_images_by_supplier[supplier_id]:
                    all_images_by_supplier[supplier_id][hashtag_image.hashtag] = {"images": [], "total_count":0}
                all_images_by_supplier[supplier_id][hashtag_image.hashtag]["images"].append({
                    'image_path': hashtag_image.image_path,
                    'actual_activity_date': str(hashtag_image.created_at),
                    'latitude': str(hashtag_image.latitude),
                    'longitude': str(hashtag_image.longitude),
                    'comment': str(hashtag_image.comment),
                    'inventory_name': hashtag_image.hashtag
                })
                all_images_by_supplier[supplier_id][hashtag_image.hashtag]["total_count"] += 1

            ongoing_supplier_id_list = [supplier[object_id_alias] for supplier in ongoing_suppliers]

            completed_suppliers = ShortlistedSpaces.objects.filter(proposal__proposal_id=campaign_id,
                                                                   is_completed=True).values('object_id')

            completed_supplier_id_list = [supplier['object_id'] for supplier in completed_suppliers]

            upcoming_supplier_id_list = set(shortlisted_suppliers_id_list) - set(
                ongoing_supplier_id_list + completed_supplier_id_list)

            ongoing_suppliers_list = []
            total_ongoing_leads_count = 0
            total_ongoing_hot_leads_count = 0
            total_ongoing_flat_count = 0
            for id in ongoing_supplier_id_list:
                data = {
                    'supplier': supplier_objects_id_list[id],
                    'leads_data': supplier_wise_leads_count[id] if id in supplier_wise_leads_count else {},
                    'images_data': all_images_by_supplier[id] if id in all_images_by_supplier else {}
                }
                if id in inv_data_objects_list:
                    data['supplier']['inv_data'] = inv_data_objects_list[id]
                ongoing_suppliers_list.append(data)
                if 'total_leads_count' in data['leads_data']:
                    total_ongoing_leads_count = total_ongoing_leads_count + data['leads_data']['total_leads_count']
                    total_ongoing_hot_leads_count = total_ongoing_hot_leads_count + data['leads_data']['hot_leads_count']
                if supplier_objects_id_list[id]['flat_count']:
                    total_ongoing_flat_count = total_ongoing_flat_count + supplier_objects_id_list[id]['flat_count']

            completed_suppliers_list = []
            total_completed_leads_count = 0
            total_completed_hot_leads_count = 0
            total_completed_flat_count = 0
            for id in completed_supplier_id_list:
                data = {
                    'supplier': supplier_objects_id_list[id],
                    'leads_data': supplier_wise_leads_count[id] if id in supplier_wise_leads_count else {},
                    'images_data': all_images_by_supplier[id] if id in all_images_by_supplier else {}
                }
                if id in inv_data_objects_list:
                    data['supplier']['inv_data'] = inv_data_objects_list[id]
                completed_suppliers_list.append(data)
                if 'total_leads_count' in data['leads_data']:
                    total_completed_leads_count = total_completed_leads_count + data['leads_data']['total_leads_count']
                    total_completed_hot_leads_count = total_completed_hot_leads_count + data['leads_data']['hot_leads_count']
                if supplier_objects_id_list[id]['flat_count']:
                    total_completed_flat_count = total_completed_flat_count + supplier_objects_id_list[id]['flat_count']
            upcoming_suppliers_list = []
            total_upcoming_leads_count = 0
            total_upcoming_hot_leads_count = 0
            total_upcoming_flat_count = 0
            for id in upcoming_supplier_id_list:
                data = {
                    'supplier': supplier_objects_id_list[id],
                    'leads_data': supplier_wise_leads_count[id] if id in supplier_wise_leads_count else {},
                    'images_data': all_images_by_supplier[id] if id in all_images_by_supplier else {}
                }
                if id in inv_data_objects_list:
                    data['supplier']['inv_data'] = inv_data_objects_list[id]
                upcoming_suppliers_list.append(data)
                if 'total_leads_count' in data['leads_data']:
                    total_upcoming_leads_count = total_upcoming_leads_count + data['leads_data']['total_leads_count']
                    total_upcoming_hot_leads_count = total_upcoming_hot_leads_count + data['leads_data']['hot_leads_count']
                if supplier_objects_id_list[id]['flat_count']:
                    total_upcoming_flat_count = total_upcoming_flat_count + supplier_objects_id_list[id]['flat_count']
            data = {
                'ongoing': ongoing_suppliers_list,
                'completed': completed_suppliers_list,
                'upcoming': upcoming_suppliers_list,
                'overall_metrics': {
                    'ongoing': {
                        'total_leads_count': total_ongoing_leads_count,
                        'total_hot_leads_count': total_ongoing_hot_leads_count,
                        'hot_leads_percentage': calculate_percentage(total_ongoing_hot_leads_count, total_ongoing_leads_count),
                        'flat_count': total_ongoing_flat_count,
                        'leads_flat_percentage': calculate_percentage(total_ongoing_leads_count, total_ongoing_flat_count),
                        'hot_leads_percentage_by_flat_count': calculate_percentage(total_ongoing_hot_leads_count, total_ongoing_flat_count),
                        'total_suppliers_count': len(ongoing_supplier_id_list)
                    },
                    'completed': {
                        'total_leads_count': total_completed_leads_count,
                        'total_hot_leads_count': total_completed_hot_leads_count,
                        'hot_leads_percentage': calculate_percentage(total_completed_hot_leads_count, total_completed_leads_count),
                        'flat_count': total_completed_flat_count,
                        'leads_flat_percentage': calculate_percentage(total_completed_leads_count, total_completed_flat_count),
                        'hot_leads_percentage_by_flat_count': calculate_percentage(total_completed_hot_leads_count, total_completed_flat_count),
                        'total_suppliers_count': len(completed_suppliers_list)
                    },
                    'upcoming': {
                        'total_leads_count': total_upcoming_leads_count,
                        'total_hot_leads_count': total_upcoming_hot_leads_count,
                        'hot_leads_percentage': calculate_percentage(total_upcoming_hot_leads_count, total_upcoming_leads_count),
                        'flat_count': total_upcoming_flat_count,
                        'leads_flat_percentage': calculate_percentage(total_upcoming_leads_count, total_upcoming_flat_count),
                        'hot_leads_percentage_by_flat_count': calculate_percentage(total_upcoming_hot_leads_count, total_upcoming_flat_count),
                        'total_suppliers_count': len(upcoming_suppliers_list)
                    }
                }
            }
            return ui_utils.handle_response(class_name, data=data, success=True)

        except Exception as e:
            print e
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
        #try:
        campaign_id = request.query_params.get('campaign_id', None)
        leads_form_summary_data = LeadsFormSummary.objects.filter(campaign_id=campaign_id)\
            .values('supplier_id','total_leads_count','hot_leads_count','hot_leads_percentage')
        supplier_ids = list(set(leads_form_summary_data.values_list('supplier_id', flat=True)))
        supplier_info_1 = SupplierTypeSociety.objects.filter(supplier_id__in=supplier_ids)
        supplier_info = SupplierTypeSocietySerializer2(supplier_info_1, many=True).data
        all_suppliers_data = {}
        all_localities_data = {}
        for curr_row in leads_form_summary_data:
            supplier_id = curr_row['supplier_id']
            total_leads = curr_row['total_leads_count']
            hot_leads = curr_row['hot_leads_count']
            hot_leads_percentage = curr_row['hot_leads_percentage']
            curr_supplier_data = {
                "is_interested": True,
                "campaign": campaign_id,
                "object_id": supplier_id,
                "interested": hot_leads,
                "total": total_leads,
                "data": supplier_info,
                "hot_leads_percentage": hot_leads_percentage
            }
            all_suppliers_data[supplier_id] = curr_supplier_data

            curr_supplier_info = [x for x in supplier_info if x['supplier_id'] == supplier_id]
            supplier_locality = curr_supplier_info[0]['society_locality']
            if supplier_locality in all_localities_data:
                all_localities_data[supplier_locality]["interested"] = all_localities_data[supplier_locality][
                                                                           "interested"] + hot_leads
                all_localities_data[supplier_locality]["total"] = all_localities_data[supplier_locality][
                                                                      "total"] + total_leads
            else:
                curr_locality_data = {
                    "is_interested": True,
                    "campaign": campaign_id,
                    "locality": supplier_locality,
                    "interested": hot_leads,
                    "total": total_leads,
                }
                all_localities_data[supplier_locality] = curr_locality_data

        leads_form_data = LeadsFormData.objects.filter(campaign_id=campaign_id).exclude(status='inactive').all()
        date_data = {}
        weekday_data = {}
        all_entries_checked = []



        return ui_utils.handle_response(class_name, data=all_localities_data, success=True)
        #except Exception as e:
        #    return ui_utils.handle_response(class_name, exception_object=e, request=request)


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
            date = request.query_params.get('date', None)

            content_type = ui_utils.fetch_content_type(inv_code)
            content_type_id = content_type.id

            if str(date) != 'undefined':
                result = InventoryActivityImage.objects. \
                    filter(
                    inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__shortlisted_spaces__object_id=supplier_id,
                    inventory_activity_assignment__inventory_activity__activity_type=act_type,
                    inventory_activity_assignment__activity_date = date,
                    inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__inventory_content_type_id=content_type_id). \
                    values()
            else:
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

    @list_route()
    def get_datewise_suppliers_inventory_status(self, request):
        """
        It will retrieve the images of suppliers
        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            campaign_id = request.query_params.get("campaign_id",None)
            date = request.query_params.get("date",None)
            inv_type = request.query_params.get("inv_type",None)
            act_type = request.query_params.get("act_type",None)
            if campaign_id is None or date is None or inv_type is None or act_type is None:
                return Response("Campaign Id or Date or inv type or act type is not provided")
            assigned_objects = InventoryActivityAssignment.objects.select_related('inventory_activity',
                                    'inventory_activity__shortlisted_inventory_details','inventory_activity__shortlisted_inventory_details__shortlisted_spaces'). \
                filter(inventory_activity__shortlisted_inventory_details__shortlisted_spaces__proposal=campaign_id,
                       activity_date=date,
                       inventory_activity__activity_type=act_type).\
                annotate(supplier_id=F('inventory_activity__shortlisted_inventory_details__shortlisted_spaces__object_id'),
                         assignment_id=F('id'),
                         inv_name=F('inventory_activity__shortlisted_inventory_details__ad_inventory_type__adinventory_name'),
                         space_id=F('inventory_activity__shortlisted_inventory_details__shortlisted_spaces__id')). \
                values('supplier_id','inv_name','space_id'). \
                annotate(total=Count('supplier_id'))

            completed_objects = InventoryActivityImage.objects.select_related('inventory_activity_assignment',
                                                          'inventory_activity_assignment__inventory_activity',
                                                          'inventory_activity_assignment__inventory_activity__shortlisted_inventory_details',
                                                          'inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__shortlisted_spaces'). \
                filter(inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__shortlisted_spaces__proposal=campaign_id,
                inventory_activity_assignment__activity_date=date,
                inventory_activity_assignment__inventory_activity__activity_type=act_type). \
                annotate(supplier_id=F('inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__shortlisted_spaces__object_id'),
                         inv_name=F('inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__ad_inventory_type__adinventory_name')). \
                values('supplier_id','inv_name'). \
                annotate(total=Count('inventory_activity_assignment', distinct=True))
            assigned_objects_map = {supplier['supplier_id'] : supplier for supplier in assigned_objects}
            completed_objects_map = {supplier['supplier_id']: supplier for supplier in completed_objects}

            # need to do by different supplier wise
            suppliers = SupplierTypeSociety.objects.filter(supplier_id__in=assigned_objects_map.keys()).values()
            suppliers_map = {supplier['supplier_id']:supplier for supplier in suppliers}
            result = {}
            for supplier in assigned_objects:
                if supplier['supplier_id'] not in result:
                    result[supplier['supplier_id']] = {}
                if supplier['inv_name'] not in result[supplier['supplier_id']]:
                    result[supplier['supplier_id']][supplier['inv_name']] = {}
                result[supplier['supplier_id']][supplier['inv_name']]['assigned'] = supplier['total']
                result[supplier['supplier_id']][supplier['inv_name']]['completed'] = 0
                result[supplier['supplier_id']]['supplier_data'] = suppliers_map[supplier['supplier_id']]
                result[supplier['supplier_id']]['space_id'] = supplier['space_id']
            for supplier in completed_objects:
                if supplier['supplier_id'] in result:
                    if supplier['inv_name'] in result[supplier['supplier_id']]:
                        result[supplier['supplier_id']][supplier['inv_name']]['completed'] = supplier['total']

            return handle_response(class_name, data=result, success=True)

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

class DeleteInventoryActivityAssignment(APIView):

    def post(self, request, id):
        class_name = self.__class__.__name__
        try:
            if not InventoryActivityImage.objects.filter(inventory_activity_assignment=id):
                InventoryActivityAssignment.objects.get(pk=id).delete()
                return ui_utils.handle_response(class_name, data=True, success=True)
            else:
                return ui_utils.handle_response(class_name, data="Image for this assignment is already present, Can not delete it", success=False)
        except Exception as e:
            return handle_response(class_name, exception_object=e, request=request)

class GetCampaignAssignments(APIView):
    @staticmethod
    def get(request, campaign_id):
        campaign_list_query = CampaignAssignment.objects.filter(campaign_id = campaign_id)
        campaign_list = CampaignAssignmentSerializer(campaign_list_query,many=True).data
        return ui_utils.handle_response({}, data=campaign_list, success=True)

class DeleteCampaignAssignments(APIView):
    @staticmethod
    def delete(request, assignment_id):
        assignment_query = CampaignAssignment.objects.get(id=assignment_id)
        assignment_query.delete()
        return ui_utils.handle_response({}, data='success', success=True)

class GetAdInventoryTypeAndDurationTypeData(APIView):
    @staticmethod
    def get(request):
        inventory_types = AdInventoryType.objects.all().values()
        duration_types = DurationType.objects.all().values()
        data = {
            'inventory_types' : inventory_types,
            'duration_types' : duration_types
        }
        return ui_utils.handle_response({}, data=data, success=True)

class AddDynamicInventoryIds(APIView):
    @staticmethod
    def post(request):
        data = request.data
        inv = AdInventoryType.objects.get(id=data['ad_inv_id'])
        duration = DurationType.objects.get(id=data['duration_id'])
        content_type = ui_utils.fetch_content_type(str(inv.adinventory_name))
        space = ShortlistedSpaces.objects.get(id=data['space_id'])
        now_time = timezone.now()
        shortlisted_inventories = []
        for inventory in range(data['inv_count']):
            inventory_id = "TEST" + str(inv.adinventory_name.strip()) + str(random.randint(1,2000)) + str(inventory)
            data = {
                'ad_inventory_type': inv,
                'ad_inventory_duration': duration,
                'inventory_id': inventory_id,
                'shortlisted_spaces': space,
                'created_at': now_time,
                'updated_at': now_time,
                'inventory_content_type_id': content_type.id
            }

            shortlisted_inventories.append(ShortlistedInventoryPricingDetails(**data))
        ShortlistedInventoryPricingDetails.objects.bulk_create(shortlisted_inventories)
        return ui_utils.handle_response({}, data={}, success=True)

class DeleteAdInventoryIds(APIView):
    @staticmethod
    def post(request):
        data = request.data
        total = 0
        for inventory in range(len(data)):
            if not InventoryActivityImage.objects.select_related('inventory_activity_assignment','inventory_activity_assignment__inventory_activity','inventory_activity_assignment__inventory_activity__shortlisted_inventory_details').filter(inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__id=data[inventory]):
                ShortlistedInventoryPricingDetails.objects.get(id=data[inventory]).delete()
                total += 1
        result = {
         'msg' : str(total) + " Inventories Deleted"
        }
        return ui_utils.handle_response({}, data=result, success=True)


@shared_task()
def get_leads_data_for_multiple_campaigns(campaign_list, cache_again=False):
    multi_campaign_return_data = {}

    # GETTING FROM CACHE START
    if cache_again is False:
        remaining_campaign_list = []
        for campaign in campaign_list:
            if str(campaign) in cache:
                multi_campaign_return_data[str(campaign)] = cache.get(str(campaign))
            else:
                remaining_campaign_list.append(campaign)
    else:
        remaining_campaign_list = campaign_list
    # GETTING FROM CACHE ENDS
    campaign_objects = ProposalInfo.objects.filter(proposal_id__in=remaining_campaign_list).values()
    campaign_objects_list = {campaign['proposal_id']: campaign for campaign in campaign_objects}
    valid_campaign_list = campaign_objects_list.keys()
    # leads_from_data = LeadsFormData.filter(campaign_id__in = campaign_list)
    # lead_items = LeadsFormItems.filter(campaign_id__in=campaign_list)
    for campaign_id in valid_campaign_list:
        shortlisted_supplier_ids = ShortlistedSpaces.objects.filter(proposal_id=campaign_id).values_list(
            'object_id')
        flat_count = SupplierTypeSociety.objects.filter(supplier_id__in=shortlisted_supplier_ids). \
            values('flat_count').aggregate(Sum('flat_count'))['flat_count__sum']
        leads_form_data = LeadsFormData.objects.filter(campaign_id=campaign_id)
        # leads_form_items = LeadsFormItems.objects.filter(campaign_id = campaign_id)
        leads_form_data_array = []
        for curr_object in leads_form_data:
            curr_data_1 = curr_object.__dict__
            curr_data = {key: curr_data_1[key] for key in ['item_id', 'item_value', 'leads_form_id', 'entry_id']}
            leads_form_data_array.append(curr_data)

        # combination of entry and form id is a lead
        total_leads = leads_form_data.values('entry_id', 'leads_form_id').distinct()
        total_leads_count = len(total_leads)

        # now computing hot leads

        hot_leads = 0
        hot_lead_fields = LeadsFormItems.objects.filter(campaign_id=campaign_id) \
            .exclude(hot_lead_criteria__isnull=True).values('item_id', 'leads_form_id', 'hot_lead_criteria')
        for curr_lead in total_leads:
            hot_lead = False
            leads_form_id = curr_lead['leads_form_id']
            entry_id = curr_lead['entry_id']
            # get all forms with hot lead criteria
            hot_lead_items_current = [x for x in hot_lead_fields if x['leads_form_id'] == leads_form_id]
            # data_current = [x for x in leads_form_data_array if x['leads_form'] == leads_form_id
            #                and x['entry_id'] == entry_id]
            for lead_item in hot_lead_items_current:
                hot_lead_item = lead_item['item_id']
                hot_lead_value = lead_item['hot_lead_criteria']
                data_current_hot = [x for x in leads_form_data_array if x['item_id'] == hot_lead_item and
                                    x['item_value'] == hot_lead_value and x['leads_form_id'] == leads_form_id
                                    and x['entry_id'] == entry_id]
                if len(data_current_hot) > 0 and hot_lead == False:
                    hot_lead = True
                    hot_leads = hot_leads + 1
        if hot_leads > 0:
            is_interested = 'true'
        else:
            is_interested = 'false'

        hot_lead_ratio = float(hot_leads / total_leads_count) if total_leads_count > 0 else 0

        multi_campaign_return_data[campaign_id] = {
            'total': total_leads_count,
            'is_interested': is_interested,
            'hot_lead_ratio': hot_lead_ratio,
            'data': campaign_objects_list[campaign_id],
            'interested': hot_leads,
            'campaign': campaign_id,
            'flat_count': flat_count
        }
        cache.set(str(campaign_id), multi_campaign_return_data[campaign_id], timeout=CACHE_TTL * 100)
    return multi_campaign_return_data


class CampaignLeadsMultiple(APIView):
    def post(self, request, pk=None):
        class_name = self.__class__.__name__
        try:
            campaign_list = request.data
            multi_campaign_return_data = get_leads_data_for_multiple_campaigns(campaign_list)
            return ui_utils.handle_response(class_name, data=multi_campaign_return_data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


@shared_task()
def get_leads_data_for_campaign(campaign_id, user_start_date_str=None, user_end_date_str=None, cache_again=False):
    cache_string = "single_" + str(campaign_id) + str(user_start_date_str) + str(user_end_date_str)
    if not cache_again:
        if cache_string in cache:
            final_data = cache.get(cache_string)
            return final_data
    format_str = '%d/%m/%Y'
    user_start_datetime = datetime.strptime(user_start_date_str,format_str) if user_start_date_str is not None else None
    user_end_datetime = datetime.strptime(user_end_date_str,format_str) if user_start_date_str is not None else None
    # will be used later

    leads_form_data = LeadsFormData.objects.filter(campaign_id=campaign_id).exclude(status='inactive').all()
    supplier_ids = list(set(leads_form_data.values_list('supplier_id', flat=True)))

    all_suppliers_list_non_analytics = {}
    all_localities_data_non_analytics = {}
    lead_form_items_list = LeadsFormItems.objects.filter(campaign_id=campaign_id).exclude(status='inactive').all()
    supplier_wise_lead_count = {}
    supplier_data_1 = SupplierTypeSociety.objects.filter(supplier_id__in=supplier_ids)
    supplier_data = SupplierTypeSocietySerializer2(supplier_data_1, many=True).data

    all_flat_data = {
        "0-150":{
            "campaign": campaign_id,
            "flat_category": 1,
            "interested": 0,
            "total": 0,
            "suppliers": 0,
            "flat_count": 0
        },
        "151-399": {
            "campaign": campaign_id,
            "flat_category": 2,
            "interested": 0,
            "total": 0,
            "suppliers": 0,
            "flat_count": 0
        },
        "400+": {
            "campaign": campaign_id,
            "flat_category": 3,
            "interested": 0,
            "total": 0,
            "suppliers": 0,
            "flat_count": 0
        }
    }

    for curr_supplier_data in supplier_data:
        supplier_id = curr_supplier_data['supplier_id']
        supplier_locality = curr_supplier_data['society_locality']
        supplier_flat_count = curr_supplier_data['flat_count'] if curr_supplier_data['flat_count'] else 0
        lead_count = lead_counter(campaign_id, supplier_id, lead_form_items_list)
        supplier_wise_lead_count[supplier_id] = lead_count
        hot_leads = lead_count['hot_leads']
        total_leads = lead_count['total_leads']
        # getting society information

        hot_leads_percentage = round(float(hot_leads) / float(total_leads), 5)*100 if total_leads > 0 else 0
        curr_supplier_lead_data = {
            "is_interested": True,
            "campaign": campaign_id,
            "object_id": supplier_id,
            "interested": hot_leads,
            "total": total_leads,
            "data": curr_supplier_data,
            "hot_leads_percentage": hot_leads_percentage,
            "flat_count": supplier_flat_count
        }
        all_suppliers_list_non_analytics[supplier_id] = curr_supplier_lead_data

        if supplier_locality in all_localities_data_non_analytics:
            all_localities_data_non_analytics[supplier_locality]["interested"] = all_localities_data_non_analytics[
                                                                supplier_locality]["interested"] + hot_leads
            all_localities_data_non_analytics[supplier_locality]["total"] = all_localities_data_non_analytics[
                                                                supplier_locality]["total"] + total_leads
            all_localities_data_non_analytics[supplier_locality]["suppliers"] = all_localities_data_non_analytics[
                                                                supplier_locality][ "suppliers"] + 1
            all_localities_data_non_analytics[supplier_locality]["flat_count"] = \
                all_localities_data_non_analytics[supplier_locality]["flat_count"] + supplier_flat_count

        else:
            curr_locality_data = {
                "is_interested": True,
                "campaign": campaign_id,
                "locality": supplier_locality,
                "interested": hot_leads,
                "total": total_leads,
                "suppliers": 1,
                "flat_count": supplier_flat_count
            }
            all_localities_data_non_analytics[supplier_locality] = curr_locality_data

        if supplier_flat_count<150:
            curr_flat_data = all_flat_data['0-150']
            curr_flat_data['interested'] = curr_flat_data['interested']+hot_leads
            curr_flat_data['total'] = curr_flat_data['total']+total_leads
            curr_flat_data['suppliers'] = curr_flat_data['suppliers'] + 1
            curr_flat_data['flat_count'] = curr_flat_data['flat_count'] + supplier_flat_count
            all_flat_data['0-150'] = curr_flat_data
        elif supplier_flat_count<400:
            curr_flat_data = all_flat_data['151-399']
            curr_flat_data['interested'] = curr_flat_data['interested']+hot_leads
            curr_flat_data['total'] = curr_flat_data['total']+total_leads
            curr_flat_data['suppliers'] = curr_flat_data['suppliers'] + 1
            curr_flat_data['flat_count'] = curr_flat_data['flat_count'] + supplier_flat_count
            all_flat_data['151-399'] = curr_flat_data
        else:
            curr_flat_data = all_flat_data['400+']
            curr_flat_data['interested'] = curr_flat_data['interested'] + hot_leads
            curr_flat_data['total'] = curr_flat_data['total'] + total_leads
            curr_flat_data['suppliers'] = curr_flat_data['suppliers'] + 1
            curr_flat_data['flat_count'] = curr_flat_data['flat_count'] + supplier_flat_count
            all_flat_data['400+'] = curr_flat_data

    all_suppliers_list = z_calculator_dict(all_suppliers_list_non_analytics, "hot_leads_percentage")
    all_localities_data_hot_ratio = hot_lead_ratio_calculator(all_localities_data_non_analytics)
    all_localities_data = z_calculator_dict(all_localities_data_hot_ratio, "hot_leads_percentage")

    # date-wise
    date_data = {}
    weekday_data = {}
    phase_data = {}
    all_entries_checked = []
    campaign_dates = leads_form_data.order_by('created_at').values_list('created_at',flat=True).distinct()
    if len(campaign_dates) == 0:
        final_data_dict = {'supplier': {}, 'date': {},
                           'locality': {}, 'weekday': {},
                           'flat': {}, 'phase': {}}
        return final_data_dict
    start_datetime = campaign_dates[0]
    end_datetime = campaign_dates[len(campaign_dates)-1]
    if user_start_datetime is not None:
        start_datetime = max(campaign_dates[0], user_start_datetime)
    if user_end_datetime is not None:
        end_datetime = min(campaign_dates[len(campaign_dates)-1], user_end_datetime)

    start_datetime_phase = start_datetime - timedelta(days=start_datetime.weekday())
    end_datetime_phase = end_datetime + timedelta(days=6-end_datetime.weekday())

    prev_phase = 0

    # for curr_date in campaign_dates:
    #     curr_phase = 1+((curr_date-start_datetime_phase).days)/7
    #     if curr_phase > prev_phase:
    #         phase_data['curr_phase'] = {
    #
    #         }

    weekday_names = {'0': 'Monday', '1': 'Tuesday', '2': 'Wednesday', '3': 'Thursday',
                     '4': 'Friday', '5': 'Saturday', '6': 'Sunday'}

    for curr_data in leads_form_data:

        curr_entry_details = {
            'leads_form_id': curr_data.leads_form_id,
            'entry_id': curr_data.entry_id
        }
        if curr_entry_details in all_entries_checked:
            continue
        else:
            all_entries_checked.append(curr_entry_details)

        time = curr_data.created_at
        curr_date = str(time.date())
        curr_time = str(time)
        curr_phase_int = 1 + (time - start_datetime_phase).days / 7
        curr_phase_start = time - timedelta(days=time.weekday())
        curr_phase_end = curr_phase_start + timedelta(days=7)
        curr_phase = str(curr_phase_int)
        if curr_phase not in phase_data:
            phase_data[curr_phase] = {
                'total': 0,
                'interested': 0,
                'suppliers': [],
                'supplier_count': 0,
                'flat_count': 0,
                'phase': curr_phase,
                'start date': curr_phase_start,
                'end date': curr_phase_end
            }

        curr_weekday = weekday_names[str(time.weekday())]

        supplier_id = curr_data.supplier_id
        curr_supplier_data = [x for x in supplier_data if x['supplier_id']==supplier_id][0]
        flat_count = curr_supplier_data['flat_count'] if curr_supplier_data['flat_count'] else 0
        lead_count = supplier_wise_lead_count[supplier_id]
        hot_lead_details = lead_count['hot_lead_details']

        if curr_date not in date_data:
            date_data[curr_date] = {
                'total': 0,
                'is_interested': True,
                'interested': 0,
                'created_at': curr_time,
                'suppliers': [],
                'supplier_count': 0,
                'flat_count': 0
            }

        if curr_weekday not in weekday_data:
            weekday_data[curr_weekday] = {
                'total': 0,
                'interested': 0,
                'suppliers': [],
                'supplier_count': 0,
                'flat_count': 0
            }

        date_data[curr_date]['total'] = date_data[curr_date]['total'] + 1
        weekday_data[curr_weekday]['total'] = weekday_data[curr_weekday]['total'] + 1
        phase_data[curr_phase]['total']=phase_data[curr_phase]['total']+1

        if curr_entry_details in hot_lead_details:
            date_data[curr_date]['interested'] = date_data[curr_date]['interested'] + 1
            weekday_data[curr_weekday]['interested'] = weekday_data[curr_weekday]['interested'] + 1
            phase_data[curr_phase]['interested'] = phase_data[curr_phase]['interested'] + 1

        if supplier_id not in date_data[curr_date]['suppliers']:
            date_data[curr_date]['supplier_count'] = date_data[curr_date]['supplier_count'] + 1
            date_data[curr_date]['flat_count'] = date_data[curr_date]['flat_count'] + flat_count
            date_data[curr_date]['suppliers'].append(supplier_id)

        if supplier_id not in weekday_data[curr_weekday]['suppliers']:
            weekday_data[curr_weekday]['supplier_count'] = weekday_data[curr_weekday]['supplier_count'] + 1
            weekday_data[curr_weekday]['flat_count'] = weekday_data[curr_weekday]['flat_count'] + flat_count
            weekday_data[curr_weekday]['suppliers'].append(supplier_id)

        if supplier_id not in phase_data[curr_phase]['suppliers']:
            phase_data[curr_phase]['supplier_count'] = phase_data[curr_phase]['supplier_count'] + 1
            phase_data[curr_phase]['flat_count'] = phase_data[curr_phase]['flat_count'] + flat_count
            phase_data[curr_phase]['suppliers'].append(supplier_id)

    date_data_hot_ratio = hot_lead_ratio_calculator(date_data)
    weekday_data_hot_ratio = hot_lead_ratio_calculator(weekday_data)
    phase_data_hot_ratio = hot_lead_ratio_calculator(phase_data)
    all_dates_data = z_calculator_dict(date_data_hot_ratio,"hot_leads_percentage")
    all_weekdays_data = z_calculator_dict(weekday_data_hot_ratio,"hot_leads_percentage")
    all_phase_data = z_calculator_dict(phase_data_hot_ratio,"hot_leads_percentage")
    all_flat_data = hot_lead_ratio_calculator(all_flat_data)

    final_data = {'supplier_data': all_suppliers_list, 'date_data': all_dates_data,
                  'locality_data': all_localities_data, 'weekday_data': all_weekdays_data,
                  'flat_data': all_flat_data, 'phase_data': phase_data}
    cache.set(cache_string, final_data, timeout=CACHE_TTL * 100)
    return final_data

class CampaignLeads(APIView):

    def get(self, request):
        class_name = self.__class__.__name__
        query_type = request.query_params.get('query_type')
        user_start_date_str = request.query_params.get('start_date', None)
        user_end_date_str = request.query_params.get('end_date', None)
        campaign_id = request.query_params.get('campaign_id', None)
        final_data = get_leads_data_for_campaign(campaign_id, user_start_date_str, user_end_date_str, cache_again=False)
        return ui_utils.handle_response(class_name, data=final_data, success=True)


class CampaignLeadsCustom(APIView):

    def get(self, request):
        class_name = self.__class__.__name__
        query_type = request.query_params.get('query_type')
        campaign_id = request.query_params.get('campaign_id', None)
        user_start_str = request.query_params.get('start_date', None)
        user_end_str = request.query_params.get('end_date', None)
        format_str = '%Y-%m-%d'
        user_start_datetime = datetime.strptime(user_start_str, format_str) if user_start_str is not None else None
        user_end_datetime = datetime.strptime(user_end_str, format_str) if user_end_str is not None else None
        final_data = {}
        date_data = {}
        weekday_data = {}
        phase_data = {}
        all_suppliers_list = {}
        all_localities_data = {}
        all_flat_data = {}
        supplier_additional_metrics = []
        locality_additional_metrics = []
        flat_additional_metrics = []
        if query_type in ['supplier', 'flat', 'locality']:
            leads_form_summary_query = LeadsFormSummary.objects.filter(campaign_id=campaign_id).all()
            leads_form_summary_data = LeadsFormSummarySerializer(leads_form_summary_query, many=True).data
            supplier_ids = list(set(leads_form_summary_query.values_list('supplier_id', flat=True)))
            supplier_data_objects = SupplierTypeSociety.objects.filter(supplier_id__in=supplier_ids)
            supplier_data = SupplierTypeSocietySerializer2(supplier_data_objects, many=True).data

            all_suppliers_list_non_analytics = {}
            all_localities_data_non_analytics = {}
            all_flat_data = {
                "0-150": {
                    "campaign": campaign_id,
                    "flat_category": 1,
                    "interested": 0,
                    "total": 0,
                    "suppliers": 0,
                    "flat_count": 0
                },
                "151-399": {
                    "campaign": campaign_id,
                    "flat_category": 2,
                    "interested": 0,
                    "total": 0,
                    "suppliers": 0,
                    "flat_count": 0
                },
                "400+": {
                    "campaign": campaign_id,
                    "flat_category": 3,
                    "interested": 0,
                    "total": 0,
                    "suppliers": 0,
                    "flat_count": 0
                }
            }

            for supplier_id in supplier_ids:

                curr_supplier_properties = [x for x in supplier_data if x['supplier_id']==supplier_id][0]
                curr_supplier_leads = [x for x in leads_form_summary_data if x['supplier_id']==supplier_id][0]
                total_leads = curr_supplier_leads['total_leads_count']
                hot_leads = curr_supplier_leads['hot_leads_count']
                hot_leads_percentage = curr_supplier_leads['hot_leads_percentage']
                flat_count = curr_supplier_properties['flat_count']
                supplier_locality = curr_supplier_properties['society_locality']
                if query_type == 'supplier':
                    curr_supplier_lead_data = {
                        "is_interested": True,
                        "campaign": campaign_id,
                        "object_id": supplier_id,
                        "interested": hot_leads,
                        "total": total_leads,
                        "data": curr_supplier_properties,
                        "hot_leads_percentage": hot_leads_percentage,
                        "flat_count": flat_count
                    }
                    all_suppliers_list_non_analytics[supplier_id] = curr_supplier_lead_data
                    supplier_additional_metrics.append({
                        'supplier_id': supplier_id,
                        'hot_leads_percentage': hot_leads_percentage,
                        'hot_lead_flat_ratio': round(hot_leads/float(flat_count), 3),
                        'total_lead_flat_ratio': round(total_leads/float(flat_count), 3)
                    })

                if query_type == 'locality':
                    if supplier_locality in all_localities_data_non_analytics:
                        all_localities_data_non_analytics[supplier_locality]["interested"] = \
                            all_localities_data_non_analytics[supplier_locality]["interested"] + hot_leads
                        all_localities_data_non_analytics[supplier_locality]["total"] = \
                            all_localities_data_non_analytics[supplier_locality]["total"] + total_leads
                        all_localities_data_non_analytics[supplier_locality]["suppliers"] = \
                            all_localities_data_non_analytics[supplier_locality]["suppliers"] + 1
                        all_localities_data_non_analytics[supplier_locality]["flat_count"] = \
                            all_localities_data_non_analytics[supplier_locality]["flat_count"] + flat_count

                    else:
                        curr_locality_data = {
                            "is_interested": True,
                            "campaign": campaign_id,
                            "locality": supplier_locality,
                            "interested": hot_leads,
                            "total": total_leads,
                            "suppliers": 1,
                            "flat_count": flat_count
                        }
                        all_localities_data_non_analytics[supplier_locality] = curr_locality_data

                if query_type == 'flat':
                    if flat_count < 150:
                        curr_flat_data = all_flat_data['0-150']
                        curr_flat_data['interested'] = curr_flat_data['interested'] + hot_leads
                        curr_flat_data['total'] = curr_flat_data['total'] + total_leads
                        curr_flat_data['suppliers'] = curr_flat_data['suppliers'] + 1
                        curr_flat_data['flat_count'] = curr_flat_data['flat_count'] + flat_count
                        all_flat_data['0-150'] = curr_flat_data
                    elif flat_count < 400:
                        curr_flat_data = all_flat_data['151-399']
                        curr_flat_data['interested'] = curr_flat_data['interested'] + hot_leads
                        curr_flat_data['total'] = curr_flat_data['total'] + total_leads
                        curr_flat_data['suppliers'] = curr_flat_data['suppliers'] + 1
                        curr_flat_data['flat_count'] = curr_flat_data['flat_count'] + flat_count
                        all_flat_data['151-399'] = curr_flat_data
                    else:
                        curr_flat_data = all_flat_data['400+']
                        curr_flat_data['interested'] = curr_flat_data['interested'] + hot_leads
                        curr_flat_data['total'] = curr_flat_data['total'] + total_leads
                        curr_flat_data['suppliers'] = curr_flat_data['suppliers'] + 1
                        curr_flat_data['flat_count'] = curr_flat_data['flat_count'] + flat_count
                        all_flat_data['400+'] = curr_flat_data

            all_suppliers_list = z_calculator_dict(all_suppliers_list_non_analytics, "hot_leads_percentage")
            all_localities_data_hot_ratio = hot_lead_ratio_calculator(all_localities_data_non_analytics)

            localities = all_localities_data_non_analytics.keys()
            for locality in localities:
                hot_leads_percentage = all_localities_data_hot_ratio[locality]['hot_leads_percentage']
                flat_count = all_localities_data_hot_ratio[locality]['flat_count']
                hot_leads = all_localities_data_hot_ratio[locality]['interested']
                total_leads = all_localities_data_hot_ratio[locality]['total']
                hot_lead_flat_ratio = round(hot_leads / float(flat_count), 3) if flat_count>0 else 0
                total_lead_flat_ratio = round(total_leads / float(flat_count), 3) if flat_count>0 else 0
                locality_additional_metrics.append({
                    'locality': locality,
                    'hot_leads_percentage': hot_leads_percentage,
                    'hot_lead_flat_ratio': hot_lead_flat_ratio,
                    'total_lead_flat_ratio': total_lead_flat_ratio
                })

            all_localities_data = z_calculator_dict(all_localities_data_hot_ratio, "hot_leads_percentage")
            flat_types = ['0-150','151-399','400+']
            all_flat_data = hot_lead_ratio_calculator(all_flat_data)
            for category in flat_types:
                hot_leads_percentage = all_flat_data[category]['hot_leads_percentage']
                hot_leads = all_flat_data[category]['interested']
                flat_count = all_flat_data[category]['flat_count']
                total_leads = all_flat_data[category]['total']
                hot_lead_flat_ratio = round(hot_leads / float(flat_count), 3) if flat_count>0 else 0
                total_lead_flat_ratio = round(total_leads / float(flat_count), 3) if flat_count>0 else 0
                flat_additional_metrics.append({
                    'flat category': category,
                    'hot_leads_percentage': hot_leads_percentage,
                    'hot_lead_flat_ratio': hot_lead_flat_ratio,
                    'total_lead_flat_ratio': total_lead_flat_ratio
                })


            supplier_hot_lead_pct = sorted(supplier_additional_metrics, key=itemgetter('hot_leads_percentage'))
            supplier_hot_lead_flat_ratio = sorted(supplier_additional_metrics, key=itemgetter('hot_lead_flat_ratio'))
            supplier_total_lead_flat_ratio = sorted(supplier_additional_metrics, key=itemgetter('total_lead_flat_ratio'))
            all_suppliers_list['hot lead % sorted'] = supplier_hot_lead_pct
            all_suppliers_list['hot leads per flat sorted'] = supplier_hot_lead_flat_ratio
            all_suppliers_list['total leads per flat sorted'] = supplier_total_lead_flat_ratio

            locality_hot_lead_pct = sorted(locality_additional_metrics, key=itemgetter('hot_leads_percentage'))
            locality_hot_lead_flat_ratio = sorted(locality_additional_metrics, key=itemgetter('hot_lead_flat_ratio'))
            locality_total_lead_flat_ratio = sorted(locality_additional_metrics, key=itemgetter('total_lead_flat_ratio'))
            all_localities_data['hot lead % sorted'] = locality_hot_lead_pct
            all_localities_data['hot leads per flat sorted'] = locality_hot_lead_flat_ratio
            all_localities_data['total leads per flat sorted'] = locality_total_lead_flat_ratio

            flat_hot_lead_pct = sorted(flat_additional_metrics, key=itemgetter('hot_leads_percentage'))
            flat_hot_lead_flat_ratio = sorted(flat_additional_metrics, key=itemgetter('hot_lead_flat_ratio'))
            flat_total_lead_flat_ratio = sorted(flat_additional_metrics, key=itemgetter('total_lead_flat_ratio'))
            all_flat_data['hot lead % sorted'] = flat_hot_lead_pct
            all_flat_data['hot leads per flat sorted'] = flat_hot_lead_flat_ratio
            all_flat_data['total leads per flat sorted'] = flat_total_lead_flat_ratio


        if query_type in ['date','weekday','phase']:
            leads_form_items = []
            leads_form_data = []
            all_entries_checked = []
            leads_form_data_objects = LeadsFormData.objects.filter(campaign_id=campaign_id).exclude(status='inactive').all()
            leads_form_items_objects = LeadsFormItems.objects.filter(campaign_id=campaign_id).exclude(
                status='inactive').all()
            for item in leads_form_items_objects:
                leads_form_items.append(item.__dict__)
            supplier_ids = list(set(leads_form_data_objects.values_list('supplier_id', flat=True)))
            supplier_data_objects = SupplierTypeSociety.objects.filter(supplier_id__in=supplier_ids)
            supplier_data = SupplierTypeSocietySerializer2(supplier_data_objects, many=True).data
            campaign_dates = leads_form_data_objects.order_by('created_at').values_list('created_at', flat=True).distinct()
            leads_form_data_objects_dates = leads_form_data_objects
            if user_start_datetime is not None:
                leads_form_data_objects_dates = leads_form_data_objects.filter(created_at__gte=user_start_datetime)
            if user_end_datetime is not None:
                leads_form_data_objects_dates = leads_form_data_objects_dates.filter(created_at__lte=user_end_datetime)
            campaign_dates = leads_form_data_objects_dates.order_by('created_at').\
                values_list('created_at', flat=True).distinct()
            if len(campaign_dates) == 0:
                final_data_dict = {'supplier': {}, 'date': {},
                                   'locality': {}, 'weekday': {},
                                   'flat': {}, 'phase': {}}
                return ui_utils.handle_response(class_name, data=final_data_dict, success=True)
            start_datetime = campaign_dates[0]
            end_datetime = campaign_dates[len(campaign_dates) - 1]
            start_datetime_phase = start_datetime - timedelta(days=start_datetime.weekday())

            weekday_names = {'0': 'Monday', '1': 'Tuesday', '2': 'Wednesday', '3': 'Thursday',
                             '4': 'Friday', '5': 'Saturday', '6': 'Sunday'}

            hot_lead_items = {}

            for data in leads_form_data_objects:
                leads_form_data.append(data.__dict__)

            for curr_data in leads_form_data:

                leads_form_id = curr_data['leads_form_id']
                entry_id = curr_data['entry_id']
                supplier_id = curr_data['supplier_id']

                curr_entry_details = {
                    'leads_form_id': leads_form_id,
                    'entry_id': entry_id
                }
                if curr_entry_details in all_entries_checked:
                    continue
                else:
                    all_entries_checked.append(curr_entry_details)

                time = curr_data['created_at']
                curr_date = str(time.date())
                curr_time = str(time)

                curr_data_all_fields = [x for x in leads_form_data if x['leads_form_id'] == leads_form_id
                                        and x['entry_id'] == entry_id]
                current_form_items = [x for x in leads_form_items if x['leads_form_id'] == leads_form_id]


                is_hot_lead = 0
                for curr_item in current_form_items:
                    if 'counseling' in curr_item['key_name']:
                        item_id = curr_item['item_id']
                        curr_data_c = [x for x in curr_data_all_fields if x['item_id']==item_id][0]
                        item_value = curr_data_c['item_value']
                        if item_value is not None and len(item_value)>0:
                            is_hot_lead = 1
                            break
                if is_hot_lead == 0:
                    if str(leads_form_id) in hot_lead_items:
                        hot_lead_items_current = hot_lead_items[str(leads_form_id)]
                    else:
                        hot_lead_items_current = [x['item_id'] for x in current_form_items if x['hot_lead_criteria'] is not None]
                        hot_lead_items[str(leads_form_id)] = hot_lead_items_current

                    for item_id in hot_lead_items_current:
                        curr_data_value = [x['item_value'] for x in curr_data_all_fields if x['item_id']==item_id]
                        hot_lead_criterion = [x['hot_lead_criteria'] for x in current_form_items if x['item_id']==item_id]

                        if curr_data_value == hot_lead_criterion:
                            is_hot_lead = 1
                            break

                curr_supplier_data = [x for x in supplier_data if x['supplier_id'] == supplier_id][0]
                flat_count = curr_supplier_data['flat_count'] if curr_supplier_data['flat_count'] else 0

                if query_type == 'phase':
                    curr_phase_int = 1 + (time - start_datetime_phase).days / 7
                    curr_phase_start = time - timedelta(days=time.weekday())
                    curr_phase_end = curr_phase_start + timedelta(days=7)
                    curr_phase = str(curr_phase_int)
                    if curr_phase not in phase_data:
                        phase_data[curr_phase] = {
                            'total': 0,
                            'interested': 0,
                            'suppliers': [],
                            'supplier_count': 0,
                            'flat_count': 0,
                            'phase': curr_phase,
                            'start date': curr_phase_start,
                            'end date': curr_phase_end
                        }
                    phase_data[curr_phase]['total'] = phase_data[curr_phase]['total'] + 1
                    phase_data[curr_phase]['interested'] = phase_data[curr_phase]['interested'] + is_hot_lead

                    if supplier_id not in phase_data[curr_phase]['suppliers']:
                        phase_data[curr_phase]['supplier_count'] = phase_data[curr_phase]['supplier_count'] + 1
                        phase_data[curr_phase]['flat_count'] = phase_data[curr_phase]['flat_count'] + flat_count
                        phase_data[curr_phase]['suppliers'].append(supplier_id)

                if query_type == 'date':
                    if curr_date not in date_data:
                        date_data[curr_date] = {
                            'total': 0,
                            'is_interested': True,
                            'interested': 0,
                            'created_at': curr_time,
                            'suppliers': [],
                            'supplier_count': 0,
                            'flat_count': 0
                        }
                    date_data[curr_date]['total'] = date_data[curr_date]['total'] + 1
                    date_data[curr_date]['interested'] = date_data[curr_date]['interested'] + is_hot_lead

                    if supplier_id not in date_data[curr_date]['suppliers']:
                        date_data[curr_date]['supplier_count'] = date_data[curr_date]['supplier_count'] + 1
                        date_data[curr_date]['flat_count'] = date_data[curr_date]['flat_count'] + flat_count
                        date_data[curr_date]['suppliers'].append(supplier_id)

                if query_type == 'weekday':
                    curr_weekday = weekday_names[str(time.weekday())]
                    if curr_weekday not in weekday_data:
                        weekday_data[curr_weekday] = {
                            'total': 0,
                            'interested': 0,
                            'suppliers': [],
                            'supplier_count': 0,
                            'flat_count': 0
                        }
                    weekday_data[curr_weekday]['total'] = weekday_data[curr_weekday]['total'] + 1
                    weekday_data[curr_weekday]['interested'] = weekday_data[curr_weekday]['interested'] + is_hot_lead

                    if supplier_id not in weekday_data[curr_weekday]['suppliers']:
                        weekday_data[curr_weekday]['supplier_count'] = weekday_data[curr_weekday]['supplier_count'] + 1
                        weekday_data[curr_weekday]['flat_count'] = weekday_data[curr_weekday]['flat_count'] + flat_count
                        weekday_data[curr_weekday]['suppliers'].append(supplier_id)
            date_data_hot_ratio = hot_lead_ratio_calculator(date_data)
            weekday_data_hot_ratio = hot_lead_ratio_calculator(weekday_data)
            phase_data_hot_ratio = hot_lead_ratio_calculator(phase_data)
            date_data = z_calculator_dict(date_data_hot_ratio,"hot_leads_percentage")
            weekday_data = z_calculator_dict(weekday_data_hot_ratio,"hot_leads_percentage")
            phase_data = z_calculator_dict(phase_data_hot_ratio,"hot_leads_percentage")

        final_data_dict = {'supplier': all_suppliers_list, 'date': date_data,
                           'locality': all_localities_data, 'weekday': weekday_data,
                           'flat': all_flat_data, 'phase': phase_data}

        final_data = final_data_dict[query_type] if query_type in final_data_dict.keys() else 'incorrect query type'

        return ui_utils.handle_response(class_name, data=final_data, success=True)


class CityWiseMultipleCampaignLeads(APIView):
    def get(self, request):
        username = request.user
        user_id = BaseUser.objects.get(username=username).id
        campaign_list = CampaignAssignment.objects.filter(assigned_to_id=user_id).values_list('campaign_id', flat=True)\
                             .distinct()
        campaign_leads = LeadsFormSummary.objects.filter(campaign_id__in=campaign_list).values(
            'supplier_id', 'campaign_id','total_leads_count','hot_leads_count')
        supplier_ids = campaign_leads.values_list('supplier_id',flat = True).distinct()
        supplier_properties = SupplierTypeSociety.objects.filter(supplier_id__in=supplier_ids)\
            .values('supplier_id', 'society_city', 'flat_count')
        city_list = supplier_properties.values_list('society_city',flat=True).distinct()
        city_leads_data = {}
        city_additional_metrics = []
        for curr_city in city_list:
            supplier_ids = list(set([x['supplier_id'] for x in supplier_properties if x['society_city'] == curr_city]))
            curr_city_campaign_data = [x for x in campaign_leads if x['supplier_id'] in supplier_ids]
            curr_city_supplier_data = [x for x in supplier_properties if x['supplier_id'] in supplier_ids and
                                       x['flat_count'] is not None]
            hot_leads = sum(x['hot_leads_count'] for x in curr_city_campaign_data)
            total_leads = sum(x['total_leads_count'] for x in curr_city_campaign_data)
            flat_count = sum(x['flat_count'] for x in curr_city_supplier_data)
            hot_leads_percentage = round(float(hot_leads)/float(total_leads)*100, 3)
            curr_city_leads = {
                "interested": hot_leads,
                "total": total_leads,
                "hot_leads_percentage": hot_leads_percentage,
                "flat_count": flat_count,
                "supplier count": len(supplier_ids)
            }
            city_leads_data[curr_city] = curr_city_leads

            city_additional_metrics.append({
                'city': curr_city,
                'hot_leads_percentage': hot_leads_percentage,
                'hot_lead_flat_ratio': round(hot_leads / float(flat_count), 3),
                'total_lead_flat_ratio': round(total_leads / float(flat_count), 3)
            })

        city_leads_data_z = z_calculator_dict(city_leads_data,"hot_leads_percentage")
        city_hot_lead_pct = sorted(city_additional_metrics, key=itemgetter('hot_leads_percentage'))
        city_hot_lead_flat_ratio=sorted(city_additional_metrics, key=itemgetter('hot_lead_flat_ratio'))
        city_total_lead_flat_ratio = sorted(city_additional_metrics, key=itemgetter('total_lead_flat_ratio'))
        city_leads_data_z.update({
            'hot lead % sorted': city_hot_lead_pct,
            'hot lead per flat sorted': city_hot_lead_flat_ratio,
            'total lead per flat sorted': city_total_lead_flat_ratio
        })

        #campaign_suppliers = ShortlistedSpaces.objects.filter(proposal_id__in=campaign_list)
        return ui_utils.handle_response({}, data=city_leads_data_z, success=True)


class PhaseWiseMultipleCampaignLeads(APIView):
    def post(self, request):
        class_name = self.__class__.__name__
        campaign_list = request.data
        phase_data_all = {}
        all_entries_checked = []
        for campaign_id in campaign_list:
            hot_lead_details = []
            leads_form_data_objects = LeadsFormData.objects.filter(campaign_id=campaign_id).exclude(status='inactive').all()
            leads_form_items_objects = LeadsFormItems.objects.filter(campaign_id=campaign_id).exclude(status='inactive').all()
            #leads_form_items = LeadsFormItemsSerializer(leads_form_items_objects).data
            leads_form_items = []
            leads_form_data = []
            phase_data = {}
            for item in leads_form_items_objects:
                leads_form_items.append(item.__dict__)
            for data in leads_form_data_objects:
                leads_form_data.append(data.__dict__)
            #campaign_dates = leads_form_data_objects.order_by('created_at').values_list('created_at', flat=True).distinct()
            campaign_dates = leads_form_data_objects.order_by('created_at').values_list('created_at', flat=True).distinct()
            start_datetime = campaign_dates[0]
            start_datetime_phase = start_datetime - timedelta(days=start_datetime.weekday())

            hot_lead_items = {}
            for curr_data in leads_form_data:

                leads_form_id = curr_data['leads_form_id']
                entry_id = curr_data['entry_id']

                curr_entry_details = {
                    'leads_form_id': leads_form_id,
                    'entry_id': entry_id
                }

                if curr_entry_details in all_entries_checked:
                    continue
                else:
                    all_entries_checked.append(curr_entry_details)

                # supplier_id = curr_data['supplier_id']
                # curr_supplier_data = [x for x in supplier_data if x['supplier_id'] == supplier_id][0]
                # flat_count = curr_supplier_data['flat_count']

                curr_data_all_fields = [x for x in leads_form_data if x['leads_form_id']==leads_form_id
                                        and x['entry_id']==entry_id]
                current_form_items = [x for x in leads_form_items if x['leads_form_id']==leads_form_id]

                if str(leads_form_id) in hot_lead_items:
                    hot_lead_items_current = hot_lead_items[str(leads_form_id)]
                else:
                    hot_lead_items_current = [x['item_id'] for x in current_form_items if x['hot_lead_criteria'] is not None]
                    hot_lead_items[str(leads_form_id)] = hot_lead_items_current

                is_hot_lead = 0
                for item_id in hot_lead_items_current:
                    curr_data_value = [x['item_value'] for x in curr_data_all_fields if x['item_id']==item_id]
                    hot_lead_criterion = [x['hot_lead_criteria'] for x in current_form_items if x['item_id']==item_id]

                    if curr_data_value == hot_lead_criterion:
                        is_hot_lead = 1
                        continue

                time = curr_data['created_at']
                curr_date = str(time.date())
                curr_time = str(time)
                curr_phase_int = 1 + (time - start_datetime_phase).days / 7
                curr_phase_start = time - timedelta(days=time.weekday())
                curr_phase_end = curr_phase_start + timedelta(days=7)
                curr_phase = str(curr_phase_int)
                if curr_phase not in phase_data:
                    phase_data[curr_phase] = {
                        'total': 0,
                        'interested': 0,
                        'phase': curr_phase,
                        'start date': curr_phase_start,
                        'end date': curr_phase_end
                    }

                phase_data[curr_phase]['total'] = phase_data[curr_phase]['total'] + 1
                phase_data[curr_phase]['interested'] = phase_data[curr_phase]['interested'] + is_hot_lead
                # if supplier_id not in phase_data[curr_phase]['suppliers']:
                #     phase_data[curr_phase]['supplier_count'] = phase_data[curr_phase]['supplier_count'] + 1
                #     phase_data[curr_phase]['flat_count'] = phase_data[curr_phase]['flat_count'] + flat_count
                #     phase_data[curr_phase]['suppliers'].append(supplier_id)

            phase_data_hot_ratio = hot_lead_ratio_calculator(phase_data)
            phase_data_campaign = z_calculator_dict(phase_data_hot_ratio, "hot_leads_percentage")
            phase_data_all[campaign_id] = phase_data_campaign


        return ui_utils.handle_response(class_name, data=phase_data_all, success=True)



class Comment(APIView):
    @staticmethod
    def post(request, campaign_id):
        user_id = request.user.id
        comment = request.data['comment']
        shortlisted_spaces_id = request.data['shortlisted_spaces_id'] if 'shortlisted_spaces_id' in request.data else None
        if not shortlisted_spaces_id:
            return ui_utils.handle_response({}, data='Shortlisted Space Id is Mandatory')

        related_to = request.data['related_to'] if 'related_to' in request.data else None
        inventory_type = request.data['inventory_type'] if 'inventory_type' in request.data else None
        inventory_comment = CampaignComments(**{
            "user_id": user_id,
            "shortlisted_spaces_id": shortlisted_spaces_id,
            "comment": comment,
            "campaign_id": campaign_id,
            "related_to": related_to,
            "inventory_type": inventory_type
        })
        inventory_comment.save()
        return ui_utils.handle_response({}, data='success', success=True)

    @staticmethod
    def get(request, campaign_id):
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Asia/Kolkata')
        shortlisted_spaces_id = request.query_params.get('shortlisted_spaces_id', None)
        related_to = request.query_params.get('related_to', None)
        inventory_type = request.query_params.get('inventory_type', None)
        all_campaign_comments = CampaignComments.objects.filter(campaign_id=campaign_id).all()
        if shortlisted_spaces_id:
            all_campaign_comments = all_campaign_comments.filter(shortlisted_spaces_id=shortlisted_spaces_id)
        if related_to:
            all_campaign_comments = all_campaign_comments.filter(related_to=related_to)
        if inventory_type:
            all_campaign_comments = all_campaign_comments.filter(inventory_type=inventory_type)
        all_campaign_comments_dict = {}
        for comment in all_campaign_comments:
            shortlisted_spaces_id = comment.shortlisted_spaces_id if comment.shortlisted_spaces_id else None
            if shortlisted_spaces_id not in all_campaign_comments_dict:
                all_campaign_comments_dict[shortlisted_spaces_id] = {}
            if not comment.inventory_type:
                if 'general' not in all_campaign_comments_dict[shortlisted_spaces_id]:
                    all_campaign_comments_dict[shortlisted_spaces_id]['general'] = []
            elif comment.inventory_type not in all_campaign_comments_dict[shortlisted_spaces_id]:
                all_campaign_comments_dict[shortlisted_spaces_id][comment.inventory_type] = []
            comment_obj = {
                'comment': comment.comment,
                'user_id': comment.user.id,
                'user_name': comment.user.username,
                'shortlisted_spaces_id': shortlisted_spaces_id,
                'inventory_type': comment.inventory_type,
                'related_to': comment.related_to,
                'timestamp': comment.created_at.replace(tzinfo=from_zone).astimezone(to_zone)
            }
            if comment.inventory_type:
                all_campaign_comments_dict[shortlisted_spaces_id][comment.inventory_type].append(comment_obj)
            else:
                all_campaign_comments_dict[shortlisted_spaces_id]['general'].append(comment_obj)
        if request.query_params.get('shortlisted_spaces_id', None):
            if shortlisted_spaces_id in all_campaign_comments_dict:
                all_campaign_comments_dict = all_campaign_comments_dict[shortlisted_spaces_id]
        return ui_utils.handle_response({}, data=all_campaign_comments_dict, success=True)


class SupplierPhaseUpdate(APIView):

    def put(self,request):
        class_name = self.__class__.__name__
        leads_form_data_objects = LeadsFormData.objects.exclude(status='inactive').order_by('created_at').all()
        campaign_list = list(set(leads_form_data_objects.values_list('campaign_id',flat=True)))
        leads_form_data = []
        data_keys = ['created_at','supplier_id','campaign_id']
        # for item in leads_form_items_objects:
        #     leads_form_items.append(item.__dict__)
        supplier_phase_data = []
        for data in leads_form_data_objects:
            curr_data = data.__dict__
            data_part = {key:curr_data[key] for key in data_keys}
            leads_form_data.append(data_part)
        now_time = timezone.now()
        suppliers_list_campaigns = []
        for campaign_id in campaign_list:
            leads_form_data_campaign = [x for x in leads_form_data if x['campaign_id'] == campaign_id]
            campaign_dates = [x['created_at'] for x in leads_form_data_campaign]
            start_datetime = campaign_dates[0]
            start_datetime_phase = start_datetime - timedelta(days=start_datetime.weekday())
            end_datetime = campaign_dates[len(campaign_dates)-1]
            end_datetime_phase = end_datetime + timedelta(days=(6-start_datetime.weekday()))
            total_phases = (end_datetime_phase - start_datetime_phase).days/7
            actual_phase = 1
            for curr_phase in range(0, total_phases):
                start_datetime_curr_phase = start_datetime + timedelta(days=7*curr_phase)
                end_datetime_curr_phase = start_datetime_curr_phase + timedelta(days=7)
                suppliers_list = list(set([x['supplier_id'] for x in leads_form_data_campaign if start_datetime_curr_phase <=
                                        x['created_at'] < end_datetime_curr_phase]))
                if len(suppliers_list)>0:
                    curr_campaign_phase_data = {
                        'phase_no': actual_phase,
                        'start_date': start_datetime_curr_phase,
                        'end_date': end_datetime_curr_phase,
                        'campaign_id': campaign_id,
                        'created_at': now_time,
                        'updated_at': now_time,
                        'comments': 'migrated from historic data'
                    }
                    supplier_phase_data.append(SupplierPhase(**curr_campaign_phase_data))
                    for supplier in suppliers_list:
                        suppliers_list_campaigns.append({
                            'object_id': supplier,
                            'campaign_id': campaign_id,
                            'phase_no': actual_phase
                        })
                    actual_phase = actual_phase+1
        SupplierPhase.objects.bulk_create(supplier_phase_data)

        # updating shortlisted spaces table
        for curr_element in suppliers_list_campaigns:
            object_id = curr_element['object_id']
            campaign_id = curr_element['campaign_id']
            phase_no = curr_element['phase_no']
            phase_no_id = SupplierPhase.objects.get(campaign_id=campaign_id, phase_no = phase_no).id
            ShortlistedSpaces.objects.filter(proposal_id=campaign_id, object_id=object_id).update(phase_no_id=phase_no_id)

        return ui_utils.handle_response(class_name, data={}, success=True)


# class FixInvalidDates(APIView):
#
#     def put(self,request):
#         class_name = self.__class__.__name__
#         invalid_date_suppliers = SupplierTypeSociety.objects.filter(created_at = '0000-00-00 00:00:00.000000').all()
#         suppliers_list = invalid_date_suppliers.values_list('supplier_id',flat=True)
#         for supplier_id in suppliers_list:
#             SupplierTypeSociety.update_or_create(created_at='1970-01-01', defaults = {
#                 'supplier_id': supplier_id
#             })
#         return ui_utils.handle_response(class_name, data={}, success=True)
