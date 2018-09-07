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

from v0.ui.base.serializers import GroupSerializer
from v0.ui.permissions.serializers import UserInquirySerializer, PermissionSerializer
from v0.ui.user.serializers import BaseUserSerializer, BaseUserUpdateSerializer, BaseUserCreateSerializer
from v0.ui.user.models import UserInquiry
from v0.ui.location.models import CityArea
from v0.ui.location.serializers import CityAreaSerializer
from v0.ui.account.serializers import ContactDetailsSerializer, ContactDetailsGenericSerializer, SignupSerializer, \
    BusinessTypeSubTypeReadOnlySerializer, OperationsInfoSerializer
from v0.ui.account.models import ContactDetails, ContactDetailsGeneric, Signup
from v0.ui.inventory.models import SupplierTypeSociety, StallInventory
# from v0.ui.inventory.serializers import SupplierTypeSocietySerializer
from rest_framework.decorators import detail_route, list_route
from v0.ui.account.models import OperationsInfo, BusinessTypes, \
    BusinessSubTypes
from v0.ui.common.models import BaseUser
from v0.ui.permissions.models import CustomPermissions
from v0.ui.base.models import DurationType
from v0.ui.finances.models import RatioDetails, DoorToDoorInfo
from v0.ui.finances.serializers import DoorToDoorInfoSerializer, RatioDetailsSerializer
from v0.ui.supplier.serializers import SupplierInfoSerializer, SupplierTypeSocietySerializer
from v0.ui.components.models import CommunityHallInfo, LiftDetails, NoticeBoardDetails, SocietyFlat, SwimmingPoolInfo, \
    FlatType, MailboxInfo, SocietyTower, CommonAreaDetails, Amenity
from v0.ui.components.serializers import LiftDetailsSerializer, CommunityHallInfoSerializer, FlatTypeSerializer, \
    NoticeBoardDetailsSerializer, SocietyFlatSerializer, SwimmingPoolInfoSerializer, MailboxInfoSerializer, \
    CommonAreaDetailsSerializer, SocietyTowerSerializer
import utils as v0_utils
from constants import model_names
import v0.ui.utils as ui_utils
import errors
import constants as v0_constants
import v0.ui.website.utils as website_utils
from v0.ui.supplier.models import SupplierInfo, SupplierTypeCorporate, SupplierAmenitiesMap

from v0.ui.events.models import Events
from v0.ui.events.serializers import EventsSerializer
import re


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
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

