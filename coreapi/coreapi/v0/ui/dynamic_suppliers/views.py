from __future__ import absolute_import
import redis
from rest_framework.views import APIView
from v0.ui.utils import handle_response, get_user_organisation_id, create_validation_msg
from .models import BaseSupplySupplierType, SupplySupplierType, SupplySupplier
from bson.objectid import ObjectId
from datetime import datetime
from .utils import validate_supplier_type_data, validate_with_supplier_type
from v0.ui.supplier.models import (SupplierTypeSociety)
from v0.ui.proposal.models import (ShortlistedSpaces)
from v0.ui.inventory.serializers import (ShortlistedSpacesSerializer, ShortlistedInventoryPricingDetailsSerializer)
from v0.ui.dynamic_booking.models import BookingData, BookingInventoryActivity
from v0.ui.supplier.serializers import SupplierTypeSocietySerializer, SupplierTypeSocietySerializer2
from v0.ui.dynamic_booking.models import BaseBookingTemplate, BookingTemplate, BookingData, BookingInventory
from v0.ui.finances.models import ShortlistedInventoryPricingDetails
from v0.ui.inventory.models import InventoryActivityImage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def get_paginated_result(data, entries, page):
    paginator = Paginator(data, entries)
    try:
        result = paginator.page(int(page))
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    return result

class SupplierType(APIView):
    @staticmethod
    def post(request):
        name = request.data['name'] if 'name' in request.data else False
        is_global = request.data['is_global'] if 'is_global' in request.data else False
        supplier_attributes = request.data['supplier_attributes'] if 'supplier_attributes' in request.data else False
        organisation_id = get_user_organisation_id(request.user)
        base_supplier_type_id = request.data['base_supplier_type_id'] if 'base_supplier_type_id' in request.data else False
        dict_of_req_attributes = {"name": name, "supplier_attributes": supplier_attributes,
                                  "organisation_id": organisation_id, "base_supplier_type_id": base_supplier_type_id}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)
        supplier_type_dict = dict_of_req_attributes
        supplier_type_dict["is_global"] = is_global
        supplier_type_dict["created_at"] = datetime.now()
        supplier_type_dict["inventory_list"] = request.data['inventory_list'] if 'inventory_list' in request.data else []
        supplier_type_dict["additional_attributes"] = request.data[
            'additional_attributes'] if 'additional_attributes' in request.data else {}
        is_valid_adv, validation_msg_dict_adv = validate_supplier_type_data(supplier_type_dict)
        if not is_valid_adv:
            return handle_response('', data=validation_msg_dict_adv, success=False)
        SupplySupplierType(**supplier_type_dict).save()
        return handle_response('', data={"success": True}, success=True)

    @staticmethod
    def get(request):
        all_supply_supplier_type = SupplySupplierType.objects.all()
        all_supply_supplier_type_dict = {}
        for supply_supplier_type in all_supply_supplier_type:
            all_supply_supplier_type_dict[str(supply_supplier_type._id)] = {
                "id": str(supply_supplier_type._id),
                "base_supplier_type_id": str(supply_supplier_type.base_supplier_type_id),
                "name": supply_supplier_type.name,
                "supplier_attributes": supply_supplier_type.supplier_attributes,
                "inventory_list":supply_supplier_type.inventory_list,
                "additional_attributes": supply_supplier_type.additional_attributes
            }
        return handle_response('', data=all_supply_supplier_type_dict, success=True)


