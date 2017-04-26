import random

from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.apps import apps
import django.apps
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Permission, Group
from django.forms import model_to_dict
from django.conf import settings
from bulk_update.helper import bulk_update


from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets

from v0.serializers import BannerInventorySerializer, CommunityHallInfoSerializer, DoorToDoorInfoSerializer, LiftDetailsSerializer, NoticeBoardDetailsSerializer, PosterInventorySerializer, SocietyFlatSerializer, StandeeInventorySerializer, SwimmingPoolInfoSerializer, WallInventorySerializer, UserInquirySerializer, CommonAreaDetailsSerializer, ContactDetailsSerializer, EventsSerializer, InventoryInfoSerializer, MailboxInfoSerializer, OperationsInfoSerializer, PoleInventorySerializer, PosterInventoryMappingSerializer, RatioDetailsSerializer, SignupSerializer, StallInventorySerializer, StreetFurnitureSerializer, SupplierInfoSerializer, SupplierTypeSocietySerializer, SocietyTowerSerializer, CityAreaSerializer, ContactDetailsGenericSerializer, FlatTypeSerializer, PermissionSerializer, BusinessTypeSubTypeReadOnlySerializer, GroupSerializer, BaseUserSerializer, BaseUserUpdateSerializer
from rest_framework.decorators import detail_route, list_route
from v0.models import BannerInventory, CommunityHallInfo, DoorToDoorInfo, LiftDetails, NoticeBoardDetails, PosterInventory, SocietyFlat, StandeeInventory, SwimmingPoolInfo, WallInventory, UserInquiry, CommonAreaDetails, ContactDetails, Events, InventoryInfo, MailboxInfo, OperationsInfo, PoleInventory, PosterInventoryMapping, RatioDetails, Signup, StallInventory, StreetFurniture, SupplierInfo, SupplierTypeSociety, SocietyTower, CityArea, ContactDetailsGeneric, SupplierTypeCorporate, FlatType, BaseUser, CustomPermissions, BusinessTypes, BusinessSubTypes, AdInventoryType, DurationType, \
    Amenity, SupplierAmenitiesMap
from v0.models import AD_INVENTORY_CHOICES
import utils as v0_utils
from constants import model_names
import v0.ui.utils as ui_utils
import errors
import v0.ui.website.constants as website_constants
import constants as v0_constants
import v0.ui.website.utils as website_utils


