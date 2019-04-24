from __future__ import print_function
from __future__ import absolute_import
from openpyxl import load_workbook
from rest_framework.views import APIView
from v0.ui.utils import (get_supplier_id, handle_response, get_content_type, save_flyer_locations, make_supplier_data,
                         get_model, get_serializer, save_supplier_data, get_region_based_query, get_supplier_image,
                         save_basic_supplier_details)
from .models import (SupplierTypeSociety, SupplierAmenitiesMap, SupplierTypeCorporate, SupplierTypeGym,
                    SupplierTypeRetailShop, CorporateParkCompanyList, CorporateBuilding, SupplierTypeBusDepot,
                    SupplierTypeCode, SupplierTypeBusShelter, CorporateCompanyDetails, RETAIL_SHOP_TYPE)
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from v0.ui.finances.models import PriceMappingDefault
from v0.ui.location.models import State, City, CityArea, CitySubArea
from v0.ui.inventory.models import AdInventoryType, InventorySummary
from v0.ui.base.models import DurationType
import v0.ui.utils as ui_utils
from v0.ui.utils import get_from_dict
from v0.ui.controller import inventory_summary_insert
from django.core.exceptions import ObjectDoesNotExist


def get_state_map():
    all_city = City.objects.all()
    state_map = {}
    for city in all_city:
        state_map[city.city_code] = {'state_name': city.state_code.state_name, 'state_code': city.state_code.state_code}
    return state_map


def create_price_mapping_default(days_count, adinventory_name, adinventory_type, new_supplier,
                                 actual_supplier_price, content_type, supplier_id):
    duration_types = DurationType.objects.filter()
    adinventory_types = AdInventoryType.objects.filter(adinventory_name=adinventory_name)
    for adinv_type in adinventory_types:
        for dur_type in duration_types:
            if dur_type.days_count == days_count and adinv_type.adinventory_name == adinventory_name and adinv_type.adinventory_type == adinventory_type:
                obj,created = PriceMappingDefault.objects.get_or_create(supplier=new_supplier.supplier_id, duration_type=dur_type,
                                              adinventory_type=adinv_type,
                                              content_type=content_type,
                                              object_id=supplier_id)

                obj.actual_supplier_price = actual_supplier_price
                obj.save()
            else:
                if (adinv_type.adinventory_name == 'FLIER' and dur_type.duration_name == 'Unit Daily') or adinv_type.adinventory_name != 'FLIER':
                    PriceMappingDefault.objects.get_or_create(supplier=new_supplier, duration_type=dur_type,
                                                          adinventory_type=adinv_type,
                                                          content_type=content_type,
                                                          object_id=supplier_id)


