from openpyxl import load_workbook
from pathlib import Path
from rest_framework.views import APIView
from v0.ui.utils import get_supplier_id, handle_response, get_content_type, save_flyer_locations
from models import SupplierTypeSociety
from v0.ui.location.models import City
from v0.ui.account.models import ContactDetails
from v0.models import DurationType
from v0.ui.inventory.models import AdInventoryType
from v0.ui.finances.models import PriceMappingDefault

def get_state_map():
    all_city = City.objects.all()
    state_map = {}
    for city in all_city:
        state_map[city.city_code] = {'state_name': city.state_code.state_name, 'state_code': city.state_code.state_code}
    return state_map


class SocietyDataImport(APIView):
    """

    """

    def post(self, request):
        source_file = request.data['file']
        path = Path.cwd()
        wb = load_workbook(source_file)
        ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
        society_data_list = []
        for index, row in enumerate(ws.iter_rows()):
            if index > 0:
                society_data_list.append({
                    'society_name': row[0].value if row[0].value else None,
                    'society_city': str(row[1].value) if row[1].value else None,
                    'society_locality': row[2].value if row[2].value else None,
                    'society_subarea': row[3].value if row[3].value else None,
                    'supplier_code': row[4].value if row[4].value else None,
                    'society_zip': int(row[5].value) if row[5].value else None,
                    'society_latitude': float(row[6].value) if row[6].value else None,
                    'society_longitude': float(row[7].value) if row[7].value else None,
                    'tower_count': int(row[8].value) if row[8].value else None,
                    'flat_count': int(row[9].value) if row[9].value else None,
                    'designation': row[10].value if row[10].value else None,
                    'salutation': row[11].value if row[11].value else None,
                    'contact_name': row[12].value if row[12].value else None,
                    'email': row[13].value if row[13].value else None,
                    'mobile': row[14].value if row[14].value else None,
                    'name_for_payment': row[15].value if row[15].value else None,
                    'ifsc_code': row[16].value if row[16].value else None,
                    'bank_name': row[17].value if row[17].value else None,
                    'account_no': row[18].value if row[18].value else None,
                    'stall_allowed': True if row[19].value in ['Y', 'y', 't', 'T', 'true', 'True'] else False,
                    'poster_allowed_nb': True if row[20].value in ['Y', 'y', 't', 'T', 'true', 'True'] else False,
                    'nb_per_tower': int(row[21].value) if row[21].value else None,
                    'poster_allowed_lift': True if row[22].value in ['Y', 'y', 't', 'T', 'true', 'True'] else False,
                    'door_to_door': True if row[23].value in ['Y', 'y', 't', 'T', 'true', 'True'] else False,
                    'stall_price': float(row[24].value) if row[24].value else None,
                    'poster_price': float(row[25].value) if row[25].value else None,
                    'flier_price': float(row[26].value) if row[26].value else None,
                    # 'status': row[27].value,
                    # 'comment': row[27].value,
                })
        all_states_map = get_state_map()
        for society in society_data_list:
            if society['supplier_code'] is not None:
                data = {
                    'city_code': society['society_city'],
                    'area_code': society['society_locality'],
                    'subarea_code': society['society_subarea'],
                    'supplier_type': 'RS',
                    'supplier_code': society['supplier_code'],
                    'supplier_name': society['society_name']
                }
                supplier_id = get_supplier_id(data, state_name=all_states_map[society['society_city']]['state_name'],
                                              state_code=all_states_map[society['society_city']]['state_code'])
                new_society = SupplierTypeSociety(**{
                    'supplier_id': supplier_id,
                    'society_name': society['society_name'],
                    'society_locality': society['society_locality'],
                    'society_subarea': society['society_subarea'],
                    'supplier_code': society['supplier_code'],
                    'society_zip': society['society_zip'],
                    'society_latitude': society['society_latitude'],
                    'society_longitude': society['society_longitude'],
                    'tower_count': society['tower_count'],
                    'flat_count': society['flat_count'],
                    'name_for_payment': society['name_for_payment'],
                    'ifsc_code': society['ifsc_code'],
                    'bank_name': society['bank_name'],
                    'account_no': society['account_no'],
                    'stall_allowed': society['stall_allowed']
                })
                new_society.save()
                new_contact_data = {
                    'name': society['contact_name'],
                    'email': society['email'],
                    'designation': society['designation'],
                    'salutation': society['salutation'],
                    'mobile': society['mobile'],
                    'content_type': get_content_type('RS').data['data'],
                    'object_id': supplier_id
                }
                obj, is_created = ContactDetails.objects.get_or_create(**new_contact_data)
                obj.save()
                duration_type = DurationType.objects.get(days_count='1')
                adinventory_type = AdInventoryType.objects.get(adinventory_name="STALL", adinventory_type="Small")
                PriceMappingDefault.objects.get_or_create(supplier=new_society, duration_type=duration_type,
                                                          adinventory_type=adinventory_type,
                                                          actual_supplier_price=society['stall_price'],
                                                          content_type=get_content_type('RS').data['data'],
                                                          object_id=supplier_id)

                duration_type = DurationType.objects.get(days_count='3')
                adinventory_type = AdInventoryType.objects.get(adinventory_name="POSTER", adinventory_type="A4")
                PriceMappingDefault.objects.get_or_create(supplier=new_society, duration_type=duration_type,
                                                          adinventory_type=adinventory_type,
                                                          actual_supplier_price=society['poster_price'],
                                                          content_type=get_content_type('RS').data['data'],
                                                          object_id=supplier_id)
                save_flyer_locations(0, 1, new_society, society['supplier_code'])
                duration_type = DurationType.objects.get(days_count='1')
                adinventory_type = AdInventoryType.objects.get(adinventory_name="FLIER", adinventory_type="Door-to-Door")
                PriceMappingDefault.objects.get_or_create(supplier=new_society, duration_type=duration_type,
                                                          adinventory_type=adinventory_type,
                                                          actual_supplier_price=society['flier_price'],
                                                          content_type=get_content_type('RS').data['data'],
                                                          object_id=supplier_id)
        return handle_response({}, data='success', success=True)
