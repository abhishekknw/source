from __future__ import print_function
from __future__ import absolute_import
from v0.ui.dynamic_booking.views import (get_dynamic_booking_data_by_campaign)
from v0.ui.dynamic_booking.utils import get_dynamic_inventory_data_by_campaign
import random
import math
import numpy as np
from django.db.models import Count, Sum
from v0.ui.campaign.serializers import CampaignAssignmentSerializerReadOnly
from dateutil import tz
from datetime import datetime
from datetime import timedelta
from v0.ui.proposal.models import ProposalInfo, ShortlistedSpaces, SupplierPhase, HashTagImages, ProposalCenterMapping
from v0.ui.organisation.models import Organisation
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
from .models import (CampaignSocietyMapping, Campaign, CampaignAssignment, CampaignComments)
from .serializers import (CampaignListSerializer, CampaignSerializer, CampaignAssignmentSerializer)
from v0.ui.proposal.models import ShortlistedSpaces
from v0.ui.supplier.serializers import SupplierTypeSocietySerializer, SupplierTypeSocietySerializer2
from v0.ui.inventory.models import InventoryActivityImage, InventoryActivityAssignment, InventoryActivity, AdInventoryType
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework import status
import gpxpy.geo
from v0.ui.leads.models import (get_leads_summary, get_leads_summary_by_campaign, get_extra_leads_dict,
            get_leads_summary_by_campaign_and_hotness_level)