class SupplierTypeById(APIView):
    @staticmethod
    def get(request, supplier_type_id):
        supply_supplier_type = SupplySupplierType.objects.raw({'_id':ObjectId(supplier_type_id)})[0]
        supply_supplier_type = {
            "id": str(supply_supplier_type._id),
            "base_supplier_type_id": str(supply_supplier_type.base_supplier_type_id),
            "name": supply_supplier_type.name,
            "supplier_attributes": supply_supplier_type.supplier_attributes,
            "inventory_list": supply_supplier_type.inventory_list,
            "additional_attributes": supply_supplier_type.additional_attributes
        }
        return handle_response('', data=supply_supplier_type, success=True)


    @staticmethod
    def put(request, supplier_type_id):
        new_name = request.data['name'] if 'name' in request.data else None
        new_attributes = request.data['supplier_attributes'] if 'supplier_attributes' in request.data else None
        is_global = request.data['is_global'] if 'is_global' in request.data else False
        base_supplier_type_id = request.data['base_supplier_type_id'] if 'base_supplier_type_id' in request.data else False
        dict_of_req_attributes = {"name": new_name, "supplier_attributes": new_attributes,
                                  "base_supplier_type_id": base_supplier_type_id}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)
        supplier_type_dict = dict_of_req_attributes
        supplier_type_dict["is_global"] = is_global
        supplier_type_dict["updated_at"] = datetime.now()
        if 'inventory_list' in request.data:
            supplier_type_dict["inventory_list"] = request.data['inventory_list']
        if 'additional_attributes' in request.data:
            supplier_type_dict["additional_attributes"] = request.data['additional_attributes']
        is_valid_adv, validation_msg_dict_adv = validate_supplier_type_data(supplier_type_dict)
        if not is_valid_adv:
            return handle_response('', data=validation_msg_dict_adv, success=False)
        print(supplier_type_dict)
        SupplySupplierType.objects.raw({'_id': ObjectId(supplier_type_id)}).update({"$set": supplier_type_dict})
        return handle_response('', data="success", success=True)


    @staticmethod
    def delete(request, supplier_type_id):
        exist_supplier_query = SupplySupplierType.objects.raw({'_id': ObjectId(supplier_type_id)})[0]
        exist_supplier_query.delete()
        return handle_response('', data="success", success=True)


class Supplier(APIView):
    @staticmethod
    def post(request):
        name = request.data['name'] if 'name' in request.data else None
        supplier_type_id = request.data['supplier_type_id'] if 'supplier_type_id' in request.data else None
        is_custom = request.data['is_custom'] if 'is_custom' in request.data else None
        supplier_attributes = request.data['supplier_attributes']
        organisation_id = get_user_organisation_id(request.user)
        dict_of_req_attributes = {"name": name, "supplier_type_id": supplier_type_id, "is_custom": is_custom,
                                  "supplier_attributes": supplier_attributes, "organisation_id": organisation_id}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)
        supplier_dict = dict_of_req_attributes
        supplier_dict['created_by'] = request.user.id
        supplier_dict['created_at'] = datetime.now()
        supplier_dict["inventory_list"] = request.data['inventory_list'] if 'inventory_list' in request.data else []
        supplier_dict["additional_attributes"] = request.data['additional_attributes'] if 'additional_attributes' in request.data else {}


        (is_valid_adv, validation_msg_dict_adv) = validate_with_supplier_type(supplier_dict,supplier_type_id)
        if not is_valid_adv:
            return handle_response('', data=validation_msg_dict_adv, success=False)
        SupplySupplier(**supplier_dict).save()
        return handle_response('', data={"success": True}, success=True)


    @staticmethod
    def get(request):
        all_supply_supplier = SupplySupplier.objects.all()

        page = request.query_params.get('page', 1)
        entries = 10000
        suppliers = get_paginated_result(all_supply_supplier, entries, page)

        all_supply_supplier_dict = {}
        for supply_supplier in suppliers:
            all_supply_supplier_dict[str(supply_supplier._id)] = {
                "id": str(supply_supplier._id),
                "supplier_type_id": str(supply_supplier.supplier_type_id),
                "name": supply_supplier.name,
                "supplier_attributes": supply_supplier.supplier_attributes,
                "additional_attributes": supply_supplier.additional_attributes,
                "inventory_list": supply_supplier.inventory_list,
                "is_custom": supply_supplier.is_custom,
                "organisation_id": supply_supplier.organisation_id,
                "created_by": supply_supplier.created_by,
                "created_at": supply_supplier.created_at,
            }
        return handle_response('', data=all_supply_supplier_dict, success=True)


