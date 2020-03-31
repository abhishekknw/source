import logging

logger = logging.getLogger(__name__)
from django.db.models import Count

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

import v0.constants as v0_constants
from v0.ui.utils import get_model
from v0.ui.supplier.models import (SupplierTypeSociety, SupplierTypeRetailShop,
                                   SupplierTypeSalon, SupplierTypeGym,
                                   SupplierTypeCorporate, SupplierTypeBusShelter,
                                   SupplierTypeCode, RETAIL_SHOP_TYPE)
from v0.ui.account.models import ContactDetails


class GetSupplierSummary(APIView):
    @staticmethod
    def get(request):
        try:
            valid_supplier_type_code_instances = SupplierTypeCode.objects.all()
            data = {}

            for instance in valid_supplier_type_code_instances:
                supplier_type_code = instance.supplier_type_code
                error = False
                try:
                    model_name = get_model(supplier_type_code)
                    suppliers = model_name.objects.all().values('supplier_id')

                except Exception:
                    error = True
                supplier_ids = [supplier['supplier_id'] for supplier in suppliers]
                contact_name_total_filled_suppliers = []
                contact_number_total_filled_suppliers = []

                # Get contact details
                contact_details = ContactDetails.objects.filter(object_id__in=supplier_ids).values('name', 'mobile','object_id')
                if contact_details and len(contact_details) > 0:
                    for contact_detail in contact_details:
                        if contact_detail['name']:
                            contact_name_total_filled_suppliers.append(contact_detail['object_id'])
                        if contact_detail['mobile']:
                            contact_number_total_filled_suppliers.append(contact_detail['object_id'])
                contact_name_filled_suppliers = list(set(contact_name_total_filled_suppliers))
                contact_number_filled_suppliers = list(set(contact_number_total_filled_suppliers))
                data[supplier_type_code] = {
                    'supplier_count': len(supplier_ids),
                    'supplier_ids': supplier_ids,
                    'name': instance.supplier_type_name,
                    'contact_name_filled_count': len(contact_name_filled_suppliers),
                    'contact_number_filled_count': len(contact_number_filled_suppliers),
                    'contact_name_not_filled_count': len(supplier_ids) - len(contact_name_filled_suppliers),
                    'contact_number_not_filled_count': len(supplier_ids) - len(contact_name_filled_suppliers),
                    'contact_name_filled_suppliers': contact_name_filled_suppliers,
                    'contact_number_filled_suppliers': contact_number_filled_suppliers,
                    'contact_name_not_filled_suppliers': [item for item in supplier_ids if item not in contact_name_filled_suppliers],
                    'contact_number_not_filled_suppliers': [item for item in supplier_ids if item not in contact_number_filled_suppliers],
                    'contact_name_total_filled_suppliers': contact_name_total_filled_suppliers,
                    'contact_number_total_filled_suppliers': contact_number_total_filled_suppliers,
                    'contact_name_total_filled_count': len(contact_name_total_filled_suppliers),
                    'contact_number_total_filled_count': len(contact_number_total_filled_suppliers),
                    'error': error,
                }
            return Response(data={"status": True, "data": data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response(data={"status": False, "error": "Error getting data"}, status=status.HTTP_400_BAD_REQUEST)


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
                supplier_list = SupplierTypeSociety.objects.filter(society_city__icontains=city).values('society_name','society_locality', 'society_subarea',
                                                                                                      'society_address1','society_city', 'supplier_id',
                                                                                                        'society_locality', 'society_longitude', 'society_latitude', 'society_state')

            is_society = False
            if supplier_type == 'RS':
                is_society = True

            if supplier_type in ['RE', 'CP', 'BS']:
                model = supplier_mapping[supplier_type]
                supplier_list = model.objects.filter(city__icontains=city).values('name', 'area','subarea','city', 'supplier_id', 'latitude', 'longitude', 'state', 'address1')

            supplier_details_with_contact = []
            for supplier in supplier_list:
                index = 0
                # Get contact details
                contact_details = ContactDetails.objects.filter(object_id=supplier['supplier_id'])\
                    .values('object_id', 'name', 'mobile','contact_type')
                if contact_details:
                    contact_detail = contact_details[0]
                    supplier['contact_name'] = contact_detail['name']
                    supplier['contact_number'] = contact_detail['mobile']
                    supplier['contact_type'] = contact_detail['contact_type']
                    supplier_details_with_contact.append({
                        'id': index,
                        'name': supplier['society_name'] if is_society else supplier['name'],
                        'area': supplier['society_locality'] if is_society else supplier['area'],
                        'city': supplier['society_city'] if is_society else supplier['city'],
                        'subarea': supplier['society_subarea'] if is_society else supplier['subarea'],
                        'latitude': supplier['society_latitude'] if is_society else supplier['latitude'],
                        'longitude': supplier['society_longitude'] if is_society else supplier['longitude'],
                        'supplier_id': supplier['supplier_id'],
                        'state': supplier['society_state'] if is_society else supplier['state'],
                        'address': supplier['society_address1'] if is_society else supplier['address1'],
                        'contact_name': contact_detail['name'],
                        'contact_number': contact_detail['mobile'],
                        'contact_type': contact_detail['contact_type']
                    })
                else:
                    supplier_details_with_contact.append(supplier)
                    index += 1
            return Response(data={"status": True, "data": supplier_details_with_contact}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response(data={"status": False, "error": "Error getting data"}, status=status.HTTP_400_BAD_REQUEST)