class PopulateContentTypeFields(APIView):
    """
    This API is written to populate existing content type fields for models who are mapped to
    supplier type table. example supplier_type_society table.
    """

    def post(self, request):
        """
        Args:
            request: request params

        Returns: success in case populating content type fields succeeds, error if fails
        ---
        parameters:
        - name: supplier_model_name
          description: example 'SupplierTypeSociety'. The name of the supplier model which exists as a FK into the model for which you want to populate content types

        """
        class_name = self.__class__.__name__

        supplier_model_name = request.data.get('supplier_model_name')
        if not supplier_model_name:
            return Response({'status': False, 'error': 'Please provide supplier model name'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            supplier_model = apps.get_model('v0', supplier_model_name)
            load_names = [apps.get_model('v0', model) for model in model_names]
            ContentType = apps.get_model('contenttypes', 'ContentType')
            content_type = ContentType.objects.get(model=supplier_model_name)
            for name in load_names:
                response = v0_utils.do_each_model(name, supplier_model, content_type)
                if not response.data['status']:
                    return response
            return ui_utils.handle_response(class_name, data='success', success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

class SetUserToMasterUser(APIView):
    """
    The api sets user_id field to master user if any in the database.
    Careful before using it because it will update user field of all the rows to master 
    user which may not be what you want everytime. 
    """
    permission_classes = (permissions.IsAuthenticated, )
    def post(self, request):
        class_name = self.__class__.__name__
        try:
            master_user = BaseUser.objects.get(id=1)
            # get all models from the app 'v0' 
            all_models = apps.get_app_config('v0').models
            # exclude these models 
            models_to_exclude = [BaseUser, CustomPermissions]
            # run for each model and update all records 
            for model in all_models.values():
                if hasattr(model, 'user') and model not in models_to_exclude:
                    model.objects.all().update(user=master_user)
            return ui_utils.handle_response(class_name, data='succesfully updated all users of all modes to master user', success=True)        
        except ObjectDoesNotExist as e:
          return ui_utils.handle_response(class_name, exception_object=e)            
        except Exception as e:
          return ui_utils.handle_response(class_name, exception_object=e)

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


'''class CarDisplayInventoryAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = CarDisplayInventory.objects.get(pk=id)
            serializer = CarDisplayInventorySerializer(item)
            return Response(serializer.data)
        except CarDisplayInventory.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = CarDisplayInventory.objects.get(pk=id)
        except CarDisplayInventory.DoesNotExist:
            return Response(status=404)
        serializer = CarDisplayInventorySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = CarDisplayInventory.objects.get(pk=id)
        except CarDisplayInventory.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class CarDisplayInventoryAPIListView(APIView):

    def get(self, request, format=None):
        items = CarDisplayInventory.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = CarDisplayInventorySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = CarDisplayInventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)'''


class CommunityHallInfoAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = CommunityHallInfo.objects.get(pk=id)
            serializer = CommunityHallInfoSerializer(item)
            return Response(serializer.data)
        except CommunityHallInfo.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = CommunityHallInfo.objects.get(pk=id)
        except CommunityHallInfo.DoesNotExist:
            return Response(status=404)
        serializer = CommunityHallInfoSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = CommunityHallInfo.objects.get(pk=id)
        except CommunityHallInfo.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class CommunityHallInfoAPIListView(APIView):

    def get(self, request, format=None):
        items = CommunityHallInfo.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = CommunityHallInfoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = CommunityHallInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class DoorToDoorInfoAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = DoorToDoorInfo.objects.get(pk=id)
            serializer = DoorToDoorInfoSerializer(item)
            return Response(serializer.data)
        except DoorToDoorInfo.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = DoorToDoorInfo.objects.get(pk=id)
        except DoorToDoorInfo.DoesNotExist:
            return Response(status=404)
        serializer = DoorToDoorInfoSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = DoorToDoorInfo.objects.get(pk=id)
        except DoorToDoorInfo.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class DoorToDoorInfoAPIListView(APIView):

    def get(self, request, format=None):
        items = DoorToDoorInfo.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = DoorToDoorInfoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = DoorToDoorInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class LiftDetailsAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = LiftDetails.objects.get(pk=id)
            serializer = LiftDetailsSerializer(item)
            return Response(serializer.data)
        except LiftDetails.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = LiftDetails.objects.get(pk=id)
        except LiftDetails.DoesNotExist:
            return Response(status=404)
        serializer = LiftDetailsSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = LiftDetails.objects.get(pk=id)
        except LiftDetails.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class LiftDetailsAPIListView(APIView):

    def get(self, request, format=None):
        items = LiftDetails.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = LiftDetailsSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = LiftDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class NoticeBoardDetailsAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = NoticeBoardDetails.objects.get(pk=id)
            serializer = NoticeBoardDetailsSerializer(item)
            return Response(serializer.data)
        except NoticeBoardDetails.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = NoticeBoardDetails.objects.get(pk=id)
        except NoticeBoardDetails.DoesNotExist:
            return Response(status=404)
        serializer = NoticeBoardDetailsSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = NoticeBoardDetails.objects.get(pk=id)
        except NoticeBoardDetails.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class NoticeBoardDetailsAPIListView(APIView):

    def get(self, request, format=None):
        items = NoticeBoardDetails.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = NoticeBoardDetailsSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = NoticeBoardDetailsSerializer(data=request.data)
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


class SocietyFlatAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = SocietyFlat.objects.get(pk=id)
            serializer = SocietyFlatSerializer(item)
            return Response(serializer.data)
        except SocietyFlat.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = SocietyFlat.objects.get(pk=id)
        except SocietyFlat.DoesNotExist:
            return Response(status=404)
        serializer = SocietyFlatSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = SocietyFlat.objects.get(pk=id)
        except SocietyFlat.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class SocietyFlatAPIListView(APIView):

    def get(self, request, format=None):
        items = SocietyFlat.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = SocietyFlatSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = SocietyFlatSerializer(data=request.data)
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


class SwimmingPoolInfoAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = SwimmingPoolInfo.objects.get(pk=id)
            serializer = SwimmingPoolInfoSerializer(item)
            return Response(serializer.data)
        except SwimmingPoolInfo.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = SwimmingPoolInfo.objects.get(pk=id)
        except SwimmingPoolInfo.DoesNotExist:
            return Response(status=404)
        serializer = SwimmingPoolInfoSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = SwimmingPoolInfo.objects.get(pk=id)
        except SwimmingPoolInfo.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class SwimmingPoolInfoAPIListView(APIView):

    def get(self, request, format=None):
        items = SwimmingPoolInfo.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = SwimmingPoolInfoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = SwimmingPoolInfoSerializer(data=request.data)
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


class UserInquiryAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = UserInquiry.objects.get(pk=id)
            serializer = UserInquirySerializer(item)
            return Response(serializer.data)
        except UserInquiry.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = UserInquiry.objects.get(pk=id)
        except UserInquiry.DoesNotExist:
            return Response(status=404)
        serializer = UserInquirySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = UserInquiry.objects.get(pk=id)
        except UserInquiry.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class UserInquiryAPIListView(APIView):

    def get(self, request, format=None):
        items = UserInquiry.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = UserInquirySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = UserInquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CommonAreaDetailsAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = CommonAreaDetails.objects.get(pk=id)
            serializer = CommonAreaDetailsSerializer(item)
            return Response(serializer.data)
        except CommonAreaDetails.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = CommonAreaDetails.objects.get(pk=id)
        except CommonAreaDetails.DoesNotExist:
            return Response(status=404)
        serializer = CommonAreaDetailsSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = CommonAreaDetails.objects.get(pk=id)
        except CommonAreaDetails.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class CommonAreaDetailsAPIListView(APIView):

    def get(self, request, format=None):
        items = CommonAreaDetails.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = CommonAreaDetailsSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = CommonAreaDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ContactDetailsAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = ContactDetails.objects.get(pk=id)
            serializer = ContactDetailsSerializer(item)
            return Response(serializer.data)
        except ContactDetails.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = ContactDetails.objects.get(pk=id)
        except ContactDetails.DoesNotExist:
            return Response(status=404)
        serializer = ContactDetailsSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = ContactDetails.objects.get(pk=id)
        except ContactDetails.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class ContactDetailsAPIListView(APIView):

    def get(self, request, format=None):
        items = ContactDetails.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = ContactDetailsSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = ContactDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class EventsAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = Events.objects.get(pk=id)
            serializer = EventsSerializer(item)
            return Response(serializer.data)
        except Events.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = Events.objects.get(pk=id)
        except Events.DoesNotExist:
            return Response(status=404)
        serializer = EventsSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = Events.objects.get(pk=id)
        except Events.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class EventsAPIListView(APIView):

    def get(self, request, format=None):
        items = Events.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = EventsSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = EventsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


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


class MailboxInfoAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = MailboxInfo.objects.get(pk=id)
            serializer = MailboxInfoSerializer(item)
            return Response(serializer.data)
        except MailboxInfo.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = MailboxInfo.objects.get(pk=id)
        except MailboxInfo.DoesNotExist:
            return Response(status=404)
        serializer = MailboxInfoSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = MailboxInfo.objects.get(pk=id)
        except MailboxInfo.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class MailboxInfoAPIListView(APIView):
    def get(self, request, format=None):
        items = MailboxInfo.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = MailboxInfoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = MailboxInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class OperationsInfoAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = OperationsInfo.objects.get(pk=id)
            serializer = OperationsInfoSerializer(item)
            return Response(serializer.data)
        except OperationsInfo.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = OperationsInfo.objects.get(pk=id)
        except OperationsInfo.DoesNotExist:
            return Response(status=404)
        serializer = OperationsInfoSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = OperationsInfo.objects.get(pk=id)
        except OperationsInfo.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class OperationsInfoAPIListView(APIView):

    def get(self, request, format=None):
        items = OperationsInfo.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = OperationsInfoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = OperationsInfoSerializer(data=request.data)
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


class RatioDetailsAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = RatioDetails.objects.get(pk=id)
            serializer = RatioDetailsSerializer(item)
            return Response(serializer.data)
        except RatioDetails.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = RatioDetails.objects.get(pk=id)
        except RatioDetails.DoesNotExist:
            return Response(status=404)
        serializer = RatioDetailsSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = RatioDetails.objects.get(pk=id)
        except RatioDetails.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class RatioDetailsAPIListView(APIView):

    def get(self, request, format=None):
        items = RatioDetails.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = RatioDetailsSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = RatioDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class SignupAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = Signup.objects.get(pk=id)
            serializer = SignupSerializer(item)
            return Response(serializer.data)
        except Signup.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = Signup.objects.get(pk=id)
        except Signup.DoesNotExist:
            return Response(status=404)
        serializer = SignupSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = Signup.objects.get(pk=id)
        except Signup.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class SignupAPIListView(APIView):

    def get(self, request, format=None):
        items = Signup.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = SignupSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = SignupSerializer(data=request.data)
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


class SupplierInfoAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = SupplierInfo.objects.get(pk=id)
            serializer = SupplierInfoSerializer(item)
            return Response(serializer.data)
        except SupplierInfo.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = SupplierInfo.objects.get(pk=id)
        except SupplierInfo.DoesNotExist:
            return Response(status=404)
        serializer = SupplierInfoSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = SupplierInfo.objects.get(pk=id)
        except SupplierInfo.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class SupplierInfoAPIListView(APIView):

    def get(self, request, format=None):
        items = SupplierInfo.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = SupplierInfoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = SupplierInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class SupplierTypeSocietyAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = SupplierTypeSociety.objects.get(pk=id)
            serializer = SupplierTypeSocietySerializer(item)
            return Response(serializer.data)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = SupplierTypeSociety.objects.get(pk=id)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        serializer = SupplierTypeSocietySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = SupplierTypeSociety.objects.get(pk=id)
        except SupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class SupplierTypeSocietyAPIListView(APIView):

    def get(self, request, format=None):
        items = SupplierTypeSociety.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = SupplierTypeSocietySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        """
        Args:
            request: request param containg society data
            format: none

        Returns: The data created by this particular user
        """
        serializer = SupplierTypeSocietySerializer(data=request.data)
        current_user = request.user
        if serializer.is_valid():
            serializer.save(created_by=current_user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class SocietyTowerAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = SocietyTower.objects.get(pk=id)
            serializer = SocietyTowerSerializer(item)
            return Response(serializer.data)
        except SocietyTower.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = SocietyTower.objects.get(pk=id)
        except SocietyTower.DoesNotExist:
            return Response(status=404)
        serializer = SocietyTowerSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = SocietyTower.objects.get(pk=id)
        except SocietyTower.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class SocietyTowerAPIListView(APIView):

    def get(self, request, format=None):
        items = SocietyTower.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = SocietyTowerSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = SocietyTowerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class FlatTypeAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = FlatType.objects.get(pk=id)
            serializer = FlatTypeSerializer(item)
            return Response(serializer.data)
        except FlatType.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = FlatType.objects.get(pk=id)
        except FlatType.DoesNotExist:
            return Response(status=404)
        serializer = FlatTypeSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = FlatType.objects.get(pk=id)
        except FlatType.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class FlatTypeAPIListView(APIView):

    def get(self, request, format=None):
        items = FlatType.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = FlatTypeSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = FlatTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class SocietyAPIFiltersView(APIView):

     def get(self, request, format=None):
        try:
            item = CityArea.objects.all()
            serializer = CityAreaSerializer(item)
            return Response(serializer.data)
        except StallInventory.DoesNotExist:
            return Response(status=404)


class PermissionsViewSet(viewsets.ViewSet):
    """
    A View Set over Permissions. An Internal API.

    """

    def list(self, request):
        """
        Lists all permissions
        Args:
            request:
        Returns: all permissions

        """
        class_name = self.__class__.__name__
        try:
            queryset = Permission.objects.all()
            serializer = PermissionSerializer(queryset, many=True)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    def retrieve(self, request, pk=None):
        """
        Fetches a single Permission
        Args:
            request:
            pk: primary key of Permission model

        Returns:

        """
        class_name = self.__class__.__name__

        try:
            permission = Permission.objects.get(pk=pk)
            serializer = PermissionSerializer(permission)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    def create(self, request):
        """
        Creates a permission instance

        Args:
            request:

        Returns:
        """
        class_name = self.__class__.__name__
        try:
            codename = request.data['codename']
            name = request.data['name']
            content_type_id = request.data['content_type_id']
            content_type = ContentType.objects.get(pk=content_type_id)
            permission = Permission.objects.create(codename=codename, name=name, content_type=content_type)
            return ui_utils.handle_response(class_name, data=model_to_dict(permission), success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    def update(self, request, pk=None):
        """
        updates a single instance of Permission
        Args:
            request:

        Returns: updated instance of Permission model
        """
        class_name = self.__class__.__name__

        try:
            Permission.objects.filter(pk=pk).update(**request.data)
            permission = Permission.objects.get(pk=pk)
            serializer = PermissionSerializer(permission)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    def destroy(self, request, pk=None):
        """
        Deletes a  permission object
        Args:
            request:
            pk:

        Returns:

        """
        class_name = self.__class__.__name__
        try:
            Permission.objects.get(pk=pk).delete()
            return ui_utils.handle_response(class_name, data='successfully deleted {0}'.format(pk),  success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    @detail_route(methods=['post'])
    def assign_permission(self, request, pk=None):
        """
        Args:
            request: contains user_id

        Returns: success in case permission is assigned to a user

        """
        class_name = self.__class__.__name__
        try:
            user_id = request.data['user_id']
            permission = Permission.objects.get(pk=pk)
            user = BaseUser.objects.get(id=user_id)
            user.user_permissions.add(permission)
            return ui_utils.handle_response(class_name, data='Permission added successfully', success=True)

        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    @list_route(methods=['GET'])
    def get_user_permissions(self, request):
        """
        fetches all permission assigned ever to a user
        Args:
            request:

        Returns:

        """
        class_name = self.__class__.__class__
        try:
            user_id = request.query_params['user_id']
            user = BaseUser.objects.get(id=user_id)
            user_permissions = user.user_permissions.all()
            serializer = PermissionSerializer(user_permissions, many=True)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    @detail_route(methods=['POST'])
    def remove_user_permission(self, request, pk=None):
        """
        removes a permission of a user
        Args:
            request: contains user_id

        Returns: 'success in case permission is removed
        """
        class_name = self.__class__.__name__
        try:
            user_id = request.data['user_id']
            user = BaseUser.objects.get(pk=user_id)
            permission = Permission.objects.get(pk=pk)
            user.user_permissions.remove(permission)
            return ui_utils.handle_response(class_name, data='success', success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    @list_route(methods=['POST'])
    def remove_all_user_permissions(self, request):
        """
        removes all permissions of a user
        Args:
            request: contains user_id

        Returns:

        """
        class_name = self.__class__.__name__
        try:
            user_id = request.data['user_id']
            user = BaseUser.objects.get(pk=user_id)
            user.user_permissions.clear()
            return ui_utils.handle_response(class_name, data='success', success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class CreateSocietyTestData(APIView):
    """
    This is an API which creates 10 sample societies. it adds following information
    the various inventories allowed in each society
    and cost of each inventory for specific time.
    It adds what kinds of flats are available in each society.
    adds society type.
    adds society size.
    adds society location rating.
    adds flat average rental per square fit.
    adds flat sale cost per sqft.
    adds number of tenants and number of total flats for each society
    adds possession year
    adds amenities
    make sure some societies are standalone.
    """

    def post(self, request):
        class_name = self.__class__.__name__
        """
        Creates random N societies over M centers.  Useful for testing the front end with low data volume.
        Args:
            request:
        Returns:
        """
        try:
            city_name = request.data['city_name']
            radius = float(request.data['radius'])
            city_code = request.data['city_code']
            centers = request.data['centers']
            total_society_count = int(request.data['society_count'])
            society_detail = request.data.get('society_detail')
            default_database_name = settings.DATABASES['default']['NAME']
            result = {}
            society_list = []

            if default_database_name != v0_constants.database_name:
                return ui_utils.handle_response(class_name, data=errors.INCORRECT_DATABASE_NAME_ERROR.format(default_database_name, v0_constants.database_name))
            # make the list of addresses by combining city name with center names
            addresses = [city_name + ',' + center_name for center_name in centers]
            SupplierTypeSociety.objects.all().delete()  # delete all societies before proceeding
            society_count = total_society_count/len(addresses)  # societies per address
            coordinates = []
            for address in addresses:
                geo_code_instance = v0_utils.get_geo_code_instance(address)
                if not geo_code_instance:
                    return ui_utils.handle_response(class_name, data=errors.NO_GEOCODE_INSTANCE_FOUND.format(address))
                location_lat, location_long = geo_code_instance.latlng
                # location_lat, location_long are coordinates of origin.
                if society_count < 4:
                    coordinates = v0_utils.generate_coordinates_in_quadrant(society_count, location_lat, location_long, radius)
                else:
                    society_per_quadrant = society_count/4
                    remainder = society_count % 4
                    coordinates.extend(v0_utils.generate_coordinates_in_quadrant(society_per_quadrant, location_lat, location_long, radius, v0_constants.first_quadrant_code))
                    coordinates.extend(v0_utils.generate_coordinates_in_quadrant(society_per_quadrant, location_lat, location_long, radius, v0_constants.second_quadrant_code))
                    coordinates.extend(v0_utils.generate_coordinates_in_quadrant(society_per_quadrant, location_lat, location_long, radius, v0_constants.third_quadrant_code))
                    coordinates.extend(v0_utils.generate_coordinates_in_quadrant(society_per_quadrant + remainder, location_lat, location_long, radius, v0_constants.fourth_quadrant_code))
                result[address] = society_count

            suppliers_dict = v0_utils.assign_supplier_ids(city_code, website_constants.society, coordinates)

            for society_id, detail in suppliers_dict.iteritems():
                detail['supplier_id'] = society_id
                detail['society_latitude'] = detail['latitude']
                detail['society_longitude'] = detail['longitude']
                detail['society_name'] = society_id
                del detail['latitude']
                del detail['longitude']
                society_list.append(SupplierTypeSociety(**detail))
            SupplierTypeSociety.objects.bulk_create(society_list)
            v0_utils.handle_society_detail(suppliers_dict, society_detail)
            result['total_count'] = len(society_list)
            return ui_utils.handle_response(class_name, data=result, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class CreateBusinessTypeSubType(APIView):
    """
    Creates BusinessType and their SubTypes in the System. Deletes Previous, if any.
    """

    def post(self, request):
        """
        API to create Business Type and SubTypes
        The SubType Instances cannot be collected at the time of collecting Type instances because SubTypes depend on respective
        Type instances. Hence first we create Type instances and then create SubType instances.
        Args:
            request: JSON for business type and subtypes

        Returns: The created instances

        """
        class_name = self.__class__.__name__
        try:
            default_database_name = settings.DATABASES['default']['NAME']

            if default_database_name != v0_constants.database_name:
                return ui_utils.handle_response(class_name, data=errors.INCORRECT_DATABASE_NAME_ERROR.format(default_database_name, v0_constants.database_name))

            business_type_instances = []  # to store actual objects of BusinessType
            business_sub_type_data = []  # to store data in list of dict form for BusinessSubType
            business_type_code_list = []  # to store list of all codes of BusinessType. Later used to fetch objects of BusinessType
            business_sub_type_instances = []  # to store actual instances of BusinessSubType.

            for business_type, detail in request.data.iteritems():

                business_type_code = detail['code']
                business_type_code_list.append(business_type_code)

                business_type_instances.append(BusinessTypes(business_type=business_type, business_type_code=business_type_code))
                for sub_type_dict in detail['subtypes']:
                    data = {
                        'business_sub_type': sub_type_dict['name'],
                        'business_sub_type_code': sub_type_dict['code'],
                        'business_type_code': business_type_code
                    }
                    business_sub_type_data.append(data)

            # create Type instances here
            BusinessTypes.objects.all().delete()
            BusinessTypes.objects.bulk_create(business_type_instances)
            business_type_instances = BusinessTypes.objects.filter(business_type_code__in=business_type_code_list)
            # map from code to type instances so that we can fetch type instance from knowing the code itself.
            business_type_instances_map = {instance.business_type_code: instance for instance in business_type_instances}

            # now create SubType instances
            for sub_type_data in business_sub_type_data:
                sub_type_data['business_type'] = business_type_instances_map[sub_type_data['business_type_code']]
                del sub_type_data['business_type_code']
                business_sub_type_instances.append(BusinessSubTypes(**sub_type_data))
            BusinessSubTypes.objects.all().delete()
            BusinessSubTypes.objects.bulk_create(business_sub_type_instances)
            serializer = BusinessTypeSubTypeReadOnlySerializer(business_type_instances, many=True)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


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
                return ui_utils.handle_response(class_name, data=errors.INCORRECT_DATABASE_NAME_ERROR.format(default_database_name, v0_constants.database_name))

            # for simplicity i have every combination
            for duration_code, duration_value in website_constants.duration_dict.iteritems():
                DurationType.objects.get_or_create(duration_name=duration_value)
            for inventory_tuple in AD_INVENTORY_CHOICES:
                for ad_inventory_type_code, ad_inventory_type_value in website_constants.type_dict.iteritems():
                    AdInventoryType.objects.get_or_create(adinventory_name=inventory_tuple[0], adinventory_type=ad_inventory_type_value)
            return ui_utils.handle_response(class_name, data='success', success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


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
                return ui_utils.handle_response(class_name, data=errors.INCORRECT_DATABASE_NAME_ERROR.format(default_database_name, v0_constants.database_name))

            inventory_detail = request.data['inventory_detail']
            suppliers = SupplierTypeSociety.objects.all().values_list('supplier_id', flat=True)
            if not suppliers:
                raise Exception("NO societies in the database yet. Add them first and then hit this API.")
            response = ui_utils.get_content_type(website_constants.society)
            if not response.data['status']:
                return response
            content_type = response.data['data']
            v0_utils.handle_supplier_inventory_detail(inventory_detail, suppliers, content_type)
            return ui_utils.handle_response(class_name, data='success', success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class SetInventoryPricing(APIView):
    """
    sets prices to various inventories assigned
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
                return ui_utils.handle_response(class_name, data=errors.INCORRECT_DATABASE_NAME_ERROR.format(default_database_name, v0_constants.database_name))

            supplier_ids = SupplierTypeSociety.objects.all().values_list('supplier_id', flat=True)
            response = ui_utils.get_content_type(website_constants.society)
            if not response.data['status']:
                return response
            content_type = response.data['data']
            v0_utils.handle_inventory_pricing(supplier_ids, content_type, request.data)
            return ui_utils.handle_response(class_name, data='success', success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class PopulateAmenities(APIView):
    """
    randomly assigns amenities to random suppliers
    """
    def post(self, request):
        """
        Args:
            request: requires  { 'amenity_data': { 'code': "GY", 'name' : "GYM" }, 'supplier_type_code': "RS" }
        Returns: creates amenities in the system given in amenity_data and assigns each supplier a random set of amenities between 0 and total amenity count

        """
        class_name = self.__class__.__name__
        try:
            default_database_name = settings.DATABASES['default']['NAME']

            if default_database_name != v0_constants.database_name:
                return ui_utils.handle_response(class_name, data=errors.INCORRECT_DATABASE_NAME_ERROR.format(default_database_name, v0_constants.database_name))

            supplier_type_code = request.data['supplier_type_code']
            content_type = ui_utils.fetch_content_type(supplier_type_code)
            supplier_model = apps.get_model(settings.APP_NAME, content_type.model)
            # make amenities only if amenity_data is provided
            if request.data.get('amenity_data'):

                amenity_data = request.data['amenity_data']

                amenity_instances = []
                for code, name in amenity_data.iteritems():
                    amenity_instances.append(Amenity(**{'code': code, 'name': name}))

                Amenity.objects.all().delete()
                Amenity.objects.bulk_create(amenity_instances)

            amenity_instances = list(Amenity.objects.all())
            amenity_instance_count = len(amenity_instances)

            supplier_ids = supplier_model.objects.all().values_list('supplier_id', flat=True)
            supplier_amenity_instances = []

            for supplier_id in supplier_ids:
                count_of_amenity_to_be_assigned = random.randint(0, amenity_instance_count) # assign anywhere between zero to max amenity count
                for sub_index in range(count_of_amenity_to_be_assigned):
                    amenity = amenity_instances[sub_index]
                    supplier_amenity_instances.append(SupplierAmenitiesMap(content_type=content_type, amenity=amenity, object_id=supplier_id))

            SupplierAmenitiesMap.objects.all().delete()
            SupplierAmenitiesMap.objects.bulk_create(supplier_amenity_instances)

            return ui_utils.handle_response(class_name, data='success', success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class UserViewSet(viewsets.ViewSet):
    """
    A View set for handling all the user related logic
    """
    authentication_classes = []
    permission_classes = []

    def retrieve(self, request, pk=None):
        """
        The API is only used to fetch one User object by user id.
        Args:
            request: The request body
            pk: The pk of BaseUser table

        Returns: a User object
        """
        class_name = self.__class__.__name__
        try:
            user = BaseUser.objects.get(pk=pk)
            serializer = BaseUserSerializer(user)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except ObjectDoesNotExist as e:
            return ui_utils.handle_response(class_name, data=pk, exception_object=e)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    def update(self, request, pk=None):
        """
        API used to update one single user. The API does not update a password for a user, though you have to
        provide password in the request body. There is a separate api for updating password of the user.
        Args:
            request: A request body
            pk: pk value

        Returns: updated one object

        """
        class_name = self.__class__.__name__
        try:
            user = BaseUser.objects.get(pk=pk)            
            groups = Group.objects.filter(name__in=request.data.get('groups'))
            serializer = BaseUserUpdateSerializer(user, data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                for instance in groups:
                    user.groups.add(instance)
                return ui_utils.handle_response(class_name, data=serializer.data, success=True)
            return ui_utils.handle_response(class_name, data=serializer.errors)
        except ObjectDoesNotExist as e:
            return ui_utils.handle_response(class_name, data=pk, exception_object=e)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    def create(self, request):
        """
        Create one single user
        Args:
            request:  Request body

        Returns: created user
        """
        class_name = self.__class__.__name__
        try:
            # fetch all groups objects
            group_instances = Group.objects.filter(name__in=request.data.get('groups'))
            serializer = BaseUserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                for instance in group_instances:
                    user.groups.add(instance)
                return ui_utils.handle_response(class_name, data=serializer.data, success=True)
            return ui_utils.handle_response(class_name, data=serializer.errors)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    def list(self, request):
        """
        list all users in the system
        Args:
            request: The request body

        Returns: list all users

        """
        class_name = self.__class__.__name__
        try:
            users = BaseUser.objects.all()
            serializer = BaseUserSerializer(users, many=True)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    def destroy(self, request, pk=None):
        """
        Deletes a single user
        Args:
            request: The Request body
            pk: pk value

        Returns: pk of object which got deleted

        """
        class_name = self.__class__.__name__
        try:
            BaseUser.objects.get(pk=pk).delete()
            return ui_utils.handle_response(class_name, data=pk, success=True)
        except ObjectDoesNotExist as e:
            return ui_utils.handle_response(class_name, data=pk, exception_object=e)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    @detail_route(methods=['POST'])
    def change_password(self, request, pk=None):
        """
        This API must be used only to change password of the user.
        Args:
            request: Request method
            pk: pk value
        Returns: changes the password of the BaseUser instance and returns a success message

        """
        class_name = self.__class__.__name__
        try:
            user = BaseUser.objects.get(pk=pk)
            new_password = request.data['password']
            user.set_password(new_password)
            user.save()
            return ui_utils.handle_response(class_name, data='password changed successfully', success=True)
        except ObjectDoesNotExist as e:
            return ui_utils.handle_response(class_name, data=pk, exception_object=e)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class GroupViewSet(viewsets.ViewSet):
    """
    View set around groups
    """
    def list(self, request):
        """
        Lists all the groups
        Args:
            request:

        Returns:

        """
        class_name = self.__class__.__name__
        try:
            groups = Group.objects.all()
            serializer = GroupSerializer(groups, many=True)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    def retrieve(self, request, pk=None):
        """

        Args:
            request:
            pk:

        Returns:

        """
        class_name = self.__class__.__name__
        try:
            group = Group.objects.get(pk=pk)
            serializer = GroupSerializer(group)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except ObjectDoesNotExist as e:
            return ui_utils.handle_response(class_name, data=pk, exception_object=e)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    def update(self, request, pk=None):
        """

        Args:
            request:
            pk:

        Returns:

        """
        class_name = self.__class__.__name__
        try:
            group = Group.objects.get(pk=pk)
            serializer = GroupSerializer(group, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return ui_utils.handle_response(class_name, data=serializer.data, success=True)
            return ui_utils.handle_response(class_name, data=serializer.errors)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    def create(self, request):
        """

        Args:
            request:

        Returns:

        """
        class_name = self.__class__.__name__
        try:
            # fetch all groups objects
            serializer = GroupSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return ui_utils.handle_response(class_name, data=serializer.data, success=True)
            return ui_utils.handle_response(class_name, data=serializer.errors)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)

    def destroy(self, request, pk=None):
        """
        Deletes a single group
        Args:
            request: The Request body
            pk: pk value

        Returns: pk of object which got deleted

        """
        class_name = self.__class__.__name__
        try:
            Group.objects.get(pk=pk).delete()
            return ui_utils.handle_response(class_name, data=pk, success=True)
        except ObjectDoesNotExist as e:
            return ui_utils.handle_response(class_name, data=pk, exception_object=e)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class GuestUser(APIView):
    """
    creates a guest user with the details. The reason this api is written despite having a UserViewSet to manage users is
    that, the post api will get or create user from username field. The ViewSet does not return the password. but we need
    to in case of guest user.
    """
    authentication_classes = []  # we do not need authentication in this case
    permission_classes = []  # we do not need authentication in this case

    def post(self, request):
        """
        POST api creates a guest user. All guest users have code 99. The random password is also returned which makes possible
        to authenticate this user later
        """
        class_name = self.__class__.__name__
        try:
            username = request.data['username']
            mobile = request.data['mobile']
            first_name = request.data['first_name']
            user, is_created = BaseUser.objects.get_or_create(username=username)
            password = website_utils.get_random_pattern()
            user.set_password(password)
            user.mobile = mobile
            user.first_name = first_name
            user.user_code = v0_constants.guest_user_code
            user.save()
            data = {
                'id': user.id,
                'first_name': user.first_name,
                'mobile': user.mobile,
                'user_code': user.user_code,
                'password': password,
                'username': user.username
            }
            return ui_utils.handle_response(class_name, data=data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)


class SetParams(APIView):
    """
    updates societies  fields and sets correct values for built_up area for flats.

    """

    def get(self, request):
        """

        Args:
            request:

        Returns:

        """
        class_name = self.__class__.__name__
        try:
            all_societies = SupplierTypeSociety.objects.all()
            supplier_ids = [supplier.supplier_id for supplier in all_societies]
            supplier_map = {supplier_instance.supplier_id: supplier_instance for supplier_instance in all_societies}
            content_type = ui_utils.fetch_content_type('RS')
            flat_objects = FlatType.objects.filter(object_id__in=supplier_ids, content_type=content_type)

            result = {}
            for flat_instance in flat_objects:
                supplier_id = flat_instance.object_id
                flat_type = flat_instance.flat_type

                if not flat_instance.size_builtup_area:
                    flat_instance.size_builtup_area = flat_instance.size_carpet_area if flat_instance.size_carpet_area else 0

                flat_instance.size_carpet_area = flat_instance.size_builtup_area / 1.2

                if not result.get(supplier_id):
                    result[supplier_id] = {}

                result[supplier_id][flat_type] = {
                    'flat_count': flat_instance.flat_count if flat_instance.flat_count else 0,
                    'flat_rent': flat_instance.flat_rent if flat_instance.flat_rent else 0,
                    'flat_area': flat_instance.size_builtup_area if flat_instance.size_builtup_area else 0,
                }
            # update the flat objects first
            bulk_update(flat_objects)

            for supplier_id, flat_detail in result.iteritems():
                total_rent = 0
                total_area = 0.0
                for flat_type, flat_detail in result[supplier_id].iteritems():
                    total_rent += (int(flat_detail['flat_count']) * int(flat_detail['flat_rent']))
                    total_area += float(flat_detail['flat_area'])
                if not total_area:
                    supplier_map[supplier_id].flat_avg_rental_persqft = 0
                else:
                    supplier_map[supplier_id].flat_avg_rental_persqft = int(total_rent / total_area)

            # now update the society objects
            bulk_update(supplier_map.values())
            return ui_utils.handle_response(class_name, data='success', success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)