class SupplierById(APIView):
    @staticmethod
    def get(request, supplier_id):
        supply_supplier = SupplySupplier.objects.raw({'_id':ObjectId(supplier_id)})[0]
        supply_supplier = {
            "id": str(supply_supplier._id),
            "supplier_type_id": str(supply_supplier.supplier_type_id),
            "name": supply_supplier.name,
            "supplier_attributes": supply_supplier.supplier_attributes,
            "additional_attributes": supply_supplier.additional_attributes,
            "inventory_list": supply_supplier.inventory_list,
            "is_custom": supply_supplier.is_custom,
            "organisation_id": supply_supplier.organisation_id,
            "created_by": supply_supplier.created_by,
            "created_at": supply_supplier.created_at,
        }
        return handle_response('', data=supply_supplier, success=True)

    @staticmethod
    def put(request, supplier_id):
        name = request.data['name'] if 'name' in request.data else None
        supplier_type_id = request.data['supplier_type_id'] if 'supplier_type_id' in request.data else None
        is_custom = request.data['is_custom'] if 'is_custom' in request.data else None
        supplier_attributes = request.data['supplier_attributes']
        additional_attributes = request.data['additional_attributes']
        organisation_id = get_user_organisation_id(request.user)
        dict_of_req_attributes = {"name": name, "supplier_type_id": supplier_type_id, "is_custom": is_custom,
                                  "supplier_attributes": supplier_attributes, "organisation_id": organisation_id,
                                  "additional_attributes": additional_attributes}
        (is_valid, validation_msg_dict) = create_validation_msg(dict_of_req_attributes)
        if not is_valid:
            return handle_response('', data=validation_msg_dict, success=False)
        supplier_dict = dict_of_req_attributes
        supplier_dict['updated_at'] = datetime.now()
        if 'inventory_list' in request.data:
            supplier_dict["inventory_list"] = request.data['inventory_list']
        (is_valid_adv, validation_msg_dict_adv) = validate_with_supplier_type(supplier_dict, supplier_type_id)
        if not is_valid_adv:
            return handle_response('', data=validation_msg_dict_adv, success=False)
        SupplySupplier.objects.raw({'_id': ObjectId(supplier_id)}).update({"$set": supplier_dict})
        return handle_response('', data={"success": True}, success=True)


    @staticmethod
    def delete(request, supplier_id):
        exist_supplier_query = SupplySupplier.objects.raw({'_id': ObjectId(supplier_id)})[0]
        exist_supplier_query.delete()
        return handle_response('', data="success", success=True)


