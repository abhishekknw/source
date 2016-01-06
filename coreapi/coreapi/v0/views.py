from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from v0.serializers import MasterBannerInventorySerializer, MasterCarDisplayInventorySerializer, MasterCommunityHallInfoSerializer, MasterDoorToDoorInfoSerializer, MasterLiftDetailsSerializer, MasterNoticeBoardDetailsSerializer, MasterPosterInventorySerializer, MasterSocietyFlatSerializer, MasterStandeeInventorySerializer, MasterSwimmingPoolInfoSerializer, MasterWallInventorySerializer, UserInquirySerializer, CommonAreaDetailsSerializer, MasterContactDetailsSerializer, MasterEventsSerializer, MasterInventoryInfoSerializer, MasterMailboxInfoSerializer, MasterOperationsInfoSerializer, MasterPoleInventorySerializer, MasterPosterInventoryMappingSerializer, MasterRatioDetailsSerializer, MasterSignupSerializer, MasterStallInventorySerializer, MasterStreetFurnitureSerializer, MasterSupplierInfoSerializer, MasterSupplierTypeSocietySerializer, MasterSupplierTypeSocietyTowerSerializer
from v0.models import MasterBannerInventory, MasterCarDisplayInventory, MasterCommunityHallInfo, MasterDoorToDoorInfo, MasterLiftDetails, MasterNoticeBoardDetails, MasterPosterInventory, MasterSocietyFlat, MasterStandeeInventory, MasterSwimmingPoolInfo, MasterWallInventory, UserInquiry, CommonAreaDetails, MasterContactDetails, MasterEvents, MasterInventoryInfo, MasterMailboxInfo, MasterOperationsInfo, MasterPoleInventory, MasterPosterInventoryMapping, MasterRatioDetails, MasterSignup, MasterStallInventory, MasterStreetFurniture, MasterSupplierInfo, MasterSupplierTypeSociety, MasterSupplierTypeSocietyTower


class MasterBannerInventoryAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = MasterBannerInventory.objects.get(pk=id)
            serializer = MasterBannerInventorySerializer(item)
            return Response(serializer.data)
        except MasterBannerInventory.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = MasterBannerInventory.objects.get(pk=id)
        except MasterBannerInventory.DoesNotExist:
            return Response(status=404)
        serializer = MasterBannerInventorySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = MasterBannerInventory.objects.get(pk=id)
        except MasterBannerInventory.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class MasterBannerInventoryAPIListView(APIView):

    def get(self, request, format=None):
        items = MasterBannerInventory.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = MasterBannerInventorySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = MasterBannerInventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MasterCarDisplayInventoryAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = MasterCarDisplayInventory.objects.get(pk=id)
            serializer = MasterCarDisplayInventorySerializer(item)
            return Response(serializer.data)
        except MasterCarDisplayInventory.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = MasterCarDisplayInventory.objects.get(pk=id)
        except MasterCarDisplayInventory.DoesNotExist:
            return Response(status=404)
        serializer = MasterCarDisplayInventorySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = MasterCarDisplayInventory.objects.get(pk=id)
        except MasterCarDisplayInventory.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class MasterCarDisplayInventoryAPIListView(APIView):

    def get(self, request, format=None):
        items = MasterCarDisplayInventory.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = MasterCarDisplayInventorySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = MasterCarDisplayInventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MasterCommunityHallInfoAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = MasterCommunityHallInfo.objects.get(pk=id)
            serializer = MasterCommunityHallInfoSerializer(item)
            return Response(serializer.data)
        except MasterCommunityHallInfo.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = MasterCommunityHallInfo.objects.get(pk=id)
        except MasterCommunityHallInfo.DoesNotExist:
            return Response(status=404)
        serializer = MasterCommunityHallInfoSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = MasterCommunityHallInfo.objects.get(pk=id)
        except MasterCommunityHallInfo.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class MasterCommunityHallInfoAPIListView(APIView):

    def get(self, request, format=None):
        items = MasterCommunityHallInfo.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = MasterCommunityHallInfoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = MasterCommunityHallInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MasterDoorToDoorInfoAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = MasterDoorToDoorInfo.objects.get(pk=id)
            serializer = MasterDoorToDoorInfoSerializer(item)
            return Response(serializer.data)
        except MasterDoorToDoorInfo.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = MasterDoorToDoorInfo.objects.get(pk=id)
        except MasterDoorToDoorInfo.DoesNotExist:
            return Response(status=404)
        serializer = MasterDoorToDoorInfoSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = MasterDoorToDoorInfo.objects.get(pk=id)
        except MasterDoorToDoorInfo.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class MasterDoorToDoorInfoAPIListView(APIView):

    def get(self, request, format=None):
        items = MasterDoorToDoorInfo.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = MasterDoorToDoorInfoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = MasterDoorToDoorInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MasterLiftDetailsAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = MasterLiftDetails.objects.get(pk=id)
            serializer = MasterLiftDetailsSerializer(item)
            return Response(serializer.data)
        except MasterLiftDetails.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = MasterLiftDetails.objects.get(pk=id)
        except MasterLiftDetails.DoesNotExist:
            return Response(status=404)
        serializer = MasterLiftDetailsSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = MasterLiftDetails.objects.get(pk=id)
        except MasterLiftDetails.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class MasterLiftDetailsAPIListView(APIView):

    def get(self, request, format=None):
        items = MasterLiftDetails.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = MasterLiftDetailsSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = MasterLiftDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MasterNoticeBoardDetailsAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = MasterNoticeBoardDetails.objects.get(pk=id)
            serializer = MasterNoticeBoardDetailsSerializer(item)
            return Response(serializer.data)
        except MasterNoticeBoardDetails.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = MasterNoticeBoardDetails.objects.get(pk=id)
        except MasterNoticeBoardDetails.DoesNotExist:
            return Response(status=404)
        serializer = MasterNoticeBoardDetailsSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = MasterNoticeBoardDetails.objects.get(pk=id)
        except MasterNoticeBoardDetails.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class MasterNoticeBoardDetailsAPIListView(APIView):

    def get(self, request, format=None):
        items = MasterNoticeBoardDetails.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = MasterNoticeBoardDetailsSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = MasterNoticeBoardDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MasterPosterInventoryAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = MasterPosterInventory.objects.get(pk=id)
            serializer = MasterPosterInventorySerializer(item)
            return Response(serializer.data)
        except MasterPosterInventory.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = MasterPosterInventory.objects.get(pk=id)
        except MasterPosterInventory.DoesNotExist:
            return Response(status=404)
        serializer = MasterPosterInventorySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = MasterPosterInventory.objects.get(pk=id)
        except MasterPosterInventory.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class MasterPosterInventoryAPIListView(APIView):

    def get(self, request, format=None):
        items = MasterPosterInventory.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = MasterPosterInventorySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = MasterPosterInventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MasterSocietyFlatAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = MasterSocietyFlat.objects.get(pk=id)
            serializer = MasterSocietyFlatSerializer(item)
            return Response(serializer.data)
        except MasterSocietyFlat.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = MasterSocietyFlat.objects.get(pk=id)
        except MasterSocietyFlat.DoesNotExist:
            return Response(status=404)
        serializer = MasterSocietyFlatSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = MasterSocietyFlat.objects.get(pk=id)
        except MasterSocietyFlat.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class MasterSocietyFlatAPIListView(APIView):

    def get(self, request, format=None):
        items = MasterSocietyFlat.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = MasterSocietyFlatSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = MasterSocietyFlatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MasterStandeeInventoryAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = MasterStandeeInventory.objects.get(pk=id)
            serializer = MasterStandeeInventorySerializer(item)
            return Response(serializer.data)
        except MasterStandeeInventory.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = MasterStandeeInventory.objects.get(pk=id)
        except MasterStandeeInventory.DoesNotExist:
            return Response(status=404)
        serializer = MasterStandeeInventorySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = MasterStandeeInventory.objects.get(pk=id)
        except MasterStandeeInventory.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class MasterStandeeInventoryAPIListView(APIView):

    def get(self, request, format=None):
        items = MasterStandeeInventory.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = MasterStandeeInventorySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = MasterStandeeInventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MasterSwimmingPoolInfoAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = MasterSwimmingPoolInfo.objects.get(pk=id)
            serializer = MasterSwimmingPoolInfoSerializer(item)
            return Response(serializer.data)
        except MasterSwimmingPoolInfo.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = MasterSwimmingPoolInfo.objects.get(pk=id)
        except MasterSwimmingPoolInfo.DoesNotExist:
            return Response(status=404)
        serializer = MasterSwimmingPoolInfoSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = MasterSwimmingPoolInfo.objects.get(pk=id)
        except MasterSwimmingPoolInfo.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class MasterSwimmingPoolInfoAPIListView(APIView):

    def get(self, request, format=None):
        items = MasterSwimmingPoolInfo.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = MasterSwimmingPoolInfoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = MasterSwimmingPoolInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MasterWallInventoryAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = MasterWallInventory.objects.get(pk=id)
            serializer = MasterWallInventorySerializer(item)
            return Response(serializer.data)
        except MasterWallInventory.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = MasterWallInventory.objects.get(pk=id)
        except MasterWallInventory.DoesNotExist:
            return Response(status=404)
        serializer = MasterWallInventorySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = MasterWallInventory.objects.get(pk=id)
        except MasterWallInventory.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class MasterWallInventoryAPIListView(APIView):

    def get(self, request, format=None):
        items = MasterWallInventory.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = MasterWallInventorySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = MasterWallInventorySerializer(data=request.data)
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


class MasterContactDetailsAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = MasterContactDetails.objects.get(pk=id)
            serializer = MasterContactDetailsSerializer(item)
            return Response(serializer.data)
        except MasterContactDetails.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = MasterContactDetails.objects.get(pk=id)
        except MasterContactDetails.DoesNotExist:
            return Response(status=404)
        serializer = MasterContactDetailsSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = MasterContactDetails.objects.get(pk=id)
        except MasterContactDetails.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class MasterContactDetailsAPIListView(APIView):

    def get(self, request, format=None):
        items = MasterContactDetails.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = MasterContactDetailsSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = MasterContactDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MasterEventsAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = MasterEvents.objects.get(pk=id)
            serializer = MasterEventsSerializer(item)
            return Response(serializer.data)
        except MasterEvents.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = MasterEvents.objects.get(pk=id)
        except MasterEvents.DoesNotExist:
            return Response(status=404)
        serializer = MasterEventsSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = MasterEvents.objects.get(pk=id)
        except MasterEvents.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class MasterEventsAPIListView(APIView):

    def get(self, request, format=None):
        items = MasterEvents.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = MasterEventsSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = MasterEventsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MasterInventoryInfoAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = MasterInventoryInfo.objects.get(pk=id)
            serializer = MasterInventoryInfoSerializer(item)
            return Response(serializer.data)
        except MasterInventoryInfo.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = MasterInventoryInfo.objects.get(pk=id)
        except MasterInventoryInfo.DoesNotExist:
            return Response(status=404)
        serializer = MasterInventoryInfoSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = MasterInventoryInfo.objects.get(pk=id)
        except MasterInventoryInfo.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class MasterInventoryInfoAPIListView(APIView):

    def get(self, request, format=None):
        items = MasterInventoryInfo.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = MasterInventoryInfoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = MasterInventoryInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MasterMailboxInfoAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = MasterMailboxInfo.objects.get(pk=id)
            serializer = MasterMailboxInfoSerializer(item)
            return Response(serializer.data)
        except MasterMailboxInfo.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = MasterMailboxInfo.objects.get(pk=id)
        except MasterMailboxInfo.DoesNotExist:
            return Response(status=404)
        serializer = MasterMailboxInfoSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = MasterMailboxInfo.objects.get(pk=id)
        except MasterMailboxInfo.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class MasterMailboxInfoAPIListView(APIView):

    def get(self, request, format=None):
        items = MasterMailboxInfo.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = MasterMailboxInfoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = MasterMailboxInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MasterOperationsInfoAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = MasterOperationsInfo.objects.get(pk=id)
            serializer = MasterOperationsInfoSerializer(item)
            return Response(serializer.data)
        except MasterOperationsInfo.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = MasterOperationsInfo.objects.get(pk=id)
        except MasterOperationsInfo.DoesNotExist:
            return Response(status=404)
        serializer = MasterOperationsInfoSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = MasterOperationsInfo.objects.get(pk=id)
        except MasterOperationsInfo.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class MasterOperationsInfoAPIListView(APIView):

    def get(self, request, format=None):
        items = MasterOperationsInfo.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = MasterOperationsInfoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = MasterOperationsInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MasterPoleInventoryAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = MasterPoleInventory.objects.get(pk=id)
            serializer = MasterPoleInventorySerializer(item)
            return Response(serializer.data)
        except MasterPoleInventory.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = MasterPoleInventory.objects.get(pk=id)
        except MasterPoleInventory.DoesNotExist:
            return Response(status=404)
        serializer = MasterPoleInventorySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = MasterPoleInventory.objects.get(pk=id)
        except MasterPoleInventory.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class MasterPoleInventoryAPIListView(APIView):

    def get(self, request, format=None):
        items = MasterPoleInventory.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = MasterPoleInventorySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = MasterPoleInventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MasterPosterInventoryMappingAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = MasterPosterInventoryMapping.objects.get(pk=id)
            serializer = MasterPosterInventoryMappingSerializer(item)
            return Response(serializer.data)
        except MasterPosterInventoryMapping.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = MasterPosterInventoryMapping.objects.get(pk=id)
        except MasterPosterInventoryMapping.DoesNotExist:
            return Response(status=404)
        serializer = MasterPosterInventoryMappingSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = MasterPosterInventoryMapping.objects.get(pk=id)
        except MasterPosterInventoryMapping.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class MasterPosterInventoryMappingAPIListView(APIView):

    def get(self, request, format=None):
        items = MasterPosterInventoryMapping.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = MasterPosterInventoryMappingSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = MasterPosterInventoryMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MasterRatioDetailsAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = MasterRatioDetails.objects.get(pk=id)
            serializer = MasterRatioDetailsSerializer(item)
            return Response(serializer.data)
        except MasterRatioDetails.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = MasterRatioDetails.objects.get(pk=id)
        except MasterRatioDetails.DoesNotExist:
            return Response(status=404)
        serializer = MasterRatioDetailsSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = MasterRatioDetails.objects.get(pk=id)
        except MasterRatioDetails.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class MasterRatioDetailsAPIListView(APIView):

    def get(self, request, format=None):
        items = MasterRatioDetails.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = MasterRatioDetailsSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = MasterRatioDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MasterSignupAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = MasterSignup.objects.get(pk=id)
            serializer = MasterSignupSerializer(item)
            return Response(serializer.data)
        except MasterSignup.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = MasterSignup.objects.get(pk=id)
        except MasterSignup.DoesNotExist:
            return Response(status=404)
        serializer = MasterSignupSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = MasterSignup.objects.get(pk=id)
        except MasterSignup.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class MasterSignupAPIListView(APIView):

    def get(self, request, format=None):
        items = MasterSignup.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = MasterSignupSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = MasterSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MasterStallInventoryAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = MasterStallInventory.objects.get(pk=id)
            serializer = MasterStallInventorySerializer(item)
            return Response(serializer.data)
        except MasterStallInventory.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = MasterStallInventory.objects.get(pk=id)
        except MasterStallInventory.DoesNotExist:
            return Response(status=404)
        serializer = MasterStallInventorySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = MasterStallInventory.objects.get(pk=id)
        except MasterStallInventory.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class MasterStallInventoryAPIListView(APIView):

    def get(self, request, format=None):
        items = MasterStallInventory.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = MasterStallInventorySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = MasterStallInventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MasterStreetFurnitureAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = MasterStreetFurniture.objects.get(pk=id)
            serializer = MasterStreetFurnitureSerializer(item)
            return Response(serializer.data)
        except MasterStreetFurniture.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = MasterStreetFurniture.objects.get(pk=id)
        except MasterStreetFurniture.DoesNotExist:
            return Response(status=404)
        serializer = MasterStreetFurnitureSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = MasterStreetFurniture.objects.get(pk=id)
        except MasterStreetFurniture.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class MasterStreetFurnitureAPIListView(APIView):

    def get(self, request, format=None):
        items = MasterStreetFurniture.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = MasterStreetFurnitureSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = MasterStreetFurnitureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MasterSupplierInfoAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = MasterSupplierInfo.objects.get(pk=id)
            serializer = MasterSupplierInfoSerializer(item)
            return Response(serializer.data)
        except MasterSupplierInfo.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = MasterSupplierInfo.objects.get(pk=id)
        except MasterSupplierInfo.DoesNotExist:
            return Response(status=404)
        serializer = MasterSupplierInfoSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = MasterSupplierInfo.objects.get(pk=id)
        except MasterSupplierInfo.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class MasterSupplierInfoAPIListView(APIView):

    def get(self, request, format=None):
        items = MasterSupplierInfo.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = MasterSupplierInfoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = MasterSupplierInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MasterSupplierTypeSocietyAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = MasterSupplierTypeSociety.objects.get(pk=id)
            serializer = MasterSupplierTypeSocietySerializer(item)
            return Response(serializer.data)
        except MasterSupplierTypeSociety.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = MasterSupplierTypeSociety.objects.get(pk=id)
        except MasterSupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        serializer = MasterSupplierTypeSocietySerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = MasterSupplierTypeSociety.objects.get(pk=id)
        except MasterSupplierTypeSociety.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class MasterSupplierTypeSocietyAPIListView(APIView):

    def get(self, request, format=None):
        items = MasterSupplierTypeSociety.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = MasterSupplierTypeSocietySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = MasterSupplierTypeSocietySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MasterSupplierTypeSocietyTowerAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = MasterSupplierTypeSocietyTower.objects.get(pk=id)
            serializer = MasterSupplierTypeSocietyTowerSerializer(item)
            return Response(serializer.data)
        except MasterSupplierTypeSocietyTower.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = MasterSupplierTypeSocietyTower.objects.get(pk=id)
        except MasterSupplierTypeSocietyTower.DoesNotExist:
            return Response(status=404)
        serializer = MasterSupplierTypeSocietyTowerSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = MasterSupplierTypeSocietyTower.objects.get(pk=id)
        except MasterSupplierTypeSocietyTower.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class MasterSupplierTypeSocietyTowerAPIListView(APIView):

    def get(self, request, format=None):
        items = MasterSupplierTypeSocietyTower.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = MasterSupplierTypeSocietyTowerSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = MasterSupplierTypeSocietyTowerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
