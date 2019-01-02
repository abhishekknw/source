from __future__ import print_function
from django.forms import model_to_dict
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from v0.ui.inventory.serializers import (BannerInventorySerializer, PosterInventorySerializer,
                                         StandeeInventorySerializer, WallInventorySerializer, InventoryInfoSerializer,
                                         PoleInventorySerializer, PosterInventoryMappingSerializer,
                                         StallInventorySerializer, StreetFurnitureSerializer,
                                         InventoryActivityAssignmentSerializer, SocietyInventoryBookingSerializer,
                                         InventoryActivityAssignmentSerializerReadOnly, CampaignInventorySerializer)
from v0.ui.inventory.models import (StallInventory, BannerInventory, AdInventoryType, PosterInventory, StreetFurniture,
                                    StandeeInventory, WallInventory, InventoryInfo, PoleInventory,
                                    PosterInventoryMapping, AD_INVENTORY_CHOICES, InventoryActivityAssignment,
                                    INVENTORY_ACTIVITY_TYPES, InventoryActivityImage, InventoryActivity,
                                    SocietyInventoryBooking)
from v0.ui.proposal.models import (ProposalInfo)
import v0.ui.utils as ui_utils
import v0.constants as v0_constants
from v0 import errors
from v0.ui.supplier.models import SupplierAmenitiesMap, SupplierTypeSociety
from v0.ui.base.models import DurationType
import v0.utils as v0_utils
from rest_framework.pagination import PageNumberPagination
import v0.ui.website.utils as website_utils
from v0.ui.common.models import BaseUser
from django.db.models import Q, F
from v0.ui.finances.models import ShortlistedInventoryPricingDetails
import time
from bulk_update.helper import bulk_update
from django.db.models import Count
from v0.ui.campaign.models import (CampaignSocietyMapping, Campaign)
from v0.ui.campaign.serializers import (CampaignSocietyMappingSerializer, CampaignListSerializer)
import datetime