class SupplierTransfer(APIView):
    @staticmethod
    def get(request):
        supplier_objects = SupplierTypeSociety.objects.all()
        serializer = SupplierTypeSocietySerializer(supplier_objects, many=True)
        society_list = serializer.data
        new_base_supplier_for_society = BaseSupplySupplierType(**{
            "name": "Standard Template",
            "supplier_attributes": [
                                  {"name":"Supplier Id","type": "STRING"},
                                  {"name":"Name","type": "STRING"},
                                  # {"name":"Society Address 1","type": "STRING"},
                                  # {"name":"Society Address 2","type": "STRING"},
                                  # {"name":"Society Zip","type": "STRING"},
                                  {"name":"Society Name","type": "STRING"},
                                  # {"name":"Society City","type": "STRING"},
                                  # {"name":"Society State", "type": "STRING"},
                                  # {"name":"Society Longitude", "type": "STRING"},
                                  # {"name":"Society Locality", "type": "STRING"},
                                  # {"name": "Society Subarea", "type": "STRING"},
                                  # {"name": "Society Latitude", "type": "STRING"},
                                  {"name": "Society Location Type", "type": "STRING"},
                                  # {"name": "Society Type Quality", "type": "STRING"},
                                  {"name": "Society Type Quantity", "type": "STRING"},
                                  # {"name": "Flat Count", "type": "STRING"},
                                  {"name": "Flat Average Rental Per Sqft", "type": "STRING"},
                                  {"name": "Flat Sale Cost Per Sqft", "type": "STRING"},
                                  # {"name": "Tower Count", "type": "INT"},
                                  # {"name": "Payment Details Available", "type": "BOOLEAN"},
                                  {"name": "Age of Society", "type": "INT"},
                                  {"name": "Total Tenant Flat Count", "type": "INT"},
                                  # {"name": "Landmark", "type": "STRING"},
                                  # {"name": "Name for Payment", "type": "STRING"},
                                  # {"name": "Bank Name", "type": "STRING  "},
                                  # {"name": "IFSC Code", "type": "STRING"},
                                  # {"name": "Account No", "type": "STRING"},
                                  {"name": "Representative", "type": "STRING"}],
        }).save()
        base_supplier_for_society_id = new_base_supplier_for_society._id
        new_supplier_type_for_society = SupplySupplierType(**{
            "name": "Society Template",
            "base_supplier_type_id": base_supplier_for_society_id,
            "supplier_attributes": [{"name":"Supplier Id","type": "STRING"},
                                  {"name":"Name","type": "STRING"},
                                  # {"name":"Society Address 1","type": "STRING"},
                                  # {"name":"Society Address 1","type": "STRING"},
                                  # {"name":"Society Zip","type": "STRING"},
                                  {"name":"Society Name","type": "STRING"},
                                  # {"name":"Society City","type": "STRING"},
                                  # {"name":"Society State", "type": "STRING"},
                                  # {"name":"Society Longitude", "type": "STRING"},
                                  # {"name":"Society Locality", "type": "STRING"},
                                  # {"name": "Society Subarea", "type": "STRING"},
                                  # {"name": "Society Latitude", "type": "STRING"},
                                  {"name": "Society Location Type", "type": "STRING"},
                                  # {"name": "Society Type Quality", "type": "STRING"},
                                  {"name": "Society Type Quantity", "type": "STRING"},
                                  # {"name": "Flat Count", "type": "STRING"},
                                  {"name": "Flat Average Rental Per Sqft", "type": "STRING"},
                                  {"name": "Flat Sale Cost Per Sqft", "type": "STRING"},
                                  # {"name": "Tower Count", "type": "INT"},
                                  # {"name": "Payment Details Available", "type": "BOOLEAN"},
                                  {"name": "Age of Society", "type": "INT"},
                                  {"name": "Total Tenant Flat Count", "type": "INT"},
                                  # {"name": "Landmark", "type": "STRING"},
                                  # {"name": "Name for Payment", "type": "STRING"},
                                  # {"name": "Bank Name", "type": "STRING"},
                                  # {"name": "IFSC Code", "type": "STRING"},
                                  # {"name": "Account No", "type": "STRING"},
                                  {"name": "Representative", "type": "STRING"}],
            "organisation_id": "MAC1421",
            "additional_attributes": {
                "bank_details": [
                    {"name": "Name for Payment", "type": "STRING"},
                    {"name": "Account Number", "type": "STRING"},
                    {"name": "Bank Name", "type": "STRING"},
                    {"name": "IFSC Code", "type": "STRING"},
                    {"name": "Cheque Number", "type": "STRING"},
                ],
                "contact_details": [
                    {"name": "Name", "type": "STRING", "is_required": True},
                    {"name": "Designation", "type": "STRING", "is_required": True},
                    {"name": "Department", "type": "STRING", "is_required": True},
                    {"name": "Mobile Number", "type": "STRING", "is_required": True},
                    {"name": "Email", "type": "STRING", "is_required": True},
                    {"name": "MPOC", "type": "STRING", "is_required": True},
                    {"name": "Landline Number", "type": "STRING", "is_required": True},
                    {"name": "STD Code", "type": "STRING", "is_required": True},
                    {"name": "Decision Maker", "type": "STRING", "is_required": True},
                    {"name": "Comments", "type": "STRING", "is_required": True},

                ],
                "location_details": [
                    {"name": "Address", "type": "STRING", "is_required": True},
                    {"name": "Landmark", "type": "STRING", "is_required": True},
                    {"name": "State", "type": "DROPDOWN", "is_required": True, "options": []},
                    {"name": "City", "type": "DROPDOWN", "is_required": True, "options": []},
                    {"name": "Area", "type": "DROPDOWN", "is_required": True, "options": []},
                    {"name": "Sub Area", "type": "DROPDOWN", "is_required": True, "options": []},
                    {"name": "Pincode", "type": "STRING", "is_required": True},
                    {"name": "Latitude", "type": "STRING", "is_required": True},
                    {"name": "Longitude", "type": "STRING", "is_required": True},
                ],
                "society_details": [
                    {"name": "Flat Count", "type": "STRING", "is_required": True},
                    {"name": "Tower Count", "type": "STRING", "is_required": True},
                    {"name": "Quality Type", "type": "STRING", "is_required": True},
                    {"name": "Average House Hold Occupants", "type": "STRING", "is_required": True},
                    {"name": "Bachelor Tenants Allowed", "type": "DROPDOWN", "is_required": True, "options": ["Yes", "No"]},
                ]
            }

        }).save()
        new_supplier_type_id = new_supplier_type_for_society._id
        supplier_list = []
        counter = 0
        for society in society_list:
            if society['society_name']:
                name = society['society_name']
                new_supplier_type_id = new_supplier_type_id
                supplier_attributes = [
                                  {"name": "Supplier Id", "type": "STRING", "value": society['supplier_id']},
                                  {"name": "Name", "type": "STRING", "value": society['society_name']},
                                  # {"name": "Society Address 1", "type": "STRING", "value": society['society_address1']},
                                  # {"name": "Society Address 2", "type": "STRING", "value": society['society_address2']},
                                  # {"name": "Society Zip", "type": "STRING", "value": society['society_zip']},
                                  {"name": "Society Name", "type": "STRING", "value": society['society_name']},
                                  # {"name": "Society City", "type": "STRING", "value": society['society_city']},
                                  # {"name": "Society State", "type": "STRING", "value": society['society_state']},
                                  # {"name": "Society Longitude", "type": "STRING", "value": society['society_longitude']},
                                  # {"name": "Society Locality", "type": "STRING", "value": society['society_locality']},
                                  # {"name": "Society Subarea", "type": "STRING", "value": society['society_subarea']},
                                  # {"name": "Society Latitude", "type": "STRING", "value": society['society_latitude']},
                                  {"name": "Society Location Type", "type": "STRING", "value": society['society_location_type']},
                                  # {"name": "Society Type Quality", "type": "STRING", "value": society['society_type_quality']},
                                  {"name": "Society Type Quantity", "type": "STRING", "value": society['society_type_quantity']},
                                  # {"name": "Flat Count", "type": "STRING", "value": society['flat_count']},
                                  {"name": "Flat Avg Rental PerSqft", "type": "STRING", "value": society['flat_avg_rental_persqft']},
                                  {"name": "Flat Sale Cost PerSqft", "type": "STRING", "value": society['flat_sale_cost_persqft']},
                                  # {"name": "Tower Count", "type": "INT", "value": society['tower_count']},
                                  # {"name": "Payment Details Available", "type": "BOOLEAN", "value": society['payment_details_available']},
                                  {"name": "Age Of Society", "type": "INT", "value": society['age_of_society']},
                                  {"name": "Total Tenant Flat Count", "type": "INT", "value": society['total_tenant_flat_count']},
                                  # {"name": "Landmark", "type": "STRING", "value": society['landmark']},
                                  # {"name": "Name For Payment", "type": "STRING", "value": society['name_for_payment']},
                                  # {"name": "Bank Name", "type": "STRING", "value": society['bank_name']},
                                  # {"name": "IFSC Code", "type": "STRING", "value": society['ifsc_code']},
                                  # {"name": "Account No", "type": "STRING", "value": society['account_no']},
                                  {"name": "Representative", "type": "STRING", "value": society['representative']}
                                ],

                additional_attributes = {
                    "bank_details": [
                        {"name": "Name for Payment", "type": "STRING", "value": society['name_for_payment']},
                        {"name": "Account Number", "type": "STRING", "value": society['account_no']},
                        {"name": "Bank Name", "type": "STRING", "value": society['bank_name']},
                        {"name": "IFSC Code", "type": "STRING", "value": society['ifsc_code']},
                        {"name": "Cheque Number", "type": "STRING", "value": ""},
                    ],
                    "contact_details": [
                        {"name": "Name", "type": "STRING", "is_required": True, "value": ""},
                        {"name": "Designation", "type": "STRING", "is_required": True, "value": ""},
                        {"name": "Department", "type": "STRING", "is_required": True, "value": ""},
                        {"name": "Mobile Number", "type": "STRING", "is_required": True, "value": ""},
                        {"name": "Email", "type": "STRING", "is_required": True, "value": ""},
                        {"name": "MPOC", "type": "STRING", "is_required": True, "value": ""},
                        {"name": "Landline Number", "type": "STRING", "is_required": True, "value": ""},
                        {"name": "STD Code", "type": "STRING", "is_required": True, "value": ""},
                        {"name": "Decision Maker", "type": "STRING", "is_required": True, "value": ""},
                        {"name": "Comments", "type": "STRING", "is_required": True, "value": ""},

                    ],
                    "location_details": [
                        {"name": "Address", "type": "STRING", "is_required": True, "value": society['society_address1']},
                        {"name": "Landmark", "type": "STRING", "is_required": True, "value": society['landmark']},
                        {"name": "State", "type": "DROPDOWN", "is_required": True, "options": [], "value": society['society_state']},
                        {"name": "City", "type": "DROPDOWN", "is_required": True, "options": [], "value": society['society_city']},
                        {"name": "Area", "type": "DROPDOWN", "is_required": True, "options": [], "value": society['society_locality']},
                        {"name": "Sub Area", "type": "DROPDOWN", "is_required": True, "options": [], "value": society['society_subarea']},
                        {"name": "Pincode", "type": "STRING", "is_required": True, "value": society['society_zip']},
                        {"name": "Latitude", "type": "STRING", "is_required": True, "value": society['society_latitude']},
                        {"name": "Longitude", "type": "STRING", "is_required": True, "value": society['society_longitude']},
                    ],
                    "society_details": [
                        {"name": "Flat Count", "type": "STRING", "is_required": True, "value": society['flat_count']},
                        {"name": "Tower Count", "type": "STRING", "is_required": True, "value": society['tower_count']},
                        {"name": "Quality Type", "type": "STRING", "is_required": True, "value": society['society_type_quality']},
                        {"name": "Average House Hold Occupants", "type": "STRING", "is_required": True, "value": ""},
                        {"name": "Bachelor Tenants Allowed", "type": "DROPDOWN", "is_required": True,
                         "options": ["Yes", "No"], "value": ""},
                    ]
                }
                organisation_id = "MAC1421"
                dict_of_req_attributes = {"name": name, "supplier_attributes": supplier_attributes[0],
                                          "additional_attributes": additional_attributes,
                                          "organisation_id": organisation_id,
                                          "supplier_type_id": new_supplier_type_id,
                                          "old_supplier_id": society['supplier_id']}
                supplier_dict = dict_of_req_attributes
                supplier_dict["created_at"] = datetime.now()
                supplier_list.append(SupplySupplier(**supplier_dict))
                counter = counter + 1
                if counter % 500 == 0:
                    SupplySupplier.objects.bulk_create(supplier_list)
                    supplier_list = []
        if len(supplier_list) > 0:
            SupplySupplier.objects.bulk_create(supplier_list)
        return handle_response('', data={"success": True}, success=True)


