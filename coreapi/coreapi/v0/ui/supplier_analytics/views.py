import logging
logger = logging.getLogger(__name__)

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from v0.constants import supplier_code_to_names
from v0.ui.utils import get_model, get_user_organisation_id
from v0.ui.supplier.models import (SupplierTypeSociety, SupplierTypeRetailShop,
                                   SupplierTypeSalon, SupplierTypeGym,
                                   SupplierTypeCorporate, SupplierTypeBusShelter,
                                   SupplierTypeCode, RETAIL_SHOP_TYPE)
from v0.ui.account.models import ContactDetails
from .utils import get_last_week, get_last_month, get_last_3_months, get_today_yesterday


class GetSupplierSummary(APIView):
    @staticmethod
    def get(request):
        try:
            organisation_id = get_user_organisation_id(request.user)
            # Visible only for machadalo users
            if organisation_id != 'MAC1421':
                return Response(data={"status": False, "error": "Permission Error"},
                                status=status.HTTP_400_BAD_REQUEST)
            valid_supplier_type_code_instances = SupplierTypeCode.objects.all()
            data = {}
            for instance in valid_supplier_type_code_instances:
                supplier_type_code = instance.supplier_type_code
                error = False
                try:
                    model_name = get_model(supplier_type_code)
                    suppliers = model_name.objects.all().values('supplier_id', 'created_at')
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
                    'contact_number_not_filled_count': len(supplier_ids) - len(contact_number_filled_suppliers),
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
            organisation_id = get_user_organisation_id(request.user)
            # Visible only for machadalo users
            if organisation_id != 'MAC1421':
                return Response(data={"status": False, "error": "Permission Error"},
                                status=status.HTTP_400_BAD_REQUEST)
            try:
                model = get_model(supplier_type)
            except Exception:
                return Response(data={"status": False, "error": 'Error getting model'}, status=status.HTTP_400_BAD_REQUEST)
            is_society = False
            if supplier_type == 'RS':
                is_society = True
                # Query Supplier Society
                suppliers = SupplierTypeSociety.objects.values('supplier_id', 'society_city', 'flat_count', 'created_at')
            else:
                suppliers = model.objects.values('supplier_id', 'city', 'created_at')

            supplier_dict_with_cities = {}

            # Get last monday
            last_monday, last_sunday, this_monday, today = get_last_week()
            last_month_start, last_month_end, this_month_start = get_last_month()
            first_month_start = get_last_3_months()
            yest_today = get_today_yesterday()
            today = yest_today[0]
            yesterday = yest_today[1]
            day_before_yesterday = yest_today[2]
            for supplier in suppliers:
                city = supplier['society_city'] if is_society else supplier['city']

                if city not in supplier_dict_with_cities:
                    supplier_dict_with_cities[city] = {}
                    supplier_dict_with_cities[city]['count'] = 1
                    supplier_dict_with_cities[city]['supplier_ids'] = []
                    supplier_dict_with_cities[city]['contact_details'] = []
                    supplier_dict_with_cities[city]['supplier_ids'].append(supplier['supplier_id'])
                    supplier_dict_with_cities[city]['this_month_count'] = 0
                    supplier_dict_with_cities[city]['this_week_count'] = 0
                    supplier_dict_with_cities[city]['last_week_count'] = 0
                    supplier_dict_with_cities[city]['last_month_count'] = 0
                    supplier_dict_with_cities[city]['last_3_month_count'] = 0
                    supplier_dict_with_cities[city]['last_day_count'] = 0
                    supplier_dict_with_cities[city]['today_count'] = 0
                    if supplier['created_at']:
                        if last_monday <= supplier['created_at'].date() <= last_sunday:
                            supplier_dict_with_cities[city]['last_week_count'] += 1
                        if this_monday <= supplier['created_at'].date() <= today:
                            supplier_dict_with_cities[city]['this_week_count'] += 1
                        # Get monthwise data
                        if last_month_start <= supplier['created_at'].date() <= last_month_end:
                            supplier_dict_with_cities[city]['last_month_count'] += 1
                        if this_month_start <= supplier['created_at'].date() <= today:
                            supplier_dict_with_cities[city]['this_month_count'] += 1
                        # Get last 3 months data
                        if first_month_start <= supplier['created_at'].date() <= last_month_end:
                            supplier_dict_with_cities[city]['last_3_month_count'] += 1
                        # Get yesterdays data
                        if day_before_yesterday < supplier['created_at'].date() < today:
                            supplier_dict_with_cities[city]['last_day_count'] += 1
                        # Get todays data
                        if supplier['created_at'].date() > yesterday:
                            supplier_dict_with_cities[city]['today_count'] += 1
                else:
                    if supplier['created_at']:
                        if last_monday <= supplier['created_at'].date() <= last_sunday:
                            supplier_dict_with_cities[city]['last_week_count'] += 1
                        if this_monday <= supplier['created_at'].date() <= today:
                            supplier_dict_with_cities[city]['this_week_count'] += 1
                        # Get monthwise data
                        if last_month_start <= supplier['created_at'].date() <= last_month_end:
                            supplier_dict_with_cities[city]['last_month_count'] += 1
                        if this_month_start <= supplier['created_at'].date() <= today:
                            supplier_dict_with_cities[city]['this_month_count'] += 1
                        # Get last 3 months data
                        if first_month_start <= supplier['created_at'].date() <= last_month_end:
                            supplier_dict_with_cities[city]['last_3_month_count'] += 1
                        # Get yesterdays data
                        if day_before_yesterday < supplier['created_at'].date() < today:
                            supplier_dict_with_cities[city]['last_day_count'] += 1
                        # Get todays data
                        if supplier['created_at'].date() > yesterday:
                            supplier_dict_with_cities[city]['today_count'] += 1
                    supplier_dict_with_cities[city]['count'] += 1
                    supplier_dict_with_cities[city]['supplier_ids'].append(supplier['supplier_id'])

                # Add type & name
                supplier_dict_with_cities[city]['type'] = supplier_type
                supplier_dict_with_cities[city]['name'] = supplier_code_to_names[supplier_type]

            for city in supplier_dict_with_cities.keys():
                supplier_dict_with_cities[city]['contact_details'] = []
                supplier_dict_with_cities[city]['contact_name_total_filled_suppliers'] = []
                supplier_dict_with_cities[city]['contact_number_total_filled_suppliers'] = []
                supplier_dict_with_cities[city]['contact_number_decision_total_filled_suppliers'] = []
                # Get contact details
                contact_details = ContactDetails.objects.filter(object_id__in=supplier_dict_with_cities[city]['supplier_ids']).values('name', 'mobile', 'object_id', 'contact_type')
                if contact_details:
                    supplier_dict_with_cities[city]['contact_details'].append(contact_details)
                    for contact_detail in contact_details:
                        if contact_detail['name']:
                            supplier_dict_with_cities[city]['contact_name_total_filled_suppliers'].append(contact_detail['object_id'])
                        if contact_detail['mobile']:
                            supplier_dict_with_cities[city]['contact_number_total_filled_suppliers'].append(contact_detail['object_id'])
                        if contact_detail['contact_type'] in ['Chairman', 'Committe Member', 'Committee Member', 'Cultural Secretary', 'Decision Maker',
                                            'Joint Secretary', 'President', 'Secretary', 'Secretary/ President', 'Treasurer', 'Vice President']:
                            supplier_dict_with_cities[city]['contact_number_decision_total_filled_suppliers'].append(contact_detail['object_id'])

                contact_name_filled_suppliers = list(set(supplier_dict_with_cities[city]['contact_name_total_filled_suppliers']))
                contact_number_filled_suppliers = list(set(supplier_dict_with_cities[city]['contact_number_total_filled_suppliers']))
                contact_number_decision_filled_suppliers = list(set(supplier_dict_with_cities[city]['contact_number_decision_total_filled_suppliers']))
                contact_name_not_filled_suppliers = [item for item in supplier_dict_with_cities[city]['supplier_ids'] if item not in contact_name_filled_suppliers]
                contact_number_not_filled_suppliers = [item for item in supplier_dict_with_cities[city]['supplier_ids'] if item not in contact_number_filled_suppliers]
                contact_number_decision_not_filled_suppliers = [item for item in supplier_dict_with_cities[city]['supplier_ids'] if item not in contact_number_decision_filled_suppliers]

                supplier_dict_with_cities[city]['contact_name_filled_suppliers'] = contact_name_filled_suppliers
                supplier_dict_with_cities[city]['contact_number_filled_suppliers'] = contact_number_filled_suppliers
                supplier_dict_with_cities[city]['contact_number_decision_filled_suppliers'] = contact_number_decision_filled_suppliers
                supplier_dict_with_cities[city]['contact_name_not_filled_suppliers'] = contact_name_not_filled_suppliers
                supplier_dict_with_cities[city]['contact_number_not_filled_suppliers'] = contact_number_not_filled_suppliers
                supplier_dict_with_cities[city]['contact_number_decision_not_filled_suppliers'] = contact_number_decision_not_filled_suppliers
                supplier_dict_with_cities[city]['contact_name_filled_count'] = len(contact_name_filled_suppliers)
                supplier_dict_with_cities[city]['contact_number_filled_count'] = len(contact_number_filled_suppliers)
                supplier_dict_with_cities[city]['contact_number_decision_filled_count'] = len(contact_number_decision_filled_suppliers)
                supplier_dict_with_cities[city]['contact_name_not_filled_count'] = len(contact_name_not_filled_suppliers)
                supplier_dict_with_cities[city]['contact_number_not_filled_count'] = len(contact_number_not_filled_suppliers)
                supplier_dict_with_cities[city]['contact_number_decision_not_filled_count'] = len(contact_number_decision_not_filled_suppliers)
                supplier_dict_with_cities[city]['contact_number_total_filled_count'] = len(supplier_dict_with_cities[city]['contact_number_total_filled_suppliers'])
                supplier_dict_with_cities[city]['contact_name_total_filled_count'] = len(supplier_dict_with_cities[city]['contact_name_total_filled_suppliers'])
                supplier_dict_with_cities[city]['contact_number_decision_total_filled_count'] = len(supplier_dict_with_cities[city]['contact_number_decision_total_filled_suppliers'])
            return Response(data={"status": True, "data": supplier_dict_with_cities}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response(data={"status": False, "error": "Error getting data"}, status=status.HTTP_400_BAD_REQUEST)


class GetSupplierList(APIView):
    @staticmethod
    def get(request, supplier_type):
        try:
            organisation_id = get_user_organisation_id(request.user)
            # Visible only for machadalo users
            if organisation_id != 'MAC1421':
                return Response(data={"status": False, "error": "Permission Error"},
                                status=status.HTTP_400_BAD_REQUEST)
            city = request.query_params.get('city', '')
            is_society = False
            if not city:
                return Response(data={"status": False, "error": "City is mandatory"},
                                status=status.HTTP_400_BAD_REQUEST)
            try:
                model = get_model(supplier_type)
            except Exception:
                return Response(data={"status": False, "error": 'Error getting model'}, status=status.HTTP_400_BAD_REQUEST)
            if supplier_type == 'RS':
                is_society = True
                # Query Supplier Society
                supplier_list = model.objects.filter(society_city__icontains=city).values('society_name','society_locality', 'society_subarea',
                                                                                          'society_address1','society_city', 'supplier_id',
                                                                                          'society_locality', 'society_longitude', 'society_latitude',
                                                                                          'society_state', 'society_type_quality', 'flat_count')
            else:
                supplier_list = model.objects.filter(city__icontains=city).values('name', 'area','subarea','city', 'supplier_id', 'latitude', 'longitude', 'state', 'address1')

            supplier_details_with_contact = []
            for supplier in supplier_list:
                index = 0
                supplier_object = {
                    'id': index,
                    'supplier_id': supplier['supplier_id'],
                    'name': supplier['society_name'] if is_society else supplier['name'],
                    'area': supplier['society_locality'] if is_society else supplier['area'],
                    'city': supplier['society_city'] if is_society else supplier['city'],
                    'subarea': supplier['society_subarea'] if is_society else supplier['subarea'],
                    'latitude': supplier['society_latitude'] if is_society else supplier['latitude'],
                    'longitude': supplier['society_longitude'] if is_society else supplier['longitude'],
                    'state': supplier['society_state'] if is_society else supplier['state'],
                    'address': supplier['society_address1'] if is_society else supplier['address1'],
                    'flat_count': supplier['flat_count'] if is_society else None,
                    'society_type': supplier['society_type_quality'] if is_society else None,
                    'is_society': is_society if is_society else False
                }
                # Get contact details
                contact_details = ContactDetails.objects.filter(object_id=supplier['supplier_id'])\
                    .values('object_id', 'name', 'mobile','contact_type')
                if contact_details:
                    contact_detail = contact_details[0]
                    supplier_object['contact_name'] = contact_detail['name']
                    supplier_object['contact_number'] = contact_detail['mobile']
                    supplier_object['contact_type'] = contact_detail['contact_type']
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
                        'flat_count': supplier['flat_count'] if is_society else None,
                        'society_type': supplier['society_type_quality'] if is_society else None,
                        'contact_name': contact_detail['name'],
                        'contact_number': contact_detail['mobile'],
                        'contact_type': contact_detail['contact_type'],
                        'is_society': is_society if is_society else False
                    })
                else:
                    supplier_details_with_contact.append(supplier_object)
                    index += 1
            return Response(data={"status": True, "data": supplier_details_with_contact}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response(data={"status": False, "error": "Error getting data"}, status=status.HTTP_400_BAD_REQUEST)