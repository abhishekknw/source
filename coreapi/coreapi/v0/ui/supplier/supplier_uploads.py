from __future__ import print_function
from __future__ import absolute_import
from openpyxl import load_workbook
from rest_framework.views import APIView
from v0.ui.utils import (get_supplier_id, handle_response, get_content_type, save_flyer_locations, make_supplier_data,
                         get_model, get_serializer, save_supplier_data, get_region_based_query, get_supplier_image,
                         save_basic_supplier_details)
from .models import (SupplierTypeSociety, SupplierAmenitiesMap, SupplierTypeCorporate, SupplierTypeGym,
                    SupplierTypeRetailShop, CorporateParkCompanyList, CorporateBuilding, SupplierTypeBusDepot,
                    SupplierTypeCode, SupplierTypeBusShelter, CorporateCompanyDetails, RETAIL_SHOP_TYPE, SupplierMaster, AddressMaster)
from .serializers import SupplierMasterSerializer
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

        cities = City.objects.all()
        city_dict = {row.city_name:row.id for row in cities}

        areas = CityArea.objects.all()
        area_dict = {row.label:row.id for row in areas}

        subareas = CitySubArea.objects.all()
        subarea_dict = {row.subarea_name:row.id for row in subareas}

        source_file = request.data['file']
        wb = load_workbook(source_file)
        ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
        cp_data_list = []
        for index, row in enumerate(ws.iter_rows()):
            if index > 0:

                supplier_data1 = {
                    'city_id': city_dict.get(row[6].value),
                    'area_id': area_dict.get(row[4].value),
                    'subarea_id': subarea_dict.get(row[5].value),
                    'supplier_type': row[1].value,
                    'supplier_code': row[1].value,
                    'supplier_name': row[0].value,    
                }
                supplier_id = get_supplier_id(supplier_data1)

                
                if row[1].value != "RS":
                    supplier = SupplierMaster.objects.filter(supplier_name=row[0].value).first()
                    if supplier:
                        continue
                if row[1].value == "RS":
                    supplier = SupplierTypeSociety.objects.filter(society_name=row[0].value).first()
                    if supplier:
                        continue

                supplier_data = {
                    'supplier_id': supplier_id,
                    'supplier_name': row[0].value,
                    'supplier_type': row[1].value,
                    'unit_primary_count': row[2].value,
                    'representative': request.user.profile.organisation.organisation_id,
                    'unit_secondary_count': row[3].value,
                    'area': row[4].value,
                    'city': row[6].value,
                    'state': row[7].value,
                    'subarea': row[5].value,
                    'zipcode': row[8].value,
                    'address1': row[9].value,
                    'landmark': row[10].value,
                    'latitude': row[11].value,
                    'longitude': row[12].value,
                    'feedback': row[13].value,
                    'quality_rating': row[14].value,
                    'locality_rating': row[15].value,
                    'quantity_rating': row[16].value,
                }

                if row[1].value != "RS":
                    serializer = SupplierMasterSerializer(data=supplier_data)
                    if serializer.is_valid():
                        serializer.save()

                    AddressMaster(**{
                        'supplier_id': supplier_id,
                        'area': row[4].value,
                        'city': row[6].value,
                        'state': row[7].value,
                        'subarea': row[5].value,
                        'zipcode': row[8].value,
                        'address1': row[9].value,
                        'nearest_landmark': row[10].value,
                        'latitude': row[11].value,
                        'longitude': row[12].value,
                    }).save()

                ui_utils.create_supplier_from_master(supplier_data, row[1].value)

        return handle_response({}, data='success', success=True)