class AssignInventories(APIView):
    """
    Assigns inventories to all societies in the table. If already assigned, deletes them first and then re-assigns.
    Must be run after societies are created
    """

    def post(self, request):
        """

        Args:
            request:

        Returns:

        """
        class_name = self.__class__.__name__
        try:
            default_database_name = settings.DATABASES['default']['NAME']

            if default_database_name != v0_constants.database_name:
                return ui_utils.handle_response(class_name,
                                                data=errors.INCORRECT_DATABASE_NAME_ERROR.format(default_database_name,
                                                                                                 v0_constants.database_name))

            inventory_detail = request.data['inventory_detail']
            suppliers = SupplierTypeSociety.objects.all().values_list('supplier_id', flat=True)
            if not suppliers:
                raise Exception("NO societies in the database yet. Add them first and then hit this API.")
            response = ui_utils.get_content_type(v0_constants.society)
            if not response.data['status']:
                return response
            content_type = response.data['data']
            v0_utils.handle_supplier_inventory_detail(inventory_detail, suppliers, content_type)
            return ui_utils.handle_response(class_name, data='success', success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


class BannerInventoryAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = BannerInventory.objects.get(pk=id)
            serializer = BannerInventorySerializer(item)
            return Response(serializer.data)
        except BannerInventory.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = BannerInventory.objects.get(pk=id)
        except BannerInventory.DoesNotExist:
            return Response(status=404)
        serializer = BannerInventorySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = BannerInventory.objects.get(pk=id)
        except BannerInventory.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class BannerInventoryAPIListView(APIView):

    def get(self, request, format=None):
        items = BannerInventory.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = BannerInventorySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = BannerInventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CreateAdInventoryTypeDurationType(APIView):
    """
    Creates AdInventory and Duration objects if not present in the database.
    """

    def post(self, request):
        """
        Args:
            request:

        Returns:

        """
        class_name = self.__class__.__name__
        try:
            default_database_name = settings.DATABASES['default']['NAME']

            if default_database_name != v0_constants.database_name:
                return ui_utils.handle_response(class_name,
                                                data=errors.INCORRECT_DATABASE_NAME_ERROR.format(default_database_name,
                                                                                                 v0_constants.database_name))

            # for simplicity i have every combination
            for duration_code, duration_value in v0_constants.duration_dict.items():
                DurationType.objects.get_or_create(duration_name=duration_value)
            for inventory_tuple in AD_INVENTORY_CHOICES:
                for ad_inventory_type_code, ad_inventory_type_value in v0_constants.type_dict.items():
                    AdInventoryType.objects.get_or_create(adinventory_name=inventory_tuple[0],
                                                          adinventory_type=ad_inventory_type_value)
            return ui_utils.handle_response(class_name, data='success', success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


class InventoryInfoAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = InventoryInfo.objects.get(pk=id)
            serializer = InventoryInfoSerializer(item)
            return Response(serializer.data)
        except InventoryInfo.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = InventoryInfo.objects.get(pk=id)
        except InventoryInfo.DoesNotExist:
            return Response(status=404)
        serializer = InventoryInfoSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = InventoryInfo.objects.get(pk=id)
        except InventoryInfo.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class InventoryInfoAPIListView(APIView):

    def get(self, request, format=None):
        items = InventoryInfo.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = InventoryInfoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = InventoryInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class PoleInventoryAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = PoleInventory.objects.get(pk=id)
            serializer = PoleInventorySerializer(item)
            return Response(serializer.data)
        except PoleInventory.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = PoleInventory.objects.get(pk=id)
        except PoleInventory.DoesNotExist:
            return Response(status=404)
        serializer = PoleInventorySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = PoleInventory.objects.get(pk=id)
        except PoleInventory.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class PoleInventoryAPIListView(APIView):

    def get(self, request, format=None):
        items = PoleInventory.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = PoleInventorySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = PoleInventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class PosterInventoryMappingAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = PosterInventoryMapping.objects.get(pk=id)
            serializer = PosterInventoryMappingSerializer(item)
            return Response(serializer.data)
        except PosterInventoryMapping.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = PosterInventoryMapping.objects.get(pk=id)
        except PosterInventoryMapping.DoesNotExist:
            return Response(status=404)
        serializer = PosterInventoryMappingSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = PosterInventoryMapping.objects.get(pk=id)
        except PosterInventoryMapping.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class PosterInventoryMappingAPIListView(APIView):

    def get(self, request, format=None):
        items = PosterInventoryMapping.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = PosterInventoryMappingSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = PosterInventoryMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class PosterInventoryAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = PosterInventory.objects.get(pk=id)
            serializer = PosterInventorySerializer(item)
            return Response(serializer.data)
        except PosterInventory.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = PosterInventory.objects.get(pk=id)
        except PosterInventory.DoesNotExist:
            return Response(status=404)
        serializer = PosterInventorySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = PosterInventory.objects.get(pk=id)
        except PosterInventory.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class PosterInventoryAPIListView(APIView):

    def get(self, request, format=None):
        items = PosterInventory.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = PosterInventorySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = PosterInventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class StandeeInventoryAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = StandeeInventory.objects.get(pk=id)
            serializer = StandeeInventorySerializer(item)
            return Response(serializer.data)
        except StandeeInventory.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = StandeeInventory.objects.get(pk=id)
        except StandeeInventory.DoesNotExist:
            return Response(status=404)
        serializer = StandeeInventorySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = StandeeInventory.objects.get(pk=id)
        except StandeeInventory.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class StandeeInventoryAPIListView(APIView):

    def get(self, request, format=None):
        items = StandeeInventory.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = StandeeInventorySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = StandeeInventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class StreetFurnitureAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = StreetFurniture.objects.get(pk=id)
            serializer = StreetFurnitureSerializer(item)
            return Response(serializer.data)
        except StreetFurniture.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = StreetFurniture.objects.get(pk=id)
        except StreetFurniture.DoesNotExist:
            return Response(status=404)
        serializer = StreetFurnitureSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = StreetFurniture.objects.get(pk=id)
        except StreetFurniture.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class StreetFurnitureAPIListView(APIView):

    def get(self, request, format=None):
        items = StreetFurniture.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = StreetFurnitureSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = StreetFurnitureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class WallInventoryAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = WallInventory.objects.get(pk=id)
            serializer = WallInventorySerializer(item)
            return Response(serializer.data)
        except WallInventory.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = WallInventory.objects.get(pk=id)
        except WallInventory.DoesNotExist:
            return Response(status=404)
        serializer = WallInventorySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = WallInventory.objects.get(pk=id)
        except WallInventory.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class WallInventoryAPIListView(APIView):

    def get(self, request, format=None):
        items = WallInventory.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = WallInventorySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = WallInventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class StallInventoryAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = StallInventory.objects.get(pk=id)
            serializer = StallInventorySerializer(item)
            return Response(serializer.data)
        except StallInventory.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = StallInventory.objects.get(pk=id)
        except StallInventory.DoesNotExist:
            return Response(status=404)
        serializer = StallInventorySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = StallInventory.objects.get(pk=id)
        except StallInventory.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class StallInventoryAPIListView(APIView):

    def get(self, request, format=None):
        items = StallInventory.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = StallInventorySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = StallInventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class StandeeInventoryAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = StandeeInventory.objects.get(pk=id)
            serializer = StandeeInventorySerializer(item)
            return Response(serializer.data)
        except StandeeInventory.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = StandeeInventory.objects.get(pk=id)
        except StandeeInventory.DoesNotExist:
            return Response(status=404)
        serializer = StandeeInventorySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = StandeeInventory.objects.get(pk=id)
        except StandeeInventory.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class StandeeInventoryAPIListView(APIView):

    def get(self, request, format=None):
        items = StandeeInventory.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = StandeeInventorySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = StandeeInventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


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
            proposal = ProposalInfo.objects.get(proposal_id=campaign_id)
            response = website_utils.is_campaign(proposal)
            if not response.data['status']:
                return response
            #
            # cache_key = v0_utils.create_cache_key(class_name, campaign_id)
            # cache_value = cache.get(cache_key)
            # cache_value = None
            response = website_utils.prepare_shortlisted_spaces_and_inventories(campaign_id)
            if not response.data['status']:
                return response
            # cache.set(cache_key, response.data['data'])
            return ui_utils.handle_response(class_name, data=response.data['data'], success=True)

        except Exception as e:
            print("e2", e)
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

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
            proposal = ProposalInfo.objects.get(proposal_id=campaign_id)

            response = website_utils.is_campaign(proposal)
            if not response.data['status']:
                return response

            # clear the cache if it's a PUT request
            # cache_key = v0_utils.create_cache_key(class_name, campaign_id)
            # cache.delete(cache_key)

            data = request.data
            response = website_utils.handle_update_campaign_inventories(request.user, data)
            if not response.data['status']:
                return response

            return ui_utils.handle_response(class_name, data='successfully updated', success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


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
            do_not_query_by_date = request.query_params.get('do_not_query_by_date')
            all_users = BaseUser.objects.all().values('id', 'username')
            user_map = {detail['id']: detail['username'] for detail in all_users}
            shortlisted_supplier_id_set = set()

            # constructs a Q object based on current date and delta d days defined in constants
            assigned_date_range_query = Q()
            if not do_not_query_by_date:
                assigned_date_range_query = website_utils.construct_date_range_query('activity_date')

            proposal_query = Q()
            if proposal_id:
                proposal_query = Q(
                    inventory_activity__shortlisted_inventory_details__shortlisted_spaces__proposal_id=proposal_id)

            assigned_to_query = Q()
            if assigned_to:
                assigned_to_query = Q(assigned_to_id=int(assigned_to))

            # cache_key = v0_utils.create_cache_key(class_name, assigned_date_range_query, proposal_query, assigned_to_query)

            # we do a huge query to fetch everything we need at once.
            inv_act_assignment_objects = InventoryActivityAssignment.objects. \
                select_related('inventory_activity', 'inventory_activity__shortlisted_inventory_details',
                               'inventory_activity__shortlisted_inventory_details__shortlisted_spaces'). \
                filter(assigned_date_range_query, proposal_query, assigned_to_query).values(

                'id', 'activity_date', 'reassigned_activity_date', 'inventory_activity',
                'inventory_activity__activity_type', 'assigned_to',
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
                'inventory_activity__shortlisted_inventory_details__shortlisted_spaces__proposal__name',
            )

            result = website_utils.organise_supplier_inv_images_data(inv_act_assignment_objects, user_map)
            return ui_utils.handle_response(class_name, data=result, success=True)

        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


class InventoryActivityImageAPIView(APIView):
    """
     @Android API. used to insert image paths from Android.
     makes an entry into InventoryActivityImageAPIView table.
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
            shortlisted_inventory_detail_instance = ShortlistedInventoryPricingDetails.objects.get(
                id=request.data['shortlisted_inventory_detail_id'])
            activity_date = request.data['activity_date']
            activity_type = request.data['activity_type']
            activity_by = int(request.data['activity_by'])
            actual_activity_date = request.data['actual_activity_date']
            use_assigned_date = int(request.data['use_assigned_date'])
            assigned_to = request.user

            if use_assigned_date:
                date_query = Q(activity_date=ui_utils.get_aware_datetime_from_string(activity_date))
            else:
                date_query = Q(reassigned_activity_date=ui_utils.get_aware_datetime_from_string(activity_date))

            user = BaseUser.objects.get(id=activity_by)

            # they can send all the garbage in activity_type. we need to check if it's valid.
            valid_activity_types = [ac_type[0] for ac_type in INVENTORY_ACTIVITY_TYPES]

            if activity_type not in valid_activity_types:
                return ui_utils.handle_response(class_name,
                                                data=errors.INVALID_ACTIVITY_TYPE_ERROR.format(activity_type))

            # get the required inventory activity assignment instance.
            inventory_activity_assignment_instance = InventoryActivityAssignment.objects.get(
                activity_date=activity_date,
                inventory_activity__shortlisted_inventory_details=shortlisted_inventory_detail_instance,
                inventory_activity__activity_type=activity_type, assigned_to=assigned_to)

            # if it's not superuser and it's not assigned to take the image
            if (not user.is_superuser) and (not inventory_activity_assignment_instance.assigned_to_id == activity_by):
                return ui_utils.handle_response(class_name, data=errors.NO_INVENTORY_ACTIVITY_ASSIGNMENT_ERROR)

            # image path shall be unique
            instance, is_created = InventoryActivityImage.objects.get_or_create(image_path=request.data['image_path'])
            instance.inventory_activity_assignment = inventory_activity_assignment_instance
            instance.comment = request.data['comment']
            instance.actual_activity_date = actual_activity_date
            instance.activity_by = BaseUser.objects.get(id=activity_by)
            instance.latitude = request.data['latitude']
            instance.longitude = request.data['longitude']
            instance.save()

            return ui_utils.handle_response(class_name, data=model_to_dict(instance), success=True)

        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

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
            InventoryActivityImage.objects.get(pk=pk).delete()
            return ui_utils.handle_response(class_name, data=pk, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


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
            proposal = ProposalInfo.objects.get(proposal_id=proposal_id)

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
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


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
            act_types = set()  # to store all act types
            inv_act_assignment_to_image_data_map = {}  # map from tuple to inv act image data
            inv_image_objects = []  # inv act image objects will be stored here for bulk create

            # they can send all the garbage in activity_type. we need to check if it's valid.
            valid_activity_types = [ac_type[0] for ac_type in INVENTORY_ACTIVITY_TYPES]

            # this loop makes inv_act_assignment_to_image_data_map which maps a tuple of sid, act_date, act_type to
            # image data this is required later for creation of inv act image objects.
            image_taken_by = request.user
            inv_image_data = request.data

            # pull out all image paths for these assignment objects
            database_image_paths = InventoryActivityImage.objects.all().values_list('image_path', flat=True)

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
                    return ui_utils.handle_response(class_name, data=errors.INVALID_ACTIVITY_TYPE_ERROR.format(
                        data['activity_type']))

                image_data = {
                    'image_path': data['image_path'],
                    'comment': data['comment'],
                    'activity_by': image_taken_by,
                    'actual_activity_date': data['activity_date'],
                    'latitude': data['latitude'],
                    'longitude': data['longitude']
                }

                try:
                    # these three keys determine unique inventory assignment object for an image object
                    reference = inv_act_assignment_to_image_data_map[
                        shortlisted_inv_id, data['activity_date'], data['activity_type']]
                    reference.append(image_data)
                except KeyError:
                    reference = [image_data]
                    inv_act_assignment_to_image_data_map[
                        shortlisted_inv_id, data['activity_date'], data['activity_type']] = reference

            # i can determine weather all images synced up or not by checking this dict because we are not proceeding further in the
            # above loop if the path is already stored.
            if not inv_act_assignment_to_image_data_map:
                return ui_utils.handle_response(class_name, data=errors.ALL_IMAGES_SYNCED_UP_MESSAGE, success=True)

            # fetch only those objects which have these fields in the list and assigned to the incoming user
            inv_act_assignment_objects = InventoryActivityAssignment.objects. \
                filter(
                inventory_activity__shortlisted_inventory_details__id__in=shortlisted_inv_ids,
                inventory_activity__activity_type__in=act_types,
                activity_date__in=act_dates,
                assigned_to=image_taken_by
            )

            if not inv_act_assignment_objects:
                return ui_utils.handle_response(class_name, data=errors.NO_INVENTORY_ACTIVITY_ASSIGNMENT_ERROR,
                                                request=request)

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
                    image_data["created_at"] = datetime.datetime.now()
                    inv_image_objects.append(InventoryActivityImage(**image_data))

            InventoryActivityImage.objects.bulk_create(inv_image_objects)
            return ui_utils.handle_response(class_name,
                                            data='success. {0} objects created'.format(len(inv_image_objects)),
                                            success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


class InventoryActivityAssignmentAPIView(APIView):
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
            shortlisted_inv_objects_map = ShortlistedInventoryPricingDetails.objects.in_bulk(shortlisted_inv_ids)
            assigned_to_users_objects_map = BaseUser.objects.in_bulk(assigned_to_users_ids)

            # inv_act_assign objects container
            inv_assignment_objects = []

            for data in inv_assign_data:
                shortlisted_inv_id = int(data['shortlisted_inventory_id'])
                assigned_to_user_id = int(data['assigned_to'])

                instance, is_created = InventoryActivityAssignment.objects.get_or_create(
                    shortlisted_inventory_details=shortlisted_inv_objects_map[shortlisted_inv_id],
                    activity_type=data['activity_type'],
                    activity_date=data['activity_date']
                )
                instance.assigned_to = assigned_to_users_objects_map[assigned_to_user_id]
                instance.assigned_by = request.user

                instance.save()
                inv_assignment_objects.append(instance)

            serializer = InventoryActivityAssignmentSerializer(inv_assignment_objects, many=True)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

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
            InventoryActivityAssignment.objects.filter(id=inv_act_assignment_id).update(**data)
            instance = InventoryActivityAssignment.objects.get(id=inv_act_assignment_id)
            return ui_utils.handle_response(class_name, data=model_to_dict(instance), success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    def get(self, request):
        """
        Args:
            request:
        Returns: fetches inv act assignment  object along with the images that are associated
        """
        class_name = self.__class__.__name__
        try:
            inv_act_assignment_id = request.query_params['inventory_activity_assignment_id']
            inventory_activity_assignment_object = InventoryActivityAssignment.objects.get(id=inv_act_assignment_id)
            serializer = InventoryActivityAssignmentSerializerReadOnly(inventory_activity_assignment_object)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


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

            shortlisted_inventory_detail_ids = [int(sipd) for sipd in request.data['shortlisted_inventory_id_detail']]
            assignment_detail = request.data['assignment_detail']

            shortlisted_inventory_detail_map = ShortlistedInventoryPricingDetails.objects.in_bulk(
                shortlisted_inventory_detail_ids)
            # they can send all the garbage in activity_type. we need to check if it's valid.
            valid_activity_types = [ac_type[0] for ac_type in INVENTORY_ACTIVITY_TYPES]

            inventory_activity_objects = InventoryActivity.objects.filter(
                shortlisted_inventory_details__id__in=shortlisted_inventory_detail_ids)
            # to reduce db hits, a map is created for InventoryActivity model where (shortlisted_inventory_detail_id, activity_type)
            # is keyed for inventoryActivity instance
            inventory_activity_objects_map = {}
            for inv_act_instance in inventory_activity_objects:
                try:
                    inventory_activity_objects_map[
                        inv_act_instance.shortlisted_inventory_details_id, inv_act_instance.activity_type]
                except KeyError:
                    inventory_activity_objects_map[
                        inv_act_instance.shortlisted_inventory_details_id, inv_act_instance.activity_type] = inv_act_instance

            # to reduce db hits, all users are stored and queried beforehand.
            users = set()
            for assignment_data in assignment_detail:
                for date, user in assignment_data['date_user_assignments'].items():
                    users.add(int(user))
            user_map = BaseUser.objects.in_bulk(users)
            inventory_activity_assignment_objects = []

            # now assign for each shortlisted inventory detail id
            for shortlisted_inv_detail_id in shortlisted_inventory_detail_ids:
                for assignment_data in assignment_detail:

                    activity_type = assignment_data['activity_type']

                    if activity_type not in valid_activity_types:
                        return ui_utils.handle_response(class_name,
                                                        data=errors.INVALID_ACTIVITY_TYPE_ERROR.format(activity_type))
                    try:
                        inventory_activity_instance = inventory_activity_objects_map[
                            shortlisted_inv_detail_id, activity_type]
                    except KeyError:
                        # only create when above combo is not found
                        inventory_activity_instance, is_created = InventoryActivity.objects.get_or_create(
                            shortlisted_inventory_details=shortlisted_inventory_detail_map[shortlisted_inv_detail_id],
                            activity_type=activity_type
                        )
                    for date, user in assignment_data['date_user_assignments'].items():
                        # if it's AUDIT, you keep on creating objects
                        if inventory_activity_instance.activity_type == INVENTORY_ACTIVITY_TYPES[2][0]:
                            inv_act_assignment, is_created = InventoryActivityAssignment.objects.get_or_create(
                                inventory_activity=inventory_activity_instance,
                                activity_date=ui_utils.get_aware_datetime_from_string(date))
                        else:
                            # if it's Release/Closure, you only create once instance against release.
                            inv_act_assignment, is_created = InventoryActivityAssignment.objects.get_or_create(
                                inventory_activity=inventory_activity_instance)
                            inv_act_assignment.activity_date = ui_utils.get_aware_datetime_from_string(date)

                        inv_act_assignment.assigned_to = user_map[int(user)]
                        inv_act_assignment.assigned_by = request.user
                        inventory_activity_assignment_objects.append(inv_act_assignment)

            bulk_update(inventory_activity_assignment_objects)
            return ui_utils.handle_response(class_name, data='successfully assigned', success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


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
            inventory_activity_assignment_ids = [int(obj_id) for obj_id in data.keys()]
            user_ids = [int(detail['assigned_to']) for detail in data.values()]
            inventory_activity_assignment_map = InventoryActivityAssignment.objects.in_bulk(
                inventory_activity_assignment_ids)
            user_map = BaseUser.objects.in_bulk(user_ids)
            inventory_activity_assignment_objects = []
            for inventory_activity_assignment_id, detail in data.items():
                instance = inventory_activity_assignment_map[int(inventory_activity_assignment_id)]
                instance.reassigned_activity_date = ui_utils.get_aware_datetime_from_string(
                    detail['reassigned_activity_date'])
                instance.assigned_to = user_map[int(detail['assigned_to'])]
                inventory_activity_assignment_objects.append(instance)
            bulk_update(inventory_activity_assignment_objects)
            return ui_utils.handle_response(class_name, data='successfully reassigned', success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


class UploadInventoryActivityImageAmazon(APIView):
    """
    This API first attempts to upload the given image to amazon and saves path in inventory activity image table.
    """

    def post(self, request):
        """
        API to upload inventory activity image amazon
        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            file = request.data['file']
            extension = file.name.split('.')[-1]
            supplier_name = request.data['supplier_name'].replace(' ', '_')
            activity_name = request.data['activity_name']
            activity_date = request.data['activity_date']
            inventory_name = request.data['inventory_name']
            inventory_activity_assignment_id = request.data['inventory_activity_assignment_id']

            inventory_activity_assignment_instance = InventoryActivityAssignment.objects.get(
                pk=inventory_activity_assignment_id)

            file_name = supplier_name + '_' + inventory_name + '_' + activity_name + '_' + activity_date.replace('-',
                                                                                                                 '_') + '_' + str(
                time.time()).replace('.', '_') + '.' + extension
            website_utils.upload_to_amazon(file_name, file_content=file, bucket_name=settings.ANDROID_BUCKET_NAME)

            # Now save the path
            instance, is_created = InventoryActivityImage.objects.get_or_create(image_path=file_name)
            instance.inventory_activity_assignment = inventory_activity_assignment_instance
            instance.actual_activity_date = activity_date
            instance.save()

            return ui_utils.handle_response(class_name, data=file_name, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


class CampaignsAssignedInventoryCountApiView(APIView):
    def get(self, request, organisation_id):
        """

        :param request:
        :param organisation_id:
        :return:
        """
        class_name = self.__class__.__name__
        try:
            user = request.user
            proposal_query = Q(
                inventory_activity__shortlisted_inventory_details__shortlisted_spaces__proposal__campaign_state='PTC')
            proposal_query_images = Q(
                inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__shortlisted_spaces__proposal__campaign_state='PTC')
            accounts = []
            q1 = Q()
            q2 = Q()
            if not request.user.is_superuser:
                category = request.query_params.get('category', None)
                # if category.upper() == v0_constants.category['business']:
                #     q1 = Q(
                #         inventory_activity__shortlisted_inventory_details__shortlisted_spaces__proposal__account__organisation__organisation_id=organisation_id)
                #     q2 = Q(
                #         inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__shortlisted_spaces__proposal__account__organisation__organisation_id=organisation_id)
                # if category.upper() == v0_constants.category['business_agency']:
                #     q1 = Q(inventory_activity__shortlisted_inventory_details__shortlisted_spaces__proposal__user=user)
                #     q2 = Q(
                #         inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__shortlisted_spaces__proposal__user=user)
                # if category.upper() == v0_constants.category['supplier_agency'] or category.upper() == v0_constants.category['machadalo']:
                q1 = Q(
                    inventory_activity__shortlisted_inventory_details__shortlisted_spaces__proposal__campaignassignment__assigned_to=user)
                q2 = Q(
                    inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__shortlisted_spaces__proposal__campaignassignment__assigned_to=user)
            inv_act_assignment_objects = InventoryActivityAssignment.objects. \
                select_related('inventory_activity', 'inventory_activity__shortlisted_inventory_details',
                               'inventory_activity__shortlisted_inventory_details__shortlisted_spaces',
                               'inventory_activity__shortlisted_inventory_details__shortlisted_spaces__proposal',
                               'inventory_activity__shortlisted_inventory_details__shortlisted_spaces__proposal__account'). \
                filter(proposal_query, q1). \
                annotate(activity_type=F('inventory_activity__activity_type'),
                         inventory=F(
                             'inventory_activity__shortlisted_inventory_details__ad_inventory_type__adinventory_name'),
                         ). \
                values('activity_type', 'inventory', 'activity_date'). \
                annotate(total=Count('id')). \
                order_by('-activity_date')
            inv_act_assignment_objects2 = InventoryActivityImage.objects. \
                select_related('inventory_activity_assignment', 'inventory_activity_assignment__inventory_activity',
                               'inventory_activity_assignment__inventory_activity__shortlisted_inventory_details',
                               'inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__shortlisted_spaces',
                               'inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__shortlisted_spaces__proposal',
                               'inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__shortlisted_spaces__proposal__account'). \
                filter(proposal_query_images, q2). \
                annotate(activity_type=F('inventory_activity_assignment__inventory_activity__activity_type'),
                         inventory=F(
                             'inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__ad_inventory_type__adinventory_name'),
                         activity_date=F('inventory_activity_assignment__activity_date'),
                         ). \
                values('activity_type', 'inventory', 'activity_date'). \
                annotate(total=Count('inventory_activity_assignment', distinct=True)). \
                order_by('-activity_date')
            # result = [[item.inventory][item.activity_type][item.activity_date.date()] for item in inv_act_assignment_objects2]
            result = {}
            for item in inv_act_assignment_objects:
                inventory = str(item['inventory'])
                activity_date = str(item['activity_date'].date()) if item['activity_date'] else None
                activity_type = str(item['activity_type'])
                if not result.get(item['inventory']):
                    result[inventory] = {}
                if not result[inventory].get(activity_date):
                    result[inventory][activity_date] = {}
                if not result[inventory][activity_date].get(activity_type):
                    result[inventory][activity_date][activity_type] = {}

                result[inventory][activity_date][activity_type]['total'] = item['total']
                result[inventory][activity_date][activity_type]['actual'] = 0
                # result[item['inventory']][item['activity_type']][item['activity_date']]['actual'] = item['total']
            for item in inv_act_assignment_objects2:
                inventory = str(item['inventory'])
                activity_date = str(item['activity_date'].date()) if item['activity_date'] else None
                activity_type = str(item['activity_type'])

                result[inventory][activity_date][activity_type]['actual'] = item['total']

            return ui_utils.handle_response(class_name, data=result, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


class CampaignInventoryAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            campaign = Campaign.objects.get(pk=id)
            campaign_serializer = CampaignListSerializer(campaign)
            items = campaign.societies.all().filter(
                booking_status__in=['Shortlisted', 'Requested', 'Finalized', 'Removed'])
            serializer = CampaignInventorySerializer(items, many=True)
            response = {'inventories': serializer.data, 'campaign': campaign_serializer.data}
            return Response(response, status=200)
        except:
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
                    serializer = CampaignSocietyMappingSerializer(campaign_society, data=society)
                else:
                    # request.data['created_by'] = current_user.id
                    serializer = CampaignSocietyMappingSerializer(data=society)

                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=400)

                for inv in society['inventories']:
                    if 'id' in inv:
                        society_inv = SocietyInventoryBooking.objects.get(pk=inv['id'])
                        serializer = SocietyInventoryBookingSerializer(society_inv, data=inv)
                    else:
                        serializer = SocietyInventoryBookingSerializer(data=inv)

                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return Response(serializer.errors, status=400)

            save_type = request.data['type']
            if save_type and save_type == 'submit':
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
            return Response({'message': 'Requested Inventory Does not Exist'}, status=404)

        if type and (type == 'Permanent'):
            inventories = SocietyInventoryBooking.objects.filter(campaign=item.campaign, society=item.society)
            for key in inventories:
                key.delete()
            item.delete()
        elif type and (type == 'Temporary'):
            item.booking_status = 'Removed'
            item.save()
        else:
            return Response({'message': 'Specify a correct type/mode of deletion'}, status=400)

        return Response(status=200)
