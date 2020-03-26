import logging

logger = logging.getLogger(__name__)
from django.db.models import Count

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from v0.ui.supplier.models import (SupplierTypeSociety, SupplierTypeRetailShop,
                                   SupplierTypeSalon, SupplierTypeGym,
                                   SupplierTypeCorporate, SupplierTypeBusShelter)
from v0.ui.account.models import ContactDetails


class GetSupplierCitywiseCount(APIView):
    @staticmethod
    def get(request, supplier_type):
        try:
            supplier_count = []
            supplier_mapping = {
                'RE': SupplierTypeRetailShop,
                'CP': SupplierTypeCorporate,
                'BS': SupplierTypeBusShelter,
                'SA': SupplierTypeSalon
            }
            if supplier_type == 'RS':
                # Query Supplier Society
                supplier_count = SupplierTypeSociety.objects.values('society_city').annotate(dcount=Count('supplier_id'))
            if supplier_type in ['RE','CP','BS']:
                model = supplier_mapping[supplier_type]
                supplier_count = model.objects.values('city').annotate(dcount=Count('supplier_id'))
            return Response(data={"status": True, "data": supplier_count}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response(data={"status": False, "error": "Error getting data"}, status=status.HTTP_400_BAD_REQUEST)