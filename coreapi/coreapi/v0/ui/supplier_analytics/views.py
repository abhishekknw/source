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
            supplier_count_list = []
            supplier_mapping = {
                'RS': {'name': 'Residential'},
                'RE': {
                    'model': SupplierTypeRetailShop,
                    'name': 'Retail Shop'
                },
                'CP': {
                    'model': SupplierTypeCorporate,
                    'name': 'Corporate Park'
                },
                'BS': {
                    'model': SupplierTypeBusShelter,
                    'name': 'Bus Shelter'
                },
                'SA': {
                    'model': SupplierTypeSalon,
                    'name': 'Salon'
                }
            }
            if supplier_type == 'RS':
                # Query Supplier Society
                supplier_count_list = SupplierTypeSociety.objects.values('society_city').annotate(dcount=Count('supplier_id'))
            if supplier_type in ['RE', 'CP', 'BS']:
                model = supplier_mapping[supplier_type]['model']
                supplier_count_list = model.objects.values('city').annotate(dcount=Count('supplier_id'))
            if len(supplier_count_list) > 0:
                for supplier in supplier_count_list:
                    supplier['type'] = supplier_type
                    supplier['name'] = supplier_mapping[supplier_type]['name']
            return Response(data={"status": True, "data": supplier_count_list}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response(data={"status": False, "error": "Error getting data"}, status=status.HTTP_400_BAD_REQUEST)


class GetSupplierList(APIView):
    @staticmethod
    def get(request, supplier_type):
        try:
            city = request.query_params.get('city', '')
            if not city:
                return Response(data={"status": False, "error": "City is mandatory"},
                                status=status.HTTP_400_BAD_REQUEST)
            supplier_list = []
            supplier_mapping = {
                'RE': SupplierTypeRetailShop,
                'CP': SupplierTypeCorporate,
                'BS': SupplierTypeBusShelter,
                'SA': SupplierTypeSalon
            }
            if supplier_type == 'RS':
                # Query Supplier Society
                supplier_list = SupplierTypeSociety.objects.filter(society_city__icontains=city).values('society_name','society_locality', 'society_subarea','society_address1','society_city', 'supplier_id')
            if supplier_type in ['RE', 'CP', 'BS']:
                model = supplier_mapping[supplier_type]
                supplier_list = model.objects.filter(city__icontains=city).values('name', 'area','subarea','city', 'supplier_id')
            return Response(data={"status": True, "data": supplier_list}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response(data={"status": False, "error": "Error getting data"}, status=status.HTTP_400_BAD_REQUEST)