from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from serializers import AssignedAuditSerializer
from v0.models import SocietyInventoryBooking
from v0.serializers import SocietyInventoryBookingSerializer
from datetime import date
from django.db.models import Q





class AssignedAuditAPIListView(APIView):

    def get(self, request, format=None):
        try:
            items = SocietyInventoryBooking.objects.filter(Q(start_date=date.today()) | Q(audit_date=date.today())).order_by('society')
            serializer = AssignedAuditSerializer(items, many=True)

            return Response(serializer.data, status=200)
        except :
            return Response(status=404)