class ShortlistedSpacesTransfer(APIView):
    @staticmethod
    def get(request):
        shortlisted_spaces = ShortlistedSpaces.objects.all()
        serializer = ShortlistedSpacesSerializer(shortlisted_spaces, many=True)
        shortlisted_spaces_list = serializer.data
        base_supplier_type = BaseSupplySupplierType.objects.raw({'name': 'Base Society'})[0]
        supplier_type = SupplySupplierType.objects.raw({'name': 'Base Society'})[0]
        booking_attributes_list = [

                                {"name": "Payment Method", "type": "DROPDOWN", "options": ["NEFT", "CASH", "ONLINE"]},
                                {"name": "Payment Status", "type": "DROPDOWN", "options": ["Not Initiated", "Pending", "Cheque Released",
                                                                                           "Paid", "Rejected"]},
                                {"name": "Status", "type":"DROPDOWN", "options": ["BUFFER", "REMOVED", "FINALIZED"]},
                                {"name": "Total Negotiated Price", "type":"FLOAT"},
                                {"name": "Booking Status", "type": "DROPDOWN", "options": ["Undecided",
                                    "Decision Pending", "Conformed Booking", "Tentative Booking", "Phone Booked", "Visit Booked",
                                    "Rejected", "Send Email", "Visit Required", "Call Required"]},

                                {"name": "Is Completed", "type": "BOOLEAN"},
                                {"name": "Transaction Or Cheque No", "type": "STRING"},
                                {"name": "Phase No", "type": "INT"},
                                {"name": "Freebies", "type": "MULTISELECT", "options": ["Whatsapp Group","Email Group",
                                                                                     "Building ERP", " Door to Door"]},
                                {"name": "Stall Locations", "type": "MULTISELECT", "options": ["Nea Entry Gate","Near Exit Gate",
                                        "In Front Of Tower", "Near Garden", "Near Play Area", "Near Club House",
                                        "Near Swimming Pool", "Near Parking Area", "Near Shopping Area"]},
                                {"name": "Cost Per Flat", "type": "FLOAT"},
                                {"name": "Booking Priority", "type": "DROPDOWN", "options": ["Very High", "High"]},
                                {"name": "Sunboard Location", "type": "MULTISELECT", "options": ["Nea Entry Gate","Near Exit Gate",
                                        "In Front Of Tower", "Near Garden", "Near Play Area", "Near Club House",
                                        "Near Swimming Pool", "Near Parking Area", "Near Shopping Area"]},

                                ]
        new_base_booking_template = BaseBookingTemplate(**
        {
            "name": "Society BaseBooking",
            "booking_attributes": booking_attributes_list,
            "base_supplier_type_id": base_supplier_type._id,
            "supplier_attributes": base_supplier_type.supplier_attributes,
            "organisation_id": "MAC1421"
         }).save()
        new_base_booking_template_id = new_base_booking_template._id
        new_booking_template = BookingTemplate(**
        {
            "name":"Society Booking",
            "booking_attributes": booking_attributes_list,
            "supplier_type_id": supplier_type._id,
            "base_booking_template_id": new_base_booking_template_id,
            "supplier_attributes": supplier_type.supplier_attributes,
            "organisation_id": "MAC1421"
        }).save()
        new_booking_template_id = new_booking_template._id
        booking_list = []
        counter = 0
        for booking in shortlisted_spaces_list:
            data = {}
            data['booking_template_id'] = str(new_booking_template_id)
            data['campaign_id'] = booking['proposal']
            data['user_id'] = booking['user']
            data['center_id'] = booking['center']
            data['supplier_id_old'] = booking['object_id']
            temp_data = SupplySupplier.objects.raw({'old_supplier_id':booking['object_id']})
            if  temp_data.count() > 0:
                data['supplier_id'] = temp_data[0]._id
            else:
                continue
            for item in booking_attributes_list:
                item['value'] = booking[item['name']]
            data['booking_attributes'] = booking_attributes_list
            booking_list.append(BookingData(**data))
            counter = counter + 1
            if counter % 1000 == 0:
                BookingData.objects.bulk_create(booking_list)
                booking_list = []
        if len(booking_list) > 0:
            BookingData.objects.bulk_create(booking_list)
        return handle_response('', data={"success": True}, success=True)