@method_decorator(csrf_exempt, name='dispatch')
class CorporateParkDataImport(APIView):
    """

    """

    def post(self, request):
        source_file = request.data['file']
        wb = load_workbook(source_file)
        ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
        cp_data_list = []
        for index, row in enumerate(ws.iter_rows()):
            if index > 0:
                cp_data_list.append({
                    'name': row[0].value if row[0].value else None,
                    'city': str(row[1].value) if row[1].value else None,
                    'city_code': str(row[2].value) if row[2].value else None,
                    'area': row[3].value if row[3].value else None,
                    'area_code': row[4].value if row[4].value else None,
                    'subarea': row[5].value if row[5].value else None,
                    'subarea_code': row[6].value if row[6].value else None,
                    'code': row[7].value if row[7].value else None,
                    'supplier_code': row[8].value if row[8].value else None,
                    'supplier_id': row[9].value if row[9].value else None,
                    'zipcode': int(row[10].value) if row[10].value else None,
                    'address1': row[11].value if row[11].value else None,
                    'landmark': row[12].value if row[12].value else None,
                    'latitude': float(row[13].value) if row[13].value else None,
                    'longitude': float(row[14].value) if row[14].value else None,
                    'tower_count': int(row[15].value) if row[15].value else None,
                    'designation': row[16].value if row[16].value else None,
                    'salutation': row[17].value if row[17].value else None,
                    'contact_name': row[18].value if row[18].value else None,
                    'email': row[19].value if row[19].value else None,
                    'mobile': row[20].value if row[20].value else None,
                    'landline': row[21].value if row[21].value else None,
                    'name_for_payment': row[22].value if row[22].value else None,
                    'ifsc_code': row[23].value if row[23].value else None,
                    'bank_name': row[24].value if row[24].value else None,
                    'account_no': row[25].value if row[25].value else None,
                    'relationship_manager' : row[26].value if row[26].value else None,
                    'stall_allowed': True if row[27].value in ['Y', 'y', 't', 'T', 'true', 'True'] else False,
                    'total_stall_count': row[28].value if row[28].value else None,
                    'poster_allowed_nb': True if row[29].value in ['Y', 'y', 't', 'T', 'true', 'True'] else False,
                    'nb_per_tower': int(row[30].value) if row[30].value else None,
                    'poster_allowed_lift': True if row[31].value in ['Y', 'y', 't', 'T', 'true', 'True'] else False,
                    'lift_per_tower': int(row[32].value) if row[32].value else None,
                    'stall_price': float(row[33].value) if row[33].value else None,
                    'poster_price': float(row[34].value) if row[34].value else None,
                    'status': row[35].value,
                    'comments': row[36].value,
                })
        all_states_map = get_state_map()
        for supplier in cp_data_list:
            if supplier['supplier_code'] is not None:
                data = {
                    'city_code': supplier['city_code'],
                    'area_code': supplier['area_code'],
                    'subarea_code': supplier['subarea_code'],
                    'supplier_type': 'CP',
                    'supplier_code': supplier['supplier_code'],
                    'supplier_name': supplier['name']
                }
                supplier_id = None
                if supplier['supplier_id']:
                    supplier_id = supplier['supplier_id']
                else:
                    supplier_id = get_supplier_id(data)
                supplier_length = len(SupplierTypeSociety.objects.filter(supplier_id=supplier_id))
                if supplier_length or len(SupplierTypeCorporate.objects.filter(name=supplier['name'])):
                    instance = SupplierTypeCorporate.objects.filter(name=supplier['name'])[0]
                    instance.name = supplier['name']
                    instance.area = supplier['area']
                    instance.city = supplier['city']
                    instance.state = all_states_map[supplier['city_code']]['state_name']
                    instance.subarea = supplier['subarea']
                    instance.supplier_code = supplier['supplier_code']
                    instance.zipcode = supplier['zipcode']
                    instance.address1 = supplier['address1']
                    instance.landmark = supplier['landmark']
                    instance.latitude = supplier['latitude']
                    instance.longitude = supplier['longitude']
                    instance.tower_count = supplier['tower_count']
                    instance.name_for_payment = supplier['name_for_payment']
                    instance.ifsc_code = supplier['ifsc_code']
                    instance.bank_name = supplier['bank_name']
                    instance.account_number = supplier['account_no']
                    instance.relationship_manager = supplier['relationship_manager']
                    instance.stall_allowed = supplier['stall_allowed']
                    instance.supplier_status = supplier['status']
                    instance.comments = supplier['comments']
                    instance.save()
                    new_supplier = instance

                else:
                    new_supplier = SupplierTypeCorporate(**{
                        'supplier_id': supplier_id,
                        'name': supplier['name'],
                        'area': supplier['area'],
                        'city': supplier['city'],
                        'state': all_states_map[supplier['city_code']]['state_name'],
                        'subarea': supplier['subarea'],
                        'supplier_code': supplier['supplier_code'],
                        'zipcode': supplier['zipcode'],
                        'address1': supplier['address1'],
                        'landmark': supplier['landmark'],
                        'latitude': supplier['latitude'],
                        'longitude': supplier['longitude'],
                        'tower_count': supplier['tower_count'],
                        'name_for_payment': supplier['name_for_payment'],
                        'ifsc_code': supplier['ifsc_code'],
                        'bank_name': supplier['bank_name'],
                        'account_number': supplier['account_no'],
                        'relationship_manager': supplier['relationship_manager'],
                        'stall_allowed': supplier['stall_allowed'],
                        'supplier_status': supplier['status'],
                        'comments': supplier['comments'],
                    })
                    new_supplier.save()

                # new_contact_data = {
                #     'name': society['contact_name'],
                #     'email': society['email'],
                #     'designation': society['designation'],
                #     'salutation': society['salutation'],
                #     'mobile': society['mobile'],
                #     'landline': society['landline'],
                #     'content_type': get_content_type('RS').data['data'],
                #     'object_id': supplier_id
                # }
                # obj, is_created = ContactDetails.objects.get_or_create(**new_contact_data)
                # obj.save()

                cp_content_type = get_content_type('CP').data['data']
                create_price_mapping_default('7', "POSTER", "A4", new_supplier,
                                             supplier['poster_price'], cp_content_type, supplier_id)
                create_price_mapping_default('0', "POSTER LIFT", "A4", new_supplier,
                                             0, cp_content_type, supplier_id)
                create_price_mapping_default('0', "STANDEE", "Small", new_supplier,
                                             0, cp_content_type, supplier_id)
                create_price_mapping_default('1', "STALL", "Small", new_supplier,
                                             supplier['stall_price'], cp_content_type, supplier_id)
                create_price_mapping_default('0', "CAR DISPLAY", "A4", new_supplier,
                                             0, cp_content_type, supplier_id)
                inventory_obj = InventorySummary.objects.filter(object_id=supplier_id).first()
                inventory_id = inventory_obj.id if inventory_obj else None
                request_data = {
                    'id': inventory_id,
                    'd2d_allowed': True,
                    'poster_allowed_nb': True,
                    'supplier_type_code': 'CP',
                    'lift_count': supplier['tower_count'] * supplier['lift_per_tower'] if supplier['tower_count'] and society['lift_per_tower'] else None,
                    'stall_allowed': True,
                    'object_id': supplier_id,
                    'nb_count': supplier['tower_count'] * supplier['nb_per_tower'] if supplier['tower_count'] and supplier['nb_per_tower'] else None,
                    'user': 1,
                    'content_type': 47,
                    'total_stall_count': supplier['total_stall_count'] if supplier['total_stall_count'] else None,
                    'poster_allowed_lift': True,
                }
                class_name = self.__class__.__name__
                response = ui_utils.get_supplier_inventory(request_data.copy(), supplier_id)
                supplier_inventory_data = response.data['data']['request_data']

                if not response.data['status']:
                    return response

                supplier_inventory_data = response.data['data']['request_data']
                final_data = {
                    'id': get_from_dict(request_data, supplier_id),
                    'supplier_object': get_from_dict(response.data['data'], 'supplier_object'),
                    'inventory_object': get_from_dict(response.data['data'], 'inventory_object'),
                    'supplier_type_code': get_from_dict(request_data, 'supplier_type_code'),
                    'poster_allowed_nb': get_from_dict(request_data, 'poster_allowed_nb'),
                    'nb_count': get_from_dict(request_data, 'nb_count'),
                    'poster_campaign': get_from_dict(request_data, 'poster_campaign'),
                    'lift_count': get_from_dict(request_data, 'lift_count'),
                    'poster_allowed_lift': get_from_dict(request_data, 'poster_allowed_lift'),
                    'standee_allowed': get_from_dict(request_data, 'standee_allowed'),
                    'total_standee_count': get_from_dict(request_data, 'total_standee_count'),
                    'stall_allowed': get_from_dict(request_data, 'stall_allowed'),
                    'total_stall_count': get_from_dict(request_data, 'total_stall_count'),
                }
                try:
                    inventory_summary_insert(final_data, supplier_inventory_data)
                except ObjectDoesNotExist as e:
                    print(e)
                    # return ui_utils.handle_response(class_name, exception_object=e, request=request)
                except Exception as e:
                    print(e)
                    # return Response(data={"status": False, "error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
        return handle_response({}, data='success', success=True)
