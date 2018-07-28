from django.apps import apps
from django.forms import model_to_dict
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Permission, Group
from rest_framework.views import APIView
from v0.ui.inventory.serializers import (BannerInventorySerializer, PosterInventorySerializer,
                                         StandeeInventorySerializer, WallInventorySerializer, InventoryInfoSerializer,
                                         PoleInventorySerializer, PosterInventoryMappingSerializer,
                                         StallInventorySerializer, StreetFurnitureSerializer)
from v0.ui.inventory.models import (BannerInventory, AdInventoryType, PosterInventory, StreetFurniture,
    StandeeInventory, WallInventory, InventoryInfo, PoleInventory, PosterInventoryMapping, AD_INVENTORY_CHOICES)


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
            for duration_code, duration_value in v0_constants.duration_dict.iteritems():
                DurationType.objects.get_or_create(duration_name=duration_value)
            for inventory_tuple in AD_INVENTORY_CHOICES:
                for ad_inventory_type_code, ad_inventory_type_value in v0_constants.type_dict.iteritems():
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