class SupplierInventoryTransfer(APIView):
    @staticmethod
    def get(request):
        supplier_inventories = ShortlistedInventoryPricingDetails.objects.all()
        suppliers = SupplySupplier.objects.raw({})
        suppliers_id_map = {}
        for supplier in suppliers:
            suppliers_id_map.setdefault(supplier.old_supplier_id, None)
            suppliers_id_map[supplier.old_supplier_id] = str(supplier._id)
        inventory_list = []
        counter = 0
        for inventory in supplier_inventories:
            data = {}
            if inventory.shortlisted_spaces.object_id not in suppliers_id_map:
                continue
            else:
                data['supplier_id'] = suppliers_id_map[inventory.shortlisted_spaces.object_id]
            data['campaign_id'] = inventory.shortlisted_spaces.proposal.proposal_id
            data['inventory_name'] = inventory.ad_inventory_type.adinventory_name
            data['organisation_id'] = inventory.shortlisted_spaces.proposal.account.organisation.organisation_id
            data['supplier_id_old'] = inventory.shortlisted_spaces.object_id
            data['comments'] = []
            data['inventory_images'] = []
            data['created_by'] = inventory.user
            data["created_at"] = datetime.now()
            data["updated_at"] = datetime.now()
            data["inventory_id_old"] = inventory.id

            inventory_list.append(BookingInventory(**data))
            counter = counter + 1
            if counter % 5000 == 0:
                BookingInventory.objects.bulk_create(inventory_list)
                inventory_list = []
        if len(inventory_list) > 0:
            BookingInventory.objects.bulk_create(inventory_list)

        return handle_response('', data={"success": True}, success=True)