from v0.ui.base.models import DurationType
from v0.ui.finances.models import ShortlistedInventoryPricingDetails
from v0.ui.organisation.models import Organisation
from v0.ui.proposal.serializers import ProposalInfoSerializer
from v0.ui.account.models import ContactDetails
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from v0.ui.common.models import BaseUser
from operator import itemgetter
import requests
from celery import shared_task
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
from v0.ui.common.models import mongo_client
from django.db import connection, connections

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
            vendor = request.query_params.get('vendor',None)
            result = []
            category = request.query_params['category']
            if user.is_superuser:
                result = website_utils.get_campaigns_with_status(category, user, vendor)
            else:
                result = website_utils.get_campaigns_with_status(category, user, vendor)
            return ui_utils.handle_response(class_name, data=result, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


def get_sorted_value_keys(main_dict,sub_key):
    keys_list = list(main_dict.keys())
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
    keys = list(dict_data.keys())
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

def get_leads_summary_from_summary_table(campaign_id):
    suppliers  = list(mongo_client.leads_summary.find({"campaign_id": campaign_id}))
    result = {}
    if len(suppliers) > 0:
        for supplier in suppliers:
            result.setdefault(supplier['supplier_id'],{})
            supplier['is_hot_level_1'] = supplier['total_leads_count'] if supplier['total_leads_count'] else 0
            supplier['is_hot_level_2'] = supplier['total_hot_leads_count'] if supplier['total_hot_leads_count'] else 0
            supplier['is_hot_level_3'] = supplier['total_booking_confirmed'] if supplier['total_booking_confirmed'] else 0
            supplier['is_hot_level_4'] = supplier['total_orders_punched'] if supplier['total_orders_punched'] else 0
            result[supplier['supplier_id']] = supplier

    return result
def lead_counter(campaign_id, leads_form_data,user_start_datetime,user_end_datetime, lead_form):
    result = {}
    all_leads_summary = get_leads_summary(campaign_id,user_start_datetime,user_end_datetime)
    leads_by_hoteness_level = get_leads_summary_from_summary_table(campaign_id)

    all_campaign_leads = leads_form_data
    for summary in all_leads_summary:
        result[summary['supplier_id']] = {"hot_leads": summary['hot_leads_count'],
                                          "total_leads": summary['total_leads_count'],
                                          "hot_lead_details": [],
                                          "is_hot_level_1": leads_by_hoteness_level[summary['supplier_id']]
                                          ['is_hot_level_1']
                                            if summary['supplier_id'] in leads_by_hoteness_level else 0,
                                          "is_hot_level_2": leads_by_hoteness_level[summary['supplier_id']]
                                          ['is_hot_level_2']
                                          if summary['supplier_id'] in leads_by_hoteness_level else 0,
                                          "is_hot_level_3": leads_by_hoteness_level[summary['supplier_id']]
                                          ['is_hot_level_3']
                                          if summary['supplier_id'] in leads_by_hoteness_level else 0,
                                          "is_hot_level_4": leads_by_hoteness_level[summary['supplier_id']]
                                          ['is_hot_level_4']
                                          if summary['supplier_id'] in leads_by_hoteness_level else 0

                                          }
    for lead in all_campaign_leads:
        result[lead['supplier_id']]["hot_lead_details"].append({
            "entry_id": lead["entry_id"],
            "leads_form_id": lead["leads_form_id"]
        })
    return result


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
        campaign_id = request.query_params.get('campaign_id', None)
        current_date = timezone.now()
        object_id_alias = 'inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__shortlisted_spaces__object_id'

        shortlisted_suppliers = ShortlistedSpaces.objects.filter(proposal__proposal_id=campaign_id)
        shortlisted_suppliers_id_map = {supplier.object_id: supplier for supplier in shortlisted_suppliers}
        shortlisted_suppliers_id_list = [supplier.object_id for supplier in shortlisted_suppliers]
        shortlisted_spaces_id_list = [supplier.id for supplier in shortlisted_suppliers]
        shortlisted_spaces_id_dict = {supplier.id: supplier.object_id for supplier in shortlisted_suppliers}
        ss_id_dict_by_supplier_id = {supplier.object_id: supplier.id for supplier in shortlisted_suppliers}

        suppliers_instances = SupplierTypeSociety.objects.filter(supplier_id__in=shortlisted_suppliers_id_list)
        supplier_serializer = SupplierTypeSocietySerializer(suppliers_instances, many=True)
        suppliers = supplier_serializer.data
        flat_count = 0
        supplier_objects_id_list = {supplier['supplier_id']: supplier for supplier in suppliers}
        all_leads_count = get_leads_summary(campaign_id)
        all_campaign_extra_leads = {}
        all_extra_leads = get_extra_leads_dict(campaign_id)
        if campaign_id in all_extra_leads:
            all_campaign_extra_leads = all_extra_leads[campaign_id]
        supplier_wise_leads_count = {}

        for leads in all_leads_count:
            if leads['supplier_id'] not in supplier_objects_id_list:
                continue
            if 'flat_count' in supplier_objects_id_list[leads['supplier_id']] and supplier_objects_id_list[leads['supplier_id']]['flat_count']:
                flat_count = supplier_objects_id_list[leads['supplier_id']]['flat_count']
            else:
                flat_count = 0
            supplier_wise_leads_count[leads['supplier_id']] = {
                'hot_leads_count': leads['hot_leads_count'],
                'total_leads_count': leads['total_leads_count'],
                'hot_leads_percentage': leads['hot_leads_percentage'],
                'hot_leads_percentage_by_flat_count': calculate_percentage(leads['hot_leads_count'], flat_count),
                'flat_count': flat_count,
                'leads_flat_percentage': calculate_percentage(leads['total_leads_count'], flat_count)
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
            if id not in supplier_objects_id_list:
                continue
            data = {
                'supplier': supplier_objects_id_list[id],
                'leads_data': supplier_wise_leads_count[id] if id in supplier_wise_leads_count else {},
                'extra_leads_data': all_campaign_extra_leads[id] if id in all_campaign_extra_leads else {},
                'images_data': all_images_by_supplier[id] if id in all_images_by_supplier else {},
                'shortlisted_space_id': ss_id_dict_by_supplier_id[id],
                'phase' : shortlisted_suppliers_id_map[supplier_objects_id_list[id]['supplier_id']].phase_no.phase_no if
                    shortlisted_suppliers_id_map[supplier_objects_id_list[id]['supplier_id']].phase_no else None
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
            if id not in supplier_objects_id_list:
                continue
            data = {
                'supplier': supplier_objects_id_list[id],
                'leads_data': supplier_wise_leads_count[id] if id in supplier_wise_leads_count else {},
                'extra_leads_data': all_campaign_extra_leads[id] if id in all_campaign_extra_leads else {},
                'images_data': all_images_by_supplier[id] if id in all_images_by_supplier else {},
                'shortlisted_space_id': ss_id_dict_by_supplier_id[id],
                'phase': shortlisted_suppliers_id_map[supplier_objects_id_list[id]['supplier_id']].phase_no.phase_no if
                    shortlisted_suppliers_id_map[supplier_objects_id_list[id]['supplier_id']].phase_no else None
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
            if id not in supplier_objects_id_list:
                continue
            data = {
                'supplier': supplier_objects_id_list[id],
                'leads_data': supplier_wise_leads_count[id] if id in supplier_wise_leads_count else {},
                'extra_leads_data': all_campaign_extra_leads[id] if id in all_campaign_extra_leads else {},
                'images_data': all_images_by_supplier[id] if id in all_images_by_supplier else {},
                'shortlisted_space_id': ss_id_dict_by_supplier_id[id],
                'phase': shortlisted_suppliers_id_map[supplier_objects_id_list[id]['supplier_id']].phase_no.phase_no if
                    shortlisted_suppliers_id_map[supplier_objects_id_list[id]['supplier_id']].phase_no else None
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
        leads_form_summary_data = get_leads_summary(campaign_id)
        supplier_ids = list(set([single_summary['supplier_id'] for single_summary in leads_form_summary_data]))
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
            suppliers = SupplierTypeSociety.objects.filter(supplier_id__in=list(assigned_objects_map.keys())).values()
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
def get_leads_data_for_multiple_campaigns(campaign_list):
    multi_campaign_return_data = {}
    campaign_objects = ProposalInfo.objects.filter(proposal_id__in=campaign_list).values()
    campaign_objects_list = {campaign['proposal_id']: campaign for campaign in campaign_objects}
    valid_campaign_list = list(campaign_objects_list.keys())
    for campaign_id in valid_campaign_list:
        shortlisted_supplier_ids = ShortlistedSpaces.objects.filter(proposal_id=campaign_id).values_list(
            'object_id')
        flat_count = SupplierTypeSociety.objects.filter(supplier_id__in=shortlisted_supplier_ids). \
            values('flat_count').aggregate(Sum('flat_count'))['flat_count__sum']
        leads_form_summary_data = get_leads_summary_by_campaign(campaign_id)[0]
        multi_campaign_return_data[campaign_id] = {
            'total': leads_form_summary_data['total_leads_count'],
            'hot_lead_ratio': leads_form_summary_data['hot_leads_percentage']/100,
            'data': campaign_objects_list[campaign_id],
            'interested': leads_form_summary_data['hot_leads_count'],
            'campaign': campaign_id,
            'flat_count': flat_count
        }
    return multi_campaign_return_data


class CampaignLeadsMultiple(APIView):
    def post(self, request, pk=None):
        class_name = self.__class__.__name__
        campaign_list = request.data
        multi_campaign_return_data = get_leads_data_for_multiple_campaigns(campaign_list)
        return ui_utils.handle_response(class_name, data=multi_campaign_return_data, success=True)


def calculate_mode(num_list,window_size=3):
    if len(num_list) == 0:
        return None
    if len(num_list) == 1:
        return num_list[0]
    freq_by_windows = [0 for i in range(0,(num_list[-1] - num_list[0])//2 + 1)]
    for num in num_list:
        window_index = (num - num_list[0])//window_size
        freq_by_windows[window_index] += 1
    max_freq_index = 0
    max_freq_value = 0

    for idx,freq in enumerate(freq_by_windows):
        if freq >= max_freq_value:
            max_freq_index = idx
            max_freq_value = freq
    max_index_lower = num_list[0] + window_size * max_freq_index
    max_index_upper = max_index_lower + window_size - 1
    mode = float((max_index_upper + max_index_lower))/2.0
    return mode


def get_mean_median_mode(object_list, list_of_attributes):
    # flat_count is mandatory in object
    list_of_attributes.append('flat_count')
    all_attribute_item_list = {}
    percentage_by_flat_of_attribute = {}
    return_dict = {}
    for attribute in list_of_attributes:
        if attribute != 'flat_count':
            return_dict[attribute] = {'percentage_by_flat': 0, 'mean_by_society': 0, 'median_by_society': 0,
                                      'mode_percent_by_flat': 0, 'median_percent_by_flat': 0, 'mean_percent_by_flat': 0}
    for object in object_list:
        for attribute in list_of_attributes:
            if attribute not in object_list[object]:
                return return_dict
            if attribute not in all_attribute_item_list:
                all_attribute_item_list[attribute] = []
            if object_list[object][attribute]:
                all_attribute_item_list[attribute].append(object_list[object][attribute])
            if attribute != 'flat_count':
                if attribute not in percentage_by_flat_of_attribute:
                    percentage_by_flat_of_attribute[attribute] = []
                if object_list[object]['flat_count'] != 0:
                    if object_list[object]['flat_count']:
                        percentage_by_flat_of_attribute[attribute].append(int(round(float(object_list[object][attribute])/float(object_list[object]['flat_count']) * 100)))
    for attribute in list_of_attributes:
        if attribute != 'flat_count':
            percentage_by_flat = 0
            if attribute in all_attribute_item_list and sum(all_attribute_item_list['flat_count']) != 0:
                percentage_by_flat = float(sum(all_attribute_item_list[attribute]))/float(sum(all_attribute_item_list['flat_count'])) * 100
            mean_by_society = np.average(all_attribute_item_list[attribute]) if attribute in all_attribute_item_list else 0
            median_by_society = np.median(all_attribute_item_list[attribute]) if attribute in all_attribute_item_list else 0
            return_dict[attribute] = {
                'percentage_by_flat':  percentage_by_flat,
                'mean_by_society': 0 if math.isnan(mean_by_society) else mean_by_society,
                'median_by_society': 0 if math.isnan(median_by_society) else median_by_society,
                'mode_percent_by_flat': 0,
                'median_percent_by_flat': 0,
                'mean_percent_by_flat': 0
            }
    for attribute in percentage_by_flat_of_attribute:
        if attribute != 'flat_count':
            try:
                percentage_by_flat_of_attribute[attribute] = sorted(percentage_by_flat_of_attribute[attribute])
                median_percent_by_flat = np.median(percentage_by_flat_of_attribute[attribute])
                mean_percent_by_flat = np.average(percentage_by_flat_of_attribute[attribute])
                return_dict[attribute]['mode_percent_by_flat'] = calculate_mode(percentage_by_flat_of_attribute[attribute])
                return_dict[attribute]['median_percent_by_flat'] = 0 if math.isnan(median_percent_by_flat) else median_percent_by_flat
                return_dict[attribute]['mean_percent_by_flat'] = 0 if math.isnan(median_percent_by_flat) else mean_percent_by_flat
            except Exception as ex:
                print(ex)
                return_dict[attribute]['mode_percent_by_flat'] = None
    return return_dict


def get_leads_data_for_campaign(campaign_id, user_start_date_str=None, user_end_date_str=None):
    try:
        format_str = '%d/%m/%Y'
        phase_start_weekday = 'Tuesday' # this is used to set the phase cycle
        user_start_datetime = datetime.strptime(user_start_date_str,format_str) if user_start_date_str is not None else None
        user_end_datetime = datetime.strptime(user_end_date_str,format_str) if user_end_date_str is not None else None
        and_constraint = [{"campaign_id": campaign_id}, {"status": {"$ne": "inactive"}}]
        if user_start_datetime:
            and_constraint.append({"user_end_datetimecreated_at": {"$gte": user_start_datetime}})
        if user_end_datetime:
            and_constraint.append({"created_at": {"$lte": user_end_datetime}})
        leads_form_data = list(mongo_client.leads.find(
            {"$and": and_constraint}, {"_id": 0}))
        all_shortlisted_spaces = ShortlistedSpaces.objects.filter(proposal_id=campaign_id).all().values("object_id")
        supplier_ids = list(set([x['object_id'] for x in all_shortlisted_spaces]))
        all_suppliers_list_non_analytics = {}
        all_localities_data_non_analytics = {}
        supplier_wise_lead_count = {}
        supplier_data_1 = SupplierTypeSociety.objects.filter(supplier_id__in=supplier_ids)
        supplier_data = SupplierTypeSocietySerializer2(supplier_data_1, many=True).data
        all_flat_data = {}
        flat_categories = ['0-150', '151-399', '400+']
        flat_category_id = 0
        overall_data = {
            'supplier_count': 0,
            'total_leads': 0,
            'total_hot_leads': 0,
            'flat_count': 0,
            'is_hot_level_1': 0,
            'is_hot_level_2': 0,
            'is_hot_level_3': 0,
            'is_hot_level_4': 0,
        }
        for flat_category in flat_categories:
            flat_category_id = flat_category_id + 1
            all_flat_data[flat_category] = {
                "campaign": campaign_id,
                "flat_category": flat_category_id,
                "interested": 0,
                "total": 0,
                "suppliers": 0,
                "flat_count": 0,
                'is_hot_level_1': 0,
                'is_hot_level_2': 0,
                'is_hot_level_3': 0,
                'is_hot_level_4': 0,
            }
        lead_form = mongo_client.leads_forms.find({"campaign_id": campaign_id})
        campaign_hot_leads_dict = lead_counter(campaign_id, leads_form_data, user_start_datetime, user_end_datetime, lead_form[0])

        for curr_supplier_data in supplier_data:
            supplier_id = curr_supplier_data['supplier_id']
            supplier_locality = curr_supplier_data['society_locality']
            supplier_flat_count = curr_supplier_data['flat_count'] if curr_supplier_data['flat_count'] else 0
            lead_count = campaign_hot_leads_dict[supplier_id] if supplier_id in campaign_hot_leads_dict else None
            # leads_data =  campaign_hot_leads_dict[supplier_id]['leads'] if supplier_id in campaign_hot_leads_dict else None
            if not lead_count:
                continue
            overall_data['supplier_count'] += 1
            is_hot_level_1 = campaign_hot_leads_dict[supplier_id]['is_hot_level_1'] \
                if supplier_id in campaign_hot_leads_dict else 0
            is_hot_level_2 = campaign_hot_leads_dict[supplier_id]['is_hot_level_2'] \
                if supplier_id in campaign_hot_leads_dict else 0
            is_hot_level_3 = campaign_hot_leads_dict[supplier_id]['is_hot_level_3'] \
                if supplier_id in campaign_hot_leads_dict else 0
            is_hot_level_4 = campaign_hot_leads_dict[supplier_id]['is_hot_level_4'] \
                if supplier_id in campaign_hot_leads_dict else 0
            overall_data['is_hot_level_1'] += is_hot_level_1
            overall_data['is_hot_level_2'] += is_hot_level_2
            overall_data['is_hot_level_3'] += is_hot_level_3
            overall_data['is_hot_level_4'] += is_hot_level_4
            supplier_wise_lead_count[supplier_id] = lead_count
            hot_leads = lead_count['hot_leads']
            total_leads = lead_count['total_leads']
            overall_data['total_leads'] += total_leads
            overall_data['total_hot_leads'] += hot_leads
            overall_data['flat_count'] += supplier_flat_count
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
                "flat_count": supplier_flat_count,
                'is_hot_level_1': is_hot_level_1,
                'is_hot_level_2': is_hot_level_2,
                'is_hot_level_3': is_hot_level_3,
                'is_hot_level_4': is_hot_level_4,
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
                all_localities_data_non_analytics[supplier_locality]["is_hot_level_1"] = \
                    all_localities_data_non_analytics[supplier_locality]["is_hot_level_1"] + is_hot_level_1
                all_localities_data_non_analytics[supplier_locality]["is_hot_level_2"] = \
                    all_localities_data_non_analytics[supplier_locality]["is_hot_level_2"] + is_hot_level_2
                all_localities_data_non_analytics[supplier_locality]["is_hot_level_3"] = \
                    all_localities_data_non_analytics[supplier_locality]["is_hot_level_3"] + is_hot_level_3
                all_localities_data_non_analytics[supplier_locality]["is_hot_level_4"] = \
                    all_localities_data_non_analytics[supplier_locality]["is_hot_level_4"] + is_hot_level_4

            else:
                curr_locality_data = {
                    "is_interested": True,
                    "campaign": campaign_id,
                    "locality": supplier_locality,
                    "interested": hot_leads,
                    "total": total_leads,
                    "suppliers": 1,
                    "flat_count": supplier_flat_count,
                    'is_hot_level_1': is_hot_level_1,
                    'is_hot_level_2': is_hot_level_2,
                    'is_hot_level_3': is_hot_level_3,
                    'is_hot_level_4': is_hot_level_4,
                }
                all_localities_data_non_analytics[supplier_locality] = curr_locality_data

            if supplier_flat_count<150:
                curr_flat_data = all_flat_data['0-150']
                curr_flat_data['interested'] = curr_flat_data['interested']+hot_leads
                curr_flat_data['total'] = curr_flat_data['total']+total_leads
                curr_flat_data['suppliers'] = curr_flat_data['suppliers'] + 1
                curr_flat_data['flat_count'] = curr_flat_data['flat_count'] + supplier_flat_count
                curr_flat_data['is_hot_level_1'] = curr_flat_data['is_hot_level_1'] + is_hot_level_1
                curr_flat_data['is_hot_level_2'] = curr_flat_data['is_hot_level_2'] + is_hot_level_2
                curr_flat_data['is_hot_level_3'] = curr_flat_data['is_hot_level_3'] + is_hot_level_3
                curr_flat_data['is_hot_level_4'] = curr_flat_data['is_hot_level_4'] + is_hot_level_4
                all_flat_data['0-150'] = curr_flat_data
            elif supplier_flat_count<400:
                curr_flat_data = all_flat_data['151-399']
                curr_flat_data['interested'] = curr_flat_data['interested']+hot_leads
                curr_flat_data['total'] = curr_flat_data['total']+total_leads
                curr_flat_data['suppliers'] = curr_flat_data['suppliers'] + 1
                curr_flat_data['flat_count'] = curr_flat_data['flat_count'] + supplier_flat_count
                curr_flat_data['is_hot_level_1'] = curr_flat_data['is_hot_level_1'] + is_hot_level_1
                curr_flat_data['is_hot_level_2'] = curr_flat_data['is_hot_level_2'] + is_hot_level_2
                curr_flat_data['is_hot_level_3'] = curr_flat_data['is_hot_level_3'] + is_hot_level_3
                curr_flat_data['is_hot_level_4'] = curr_flat_data['is_hot_level_4'] + is_hot_level_4
                all_flat_data['151-399'] = curr_flat_data
            else:
                curr_flat_data = all_flat_data['400+']
                curr_flat_data['interested'] = curr_flat_data['interested'] + hot_leads
                curr_flat_data['total'] = curr_flat_data['total'] + total_leads
                curr_flat_data['suppliers'] = curr_flat_data['suppliers'] + 1
                curr_flat_data['flat_count'] = curr_flat_data['flat_count'] + supplier_flat_count
                curr_flat_data['is_hot_level_1'] = curr_flat_data['is_hot_level_1'] + is_hot_level_1
                curr_flat_data['is_hot_level_2'] = curr_flat_data['is_hot_level_2'] + is_hot_level_2
                curr_flat_data['is_hot_level_3'] = curr_flat_data['is_hot_level_3'] + is_hot_level_3
                curr_flat_data['is_hot_level_4'] = curr_flat_data['is_hot_level_4'] + is_hot_level_4
                all_flat_data['400+'] = curr_flat_data

        all_suppliers_list = z_calculator_dict(all_suppliers_list_non_analytics, "hot_leads_percentage")
        all_localities_data_hot_ratio = hot_lead_ratio_calculator(all_localities_data_non_analytics)
        all_localities_data = z_calculator_dict(all_localities_data_hot_ratio, "hot_leads_percentage")

        # date-wise
        date_data = {}
        weekday_data = {}
        phase_data = {}
        all_entries_checked = []
        campaign_dates = sorted(list(set([x['created_at'] for x in leads_form_data])))
        if len(campaign_dates) == 0:
            final_data_dict = {'supplier': {}, 'date': {},
                               'locality': {}, 'weekday': {},
                               'flat': {}, 'phase': {}, 'overall_data': {}}
            return final_data_dict
        weekday_names = {'0': 'Monday', '1': 'Tuesday', '2': 'Wednesday', '3': 'Thursday',
                         '4': 'Friday', '5': 'Saturday', '6': 'Sunday'}
        weekday_codes = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
                         'Friday': 4, 'Saturday': 5, 'Sunday': 6}
        start_datetime = campaign_dates[0]
        end_datetime = campaign_dates[len(campaign_dates)-1]
        start_weekday_int = weekday_codes[phase_start_weekday]
        start_weekday_diff = (start_datetime.weekday() - start_weekday_int) % 7
        if user_start_datetime is not None:
            start_datetime = max(campaign_dates[0], user_start_datetime)
        if user_end_datetime is not None:
            end_datetime = min(campaign_dates[len(campaign_dates)-1], user_end_datetime)

        start_datetime_phase = start_datetime - timedelta(days=start_weekday_diff)

        for curr_data in leads_form_data:
            curr_entry_details = {
                'leads_form_id': curr_data['leads_form_id'],
                'entry_id': curr_data['entry_id']
            }
            if curr_entry_details in all_entries_checked:
                continue
            else:
                all_entries_checked.append(curr_entry_details)
            time = curr_data['created_at']
            curr_date = str(time.date())
            curr_time = str(time)
            curr_phase_int = math.floor(1 + (time - start_datetime_phase).days / 7)
            curr_phase_start = time - timedelta(days = (time.weekday() - start_weekday_int)%7)
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
                    'end date': curr_phase_end,
                    'is_hot_level_1': 0,
                    'is_hot_level_2': 0,
                    'is_hot_level_3': 0,
                    'is_hot_level_4': 0,
                }

            curr_weekday = weekday_names[str(time.weekday())]

            supplier_id = curr_data['supplier_id']

            curr_supplier_data = [x for x in supplier_data if x['supplier_id']==supplier_id]
            if len(curr_supplier_data) == 0:
                continue
            curr_supplier_data = curr_supplier_data[0]
            flat_count = curr_supplier_data['flat_count'] if curr_supplier_data['flat_count'] else 0
            if curr_date not in date_data:
                date_data[curr_date] = {
                    'total': 0,
                    'is_interested': True,
                    'interested': 0,
                    'created_at': curr_time,
                    'suppliers': [],
                    'supplier_count': 0,
                    'flat_count': 0,
                    'is_hot_level_1': 0,
                    'is_hot_level_2': 0,
                    'is_hot_level_3': 0,
                    'is_hot_level_4': 0,
                }

            if curr_weekday not in weekday_data:
                weekday_data[curr_weekday] = {
                    'total': 0,
                    'interested': 0,
                    'suppliers': [],
                    'supplier_count': 0,
                    'flat_count': 0,
                    'is_hot_level_1': 0,
                    'is_hot_level_2': 0,
                    'is_hot_level_3': 0,
                    'is_hot_level_4': 0,
                }

            date_data[curr_date]['total'] = date_data[curr_date]['total'] + 1
            weekday_data[curr_weekday]['total'] = weekday_data[curr_weekday]['total'] + 1
            phase_data[curr_phase]['total']=phase_data[curr_phase]['total']+1
            add_is_interested = 0
            if curr_data['is_hot']:
                add_is_interested = 1
            date_data[curr_date]['interested'] = date_data[curr_date]['interested'] + add_is_interested
            weekday_data[curr_weekday]['interested'] = weekday_data[curr_weekday]['interested'] + add_is_interested
            phase_data[curr_phase]['interested'] = phase_data[curr_phase]['interested'] + add_is_interested

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
        mean_median_dict = get_mean_median_mode(all_suppliers_list, ['interested', 'total','is_hot_level_3','is_hot_level_4'])
        overall_data['supplier_stats'] = mean_median_dict
        final_data = {'supplier_data': all_suppliers_list, 'date_data': all_dates_data,
                      'locality_data': all_localities_data, 'weekday_data': all_weekdays_data,
                      'flat_data': all_flat_data, 'phase_data': phase_data, 'overall_data': overall_data}
        return final_data
    except Exception as e:
        return None

def bookingPerformance(campaign_id, start_date):

    all_suppliers = ShortlistedSpaces.objects.filter(proposal_id=campaign_id).values('phase_no_id', 'booking_status', 'booking_sub_status')
    phase_no=[]
    for suppliers in all_suppliers:
       all_pahses = suppliers.phase_no_id
       phase_no.append(all_phases)

    phases = SupplierPhase.objects.filter(campaign_id=campaign_id, start_date__gte=start_date)
    # for phase in phases:
        # print(phase.start_date)




class CampaignLeads(APIView):

    def get(self, request):
        try:
            class_name = self.__class__.__name__
            user_id = request.user.id
            query_type = request.query_params.get('query_type')
            user_start_date_str = request.query_params.get('start_date', None)
            user_end_date_str = request.query_params.get('end_date', None)
            campaign_id = request.query_params.get('campaign_id', None)

            # if 'NOB' in campaign_id:
            #     final_data = {}
            #     start_date = datetime.now() - timedelta(days=7)
            #     if user_start_date_str != None:
            #         start_date = datetime.now() - timedelta(days=7)
            #         final_data['last_week'] = bookingPerformance(campaign_id, start_date.strftime("%d/%m/%Y"))
            #         start_date = datetime.now() - timedelta(days=14)
            #         final_data['last_two_weeks'] = bookingPerformance(campaign_id, start_date.strftime("%d/%m/%Y"))
            #         start_date = datetime.now() - timedelta(days=21)
            #         final_data['last_three_weeks'] = bookingPerformance(campaign_id, start_date.strftime("%d/%m/%Y"))
            #         final_data['overall_data'] = bookingPerformance(campaign_id)
            # else:
            final_data = get_leads_data_for_campaign(campaign_id, user_start_date_str, user_end_date_str)
            if not final_data:
                return ui_utils.handle_response(class_name, data=final_data, success=False)
            start_date = datetime.now() - timedelta(days=7)
            final_data['last_week'] = get_leads_data_for_campaign(campaign_id, start_date.strftime("%d/%m/%Y"))['overall_data']
            start_date = datetime.now() - timedelta(days=14)
            final_data['last_two_weeks'] = get_leads_data_for_campaign(campaign_id, start_date.strftime("%d/%m/%Y"))['overall_data']
            start_date = datetime.now() - timedelta(days=21)
            final_data['last_three_weeks'] = get_leads_data_for_campaign(campaign_id, start_date.strftime("%d/%m/%Y"))['overall_data']
            final_data['overall_data'] = get_leads_data_for_campaign(campaign_id)['overall_data']
            return ui_utils.handle_response(class_name, data=final_data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, data=final_data, success=False)


@shared_task()
def get_campaign_leads_custom(campaign_id, query_type, user_start_str, user_end_str):
    format_str = '%d/%m/%Y'
    phase_start_weekday = 'Tuesday' # this is used to set the phase cycle
    user_start_datetime = datetime.strptime(user_start_str, format_str) if user_start_str is not None else None
    user_end_datetime = datetime.strptime(user_end_str, format_str) if user_end_str is not None else None
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
        leads_form_summary_data = get_leads_summary(campaign_id)
        supplier_ids = list(set([single_summary['supplier_id'] for single_summary in leads_form_summary_data]))
        supplier_data_objects = SupplierTypeSociety.objects.filter(supplier_id__in=supplier_ids)
        supplier_data = SupplierTypeSocietySerializer2(supplier_data_objects, many=True).data

        all_suppliers_list_non_analytics = {}
        all_localities_data_non_analytics = {}
        flat_categories = ['0-150','151-399','400+']
        flat_category_id = 0
        for flat_category in flat_categories:
            flat_category_id = flat_category_id + 1
            all_flat_data[flat_category] = {
                "campaign": campaign_id,
                "flat_category": flat_category_id,
                "interested": 0,
                "total": 0,
                "suppliers": 0,
                "flat_count": 0
            }

        for supplier_id in supplier_ids:

                curr_supplier_properties = [x for x in supplier_data if x['supplier_id'] == supplier_id][0]
                curr_supplier_leads = [x for x in leads_form_summary_data if x['supplier_id'] == supplier_id][0]
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

        localities = list(all_localities_data_non_analytics.keys())
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
        all_entries_checked = []
        constraints_list = [{"campaign_id": campaign_id}, {"status": {"$ne": "inactive"}}]
        if user_start_datetime is not None:
            constraints_list.append({"created_at": {"gte": user_start_datetime}})
        if user_end_datetime is not None:
            constraints_list.append({"created_at": {"lte": user_end_datetime}})
        leads_form_data = list(mongo_client.leads.find(
            {"$and": constraints_list},
            {"_id": 0}))

        supplier_ids = list(set([x['supplier_id'] for x in leads_form_data]))
        supplier_data_objects = SupplierTypeSociety.objects.filter(supplier_id__in=supplier_ids)
        supplier_data = SupplierTypeSocietySerializer2(supplier_data_objects, many=True).data
        campaign_dates = sorted(list(set([x['created_at'] for x in leads_form_data])))
        if len(campaign_dates) == 0:
            final_data_dict = {'supplier': {}, 'date': {},
                               'locality': {}, 'weekday': {},
                               'flat': {}, 'phase': {}}
            return final_data_dict[query_type]
        weekday_names = {'0': 'Monday', '1': 'Tuesday', '2': 'Wednesday', '3': 'Thursday',
                         '4': 'Friday', '5': 'Saturday', '6': 'Sunday'}
        weekday_codes = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
                         'Friday': 4, 'Saturday': 5, 'Sunday': 6}
        start_datetime = campaign_dates[0]
        end_datetime = campaign_dates[len(campaign_dates) - 1]
        start_weekday_int = weekday_codes[phase_start_weekday]
        start_weekday_diff= (start_datetime.weekday() - start_weekday_int)%7
        start_datetime_phase = start_datetime - timedelta(days=start_weekday_diff)

        hot_lead_items = {}

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
                curr_phase_start = time - timedelta(days = (time.weekday() - start_weekday_int)%7)
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
    return final_data


class CampaignLeadsCustom(APIView):

    def get(self, request):
        class_name = self.__class__.__name__
        try:
            query_type = request.query_params.get('query_type')
            if query_type not in ['supplier', 'flat', 'locality', 'date', 'weekday', 'phase']:
                data='incorrect query type'
            campaign_id = request.query_params.get('campaign_id', None)
            user_start_str = request.query_params.get('start_date', None)
            user_end_str = request.query_params.get('end_date', None)
            format_str = '%Y-%m-%d'
            final_data = get_campaign_leads_custom(campaign_id, query_type, user_start_str, user_end_str)
            return ui_utils.handle_response(class_name, data=final_data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


class CityWiseMultipleCampaignLeads(APIView):
    def get(self, request):
        username = request.user
        user_id = BaseUser.objects.get(username=username).id
        campaign_list = CampaignAssignment.objects.filter(assigned_to_id=user_id).values_list('campaign_id', flat=True)\
                             .distinct()
        campaign_list = [campaign_id for campaign_id in campaign_list]
        campaign_leads = get_leads_summary(campaign_list)
        supplier_ids = list(set([single_summary['supplier_id'] for single_summary in campaign_leads]))
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
            phase_data = {}
            leads_form_data = list(mongo_client.leads.find(
                {"$and":[{"campaign_id": campaign_id}, {"status": {"$ne": "inactive"}}]},
                {"_id": 0}))
            campaign_dates = sorted(list(set([x['created_at'] for x in leads_form_data])))

            start_datetime = campaign_dates[0]
            start_datetime_phase = start_datetime - timedelta(days=start_datetime.weekday())

            for curr_data in leads_form_data:
                is_hot_lead = 1 if curr_data['is_hot'] else 0
                time = curr_data['created_at']
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


# class SupplierPhaseUpdate(APIView):
#
#     def put(self,request):
#         class_name = self.__class__.__name__
#         leads_form_data_objects = LeadsFormData.objects.exclude(status='inactive').order_by('created_at').all()
#         campaign_list = list(set(leads_form_data_objects.values_list('campaign_id',flat=True)))
#         leads_form_data = []
#         data_keys = ['created_at','supplier_id','campaign_id']
#         # for item in leads_form_items_objects:
#         #     leads_form_items.append(item.__dict__)
#         supplier_phase_data = []
#         for data in leads_form_data_objects:
#             curr_data = data.__dict__
#             data_part = {key:curr_data[key] for key in data_keys}
#             leads_form_data.append(data_part)
#         now_time = timezone.now()
#         suppliers_list_campaigns = []
#         for campaign_id in campaign_list:
#             leads_form_data_campaign = [x for x in leads_form_data if x['campaign_id'] == campaign_id]
#             campaign_dates = [x['created_at'] for x in leads_form_data_campaign]
#             start_datetime = campaign_dates[0]
#             start_datetime_phase = start_datetime - timedelta(days=start_datetime.weekday())
#             end_datetime = campaign_dates[len(campaign_dates)-1]
#             end_datetime_phase = end_datetime + timedelta(days=(6-start_datetime.weekday()))
#             total_phases = (end_datetime_phase - start_datetime_phase).days/7
#             actual_phase = 1
#             for curr_phase in range(0, total_phases):
#                 start_datetime_curr_phase = start_datetime + timedelta(days=7*curr_phase)
#                 end_datetime_curr_phase = start_datetime_curr_phase + timedelta(days=7)
#                 suppliers_list = list(set([x['supplier_id'] for x in leads_form_data_campaign if start_datetime_curr_phase <=
#                                         x['created_at'] < end_datetime_curr_phase]))
#                 if len(suppliers_list)>0:
#                     curr_campaign_phase_data = {
#                         'phase_no': actual_phase,
#                         'start_date': start_datetime_curr_phase,
#                         'end_date': end_datetime_curr_phase,
#                         'campaign_id': campaign_id,
#                         'created_at': now_time,
#                         'updated_at': now_time,
#                         'comments': 'migrated from historic data'
#                     }
#                     SupplierPhase(**curr_campaign_phase_data).save()
#                     for supplier in suppliers_list:
#                         suppliers_list_campaigns.append({
#                             'object_id': supplier,
#                             'campaign_id': campaign_id,
#                             'phase_no': actual_phase
#                         })
#                     actual_phase = actual_phase+1
#
#         # updating shortlisted spaces table
#         for curr_element in suppliers_list_campaigns:
#             object_id = curr_element['object_id']
#             campaign_id = curr_element['campaign_id']
#             phase_no = curr_element['phase_no']
#             phase_no_id = SupplierPhase.objects.get(campaign_id=campaign_id, phase_no = phase_no).id
#             ShortlistedSpaces.objects.filter(proposal_id=campaign_id, object_id=object_id).update(phase_no_id=phase_no_id)
#
#         return ui_utils.handle_response(class_name, data={}, success=True)


class GetPermissionBoxImages(APIView):
    @staticmethod
    def get(request, campaign_id, supplier_id):
        try:
            data = HashTagImages.objects.filter(object_id=supplier_id,campaign_id=campaign_id,hashtag='Permission Box')
            return ui_utils.handle_response({}, data=data, success=True)
        except Exception as e:
            return ui_utils.handle_response({}, exception_object=e, request=request)

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


def get_campaign_wise_summary(all_campaign_ids, user_start_datetime=None, user_end_datetime=None):
    all_campaign_objects = ProposalInfo.objects.filter(proposal_id__in=all_campaign_ids).all()
    all_campaign_id_name_map = {campaign.proposal_id: campaign.name for campaign in all_campaign_objects}
    leads_summary_by_supplier = get_leads_summary(campaign_list=all_campaign_ids,user_start_datetime=user_start_datetime, user_end_datetime=user_end_datetime)
    campaign_supplier_map = {}
    reverse_campaign_supplier_map = {}
    all_supplier_ids = []
    campaign_wise_leads = {}
    for summary_point in leads_summary_by_supplier:
        if summary_point["campaign_id"] not in campaign_supplier_map:
            campaign_supplier_map[summary_point["campaign_id"]] = []
        if summary_point["supplier_id"] not in campaign_supplier_map[summary_point["campaign_id"]]:
            campaign_supplier_map[summary_point["campaign_id"]].append(summary_point["supplier_id"])
        if summary_point["supplier_id"] not in all_supplier_ids:
            all_supplier_ids.append(summary_point["supplier_id"])
        if summary_point["campaign_id"] not in campaign_wise_leads:
            campaign_wise_leads[summary_point["campaign_id"]] = {
                "total_leads_count": 0, "hot_leads_count": 0
            }
        campaign_wise_leads[summary_point["campaign_id"]]["total_leads_count"] += summary_point["total_leads_count"]
        campaign_wise_leads[summary_point["campaign_id"]]["hot_leads_count"] += summary_point["hot_leads_count"]

        reverse_campaign_supplier_map[summary_point["supplier_id"]] = summary_point["campaign_id"]
    campaign_summary = {"campaign_wise": {}, "all_campaigns": {}}
    all_society_flat_counts = SupplierTypeSociety.objects.filter(supplier_id__in=all_supplier_ids).values(
        "supplier_id", "flat_count")
    campaign_flat_count_map = {}
    supplier_flat_count_map = {}
    for society in all_society_flat_counts:
        supplier_flat_count_map[society["supplier_id"]] = society["flat_count"]
        campaign_id = reverse_campaign_supplier_map[society["supplier_id"]]
        if campaign_id not in campaign_flat_count_map:
            campaign_flat_count_map[campaign_id] = 0
        if society["flat_count"]:
            campaign_flat_count_map[campaign_id] += society["flat_count"]
    leads_summary_by_supplier_dict = {}
    for summary_point in leads_summary_by_supplier:
        if summary_point["campaign_id"] not in leads_summary_by_supplier_dict:
            leads_summary_by_supplier_dict[summary_point["campaign_id"]] = {}
        if summary_point["supplier_id"] in supplier_flat_count_map:
            summary_point["flat_count"] = supplier_flat_count_map[summary_point["supplier_id"]]
        else:
            summary_point["flat_count"] = 0
        leads_summary_by_supplier_dict[summary_point["campaign_id"]][summary_point["supplier_id"]] = summary_point
    for campaign_id in campaign_wise_leads:
        if campaign_id not in campaign_flat_count_map:
            continue
        if campaign_id not in all_campaign_id_name_map:
            continue
        flat_count = campaign_flat_count_map[campaign_id]
        analytics = get_mean_median_mode(leads_summary_by_supplier_dict[campaign_id],
                                         ["total_leads_count", "hot_leads_count"])
        campaign_summary["campaign_wise"][campaign_id] = {
            "name": all_campaign_id_name_map[campaign_id],
            "total": campaign_wise_leads[campaign_id]["total_leads_count"],
            "interested": campaign_wise_leads[campaign_id]["hot_leads_count"],
            "total_supplier_count": len(campaign_supplier_map[campaign_id]),
            "flat_count": flat_count,
            "hot_leads_analytics": {
                "percentage_by_flat": analytics["hot_leads_count"]["percentage_by_flat"],
                "mean_percent_by_flat": analytics["hot_leads_count"]["mean_percent_by_flat"],
                "median_percent_by_flat": analytics["hot_leads_count"]["median_percent_by_flat"],
                "mode_percent_by_flat": analytics["hot_leads_count"]["mode_percent_by_flat"],
                "median_by_society": analytics["hot_leads_count"]["median_by_society"],
                "mean_by_society": analytics["hot_leads_count"]["mean_by_society"],
            },
            "total_leads_analytics": {
                "percentage_by_flat": analytics["total_leads_count"]["percentage_by_flat"],
                "mean_percent_by_flat": analytics["total_leads_count"]["mean_percent_by_flat"],
                "median_percent_by_flat": analytics["total_leads_count"]["median_percent_by_flat"],
                "mode_percent_by_flat": analytics["total_leads_count"]["mode_percent_by_flat"],
                "median_by_society": analytics["total_leads_count"]["median_by_society"],
                "mean_by_society": analytics["total_leads_count"]["mean_by_society"],
            },
        }
    analytics = get_mean_median_mode(campaign_summary["campaign_wise"], ["total", "interested"])
    campaign_summary["all_campaigns"]["total_leads_analytics"] = {
        "percentage_by_flat": analytics["total"]["percentage_by_flat"],
        "mean_percent_by_flat": analytics["total"]["mean_percent_by_flat"],
        "median_percent_by_flat": analytics["total"]["median_percent_by_flat"],
        "mode_percent_by_flat": analytics["total"]["mode_percent_by_flat"],
        "median_by_campaign": analytics["total"]["median_by_society"],
        "mean_by_campaign": analytics["total"]["mean_by_society"],
    }
    campaign_summary["all_campaigns"]["hot_leads_analytics"] = {
        "percentage_by_flat": analytics["interested"]["percentage_by_flat"],
        "mean_percent_by_flat": analytics["interested"]["mean_percent_by_flat"],
        "median_percent_by_flat": analytics["interested"]["median_percent_by_flat"],
        "mode_percent_by_flat": analytics["interested"]["mode_percent_by_flat"],
        "median_by_campaign": analytics["interested"]["median_by_society"],
        "mean_by_campaign": analytics["interested"]["mean_by_society"],
    }
    campaign_summary["all_campaigns"]["total_supplier_count"] = 0
    campaign_summary["all_campaigns"]["total"] = 0
    campaign_summary["all_campaigns"]["interested"] = 0
    campaign_summary["all_campaigns"]["flat_count"] = 0
    for campaign in campaign_summary["campaign_wise"]:
        campaign_summary["all_campaigns"]["total"] += campaign_summary["campaign_wise"][campaign][
            "total"]
        campaign_summary["all_campaigns"]["interested"] += campaign_summary["campaign_wise"][campaign]["interested"]
        campaign_summary["all_campaigns"]["flat_count"] += campaign_summary["campaign_wise"][campaign]["flat_count"]
        campaign_summary["all_campaigns"]["total_supplier_count"] += campaign_summary["campaign_wise"][campaign][
            "total_supplier_count"]
    return campaign_summary


def get_campaign_wise_summary_by_user(user_id, user_start_datetime=None, user_end_datetime=None):
    all_campaigns = CampaignAssignment.objects.filter(assigned_to_id=user_id).all()
    all_campaign_ids = [campaign.campaign_id for campaign in all_campaigns]
    campaign_wise_summary = get_campaign_wise_summary(all_campaign_ids, user_start_datetime, user_end_datetime)
    return campaign_wise_summary


class CampaignWiseSummary(APIView):
    @staticmethod
    def get(request):
        user_id = request.user.id
        user_start_date_str = request.query_params.get('start_date', None)
        user_end_date_str = request.query_params.get('end_date', None)
        campaign_summary = {}
        start_date = datetime.now() - timedelta(days=7)
        if user_start_date_str == None:
            campaign_summary['last_week'] = get_campaign_wise_summary_by_user(user_id, start_date)
            start_date = datetime.now() - timedelta(days=14)
            campaign_summary['last_two_weeks'] = get_campaign_wise_summary_by_user(user_id, start_date)
            start_date = datetime.now() - timedelta(days=21)
            campaign_summary['last_three_weeks'] = get_campaign_wise_summary_by_user(user_id, start_date)
            campaign_summary['overall'] = get_campaign_wise_summary_by_user(user_id)
        else:
            format_str = '%d/%m/%Y'
            user_start_datetime = datetime.strptime(user_start_date_str,format_str) if user_start_date_str is not None else None
            user_end_datetime = datetime.strptime(user_end_date_str,format_str) if user_end_date_str is not None else None
            campaign_summary['last_week'] = get_campaign_wise_summary_by_user(user_id, user_start_datetime, user_end_datetime)
            campaign_summary['last_two_weeks'] = get_campaign_wise_summary_by_user(user_id, user_start_datetime, user_end_datetime)
            campaign_summary['last_three_weeks'] = get_campaign_wise_summary_by_user(user_id, user_start_datetime, user_end_datetime)
            campaign_summary['overall'] = get_campaign_wise_summary_by_user(user_id, user_start_datetime, user_end_datetime)

        return ui_utils.handle_response({}, data=campaign_summary, success=True)


def get_duration_wise_summary_for_vendors(vendor_campaign_map, all_campaign_ids, days):
    start_date = None
    if days:
        start_date = datetime.now() - timedelta(days=days)
    campaign_summary_map = {}
    for vendor in vendor_campaign_map:
        campaign_summary_map[vendor] = get_campaign_wise_summary(vendor_campaign_map[vendor], start_date)[
            "all_campaigns"]
    campaign_summary_map['overall'] = get_campaign_wise_summary(all_campaign_ids, start_date)["all_campaigns"]
    return campaign_summary_map


class VendorWiseSummary(APIView):
    @staticmethod
    def get(request):
        user_id = request.user.id
        all_assigned_campaigns = get_all_assigned_campaigns(user_id, None)
        vendor_campaign_map = {}
        all_campaign_ids = []
        all_vendor_ids = []
        for campaign in all_assigned_campaigns:
            if campaign['principal_vendor']:
                if campaign['principal_vendor'] not in vendor_campaign_map:
                    vendor_campaign_map[campaign['principal_vendor']] = []
                vendor_campaign_map[campaign['principal_vendor']].append(campaign["proposal_id"])
                all_campaign_ids.append(campaign["proposal_id"])
                if campaign['principal_vendor'] not in all_campaign_ids:
                    all_vendor_ids.append(campaign['principal_vendor'])
        all_vendors = Organisation.objects.filter(organisation_id__in=all_vendor_ids).all()
        campaign_summary = {}
        campaign_summary['last_week'] = get_duration_wise_summary_for_vendors(vendor_campaign_map, all_campaign_ids, 7)
        campaign_summary['last_two_week'] = get_duration_wise_summary_for_vendors(vendor_campaign_map, all_campaign_ids, 14)
        campaign_summary['last_three_week'] = get_duration_wise_summary_for_vendors(vendor_campaign_map, all_campaign_ids, 21)
        campaign_summary['overall'] = get_duration_wise_summary_for_vendors(vendor_campaign_map, all_campaign_ids, None)
        campaign_summary['vendor_details'] = {}
        for vendor in all_vendors:
            campaign_summary['vendor_details'][vendor.organisation_id] = {'name': vendor.name}
        return ui_utils.handle_response({}, data=campaign_summary, success=True)


def get_duration_wise_summary_for_cities(all_city_campaign_mapping, all_campaign_ids, days):
    start_date = None
    if days:
        start_date = datetime.now() - timedelta(days=days)
    campaign_summary_map = {}
    for city in all_city_campaign_mapping:
        campaign_summary_map[city] = get_campaign_wise_summary(all_city_campaign_mapping[city], start_date)[
            "all_campaigns"]
    campaign_summary_map['overall'] = get_campaign_wise_summary(all_campaign_ids, start_date)["all_campaigns"]
    return campaign_summary_map


class CityWiseSummary(APIView):
    @staticmethod
    def get(request):
        user_id = request.user.id
        all_assigned_campaigns = get_all_assigned_campaigns(user_id, None)
        all_campaign_ids = [campaign["proposal_id"] for campaign in all_assigned_campaigns]
        all_city_campaign = ProposalCenterMapping.objects.filter(proposal_id__in=all_campaign_ids).all()
        all_city_campaign_mapping = {}
        for obj in all_city_campaign:
            if obj.city not in all_city_campaign_mapping:
                all_city_campaign_mapping[obj.city] = []
            all_city_campaign_mapping[obj.city].append(obj.proposal_id)
        campaign_summary = {}
        campaign_summary['last_week'] = get_duration_wise_summary_for_cities(all_city_campaign_mapping, all_campaign_ids, 7)
        campaign_summary['last_two_week'] = get_duration_wise_summary_for_cities(all_city_campaign_mapping, all_campaign_ids, 14)
        campaign_summary['last_three_week'] = get_duration_wise_summary_for_cities(all_city_campaign_mapping, all_campaign_ids, 21)
        campaign_summary['overall'] = get_duration_wise_summary_for_cities(all_city_campaign_mapping, all_campaign_ids, None)
        return ui_utils.handle_response({}, data=campaign_summary, success=True)

def get_all_assigned_campaigns_dynamic(user_id, vendor):
    try:
        users = BaseUser.objects.all().values('id', 'username')
        user_obj = {}
        if users:
            for user in users:
                row = {
                    "id": user.get('id', None),
                    "username": user.get('username', None)
                }
                if not user_obj.get(user['id']):
                    user_obj[user['id']] = row

        user = BaseUser.objects.get(id=user_id)
        username_list = BaseUser.objects.filter(profile__organisation=user.profile.organisation.organisation_id). \
        values_list('username')

        if user.is_superuser:
            assigned_objects = CampaignAssignment.objects.all()
        else:
            assigned_objects = CampaignAssignment.objects.filter(campaign__created_by__in=username_list)
        campaigns = []
        all_proposal_ids = []
        # check each one of them weather they are campaign or not
        for assign_object in assigned_objects:
            if assign_object.campaign.is_disabled:
                continue
            response = website_utils.is_campaign(assign_object.campaign)
            # if it is a campaign.
            if response.data['status']:
                campaigns.append(assign_object)
        serializer = CampaignAssignmentSerializerReadOnly(campaigns, many=True)
        campaign_obj = {}
        for data in serializer.data:
            if not campaign_obj.get(data['campaign']['proposal_id']):
                campaign_obj[data['campaign']['proposal_id']] = data
                campaign_state=data['campaign']['campaign_state']
                data['campaign']['campaign_state']=ui_utils.campaignState(campaign_state)
                data['campaign']["assigned_to"] = user_obj[data["assigned_to"]]['username']
                data['campaign']["assigned_by"] = user_obj[data["assigned_by"]]['username']


        campaign_list = [value for key,value in campaign_obj.items()]
        return campaign_list
    except Exception as e:
        return ui_utils.handle_response('', exception_object=e, request='')

def get_all_assigned_campaigns(user_id, vendor):
    if vendor:
        campaign_list = CampaignAssignment.objects.filter(assigned_to_id=user_id,
                                                          campaign__principal_vendor=vendor).values_list(
            'campaign_id', flat=True).distinct()
    else:
        campaign_list = CampaignAssignment.objects.filter(assigned_to_id=user_id,
                                                          ).values_list('campaign_id', flat=True).distinct()
    campaign_list = [campaign_id for campaign_id in campaign_list]
    all_campaigns = ProposalInfo.objects.filter(proposal_id__in=campaign_list)
    serialized_proposals = ProposalInfoSerializer(all_campaigns, many=True).data
    return serialized_proposals

def get_campaign_suppliers(campaign_id):
    dynamic_supplier_data = get_dynamic_booking_data_by_campaign(campaign_id)
    if len(dynamic_supplier_data):
        return dynamic_supplier_data
    supplier_list = ShortlistedSpaces.objects.filter(proposal_id=campaign_id).values_list(
        'object_id', flat=True).distinct()
    supplier_objects = SupplierTypeSociety.objects.filter(supplier_id__in=supplier_list)
    serializer = SupplierTypeSocietySerializer(supplier_objects, many=True)
    supplier_details = serializer.data
    return supplier_details


class AssignedCampaigns(APIView):
    @staticmethod
    def get(request):
        user_id = request.user.id
        vendor = request.query_params.get('vendor', None)
        all_assigned_campaigns = get_all_assigned_campaigns_dynamic(user_id, vendor)
        print(all_assigned_campaigns[0])
        all_campaign_ids = []
        for campaign in all_assigned_campaigns:
            if campaign and campaign['campaign'] and campaign['campaign']['proposal_id']:
                proposal = campaign['campaign']['proposal_id']
                if proposal not in all_campaign_ids:
                    all_campaign_ids.append(proposal)

        return ui_utils.handle_response({}, data=all_assigned_campaigns, success=True)


class BookingAttributes(APIView):
    @staticmethod
    def get(request, campaign_id):
        if not campaign_id:
            return ui_utils.handle_response({}, data='Please provide campaign id', success=False)
        supplier_details = get_campaign_suppliers(campaign_id)
        return ui_utils.handle_response({}, data=supplier_details, success=True)


class InventoryAttributes(APIView):
    @staticmethod
    def get(request, campaign_id):
        if not campaign_id:
            return ui_utils.handle_response({}, data='Please provide campaign id', success=False)
        inventory_count = get_dynamic_inventory_data_by_campaign(campaign_id)
        return ui_utils.handle_response({}, data=inventory_count, success=True)

class AllCampaigns(APIView):
    @staticmethod
    def get(request):
        is_supplier = request.query_params.get("supplier",False)
        all_campaigns = ProposalInfo.objects.filter(campaign_state="PTC")
        all_assigned_campaigns = ProposalInfoSerializer(all_campaigns, many=True).data
        all_campaign_ids = []
        if is_supplier:
            for campaign in all_assigned_campaigns:
                if campaign['proposal_id']:
                    if campaign['proposal_id'] not in all_campaign_ids:
                        all_campaign_ids.append(campaign['proposal_id'])
                        supplier_details = get_campaign_suppliers(campaign['proposal_id'])
                        campaign['supplier_details']=supplier_details
        return ui_utils.handle_response({}, data=all_assigned_campaigns, success=True)


class VendorDetails(APIView):
    @staticmethod
    def get(request):
        user_id = request.user.id
        all_assigned_campaigns = get_all_assigned_campaigns(user_id, None)
        all_vendor_ids = []
        for campaign in all_assigned_campaigns:
            if campaign['principal_vendor']:
                if campaign['principal_vendor'] not in all_vendor_ids:
                    all_vendor_ids.append(campaign['principal_vendor'])
        all_vendors = Organisation.objects.filter(organisation_id__in=all_vendor_ids).all()

        all_vendors_dict = {}
        for vendor in all_vendors:
            all_vendors_dict[vendor.organisation_id] = {'name': vendor.name}
        return ui_utils.handle_response({}, data=all_vendors_dict, success=True)


class UserCities(APIView):
    @staticmethod
    def get(request):
        user_id = request.user.id
        all_assigned_campaigns = get_all_assigned_campaigns(user_id, None)
        all_campaign_ids = [campaign['proposal_id'] for campaign in all_assigned_campaigns]
        campaign_cities = ProposalCenterMapping.objects.filter(proposal_id__in=all_campaign_ids).values_list(
            "city", flat=True)
        campaign_cities_distinct = list(set(campaign_cities))
        return ui_utils.handle_response({}, data={"list_of_cities": campaign_cities_distinct}, success=True)

class MISReportReceipts(APIView):
    @staticmethod
    def get(request):
        user_id = request.user.id
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        if start_date:
            all_campaigns = ProposalInfo.objects.all()
        else:
            all_campaigns = ProposalInfo.objects.all()
        return_list = []
        for campaign in all_campaigns:
            cursor = connection.cursor()
            cursor.execute("SELECT DISTINCT e.society_name, d.proposal_id, r.hashtag, e.Society_City, e.SOCIETY_LOCALITY \
            from shortlisted_inventory_pricing_details as c \
            inner join inventory_activity_assignment as a \
            inner join inventory_activity as b \
            inner join shortlisted_spaces as d \
            inner join supplier_society as e \
            inner join hashtag_images as r \
            on b.id = a.inventory_activity_id and b.shortlisted_inventory_details_id = c.id \
            and c.shortlisted_spaces_id = d.id and d.object_id = e.SUPPLIER_ID and r.object_id = e.supplier_id \
            where d.proposal_id in (%s) and a.activity_date between %s and %s and r.hashtag \
            = 'PERMISSION BOX'", [campaign.proposal_id,start_date, end_date])
            all_list_pb = cursor.fetchall()

            dict_details=['society_name', 'campaign_id', 'hashtag', 'society_city', 'society_locality']
            all_details_list_pb=[dict(zip(dict_details,l)) for l in all_list_pb]

            cursor.execute("SELECT DISTINCT e.society_name, d.proposal_id, r.hashtag, e.Society_City, e.SOCIETY_LOCALITY \
            from shortlisted_inventory_pricing_details as c \
            inner join inventory_activity_assignment as a \
            inner join inventory_activity as b \
            inner join shortlisted_spaces as d \
            inner join supplier_society as e \
            inner join hashtag_images as r \
            on b.id = a.inventory_activity_id and b.shortlisted_inventory_details_id = c.id \
            and c.shortlisted_spaces_id = d.id and d.object_id = e.SUPPLIER_ID and r.object_id = e.supplier_id \
            where d.proposal_id in (%s) and a.activity_date between %s and %s and r.hashtag \
            = 'RECEIPT'", [campaign.proposal_id,start_date, end_date])
            all_list_receipt = cursor.fetchall()
            all_shortlisted_spaces = ShortlistedSpaces.objects.filter(proposal_id=campaign.proposal_id, is_completed=True).all()
            all_supplier_ids = [ss.object_id for ss in all_shortlisted_spaces]
            dict_details=['society_name', 'campaign_id', 'hashtag', 'society_city', 'society_locality']
            all_details_list_receipt=[dict(zip(dict_details,l)) for l in all_list_receipt]
            return_list.append({"campaign_name": campaign.name,
                                "count_permission": len(all_details_list_pb),
                                "count_receipt": len(all_details_list_receipt),
                                "supplier_count": len(all_supplier_ids)})
        return ui_utils.handle_response({}, data=return_list, success=True)

class MISReportContacts(APIView):
    @staticmethod
    def get(request):
        user_id = request.user.id
        start_date = request.query_params.get('start_date', None)
        if start_date:
            all_campaigns = ProposalInfo.objects.filter(tentative_start_date__gte=start_date).all()
        else:
            all_campaigns = ProposalInfo.objects.all()
        return_list = []
        for campaign in all_campaigns:
            partial_dict = {"total_supplier_count": None,
                                                    "total_contacts_with_name": 0, "total_contacts_with_number": 0,
                            "campaign_name": campaign.name}
            all_shortlisted_spaces = ShortlistedSpaces.objects.filter(proposal_id=campaign.proposal_id).all()
            all_supplier_ids = [ss.object_id for ss in all_shortlisted_spaces]
            all_suppliers = ContactDetails.objects.filter(object_id__in=all_supplier_ids)
            partial_dict["total_supplier_count"] = len(all_shortlisted_spaces)
            for sc in all_suppliers:
                if sc.mobile:
                    partial_dict["total_contacts_with_number"] += 1
                if sc.name:
                    partial_dict["total_contacts_with_name"] += 1
            return_list.append(partial_dict)
        return handle_response('', data=return_list, success=True)

