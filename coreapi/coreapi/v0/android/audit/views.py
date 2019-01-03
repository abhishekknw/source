from __future__ import print_function
from __future__ import absolute_import
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from .serializers import AssignedAuditSerializer,AuditSerializer, AssignedAuditsTempSerializer
from v0.ui.finances.models import AssignedAudits, Audits
from v0.ui.inventory.models import SocietyInventoryBooking
from datetime import date
from django.db.models import Q


class AssignedAuditAPIListView(APIView):

    def get(self, request, format=None):
        try:
            #items = SocietyInventoryBooking.objects.filter(Q(start_date=date.today()) | Q(audit_date=date.today())).order_by('society')
            items = SocietyInventoryBooking.objects #.filter(Q(start_date=date.today()) | Q(audit_date=date.today())).order_by('society')
            serializer = AssignedAuditSerializer(items, many=True)

            return Response({'result':serializer.data}, status=200)
        except :
            return Response(status=404)

    def post(self, request, format=None):

        print(request.data)
        '''if 'campaign_id' in request.data:
            try:
                campaign = Campaign.objects.get(pk=request.data['campaign_id'])
            except Campaign.DoesNotExist:
                return Response(status=404)
        else:
            return Response(status=400)

        if 'society_id' in request.data:
            try:
                society = SupplierTypeSociety.objects.get(pk=request.data['society_id'])
            except SupplierTypeSociety.DoesNotExist:
                return Response(status=404)
        else:
            return Response(status=400)'''

        serializer = AuditSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=400)


        return Response({"message": "Audit saved"}, status=200)



class AssignedAuditTempAPIListView(APIView):

    def get(self, request, format=None):
        items = AssignedAudits.objects #.filter(date=date.today()).order_by('supplier_name')
        serializer = AssignedAuditsTempSerializer(items, many=True)
        return Response({'result':serializer.data}, status=200)