class InventoryActivityImageTransfer(APIView):
    def get(self, request):
        dynamic_inventory = BookingInventory.objects.raw({})
        dynamic_inventory_ids_map = {inv.inventory_id_old: inv for inv in dynamic_inventory}

        dynamic_supplier = SupplySupplier.objects.raw({})
        dynamic_supplier_ids_map = {supplier.old_supplier_id:supplier for supplier in dynamic_supplier}

        image_objects = InventoryActivityImage.objects.select_related('inventory_activity_assignment',
                                                                      'inventory_activity_assignment__inventory_activity',
                                                                      'inventory_activity_assignment__inventory_activity__shortlisted_inventory_details',
                                                                      'inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__shortlisted_spaces',
                                                                      'inventory_activity_assignment__inventory_activity__shortlisted_inventory_details__shortlisted_spaces__proposal')
        result = {}
        for item in image_objects:
            try:
                if item and str(item.inventory_activity_assignment.inventory_activity.shortlisted_inventory_details.id) in dynamic_inventory_ids_map:
                    if item.inventory_activity_assignment not in result:

                        result[item.inventory_activity_assignment] = {
                            'booking_inventory_id': str(dynamic_inventory_ids_map[str(item.inventory_activity_assignment.inventory_activity.shortlisted_inventory_details.id)]._id),
                            'supplier_id': str(dynamic_supplier_ids_map[item.inventory_activity_assignment.inventory_activity.shortlisted_inventory_details.shortlisted_spaces.object_id]._id),
                            'inventory_name': item.inventory_activity_assignment.inventory_activity.shortlisted_inventory_details.ad_inventory_type.adinventory_name,
                            'comments': [],
                            'campaign_id': item.inventory_activity_assignment.inventory_activity.shortlisted_inventory_details.shortlisted_spaces.proposal.proposal_id,
                            'organisation_id': 'MAC1421',
                            'inventory_images': [],
                            'activity_type': item.inventory_activity_assignment.inventory_activity.activity_type,
                            'activity_date': item.inventory_activity_assignment.activity_date,
                            'assigned_to_id': item.inventory_activity_assignment.assigned_to.id
                        }
                    result[item.inventory_activity_assignment]['inventory_images'].append({
                        'image_path': item.image_path,
                        'latitude': item.latitude,
                        'longitude': item.longitude,
                        'comment': item.comment,
                        'actual_activity_date': item.actual_activity_date,
                        'activity_by': item.activity_by.id
                    })
            except Exception as e:
                continue
        booking_act_list = []
        counter = 0
        for item in result.values():
            booking_act_list.append(BookingInventoryActivity(**item))
            counter = counter + 1
            if counter % 1000 == 0:
                BookingInventoryActivity.objects.bulk_create(booking_act_list)
                booking_act_list = []
        if len(booking_act_list) > 0:
            BookingInventoryActivity.objects.bulk_create(booking_act_list)
        return handle_response('', data={}, success=True)

