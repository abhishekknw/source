from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from v0.serializers import BannerInventorySerializer, CarDisplayInventorySerializer, CommunityHallInfoSerializer, DoorToDoorInfoSerializer, LiftDetailsSerializer, NoticeBoardDetailsSerializer, PosterInventorySerializer, SocietyFlatSerializer, StandeeInventorySerializer, SwimmingPoolInfoSerializer, WallInventorySerializer, UserInquirySerializer, CommonAreaDetailsSerializer, ContactDetailsSerializer, EventsSerializer, InventoryInfoSerializer, MailboxInfoSerializer, OperationsInfoSerializer, PoleInventorySerializer, PosterInventoryMappingSerializer, RatioDetailsSerializer, SignupSerializer, StallInventorySerializer, StreetFurnitureSerializer, SupplierInfoSerializer, SupplierTypeSocietySerializer, SocietyTowerSerializer, CityAreaSerializer
from v0.models import BannerInventory, CarDisplayInventory, CommunityHallInfo, DoorToDoorInfo, LiftDetails, NoticeBoardDetails, PosterInventory, SocietyFlat, StandeeInventory, SwimmingPoolInfo, WallInventory, UserInquiry, CommonAreaDetails, ContactDetails, Events, InventoryInfo, MailboxInfo, OperationsInfo, PoleInventory, PosterInventoryMapping, RatioDetails, Signup, StallInventory, StreetFurniture, SupplierInfo, SupplierTypeSociety, SocietyTower, CityArea


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


class CarDisplayInventoryAPIView(APIView):

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
        return Response(serializer.errors, status=400)


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
        except CarDisplayInventory.DoesNotExist:
            return Response(status=404)