class SetUserToMasterUser(APIView):
    """
    The api sets user_id field to master user if any in the database.
    Careful before using it because it will update user field of all the rows to master 
    user which may not be what you want everytime. 
    """
    permission_classes = (permissions.IsAuthenticated,)

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
            return ui_utils.handle_response(class_name,
                                            data='succesfully updated all users of all modes to master user',
                                            success=True)
        except ObjectDoesNotExist as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


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
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

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
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

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
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

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
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

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
            return ui_utils.handle_response(class_name, data='successfully deleted {0}'.format(pk), success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

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
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

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
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

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
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

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
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


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
                return ui_utils.handle_response(class_name,
                                                data=errors.INCORRECT_DATABASE_NAME_ERROR.format(default_database_name,
                                                                                                 v0_constants.database_name))
            # make the list of addresses by combining city name with center names
            addresses = [city_name + ',' + center_name for center_name in centers]
            SupplierTypeSociety.objects.all().delete()  # delete all societies before proceeding
            society_count = total_society_count / len(addresses)  # societies per address
            coordinates = []
            for address in addresses:
                geo_code_instance = v0_utils.get_geo_code_instance(address)
                if not geo_code_instance:
                    return ui_utils.handle_response(class_name, data=errors.NO_GEOCODE_INSTANCE_FOUND.format(address))
                location_lat, location_long = geo_code_instance.latlng
                # location_lat, location_long are coordinates of origin.
                if society_count < 4:
                    coordinates = v0_utils.generate_coordinates_in_quadrant(society_count, location_lat, location_long,
                                                                            radius)
                else:
                    society_per_quadrant = society_count / 4
                    remainder = society_count % 4
                    coordinates.extend(
                        v0_utils.generate_coordinates_in_quadrant(society_per_quadrant, location_lat, location_long,
                                                                  radius, v0_constants.first_quadrant_code))
                    coordinates.extend(
                        v0_utils.generate_coordinates_in_quadrant(society_per_quadrant, location_lat, location_long,
                                                                  radius, v0_constants.second_quadrant_code))
                    coordinates.extend(
                        v0_utils.generate_coordinates_in_quadrant(society_per_quadrant, location_lat, location_long,
                                                                  radius, v0_constants.third_quadrant_code))
                    coordinates.extend(
                        v0_utils.generate_coordinates_in_quadrant(society_per_quadrant + remainder, location_lat,
                                                                  location_long, radius,
                                                                  v0_constants.fourth_quadrant_code))
                result[address] = society_count

            suppliers_dict = v0_utils.assign_supplier_ids(city_code, v0_constants.society, coordinates)

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
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


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
            request: JSON for business type and subtypes. sample JSON looks like this

        Returns: The created instances

        """
        class_name = self.__class__.__name__
        try:
            # default_database_name = settings.DATABASES['default']['NAME']

            already_present_business_codes = BusinessTypes.objects.all().values_list('business_type_code', flat=True)

            # if default_database_name != v0_constants.database_name:
            #     return ui_utils.handle_response(class_name, data=errors.INCORRECT_DATABASE_NAME_ERROR.format(default_database_name, v0_constants.database_name))

            business_type_code_list = []  # to store list of all codes of BusinessType. Later used to fetch objects of BusinessType

            for business_type, detail in request.data.iteritems():

                business_type_code = detail['code']
                business_type_code_list.append(business_type_code)

                # if already present, fetch it
                if business_type_code in already_present_business_codes:
                    business_type_instance = BusinessTypes.objects.get(business_type_code=business_type_code)

                else:
                    # we create this business first. it's not present in the system
                    business_type_instance = BusinessTypes.objects.create(business_type_code=business_type_code,
                                                                          business_type=business_type)

                # fetch already present business sub types
                already_present_business_sub_type_codes_instances = BusinessSubTypes.objects.filter(
                    business_type=business_type_instance)

                # iterate through subtypes
                for sub_type_dict in detail['subtypes']:
                    business_sub_type_code = sub_type_dict['code']
                    check = False
                    # check weather this sub type is already present or not for this business type
                    for sub_type_instance in already_present_business_sub_type_codes_instances:
                        if sub_type_instance.business_sub_type_code == business_sub_type_code:
                            # this is already done
                            check = True
                            break

                    # if check = True, skip this part. This sub type is already present
                    if not check:
                        # business sub type not in already business sub types
                        data = {
                            'business_type': business_type_instance,
                            'business_sub_type': sub_type_dict['name'],
                            'business_sub_type_code': sub_type_dict['code']
                        }
                        BusinessSubTypes.objects.create(**data)

            business_type_instances = BusinessTypes.objects.filter(business_type_code__in=business_type_code_list)
            serializer = BusinessTypeSubTypeReadOnlySerializer(business_type_instances, many=True)
            return ui_utils.handle_response(class_name, data=serializer.data, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

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
                return ui_utils.handle_response(class_name,
                                                data=errors.INCORRECT_DATABASE_NAME_ERROR.format(default_database_name,
                                                                                                 v0_constants.database_name))

            supplier_ids = SupplierTypeSociety.objects.all().values_list('supplier_id', flat=True)
            response = ui_utils.get_content_type(v0_constants.society)
            if not response.data['status']:
                return response
            content_type = response.data['data']
            v0_utils.handle_inventory_pricing(supplier_ids, content_type, request.data)
            return ui_utils.handle_response(class_name, data='success', success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


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
                return ui_utils.handle_response(class_name,
                                                data=errors.INCORRECT_DATABASE_NAME_ERROR.format(default_database_name,
                                                                                                 v0_constants.database_name))

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
                count_of_amenity_to_be_assigned = random.randint(0,
                                                                 amenity_instance_count)  # assign anywhere between zero to max amenity count
                for sub_index in range(count_of_amenity_to_be_assigned):
                    amenity = amenity_instances[sub_index]
                    supplier_amenity_instances.append(
                        SupplierAmenitiesMap(content_type=content_type, amenity=amenity, object_id=supplier_id))

            SupplierAmenitiesMap.objects.all().delete()
            SupplierAmenitiesMap.objects.bulk_create(supplier_amenity_instances)

            return ui_utils.handle_response(class_name, data='success', success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


def validate_password(new_password):
    # used to check whether the new password is strong enough
    valid = 1
    if not any(x.isupper() for x in new_password):
        valid = 0
    if re.match("[^a-zA-Z0-9_]", new_password):
        valid = 0
    if len(new_password)<8:
        valid = 0
    # rules = [lambda s: any(x.isupper() for x in s),  # must have at least one uppercase
    #          lambda s: re.match("[^a-zA-Z0-9_]", s)==False,  # must have at least one special char
    #          lambda s: len(s) >= 8  # must be at least 8 characters
    #          ]
    # if all(rule(new_password) for rule in rules):
    #     valid = 1
    #     print 'valid'
    return valid


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
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

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
            serializer = BaseUserUpdateSerializer(user, data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return ui_utils.handle_response(class_name, data=serializer.data, success=True)
            return ui_utils.handle_response(class_name, data=serializer.errors)
        except ObjectDoesNotExist as e:
            return ui_utils.handle_response(class_name, data=pk, exception_object=e)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

    def create(self, request):
        """
        Create one single user
        Args:
            request:  Request body

        Returns: created user
        """
        class_name = self.__class__.__name__
        try:
            data = request.data
            password = data['password']
            confirm_password = data['confirm_password']
            serializer = BaseUserCreateSerializer(data=data)
            if password != confirm_password:
                return ui_utils.handle_response(class_name, data='passwords do not match', success=False)
            if validate_password(password) == 0:
                return ui_utils.handle_response(class_name, data='password should have 8 chars including a capital'
                                                                 'and a special char', success=False)
            if serializer.is_valid():
                user = serializer.save()
                return ui_utils.handle_response(class_name, data=serializer.data, success=True)
            return ui_utils.handle_response(class_name, data=serializer.errors)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

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
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

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
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

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
            password_valid = validate_password(new_password)
            if password_valid == 1:
                user.set_password(new_password)
                user.save()
                return ui_utils.handle_response(class_name, data='password changed successfully', success=True)
            else:
                return ui_utils.handle_response(class_name, data='please make sure to have 1 capital, 1 special '
                                                                 'character, and total 8 characters', success=False)
        except ObjectDoesNotExist as e:
            return ui_utils.handle_response(class_name, data=pk, exception_object=e)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


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
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

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
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

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
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

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
            return ui_utils.handle_response(class_name, exception_object=e, request=request)

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
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


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
            password_valid = validate_password(password)
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
            if password_valid == 1:
                return ui_utils.handle_response(class_name, data=data, success=True)
            else:
                return ui_utils.handle_response(class_name, data='password must have at least 8 characters'
                                                                 ' including a capital and a special char', success=False)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


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
            return ui_utils.handle_response(class_name, exception_object=e, request=request)


class CopyOrganisation(APIView):
    """

    """

    def get(self, request):
        """

        :param request:
        :return:
        """
        class_name = self.__class__.__name__
        business_info_model = apps.get_model(settings.APP_NAME, 'BusinessInfo')
        organisation_model = apps.get_model(settings.APP_NAME, 'Organisation')
        instances = business_info_model.objects.all()
        for instance in instances:

            data = {
                'name': instance.name,
                'user': instance.user,
                'organisation_id': instance.business_id,
                'type_name': instance.type_name,
                'sub_type': instance.sub_type,
                'phone': instance.phone,
                'email': instance.email,
                'address': instance.address,
                'reference_name': instance.reference_name,
                'reference_phone': instance.reference_phone,
                'reference_email': instance.reference_email,
                'comments': instance.comments,
                'category': 'BUSINESS',
            }
            try:
                organisation_model.objects.create(**data)
            except Exception as e:
                print e
        return ui_utils.handle_response(class_name, data='success', success=True)