def create_auto_complete_supplier_data(supplier_list=None):

    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    for supplier in supplier_list:
        supplier_name = supplier.name.lower()
        supplier_id = str(supplier._id)
        line = supplier_name
        '''+ '||' + str(supplier_id)'''
        n = line.strip()
        for l in range(1, len(n)):
            prefix = n[0:l]
            r.zadd('supplier_data', 0, prefix)
        r.zadd('supplier_data', 0, n + "*" + str(supplier_id))
    return handle_response('', data={}, success=True)

class AutoCompleteSupplierDataCreate(APIView):
    @staticmethod
    def get(request):
        suppliers = SupplySupplier.objects.all()
        response = create_auto_complete_supplier_data(suppliers)
        if response.data['status']:
            return handle_response('', data={}, success=True)
        return handle_response('', data={}, success=False)

class SupplierAutoComplete(APIView):
    @staticmethod
    def get(request):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        query = request.query_params.get('query','')
        prefix = query.lower()

        results = []
        rangelen = 50  # This is not random, try to get replies < MTU size
        start = r.zrank('supplier_data', prefix)
        print(prefix, start)

        if start is None:
            # print "start is none"
            return handle_response('', data=[], success=True)
        redis_data = r.zrange('supplier_data', start, start + rangelen - 1)
        redis_data = [data.decode('UTF-8') for data in redis_data]
        print(redis_data)
        try:
            k = r.zrange('supplier_data', start + rangelen - 1, start + rangelen - 1)
            print("hi", k)
            while k[0].startswith(prefix):
                start = start + 50
                redis_data = r.zrange('supplier_data', start, start + rangelen - 1)
                print(redis_data)
                redis_data.extend(redis_data)
                k = r.zrange('supplier_data', start + rangelen -
                             1, start + rangelen - 1)
        except:

            for i in redis_data:

                if i.startswith(prefix):

                    if '*' in i:
                        i_arr = i.split('*')
                        i_obj = {'name': i_arr[0], 'id': i_arr[1]}
                        results.append(i_obj)

            return handle_response('', data=results, success=True)