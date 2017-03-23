from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.apps import apps
import django.apps
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Permission
from django.forms import model_to_dict
from django.conf import settings

from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets

from v0.serializers import BannerInventorySerializer, CommunityHallInfoSerializer, DoorToDoorInfoSerializer, LiftDetailsSerializer, NoticeBoardDetailsSerializer, PosterInventorySerializer, SocietyFlatSerializer, StandeeInventorySerializer, SwimmingPoolInfoSerializer, WallInventorySerializer, UserInquirySerializer, CommonAreaDetailsSerializer, ContactDetailsSerializer, EventsSerializer, InventoryInfoSerializer, MailboxInfoSerializer, OperationsInfoSerializer, PoleInventorySerializer, PosterInventoryMappingSerializer, RatioDetailsSerializer, SignupSerializer, StallInventorySerializer, StreetFurnitureSerializer, SupplierInfoSerializer, SupplierTypeSocietySerializer, SocietyTowerSerializer, CityAreaSerializer, ContactDetailsGenericSerializer, FlatTypeSerializer, PermissionSerializer
from rest_framework.decorators import detail_route, list_route
from v0.models import BannerInventory, CommunityHallInfo, DoorToDoorInfo, LiftDetails, NoticeBoardDetails, PosterInventory, SocietyFlat, StandeeInventory, SwimmingPoolInfo, WallInventory, UserInquiry, CommonAreaDetails, ContactDetails, Events, InventoryInfo, MailboxInfo, OperationsInfo, PoleInventory, PosterInventoryMapping, RatioDetails, Signup, StallInventory, StreetFurniture, SupplierInfo, SupplierTypeSociety, SocietyTower, CityArea, ContactDetailsGeneric, SupplierTypeCorporate, FlatType, BaseUser, CustomPermissions
import utils as v0_utils
from constants import model_names
import v0.ui.utils as ui_utils
import errors
import v0.ui.website.constants as website_constants
import constants as v0_constants


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
        Creates random N societies. Useful for testing the front end with low data volume.
        Args:
            request:
        Returns:
        """
        try:
            city_name = request.data['city_name']
            radius = float(request.data['radius'])
            city_code = request.data['city_code']
            society_count = int(request.data['society_count'])
            society_detail = request.data.get('supplier_detail')
            default_database_name = settings.DATABASES['default']['NAME']
            result = {}
            society_list = []

            if default_database_name != v0_constants.database_name:
                return ui_utils.handle_response(class_name, data=errors.INCORRECT_DATABASE_NAME_ERROR.format(default_database_name, v0_constants.database_name))

            geo_code_instance = v0_utils.get_geo_code_instance(city_name)
            if not geo_code_instance:
                return ui_utils.handle_response(class_name, data=errors.NO_GEOCODE_INSTANCE_FOUND.format(city_name))
            state_code = geo_code_instance.state
            city_lat, city_long = geo_code_instance.latlng

            if society_count < 4:
                coordinates = v0_utils.generate_coordinates_in_quadrant(society_count, city_lat, city_long, radius)
            else:
                society_per_quadrant = society_count/4
                remainder = society_count % 4
                coordinates = v0_utils.generate_coordinates_in_quadrant(society_per_quadrant, city_lat, city_long, radius, v0_constants.first_quadrant_code)
                coordinates.extend(v0_utils.generate_coordinates_in_quadrant(society_per_quadrant, city_lat, city_long, radius, v0_constants.second_quadrant_code))
                coordinates.extend(v0_utils.generate_coordinates_in_quadrant(society_per_quadrant, city_lat, city_long, radius, v0_constants.third_quadrant_code))
                coordinates.extend(v0_utils.generate_coordinates_in_quadrant(society_per_quadrant + remainder, city_lat, city_long, radius, v0_constants.fourth_quadrant_code))

            suppliers_dict = v0_utils.assign_supplier_ids(state_code, city_code, website_constants.society, coordinates)
            for society_id, detail in suppliers_dict.iteritems():
                detail['supplier_id'] = society_id
                detail['society_latitude'] = detail['latitude']
                detail['society_longitude'] = detail['longitude']
                detail['society_name'] = society_id
                del detail['latitude']
                del detail['longitude']
                society_list.append(SupplierTypeSociety(**detail))
            SupplierTypeSociety.objects.all().delete()
            SupplierTypeSociety.objects.bulk_create(society_list)
            result['count'] = len(society_list)
            return ui_utils.handle_response(class_name, data=result, success=True)
        except Exception as e:
            return ui_utils.handle_response(class_name, exception_object=e)
